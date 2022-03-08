CMAKE_MINIMUM_REQUIRED(VERSION 3.5.1)
PROJECT(GRPC_USERCONTENT_SERVICER)

set (CMAKE_CXX_STANDARD 17)

find_package(Threads REQUIRED)

# Make Sure GRPC dependency is available
option(USE_SYSTEM_GRPC "Use System Install gRPC" ON)
if(USE_SYSTEM_GRPC)
  # Find protobuf-config.cmake from system installation
#  set(protobuf_MODULE_COMPATIBLE TRUE)
#  set(Protobuf CONFIG REQUIRED)
#  find_package(gRPC CONFIG REQUIRED)
#  message(STATUS "Using protobuf ${Protobuf_VERSION}")
#
#  # Find protobuf Installation
#  set(_PROTOBUF_LIBPROTOBUF protobuf::libprotobuf)
#  set(_REFLECTION gRPC::grpc++_reflection)
#  if(CMAKE_CROSSCOMPILING)
#    find_program(_PROTOBUF_PROTOC protoc)
#  else()
#    set(_PROTOBUF_PROTOC $<TARGET_FILE:protobuf::protoc>)
#  endif()
#
#  # Find gRPC Installation
#  find_package(gRPC CONFIG REQUIRED)
#  message(STATUS "Using gRPC ${gRPC_VERSION}")
#  set(_GRPC_GRPCPP gRPC::grpc++)
#  if(CMAKE_CROSSCOMPILING)
#    find_program(_GRPC_CPP_PLUGIN_EXECUTABLE grpc_cpp_plugin)
#  else()
#    set(_GRPC_CPP_PLUGIN_EXECUTABLE $<TARGET_FILE:gRPC::grpc_cpp_plugin>)
#  endif()
#else()
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

# For each for future executables if needed..
foreach(_target
  grpc_data_server)
  add_executable(${_target} "${_target}.cpp")
  target_link_libraries(${_target}
    image_grpc_proto
    ${_REFLECTION}
    ${_GRPC_GRPCPP}
    ${_PROTOBUF_LIBPROTOBUF})
endforeach()





