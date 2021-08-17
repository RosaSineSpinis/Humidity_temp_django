from functions import ProcessDataFromDjango, Plotter
import time
from pprint import pprint
import pandas as pd
import json


df = ProcessDataFromDjango().process_data()
print('type', df.dtypes)
df.iloc[:, -1] = [int(time.mktime(t.timetuple())) * 1000 for t in df.iloc[:, -1] if t]

list_of_data = []
colors = [
            'rgba(255, 99, 132, 0.6)',
            'rgba(54, 162, 235, 0.6)',
            'rgba(255, 206, 86, 0.6)',
            'rgba(75, 192, 192, 0.6)'
        ]


# class OneSeries:
#     def __init__(self, x_data, y_data, color, name):
#         self.data_xy = []
#         self.color = color
#         self.name = name
#         # print(name, x_data)
#         for idx in range(len(x_data)):
#             # print(x_data['Date_time'][idx], y_data[self.name][idx])
#             self.data_xy.append({'x': x_data['Date_time'], 'y': y_data[self.name][idx]})
#
#     def __str__(self):
#         return f"data_xy {self.data_xy} , color {self.color}, name {self.name}"
#
#
# s1 = OneSeries(df.iloc[:, [-1]], df.iloc[:, [-2]], 'rgba(255, 99, 132, 0.6)', df.columns[-2])
# s2 = OneSeries(df.iloc[:, [-1]], df.iloc[:, [-3]], 'rgba(54, 162, 235, 0.6)', df.columns[-3])
# s3 = OneSeries(df.iloc[:, [-1]], df.iloc[:, [-4]], 'rgba(255, 206, 86, 0.6)', df.columns[-4])
# s4 = OneSeries(df.iloc[:, [-1]], df.iloc[:, [-5]], 'rgba(75, 192, 192, 0.6)', df.columns[-5])
#
# data = {s1, s2, s3, s4}


for idx, col in enumerate(df.columns):
    if idx == len(df.columns) - 1:
        break

    df_new = df.loc[:, [col, 'Date_time']]
    df_new.columns = ['y', 'x']
    df_new = df_new.to_dict(orient="records")
    list_of_data.append({'series' + str(idx): {'data': df_new, 'color': colors[idx], 'name': col}})
    # pprint(list_of_data)

data_series = json.dumps(list_of_data)

# x_name = list(df.keys())[-1]


# df.iloc[:, -1] = [int(time.mktime(t.timetuple())) * 1000 for t in df.iloc[:, -1] if t]
# print(df)
# df = df.iloc[:, -2:]

# data_y = df.iloc[:, -2:-1]
# labels = df.iloc[:, -1:]
# data = df.to_dict(orient='records')
# label = list(labels.Date_time)
# print(label)
# data = list(data_y.H4)
# print(data)

# labels = labels.to_dict(orient='records')
# data_y = data_y.to_dict(orient='records')
#
# print("data type", type(labels))
# print("data type", type(data_y))
# pprint(labels)
# pprint(data_y)

# x = data[x_name]

# x = x.pd.to_datetime()
# print(x)
# print(x_name)
# print("type", type(data))
# del data[x_name]