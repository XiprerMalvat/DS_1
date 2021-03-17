from multiprocessing import Process, Lock
from collections import Counter
import redisFunc
import countWords
import wordCount
import requests

WORKERS = {}
WORKER_ID = 0

def start_worker(id):
    print(id)
    while True:
        data = redisFunc.wait_element_from_queue('jobsQueue')
        if data['program'] == 'countwords':
            result = countWords.count_words(request_file(data['url']))
        elif data['program'] == 'wordcount':
            result = wordCount.word_count(request_file(data['url']))

        if data['fragments'] == '1':
            redisFunc.send_response(data['result_queue'], result)
        else:
            redisFunc.send_element_to_add(data['queue'], data['program'], data['result_queue'], data['fragments'], result)
            redisFunc.notify_adder_worker('adderQueue', data['queue'])

def start_adder_worker(id):
    print(id)
    i = 0
    while True:
        notification = redisFunc.wait_element_from_queue('adderQueue')
        data1 = redisFunc.get_element_from_queue(notification['queue'])
        data2 = redisFunc.get_element_from_queue(notification['queue'])
        if data2 == None:
            redisFunc.send_element_to_add(data1['queue'], data1['program'], data1['result_queue'], data1['fragments'], data1['value'])
        else:
            newValue = dict(Counter(data1['value'])+Counter(data2['value']))
            if ((data1['fragments']-1) == 1):
                redisFunc.send_response(data1['result_queue'], newValue)
            else:
                redisFunc.send_element_to_add(data1['queue'], data1['program'], data1['result_queue'], data1['fragments']-1, newValue)



def terminate_worker():
    global WORKERS
    global WORKER_ID

    if WORKER_ID != 0:
        WORKERS[WORKER_ID-1].terminate()
        WORKER_ID -= 1
        del WORKERS[id]

def create_worker():
    global WORKERS
    global WORKER_ID

    if WORKER_ID == 0:
        proc = Process(target=start_adder_worker, args=(WORKER_ID,))
    else
        proc = Process(target=start_worker, args=(WORKER_ID,))
    proc.start()
    WORKERS[WORKER_ID] = proc

    WORKER_ID += 1

def request_file(url):
    resp = requests.get(url)
    return(resp.text)