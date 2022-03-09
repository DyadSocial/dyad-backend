/*
  gRPC Dataserverp
  https://github.com/grpc/grpc 
*/

#include <iostream>
#include <chrono>
#include <algorithm>
#include <memory>
#include <string>
#include <sstream>
#include <map>

#include <database_helper.hpp>

#include <grpc/grpc.h>
#include <grpcpp/security/server_credentials.h>
#include <grpcpp/server.h>
#include <grpcpp/server_builder.h>
#include <grpcpp/server_context.h>

#include "image.grpc.pb.h"
#include "image.pb.h"
#include "posts.grpc.pb.h"
#include "posts.pb.h"

using std::chrono::system_clock;
using grpc::Server;
using grpc::ServerBuilder;
using grpc::ServerContext;
using grpc::ServerReader;
using grpc::ServerReaderWriter;
using grpc::ServerWriter;
using grpc::Status;

const size_t CHUNK_SIZE = 1024 * 32;

std::vector<ImageChunk> ChunkImage(std::string image) {
  std::cout << "chunking: " << image << std::endl;
  // Edge case
  if (image.size() == 0) return {};
  // Pre allocate chunks
  std::vector<ImageChunk> chunks((image.size() - 1)  / CHUNK_SIZE + 1);
  // Keep track of current_chunk in image
  size_t current_chunk = 0;
  // Set each chunk in vector
  std::cout << current_chunk << "/" << chunks.size() << std::endl;
  while( current_chunk < chunks.size() ) {
    // Set full chunks unless the last chunk is smaller
    //int next_chunk = current_chunk + 1;
    //if (next_chunk * CHUNK_SIZE < image.size()) {
      //chunks[current_chunk].set_imagedata(std::string(image.begin() + current_chunk * CHUNK_SIZE, image.begin() + next_chunk * CHUNK_SIZE));
    //} else {
      //std::cout << current_chunk;
      std::string chunk = std::string(image.begin() + current_chunk * CHUNK_SIZE, image.end());
      chunks[current_chunk++].set_imagedata(chunk);
      std::cout << chunk << std::endl;
    //}
  }

  return chunks;
}

class ImageServerImpl final : public Images::Service {
// ImageServerImpl Private
private:
  DatabaseHelper *db_redis;
  std::string image;
// ImageServerImpl Public
public:
  explicit ImageServerImpl(std::string db_address) 
    : db_redis(DatabaseHelper::GetInstance(db_address)) {
    image = std::string();
  }

  Status UploadImage(ServerContext *context, ServerReader<ImageChunk> *reader, Ack *ack) override {
    ImageChunk chunk;
    size_t chunk_count = 1;
    auto metadata = context->client_metadata();
    auto sizePair = metadata.find("size");
    auto usernamePair = metadata.find("username");
    auto idPair = metadata.find("id");
    if (sizePair != metadata.end() && usernamePair != metadata.end() && idPair != metadata.end()) {
      image.resize(0);
      while ( reader->Read(&chunk) ) {
        image += chunk.imagedata();
        chunk_count++;
      }
      if (idPair->second.data() == "profile_picture") {
        db_redis->StoreProfileImage(usernamePair->second.data(), image);
      } else {
        db_redis->StorePostImage(usernamePair->second.data(), idPair->second.data(), image);
      }
    } else {
      return Status::CANCELLED;
    }
    ack->set_imagesize(std::to_string(image.size()));
    ack->set_imageurl("user:"+std::string(usernamePair->second.data())+":post:"+std::string(idPair->second.data()));
    return Status::OK;
  }

  Status PullImage(ServerContext *context, const ImageQuery *query, ServerWriter<ImageChunk> *writer) override {
    std::vector<ImageChunk> chunks;
    if (query->id() == "profile_picture") {
      chunks = ChunkImage(db_redis->GetProfileImage(query->author()));
    } else {
      chunks = ChunkImage(db_redis->GetPostImage(query->author(), query->id()));
    }
    for( const ImageChunk &chunk : chunks ) {
      writer->Write(chunk);
    }
    return Status::OK;
  }
};

void RunServer() {
    std::string server_addr("0.0.0.0:5442");
    ImageServerImpl service("tcp://127.0.0.1:6379");

    ServerBuilder builder;
    builder.AddListeningPort(server_addr, grpc::InsecureServerCredentials());
    builder.RegisterService(&service);
    std::unique_ptr<Server> server(builder.BuildAndStart());
    std::cout << "Server listening on " << server_addr << std::endl;
    server->Wait();
}

/*
class PostsServerImpl final : public Images::PostsSync {
// ImageServerImpl Private
private:
  DatabaseHelper *db_redis;
// ImageServerImpl Public
public:
  explicit PostsServerImpl(std::string db_address) 
    : db_redis(DatabaseHelper::GetInstance(db_address)) {
  }

  Status RefreshPosts(ServerContext *context, const PostQuery *query, ServerWriter<Post> *writer) override {
    //std::vector<Post> posts = db_redis->GetPosts(que)
    return Status::OK;
  }
};
*/

int main(int argc, char **argv) {
    RunServer();
    return 0;
}