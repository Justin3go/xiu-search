import pickle
import redis
import re
import hashlib
import sys
sys.path.append("C:\My_app\code\咻Search")
from config import REDIS_HOST, REDIS_PASSWORD

def real_time_count(key, init):
    redis_cli = redis.Redis(host=REDIS_HOST, password=REDIS_PASSWORD)
    if redis_cli.get(key):
        count = pickle.loads(redis_cli.get(key))
        count = count + 1
        count = pickle.dumps(count)
        redis_cli.set(key, count)
    else:
        count = pickle.dumps(init)
        redis_cli.set(key, count)