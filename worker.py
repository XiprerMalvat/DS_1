from multiprocessing import Process, Lock
import redisFunc
import countWords
import wordCount
import requests

WORKERS = {}
WORKER_ID = 0

def start_worker(id):
    print(id)
    while True:
        data = redisFunc.get_job_from_queue('jobsQueue')
        if data['program'] == 'countwords':
            result = countWords.count_words(request_file(data['url']))
        elif data['program'] == 'wordcount':
            result = wordCount.word_count(request_file(data['url']))

        return(result)

def terminate_worker():
    global WORKERS
    global WORKER_ID

    WORKERS[WORKER_ID-1].terminate()
    WORKER_ID -= 1
    del WORKERS[id]

def create_worker():
    global WORKERS
    global WORKER_ID

    proc = Process(target=start_worker, args=(WORKER_ID,))
    proc.start()
    WORKERS[WORKER_ID] = proc

    WORKER_ID += 1

def request_file(url):
    resp = requests.get(url)
    return(resp.text)