from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt


def epoch_to_datetime(input):
    datetime_object = datetime.fromtimestamp(input/1000)
    return datetime_object

def mobile_to_dataframe():
    # Read the JSON file into a DataFrame
    df = pd.read_json('12h.json')

    # Access the "data" key of the DataFrame
    data = df["data"]

    # Create an empty list to store the DataFrames
    dfs = []
    accelerometer_array = []
    gyroscope_array = []

    # Iterate over the elements in the "data" list
    for element in data:
        type = element["imuType"]
        for x in element["data"]:
            value = x["values"]
            timestamp = x["timestamp"]
            n = 13
            timestamp_change = [timestamp[i:i + n] for i in range(0, len(timestamp), n)]
            timestamp_time = epoch_to_datetime(int(timestamp_change[0]))
            if len(value) == 3:
                if type == "ACCELEROMETER":
                    accelerometer_array.append([timestamp_time,value[0],value[1],value[2]])
                else:
                    gyroscope_array.append([timestamp_time, value[0], value[1], value[2]])
                temp_df = pd.DataFrame(value)
                temp_df = temp_df.transpose()
                temp_df.columns = ["x-value","y-value","z-value"]
                temp_df["timestamp"] = timestamp_time
                temp_df["type"] = type
                dfs.append(temp_df)

    # Concatenate all the DataFrames in the list
    result_df = pd.concat(dfs)
    #print(result_df)
    return gyroscope_array, accelerometer_array

def plotting_mobile():

    mobile_data = mobile_to_dataframe()
    gyroscoop_x, gyroscoop_y, gyroscoop_z, time = zip(*[(x[1], x[2], x[3], x[0]) for x in mobile_data[0]])
    plt.plot(time, gyroscoop_x, '-*', label='gyroscoop x')
    plt.plot(time, gyroscoop_y, '-s', label='gyroscoop y')
    plt.plot(time, gyroscoop_z, '-o', label='gyroscoop z')
    plt.legend()
    plt.plot()
    plt.xlabel('Time')
    plt.ylabel('x,y,z values')
    plt.savefig('gyroscope.png')
    plt.show()


    accelerometer_x, accelerometer_y, accelerometer_z, time = zip(*[(x[1], x[2], x[3], x[0]) for x in mobile_data[1]])
    plt.plot(time, accelerometer_x, '-*', label='accelerometer x')
    plt.plot(time, accelerometer_y, '-s', label='accelerometer y')
    plt.plot(time, accelerometer_z, '-o', label='accelerometer z')
    plt.legend()
    plt.plot()
    plt.xlabel('Time')
    plt.ylabel('x,y,z values')
    plt.savefig('accelerometer.png')
    plt.show()


def fitbit_to_dataframe():
    # Read the JSON file into a DataFrame
    df = pd.read_json('09hfitbit.json')

    data = df["data"]
    date = data[0]["id"].split("/")[1]
    steps_total = data[0]["data"]["summary"]["steps"]
    distance_total = data[0]["data"]["summary"]["distances"][0]["distance"]

    steps_array = [[x["t"], x["v"]] for x in data[0]["data"]["activities-steps-intraday"]]
    distance_array = [[x["t"], x["v"]] for x in data[0]["data"]["activities-distance-intraday"]]
    heart_rate_array = [[x["t"], x["v"]] for x in data[0]["data"]["activities-heart-intraday"] if int(x["v"]) != 0]


    return steps_array, distance_array, heart_rate_array


def plotting_fitbit():
    fitbit_data = fitbit_to_dataframe()
    x1 = []
    y1 = []
    for x in fitbit_data[0]:
        if len(y1) == 0:
            y1.append(x[1])
        else:
            lengte = len(y1)
            y1.append(float(x[1])+float(y1[lengte-1]))
        x1.append(x[0])

    x2 = []
    y2 = []
    for x in fitbit_data[1]:
        if len(y2) == 0:
            y2.append(x[1])
        else:
            lengte = len(y2)
            y2.append(float(x[1]) + float(y2[lengte - 1]))
        x2.append(x[0])

    x3, y3 = zip(*[x for x in fitbit_data[2]])


    #Plot of the steps per day
    plt.plot(x1, y1, '-*')
    plt.plot()
    plt.xlabel('Time (24 hours)')
    plt.ylabel('Steps')
    plt.savefig('steps.png')
    plt.show()

    #Plot of the distance per day
    plt.plot(x2, y2, '-*')
    plt.plot()
    plt.xlabel('Time (24 hours)')
    plt.ylabel('Distance')
    plt.savefig('distance.png')
    plt.show()

    #Plot of the heart rate every moment of the day
    plt.plot(x3, y3, '-*')
    plt.plot()
    plt.xlabel('Time (24 hours)')
    plt.ylabel('Heart rate')
    plt.savefig('Heartrate.png')
    plt.show()


plotting_mobile()
plotting_fitbit()