/*
 gRPC Data Server
 https://github.com/grpc/grpc 
 library and logic from gRPC
*/

#include <iostream>
#include <thread>
#include <chrono>
#include <algorithm>
#include <memory>
#include <string>
#include <map>
#include <sstream>

#include <grpcpp/grpcpp.h>
#include <grpcpp/server.h>
#include <grpcpp/security/server_credentials.h>
#include <grpcpp/server_builder.h>
#include <grpcpp/server_context.h>
#include <grpcpp/ext/proto_server_reflection_plugin.h>
#include <grpcpp/health_check_service_interface.h>

#include "image.grpc.pb.h"
#include "image.pb.h"
#include "content.grpc.pb.h"
#include "content.pb.h"

#include <database_helper.hpp>

// Grpc Lib
using grpc::Server;
using grpc::CallbackServerContext;
using grpc::ServerBuilder;
using grpc::Status;

using std::chrono::system_clock;

const size_t CHUNK_SIZE = 1024 * 32; // 32 KB
std::vector<ImageChunk> ChunkImage(std::string image) {
    std::cout << "Chunking Images\n";
    // Preallocate Chunks
    std::vector<ImageChunk> chunks((image.size() - 1) / CHUNK_SIZE + 1);
    size_t curr_pos = 0;
    size_t current_chunk = 0;
    while (curr_pos < image.size()) {
        if (curr_pos >= CHUNK_SIZE) {
            chunks[current_chunk++].set_imagedata(std::string(image.begin() + curr_pos, image.begin() + curr_pos + CHUNK_SIZE));
            curr_pos -= CHUNK_SIZE;
        } else {
            chunks[current_chunk++].set_imagedata(std::string(image.begin() + curr_pos, image.end()));
            curr_pos = image.size();
        }
    }
    for (int i = 0; i < image.size(); i++) {
        std::cout << i << " ";
    }
    std::cout << "\n";
    std::cout << "Chunking Complete!\n";
    return chunks;
}

class ImageServerImpl final : public Images::CallbackService {
public:
    // Upload image storing each chunk in a class
    grpc::ServerReadReactor<ImageChunk>* UploadImage(CallbackServerContext *context,
                                                     Ack *ack) override 
    {
        class ChunkRecorder : public grpc::ServerReadReactor<ImageChunk> {
        public:
            ChunkRecorder(CallbackServerContext *context, Ack *imageAck, std::vector<ImageChunk>* chunk_list)
                : start_time_(system_clock::now()),
                  context_(context),
                  ack_(imageAck),
                  chunk_list_(chunk_list)
            {
                auto metadata = context->client_metadata();
                auto sizePair = metadata.find("size");
                auto usernamePair = metadata.find("username");
                auto idPair = metadata.find("id");
                if (sizePair != metadata.end() && usernamePair != metadata.end() && idPair != metadata.end()) {
                    std::stringstream size_str(sizePair->second.data());
                    size_str >> image_size_;
                    std::cout << "Allocating Size: " << image_size_ << std::endl;
                    image.resize(image_size_);
                    username = std::string(usernamePair->second.data());
                    id = std::string(idPair->second.data());

                } else {
                    // Could not find a size to allocate to download image
                    Finish(Status::CANCELLED);
                }
                chunk_list_->resize(image_size_);
                StartRead(&image_chunk_);
            }

            void OnDone() override { delete this; }
            void OnReadDone(bool ok) override {
                if (ok) {
                    std::cout << image_chunk_.imagedata() << std::endl;
                    for (int i = 0; i < image_chunk_.imagedata().size(); i++) {
                        std::cout << image_chunk_.imagedata()[i] << ", ";
                        image[image_pos_++] = image_chunk_.imagedata()[i];
                    }
                    chunk_count_++;
                    StartRead(&image_chunk_);
                } else {
                    DatabaseHelper *db_redis = DatabaseHelper::GetInstance();
                    if (id == "profile_picture") {
                        db_redis->StoreProfileImage(username, image);
                    } else {
                        db_redis->StorePostImage(username, id, image);
                    }
                    auto elapsed_time = std::chrono::duration_cast<std::chrono::milliseconds>(
                        system_clock::now() - start_time_);
                    std::cout << "Chunk count: " << chunk_count_ << "\n";
                    std::cout << "Time elapsed: " << elapsed_time.count() << "ms\n";
                    ack_->set_imagesize(std::to_string(image_size_));
                    ack_->set_success(true);
                    ack_->set_imageurl("https://dyadsocial.com");
                    Finish(Status::OK);
                }
            }

        private:
            std::string image;
            std::string username;
            std::string id;
            CallbackServerContext *context_;
            system_clock::time_point start_time_;
            Ack* ack_;
            std::vector<ImageChunk>* chunk_list_;
            ImageChunk image_chunk_;
            int chunk_count_ = 0;
            size_t image_size_;
            size_t image_pos_ = 0;
        };
        return new ChunkRecorder(context, ack, &chunk_list_);
    }

    grpc::ServerWriteReactor<ImageChunk> *PullImage(CallbackServerContext *context,
                                                    const ImageQuery *query) override 
    {
        class ImageBuilder : public grpc::ServerWriteReactor<ImageChunk> {
        public:
            ImageBuilder(CallbackServerContext *context,
                         const ImageQuery *query,
                         std::vector<ImageChunk> *chunk_list)
                : _chunk_list_(chunk_list),
                next_chunk_(_chunk_list_->begin())
            {
                std::string img = redis_db->GetPostImage(query->author(), query->id());
                std::cout << "Query: " << query->author() << ":" << query->id() << std::endl;
                std::cout << "Img size: " << img.size() << ", Img data: " << img << std::endl;
                if (img == "NIL") {
                    std::cout << "Cancelling Job, No Image" << std::endl;
                    Finish(Status::CANCELLED);
                    return;
                }
                *_chunk_list_ = ChunkImage(img);
                NextWrite();
            }
            void OnDone() override { delete this; }
            void OnWriteDone(bool ok) override { NextWrite(); }
        private:
            void NextWrite() {
                while (next_chunk_ != _chunk_list_->end()) {
                    const ImageChunk &chunk = *next_chunk_;
                    next_chunk_++;
                    StartWrite(&chunk);
                    return;
                }
                Finish(Status::OK);
            }
            std::vector<ImageChunk> *_chunk_list_;
            std::vector<ImageChunk>::iterator next_chunk_;
            DatabaseHelper *redis_db = DatabaseHelper::GetInstance();
        };
        return new ImageBuilder(context, query, &chunk_list_);
    }

private:
std::vector<ImageChunk> chunk_list_;
};

void RunServer() {
    std::string server_addr("0.0.0.0:5442");
    ImageServerImpl service;

    ServerBuilder builder;
    builder.AddListeningPort(server_addr, grpc::InsecureServerCredentials());
    builder.RegisterService(&service);
    std::unique_ptr<Server> server(builder.BuildAndStart());
    std::cout << "Server listening on " << server_addr << std::endl;
    server->Wait();
}

int main(int argc, char **argv) {
    RunServer();
    return 0;
}