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
            ChunkRecorder(CallbackServerContext *context, Ack imageAck, const std::vector<ImageChunk>* chunk_list)
                : start_time_(system_clock::now()),
                  context_(context),
                  ack_(ack),
                  chunk_list_(chunk_list)
            {
                auto metadata = context->client_metadata();
                auto sizePair = metadata.find("size");
                if (sizePair != metadata.end()) {
                    std::stringstream size_str(sizePair->second);
                    std::cout << "Init Size: " << metadata["size"] << std::endl;
                    size_str >> image_size_;
                } else {
                    Finish(Status::CANCELLED);
                }
                chunk_list_.resize(image_size_);
                StartRead(&image_chunk_)
            }

            void OnDone() { delete this; }
            void OnReadDone(bool ok) {
                if (ok) {
                    image_size_[chunk_count_++] = *image_chunk_;
                } else {
                    auto elapsed_time = std::chrono::duration_cast<std::chrono::milliseconds>(
                        system_clock::now() - start_time_);
                    )
                    std::cout << "Time elapsed: " << elapsed_time/1000 << "\n";
                    ack_->set_imageSize(image_size_);
                    ack_->set_success(true);
                    ack_->set_ImageURL("https://dyadsocial.com");
                    Finish(Status::OK);
                }
            }

        private:
            CallbackServerContext *context_;
            system_clock::time_point start_time_;
            Ack* ack_;
            const std::vector<ImageChunk>* chunk_list_;
            ImageChunk image_chunk_;
            int chunk_count_ = 0;
            size_t image_size_;
        };
        return new ChunkRecorder(context, ack, chunk_list);
    }
};

void RunServer

int main(int argc, char **argv) {
    RunServer();
    return 0;
}