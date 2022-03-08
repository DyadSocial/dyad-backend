// Singleton Example code from refactoring.guru
#ifndef _DATABASE_HELPER_H_
#define _DATABASE_HELPER_H_

#include <string>
#include <vector>
#include <thread>
#include <mutex>
#include <sw/redis++/redis++.h>

#include "posts.grpc.pb.h"
#include "image.grpc.pb.h"

using namespace sw::redis;

class DatabaseHelper {
private:
  static DatabaseHelper *dh_instance_;
  static std::mutex mutex_;
protected:
  Redis redis_ = Redis("tcp://127.0.0.1:6379");
  DatabaseHelper() {
  }
public:
  static DatabaseHelper *GetInstance();
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

DatabaseHelper *DatabaseHelper::GetInstance() {
  std::lock_guard<std::mutex> lock(mutex_);
  if (dh_instance_ == nullptr) {
    dh_instance_ = new DatabaseHelper();
  }
  return dh_instance_;
}

std::string DatabaseHelper::StoreProfileImage(std::string username, std::string image) {
  std::string key = "user:"+username+":profile_picture";
  redis_.set(key, image);
  std::cout << "Stored: " << *redis_.get(key) << std::endl;
  return key;
}

std::string DatabaseHelper::GetProfileImage(std::string username) {
  auto val = redis_.get("user:"+username+":profile_picture");
  if (val) {
    std::cout << "Found: " << *val << std::endl;
    return *val;
  }
  return "NIL";
}

std::string DatabaseHelper::StorePostImage(std::string username, std::string id, std::string image) {
  std::string key = "user:"+username+":post:"+id;
  std::cout << "Stored: " << *redis_.get(key) << std::endl;
  redis_.set(key, image);
  return key;
}

std::string DatabaseHelper::GetPostImage(std::string username, std::string id) {
  auto val = redis_.get("user:"+username+":post:"+id);
  if (val) {
    return *val;
  }
  return "NIL";
}


#endif // _DATABASE_HELPER_H