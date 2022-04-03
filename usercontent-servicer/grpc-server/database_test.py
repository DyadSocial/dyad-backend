import redis
from gens.google.protobuf.timestamp_pb2 import Timestamp
import gens.content_pb2 as content
import gens.posts_pb2 as posts

r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=False)
currentTime = Timestamp()
currentTime.GetCurrentTime()
testPost = posts.Post(id = "1", author = "vncp", content = "hello world", last_updated=currentTime, created=currentTime, title="TitleTest", group="reno")
print(type(testPost.SerializeToString()))
r.lpush("hi", testPost.SerializeToString())
val = r.lindex("hi", 0);
print(type(val));
response = posts.Post()
val = response.ParseFromString(val);
print(response)
print(r.lindex("hi", 500));
print(posts.PostUploadAck(id=200, saved_time=currentTime))
