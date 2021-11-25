import requests
import csv
import os
import multiprocessing
import json

SERVER_IP = "34.90.173.101:8080"

def get_gpx(lat1, long1, lat2, long2, i, bike_id):

    body = {"coordinates":[[long1,lat1],[long2,lat2]]}

    headers = {
        'Accept': 'application/json, application/geo+json, application/gpx+xml, img/png; charset=utf-8',
        'Content-Type': 'application/json; charset=utf-8'
    }
    r = requests.post('http://{}/ors/v2/directions/driving-car/geojson'.format(SERVER_IP), json=body, headers=headers)

    if r.status_code != 200:
        return
    else:
        with open("geojson/route_b{}_{}.geojson".format(bike_id, i), "w") as f:
            f.write(json.dumps(r.json()))


def process_bike(filename):
    with open(filename, newline='') as csvfile:
        bike_id = filename.split("/")[-1][0:7]
        bike_data = csv.reader(csvfile, delimiter=',', quotechar='|')
        i = 0
        for row in bike_data:
            get_gpx(row[0], row[1], row[3], row[4], i, bike_id)
            i += 1

def multithreaded_processor(file_list):
    i = 0
    for filename in file_list:
        bike_id = filename.split("/")[-1][0:7]
        # os.mkdir("gpx/" + bike_id)
        print(i)
        process_bike("../bleeperDataParse/bikeData/" + filename)
        i += 1

def split(a, n):
    k, m = divmod(len(a), n)
    return (a[i*k+min(i, m):(i+1)*k+min(i+1, m)] for i in range(n))

if __name__ == '__main__':
    # i = 0
    # for filename in os.listdir("../bleeperDataParse/bikeData/"):
    #     print(i)
    #     process_bike("../bleeperDataParse/bikeData/" + filename)
    #     i += 1
    files = os.listdir("../bleeperDataParse/bikeData/")
    chunks = list(split(files, 16))
    jobs = []
    for i in range(16):
        p = multiprocessing.Process(target=multithreaded_processor, args=(chunks[i],))
        jobs.append(p)
        p.start()