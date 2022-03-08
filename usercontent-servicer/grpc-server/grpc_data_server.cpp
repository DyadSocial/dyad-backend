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

// Grpc Lib
using grpc::Server;
using grpc::CallbackServerContext;
using grpc::ServerBuilder;
using grpc::Status;

using std::chrono::system_clock;

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
                if (sizePair != metadata.end()) {
                    std::stringstream size_str(sizePair->second.data());
                    std::cout << "Init Size: " << size_str.str() << std::endl;
                    size_str >> image_size_;
                    image.resize(image_size_);
                } else {
                    // Could not find a size to allocate to download image
                    Finish(Status::CANCELLED);
                }
                chunk_list_->resize(image_size_);
                StartRead(&image_chunk_);
            }

            void OnDone() { delete this; }
            void OnReadDone(bool ok) {
                if (ok) {
                    for (int i = 0; i < image_chunk_.imagedata().size(); i++) {
                        image[image_pos_++] = image_chunk_.imagedata()[i];
                    }
                    chunk_count_++;
                } else {
                    auto elapsed_time = std::chrono::duration_cast<std::chrono::milliseconds>(
                        system_clock::now() - start_time_);
                    std::cout << "Chunk count: " << chunk_count_ << "\n";
                    std::cout << "Time elapsed: " << elapsed_time.count()/1000 << "\n";
                    //ack_->set_imagesize(image_size_);
                    //ack_->set_success(true);
                    //ack_->set_imageurl("https://dyadsocial.com");
                    Finish(Status::OK);
                }
            }

        private:
            std::string image;
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