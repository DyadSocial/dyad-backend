/*
  Test client for the grpc data server
*/

#include <chrono>
#include <iostream>
#include <memory>
#include <string>
#include <thread>
#include <sstream>

#include <grpc/grpc.h>
#include <grpcpp/channel.h>
#include <grpcpp/client_context.h>
#include <grpcpp/create_channel.h>
#include <grpcpp/security/credentials.h>

#include "image.grpc.pb.h"

// Grpc Lib
using grpc::Channel;
using grpc::ClientContext;
using grpc::ClientReader;
using grpc::ClientReaderWriter;
using grpc::ClientWriter;
using grpc::Status;

const size_t CHUNK_SIZE = 32 * 1024;

std::vector<ImageChunk> makeImageChunks(size_t bytes) {
  // Process Chunks into a vector
  std::vector<ImageChunk> chunks((bytes - 1) / CHUNK_SIZE + 1);
  std::cout << "Allocating " << ((bytes - 1) / CHUNK_SIZE + 1) << " chunk\n";
  size_t currentChunk = 0;
  while (bytes > 0) {
    std::stringstream fake_data;
    ImageChunk chunk;
    if (bytes < CHUNK_SIZE) {
      for (int i = 0; i < bytes; i++) {
        fake_data << i % 10;
      }
      chunk.set_imagedata(fake_data.str());
      chunks[currentChunk] = chunk;
      bytes = 0;
    } else {
      for(int i = 0; i < CHUNK_SIZE; i++) {
        fake_data << i % 10;
      }
      chunk.set_imagedata(fake_data.str());
      chunks[currentChunk++] = chunk;
      bytes -= CHUNK_SIZE;
    }
  } 
  return chunks;
}

class ImageClient {
private:
  std::unique_ptr<Images::Stub> stub_;
public:
  ImageClient(std::shared_ptr<Channel> channel) 
    : stub_(Images::NewStub(channel)) {}

  void UploadImage(size_t imageSize) {
    ImageChunk chunk;
    Ack ack;
    ClientContext context;

    context.AddMetadata("size", std::to_string(imageSize));

    std::unique_ptr<ClientWriter<ImageChunk>> writer(stub_->UploadImage(&context, &ack));
    std::vector<ImageChunk> testData = makeImageChunks(imageSize);

    for (auto chunk : testData) {
      if (!writer->Write(chunk)) {
        break;
      } else {
        std::cout << "Sending " << chunk.imagedata() << std::endl;
      }
    }
    writer->WritesDone();
    Status status = writer->Finish();
    if (status.ok()) {
      std::cout << "UploadImage rpc succeeded:\n";
      std::cout << ack.imagesize() << std::endl;
      std::cout << ack.imageurl() << std::endl;
      std::cout << ack.success() << std::endl;
    } else {
      std::cout << "UploadImage rpc failed" << std::endl;
    }
  }
};


int main(int argc, char **argv) {
  ImageClient client(grpc::CreateChannel("127.0.0.1:5442", grpc::InsecureChannelCredentials()));
  client.UploadImage(std::stoi(argv[1]));

  return 0;
}

