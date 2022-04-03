# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import gens.posts_pb2 as posts__pb2


class PostsSyncStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.refreshPosts = channel.unary_stream(
                '/PostsSync/refreshPosts',
                request_serializer=posts__pb2.PostQuery.SerializeToString,
                response_deserializer=posts__pb2.Post.FromString,
                )
        self.queryPosts = channel.unary_stream(
                '/PostsSync/queryPosts',
                request_serializer=posts__pb2.PostQuery.SerializeToString,
                response_deserializer=posts__pb2.Post.FromString,
                )
        self.uploadPosts = channel.stream_unary(
                '/PostsSync/uploadPosts',
                request_serializer=posts__pb2.Post.SerializeToString,
                response_deserializer=posts__pb2.PostUploadAck.FromString,
                )


class PostsSyncServicer(object):
    """Missing associated documentation comment in .proto file."""

    def refreshPosts(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def queryPosts(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def uploadPosts(self, request_iterator, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_PostsSyncServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'refreshPosts': grpc.unary_stream_rpc_method_handler(
                    servicer.refreshPosts,
                    request_deserializer=posts__pb2.PostQuery.FromString,
                    response_serializer=posts__pb2.Post.SerializeToString,
            ),
            'queryPosts': grpc.unary_stream_rpc_method_handler(
                    servicer.queryPosts,
                    request_deserializer=posts__pb2.PostQuery.FromString,
                    response_serializer=posts__pb2.Post.SerializeToString,
            ),
            'uploadPosts': grpc.stream_unary_rpc_method_handler(
                    servicer.uploadPosts,
                    request_deserializer=posts__pb2.Post.FromString,
                    response_serializer=posts__pb2.PostUploadAck.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'PostsSync', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class PostsSync(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def refreshPosts(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(request, target, '/PostsSync/refreshPosts',
            posts__pb2.PostQuery.SerializeToString,
            posts__pb2.Post.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def queryPosts(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(request, target, '/PostsSync/queryPosts',
            posts__pb2.PostQuery.SerializeToString,
            posts__pb2.Post.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def uploadPosts(request_iterator,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.stream_unary(request_iterator, target, '/PostsSync/uploadPosts',
            posts__pb2.Post.SerializeToString,
            posts__pb2.PostUploadAck.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
