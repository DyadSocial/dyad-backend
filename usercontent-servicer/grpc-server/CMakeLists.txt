# Author: Vincent

CMAKE_MINIMUM_REQUIRED(VERSION 3.5.1)
PROJECT(GRPC_USERCONTENT_SERVICER)

set (CMAKE_CXX_STANDARD 17)

find_package(Threads REQUIRED)

SET(CMAKE_CXX_STANDARD 14)
SET(CMAKE_EXPORT_COMPILE_COMMANDS ON)

# Make Sure GRPC dependency is available
include(FetchContent)
FetchContent_Declare(
  gRPC
  GIT_REPOSITORY https://github.com/grpc/grpc
  GIT_TAG v1.44.0
)
set(FETCHCONTENT_QUIET OFF)
FetchContent_MakeAvailable(gRPC)
# Use add_subdirectory grpc targets
set(_PROTOBUF_LIBPROTOBUF libprotobuf)
set(_REFLECTION grpc++_reflection)
set(_PROTOBUF_PROTOC $<TARGET_FILE:protoc>)
set(_GRPC_GRPCPP grpc++)
if(CMAKE_CROSSCOMPILING)
  find_program(_GRPC_CPP_PLUGIN_EXECUTABLE grpc_cpp_plugin)
else()
  set(_GRPC_CPP_PLUGIN_EXECUTABLE $<TARGET_FILE:grpc_cpp_plugin>)
endif()

# Protofiles
get_filename_component(image_proto "./protos/image.proto" ABSOLUTE)
get_filename_component(image_proto_path "${image_proto}" PATH)
# Generated Headers/Sources
set(image_proto_srcs "${CMAKE_CURRENT_BINARY_DIR}/image.pb.cc")
set(image_proto_hdrs "${CMAKE_CURRENT_BINARY_DIR}/image.pb.h")
set(image_grpc_srcs "${CMAKE_CURRENT_BINARY_DIR}/image.grpc.pb.cc")
set(image_grpc_hdrs "${CMAKE_CURRENT_BINARY_DIR}/image.grpc.pb.h")
add_custom_command(
  OUTPUT "${image_proto_srcs}" "${image_proto_hdrs}" "${image_grpc_srcs}" "${image_grpc_hdrs}"
  COMMAND ${_PROTOBUF_PROTOC}
  ARGS --grpc_out "${CMAKE_CURRENT_BINARY_DIR}"
    --cpp_out "${CMAKE_CURRENT_BINARY_DIR}"
    -I "${image_proto_path}"
    --plugin=protoc-gen-grpc="${_GRPC_CPP_PLUGIN_EXECUTABLE}"
    "${image_proto}"
    DEPENDS "${image_proto}")

get_filename_component(posts_proto "./protos/posts.proto" ABSOLUTE)
get_filename_component(posts_proto_path "${posts_proto}" PATH)
# Generated Headers/Sources
set(posts_proto_srcs "${CMAKE_CURRENT_BINARY_DIR}/posts.pb.cc")
set(posts_proto_hdrs "${CMAKE_CURRENT_BINARY_DIR}/posts.pb.h")
set(posts_grpc_srcs "${CMAKE_CURRENT_BINARY_DIR}/posts.grpc.pb.cc")
set(posts_grpc_hdrs "${CMAKE_CURRENT_BINARY_DIR}/posts.grpc.pb.h")
add_custom_command(
  OUTPUT "${posts_proto_srcs}" "${posts_proto_hdrs}" "${posts_grpc_srcs}" "${posts_grpc_hdrs}"
  COMMAND ${_PROTOBUF_PROTOC}
  ARGS --grpc_out "${CMAKE_CURRENT_BINARY_DIR}"
    --cpp_out "${CMAKE_CURRENT_BINARY_DIR}"
    -I "${posts_proto_path}"
    --plugin=protoc-gen-grpc="${_GRPC_CPP_PLUGIN_EXECUTABLE}"
    "${posts_proto}"
    DEPENDS "${posts_proto}")

#Include generated hdrs
include_directories("${CMAKE_CURRENT_BINARY_DIR}")

add_library(image_grpc_proto
  ${image_proto_srcs}
  ${image_proto_hdrs}
  ${image_grpc_srcs}
  ${image_grpc_hdrs})
target_link_libraries(image_grpc_proto
  ${_REFLECTION}
  ${_GRPC_GRPCPP}
  ${_PROTOBUF_LIBPROTOBUF})

add_library(posts_grpc_proto
  ${posts_proto_srcs}
  ${posts_proto_hdrs}
  ${posts_grpc_srcs}
  ${posts_grpc_hdrs})
target_link_libraries(posts_grpc_proto
  ${_REFLECTION}
  ${_GRPC_GRPCPP}
  ${_PROTOBUF_LIBPROTOBUF})

add_library(database_helper
  "database_helper.hpp")
target_link_libraries(database_helper
  image_grpc_proto
  posts_grpc_proto
  ${_REFLECTION}
  ${_GRPC_GRPCPP}
  ${_PROTOBUF_LIBPROTOBUF})

foreach(_target
  grpc_data_server grpc_data_client database_test)
  add_executable(${_target} "${_target}.cpp")
  target_link_libraries(${_target}
    image_grpc_proto
    posts_grpc_proto
    database_helper
    ${_REFLECTION}
    ${_GRPC_GRPCPP}
    ${_PROTOBUF_LIBPROTOBUF})

  find_path(HIREDIS_HEADER hiredis)
  target_include_directories(${_target} PUBLIC ${HIREDIS_HEADER})
  find_library(HIREDIS_LIB hiredis)
  target_link_libraries(${_target} ${HIREDIS_LIB})

  find_path(REDIS_PLUS_PLUS_HEADER sw)
  target_include_directories(${_target} PUBLIC ${REDIS_PLUS_PLUS_HEADER})

  find_library(REDIS_PLUS_PLUS_LIB redis++)
  target_link_libraries(${_target} ${REDIS_PLUS_PLUS_LIB})
endforeach()





