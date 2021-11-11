import csv
import datetime


def gen_data(frame_id, bike_data):
    journies = []
    previous_loc = [["0", "0"], "2021-05-01 00:00:01"]
    for row in bike_data:
        if row[4] == str(frame_id):
            long = row[8]
            lat = row[7]
            if [long, lat] != previous_loc[0]:
                time = row[1]
                parsed_time = datetime.datetime.strptime(time, "%Y-%m-%d %H:%M:%S")
                prev_parsed_time = datetime.datetime.strptime(previous_loc[1], "%Y-%m-%d %H:%M:%S")
                duration = (parsed_time-prev_parsed_time).seconds
                journey = [previous_loc, [long, lat], duration]
                previous_loc = [[long, lat], time]
                journies.append(journey)

    return journies


def get_all_bikes():
    bikes = []
    with open('bleeperbike-historical-data-052021.csv', newline='') as csvfile:
        bike_data = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in bike_data:
            bikes.append(row[4])
    bikes = list(set(bikes))
    return bikes


def write_to_csv(frame_id, bike_data):
    with open(f'./bikeData/{frame_id}.csv', 'w') as csv_file:
        write = csv.writer(csv_file)
        journey_data = gen_data(frame_id, bike_data)
        data = []
        for journey in journey_data:
            row = []
            row.append(journey[0][0][0])
            row.append(journey[0][0][1])
            row.append(journey[0][1])
            row.append(journey[1][0])
            row.append(journey[1][1])
            row.append(journey[2])
            data.append(row)
        write.writerows(data)

data = []

with open('bleeperbike-historical-data-052021.csv', newline='') as csvfile:
    bike_data = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in bike_data:
        data.append(row)

#print(get_all_bikes())
for bike in get_all_bikes():
    print(f"Saving frame_id: {bike}")
    write_to_csv(int(bike), data)
