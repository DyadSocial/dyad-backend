/*
  gRPC Dataserver Handling client requests for posts and images (manual chunking)
Author: Vincent
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

const size_t CHUNK_SIZE = 32 * 1024;

std::vector<ImageChunk> ChunkImage(std::string image) {
  // Edge case
  if (image.size() == 0) return {};
  // Pre allocate chunks
  std::vector<ImageChunk> chunks((image.size() - 1)  / CHUNK_SIZE + 1);
  // Keep track of current_chunk in image
  size_t current_chunk = 0;
  // Set each chunk in vector
  std::cout << image << std::endl;
  std::cout << current_chunk+1 << "/" << chunks.size() << std::endl;
  while( current_chunk < chunks.size() ) {
    // Set full chunks unless the last chunk is smaller
    //int next_chunk = current_chunk + 1;
    //if (next_chunk * CHUNK_SIZE < image.size()) {
      //chunks[current_chunk].set_imagedata(std::string(image.begin() + current_chunk * CHUNK_SIZE, image.begin() + next_chunk * CHUNK_SIZE));
    //} else {
      //std::cout << current_chunk;
      std::string chunk = std::string(image.begin() + current_chunk * CHUNK_SIZE, image.begin() + (current_chunk + 1) * CHUNK_SIZE);
      std::cout << "Current Chunk: " << chunk << std::endl;
      chunks[current_chunk].set_imagesize(image.size());
      chunks[current_chunk].set_imagedata(chunk);
      current_chunk++;
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
    std::cout << "Received request for UploadImage procedure\n";
    ImageChunk chunk;
    image.resize(0);
    int chunk_count = 0;

    std::string id;
    std::string username;

    while ( reader->Read(&chunk) ) {
      if (image.size() == 0) {
        if (chunk.has_imagesize()) {
          image.resize(chunk.imagesize());
          std::cout << "Image resized: " << image.size() << std::endl;
          id = chunk.id();
          username = chunk.username();
        } else {
          return Status::CANCELLED;
        }
      }
      int img_pos = chunk_count * chunk.imagedata().size();
      for (int i = 0; i < chunk.imagedata().size(); i++) {
        image[img_pos + i] = chunk.imagedata()[i];
      }
      chunk_count++;
    }

    if (id == "profile_picture") {
      db_redis->StoreProfileImage(username, image);
    } else {
      db_redis->StorePostImage(username, id, image);
    }

    ack->set_imagesize(std::to_string(image.size()));
    ack->set_imageurl("");
    return Status::OK;
  }

  Status PullImage(ServerContext *context, const ImageQuery *query, ServerWriter<ImageChunk> *writer) override {
    std::cout << "Received request for PullImage procedure\n";
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

class PostsServerImpl final : public PostsSync::Service {
// ImageServerImpl Private
private:
  DatabaseHelper *db_redis;
// ImageServerImpl Public
public:
  explicit PostsServerImpl(std::string db_address) 
    : db_redis(DatabaseHelper::GetInstance(db_address)) {
  }

  Status refreshPosts(ServerContext *context, const PostQuery *query, ServerWriter<Post> *writer) override {
    std::cout << "Received request for RefreshPosts\n";
    std::vector<Post> posts;
    //posts = db_redis->RefreshPosts(query->gid(), query->id(), query->author());
    for ( const Post &post : posts) {
      writer->Write(post);
    }
    return Status::OK;
  }

  Status queryPosts(ServerContext *context, const PostQuery *query, ServerWriter<Post> *writer) override {
    std::cout << "Received request for QueryPosts\n";
    std::vector<Post> posts;
    //posts = db_redis->QueryPosts(query->gid(), query->id(), query->author());
    for ( const Post &post : posts) {
      writer->Write(post);
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

int main(int argc, char **argv) {
    RunServer();
    return 0;
}
