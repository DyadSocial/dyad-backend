// Singleton Example code from refactoring.guru
#ifndef _DATABASE_HELPER_H_
#define _DATABASE_HELPER_H_

#include <string>
#include <vector>
#include <thread>
#include <mutex>
#include <sstream>
#include <sw/redis++/redis++.h>

#include "posts.grpc.pb.h"
#include "image.grpc.pb.h"

using namespace sw::redis;

class DatabaseHelper {
private:
  static DatabaseHelper *dh_instance_;
  static std::mutex mutex_;
protected:
  Redis redis_;
  DatabaseHelper(std::string address) 
    : redis_(Redis(address)) { 
  }
public:
  static DatabaseHelper *GetInstance(std::string address);
  DatabaseHelper(DatabaseHelper &other) = delete;
  void operator=(const DatabaseHelper &) = delete;

  // Images
  std::string StoreProfileImage(std::string username, std::string image);
  std::string GetProfileImage(std::string username);
  std::string StorePostImage(std::string username, std::string id, std::string image);
  std::string GetPostImage(std::string username, std::string id);
  
  // Posts 10 at a time
  //std::vector<Post> QueryPosts(Group group, int post);
  //std::string StorePost(Group group, Post post);
};

DatabaseHelper *DatabaseHelper::dh_instance_{nullptr};
std::mutex DatabaseHelper::mutex_;

DatabaseHelper *DatabaseHelper::GetInstance(std::string address) {
  std::lock_guard<std::mutex> lock(mutex_);
  if (dh_instance_ == nullptr) {
    dh_instance_ = new DatabaseHelper(address);
  }
  return dh_instance_;
}

std::string DatabaseHelper::StoreProfileImage(std::string username, std::string image) {
  std::stringstream keyStream;
  keyStream << "user:" << username << ":profile_picture";
  redis_.set(keyStream.str(), image);
  return keyStream.str();
}

std::string DatabaseHelper::GetProfileImage(std::string username) {
  std::stringstream keyStream;
  keyStream << "user:" << username << ":profile_picture";
  auto val = redis_.get(keyStream.str());
  if (val) {
    return *val;
  }
  return "NULL";
}

std::string DatabaseHelper::StorePostImage(std::string username, std::string id, std::string image) {
  std::stringstream keyStream;
  keyStream << "user:" << username << ":post:" << id;
  std::cout << "-Store: " << keyStream.str() << std::endl;
  redis_.set(keyStream.str(), image);
  return keyStream.str();
}

std::string DatabaseHelper::GetPostImage(std::string username, std::string id) {
  std::stringstream keyStream;
  keyStream << "user:" << username << ":post:" << id;
  std::cout << "-Get: " << keyStream.str() << std::endl;
  auto val = redis_.get(keyStream.str());
  if (val) {
    return *val;
  }
  return "NULL";
}


#endif // _DATABASE_HELPER_H