import redis
from rq import Queue
import CountingWords

q = Queue('jobs', connection=redis.Redis())

result = q.enqueue(CountingWords.count_words_at_url, 'http://localhost:8000')

print(result)