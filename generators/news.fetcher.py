#import proto.Task_pb2 as proto

NEWS_SOURCES_FILE = '/data/scripts/data/news.sources.txt'

with open(NEWS_SOURCES_FILE) as f:
  urls = f.readlines()

print urls
#request = proto.TaskRequest()
