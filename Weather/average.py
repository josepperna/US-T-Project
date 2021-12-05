import csv




def weather_average(month):
    with open(f"{month}Rain.csv", newline='') as csvfile:
        weather_data = csv.reader(csvfile, delimiter=',', quotechar='|')
        data = []
        total15 = 0.0
        for row in weather_data:
            total15 += float(row[-1])
            if int(row[4]) % 12 == 0:
                new_row = row
                average15 = total15/12
                new_row[7] = average15
                new_row = new_row[0:8]
                total15 = 0
                data.append(new_row)
        return data


data = weather_average("May")

with open("May1.csv", "w") as f:
    wr = csv.writer(f)
    for i in data:
        wr.writerow(i)