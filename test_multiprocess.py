import os
import time
import json
import requests
import multiprocessing

proxies = {
    "http":"",
    "https":""
}

target = json.load(open('result1.txt', 'r'))
APIKEY = ""

def download_task(key, filehash):
    try:
        if os.path.exists("download/"+key+"/"+filehash):
            download_callback(key, filehash)
            return
    except:
        pass
    
    time.sleep(1)
    try:
        res = requests.get("https://androzoo.uni.lu/api/download?apikey={}&sha256={}".format(APIKEY ,filehash), proxies=proxies)
    except Exception as e:
        print(key, filehash)
        print(e)

    print(res, res.status_code)

    if res.status_code==200:
        if not os.path.exists("download/"+key):
            os.makedirs("download/"+key)
        if not os.path.exists("download/"+key+"/"+filehash):
            with open("download/"+key+"/"+filehash, "wb") as f:
                f.write(res.content)
            f.close()
        print(filehash)

        download_callback(key, filehash)


def download_callback(key, filehash):
    print(1)
    global target
    if target[key].get("downloaded") is None:
        target[key]["downloaded"] = []

    target[key]["downloaded"].append(filehash)


pool = multiprocessing.Pool(20) # remote limit
for key, values in target.items():

    if values['sha256']  != []:
        print(key, values['sha256'])
        sha256set = values['sha256']
        for filehash in sha256set:
            pool.apply_async(download_task, args=(key, filehash))

pool.close()
pool.join()
json.dump(target, open('result2.txt','w'), indent=4)