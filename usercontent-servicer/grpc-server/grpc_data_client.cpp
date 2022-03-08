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
  std::vector<ImageChunk> chunks(bytes / CHUNK_SIZE + 1);
  while (bytes >= 0) {
    std::stringstream fake_data;
    for(int i = 0; i < CHUNK_SIZE; i++) {
      fake_data << '0';
    }
    ImageChunk chunk;
    chunk.set_imagedata(fake_data.str());
    chunks.emplace_back(chunk);
    bytes -= CHUNK_SIZE;
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


int main(void) {
  std::cout << "Test random chunk creation" << std::endl;
  auto chunks = makeImageChunks(1249);
  std::cout << chunks.size() << std::endl;

  
  ImageChunk chunk = chunks[0];
  std::cout << chunk.has_imagedata() << std::endl;
  std::cout << "Chunk Data:\n";
  for (int i = 0; i < chunk.imagedata().size(); i++) {
    std::cout << chunk.imagedata()[i] << std::endl;
  }

  ImageClient client(grpc::CreateChannel("localhost:5442", grpc::InsecureChannelCredentials()));
  client.UploadImage(1249);

  return 0;
}

