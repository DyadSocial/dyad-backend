import asyncio
import logging
import redis
from typing import AsyncIterable, Iterable

import grpc
from gens.google.protobuf.timestamp_pb2 import Timestamp
import gens.content_pb2 as content
import gens.posts_pb2 as posts
import gens.posts_pb2_grpc as posts_grpc

r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=False)

def getPosts(query, filter = None):
    posts_list = []
    index = 0;
    # Populate posts with serialized binary data
    val = ""
    while val != None:
        val = r.lindex(query, index)
        if val != None:
            posts_list.append(val)
        index = index + 1
    # Deserialize the binary
    res = []
    for idx in range(len(posts_list)):
        post = posts.Post()
        post.ParseFromString(posts_list[idx])
        res.append(post)
    return res

class PostSync(posts_grpc.PostsSyncServicer):
    async def refreshPosts(self, request: posts.PostQuery, context):
        print("Service: RefreshPosts")
        for post in getPosts(request.gid):
            yield post

    async def queryPosts(self, request: posts.PostQuery, context):
        print("Service: QueryPosts")
        for post in getPosts(request.gid):
            yield post

    async def uploadPosts(self, request_iterator: AsyncIterable[posts.Post], context) -> posts.PostUploadAck:
        print("Service: UploadPosts")
        async for post in request_iterator:
            list_length = r.llen(post.group)
            found = False
            for i in range(list_length):
                list_post = r.lindex(post.group, i)
                parsed_post = posts.Post()
                parsed_post.ParseFromString(list_post) 
                if parsed_post.author == post.author and parsed_post.id and parsed_post.id == post.id:
                    print("Updating")
                    r.lset(post.group, i, post.SerializeToString())
                    found = True
            if not found:
                r.lpush(post.group, post.SerializeToString())
        time = Timestamp()
        time.GetCurrentTime()
        return posts.PostUploadAck(id=200, saved_time=time)

    async def deletePost(self, request: posts.PostQuery, context) -> posts.PostUploadAck:
        print("Service: DeletePost")
        print(request.gid)
        list_length = r.llen(request.gid)
        print(list_length)
        found = False
        for i in range(list_length):
            list_post = r.lindex(request.gid, i)
            parsed_post = posts.Post()
            parsed_post.ParseFromString(list_post)
            print(f"Request: {request.id}:{request.author}")
            print(f"Found: {parsed_post.id}:{parsed_post.author}")
            if parsed_post.author == request.author and parsed_post.id and parsed_post.id == request.id:
                print(f"Removing ID: {request.id}:{request.author}")
                r.lrem(request.gid, 0, list_post)
                found = True
        time = Timestamp()
        time.GetCurrentTime()
        return posts.PostUploadAck(id=200, saved_time=time)

async def serve() -> None:
    server = grpc.aio.server()
    posts_grpc.add_PostsSyncServicer_to_server(PostSync(), server)
    listen_addr = '0.0.0.0:50051'
    server.add_insecure_port(listen_addr)
    logging.info("Starting server on %s", listen_addr)
    await server.start()
    await server.wait_for_termination()

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(serve())