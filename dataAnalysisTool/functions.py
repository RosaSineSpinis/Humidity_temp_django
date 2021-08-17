import os
import pandas as pd
import pandas
import math
from pathlib import Path
import time
import pprint

class ProcessDataFromDjango:
    def __init__(self):
        pass

    @staticmethod
    def process_data():
        BASE_DIR = Path(__file__).resolve().parent.parent
        path = os.path.join(BASE_DIR, 'media', 'documents')
        dirs_hum_obj = OpenDirectoryPathClass(path, extension='csv', filename_list=[], phrase_in_filename='RH', path_list=[])
        filename_list, path_list = dirs_hum_obj.walkDirectoryTopDown()

        obj = PandasDataFrameListToOneData()
        df_hum = obj.listToOneDataFrameConcat(filename_list, path_list)
        df_hum = df_hum.iloc[:, 2:]


        dirs_temp_obj = OpenDirectoryPathClass(path, extension='csv', filename_list=[], phrase_in_filename='Temp', path_list=[])
        filename_list, path_list = dirs_temp_obj.walkDirectoryTopDown()
        obj = PandasDataFrameListToOneData()
        df_temp = obj.listToOneDataFrameConcat(filename_list, path_list)
        df_temp = df_temp.iloc[:, 2:]


        # print("df", df)
        # df.iloc[:, -1] = pd.to_datetime(df.iloc[:, -1])
        # print(df.dtypes)
        # data_to_plot = dict()
        # for idx, name in enumerate(df.columns):
        #     if idx > 1:
        #         data_to_plot[name] = df[name].tolist()
        #
        # return data_to_plot
        return df_hum, df_temp

    def fetch_data_to_database(self, df_hum, df_temp):
        pass

    def fetch_data_from_database(self):
        pass

    @staticmethod
    def prepare_data_to_chart_js(df):
        x_name = list(df.keys())[-1]


        df.iloc[:, -1] = [int(time.mktime(t.timetuple())) * 1000 for t in df.iloc[:, -1] if t]

        list_of_data = []

        # colors of series
        colors = [
            'rgba(255, 99, 132, 0.6)',
            'rgba(54, 162, 235, 0.6)',
            'rgba(255, 206, 86, 0.6)',
            'rgba(75, 192, 192, 0.6)'
        ]

        for idx, col in enumerate(df.columns):
            if idx == len(df.columns) - 1:
                break

            df_new = df.loc[:, [col, 'Date_time']]
            df_new.columns = ['y', 'x']
            df_new = df_new.to_dict(orient="records")

            list_of_data.append({'data': df_new, 'color': colors[idx], 'name': col})


        data_series = {'all_series': list_of_data}

        # data = df.to_dict(orient='records')


        # 'rgba(153, 102, 255, 0.6)',
        # 'rgba(255, 159, 64, 0.6)',
        # 'rgba(255, 99, 132, 0.6)'

        return data_series

class OpenDirectoryPathClass():
    # class made to cooperate with gui
    def __init__(self, path, extension, filename_list, phrase_in_filename, path_list):
        self.path = path
        self.extension = extension
        self.filename_list = filename_list # empty at the beginning
        self.phrase_in_filename = phrase_in_filename
        self.path_list = path_list # empty at the beginning

    def walkDirectoryTopDown(self):
        """
        extract foldes with specific phrase in the name
        :return: self.filename_list, self.path_list
        """
        for current_path, subfolders_name, filenames in os.walk(self.path):
            # pass
            # # print('The current folder is ' + current_path)
            # for subfolder in subfolders_name:
            #     pass
            #     # print('SUBFOLDER OF ' + current_path + ': ' + subfolder)
            for filename in filenames:
                if self.extension in filename:
                    if self.phrase_in_filename in filename:
                        # print('FILE INSIDE with ' + phrase_in_filename + " " + current_path + ': ' + filename)
                        self.path_list.append(current_path + '/' + filename)
                        self.filename_list.append(filename)

        return self.filename_list, self.path_list




class PandasDataFrameListToOneData:
    '''Takes list of paths and filenames and merge them into one, delete NULL column and sort them in ascending way'''
    def __init__(self):
        self.new_column_name = 'Date_time'

    def listToOneDataFrameConcat(self, filename_list, path_list):
        frames = []
        try:
            # print(df)
            def checkMaxNumOfColumn():
                max_num_columns = 0
                for idx, item in enumerate(path_list):
                    # print(item)
                    df = pandas.read_csv(item, encoding='utf-16', delimiter='\t')
                    # print(len(df.columns))

                    if max_num_columns < len(df.columns):
                        max_num_columns = len(df.columns)
                # print("max_num_columns", max_num_columns)
                return max_num_columns

            max_num_columns = checkMaxNumOfColumn()

            for idx, item in enumerate(path_list):
                # print(item)
                df = pandas.read_csv(item, encoding='utf-16', delimiter='\t')
                if len(df.columns) == max_num_columns:
                    # print("item", item)
                    # print(type(df))
                    # print(df.iloc[:,1])
                    # print(df)
                    # print(df.iloc[:, 2])
                    # print(df.columns)
                    # print(df)
                    # print("Unnamed: 0" in df.columns)
                    if "Unnamed: 0" in df.columns:
                        df.rename(columns={'Unnamed: 0': 'Time'}, inplace=True)  # column without name, rename then
                    if "Unnamed: 1" in df.columns:
                        df.rename(columns={'Unnamed: 1': 'Date'}, inplace=True)  # column without name, rename then
                     # print(df)
                    # df.drop(df.columns[[12]], axis=1, inplace=True) #remove columns with null, idk wjy it exists
                    df[self.new_column_name] = pandas.to_datetime(
                        df.iloc[:, 0] + ' ' + df.iloc[:, 1])  # merge data data + time and create new column
                    df[self.new_column_name] = pandas.to_datetime(df[self.new_column_name], format='%Y-%m-%d %H:%M:%S')
                    # df.to_csv('rewritten_' + filename_list[idx])  # we save file to csv just in case
                    frames.append(df)
                    df = pandas.concat(frames, ignore_index=True)
            # print(df)
            df.sort_values(by=[self.new_column_name], inplace=True, ascending=True) #sortning
            df = df.reset_index(drop=True) #reorganise index
            for column in df.columns[:]:
                if df.loc[:, column].isnull().all():
                    df.drop(df.loc[:, [column]], axis=1, inplace=True) #remove columns with null
                    continue
                if df.loc[:, column].nunique() == 1:
                    # print("df.loc[:, column] ", df.loc[:, column])
                    df.drop(df.loc[:, [column]], axis=1, inplace=True) #remove columns with null
            if 'Date' in df.columns:
                df.loc[:,'Date'] = pandas.to_datetime(df.loc[:,'Date'], format='%d/%m/%Y')
            else:
                df.rename(columns = {df.columns[1]: 'Data'}, inplace=True)
                df.iloc[:, 1] = pandas.to_datetime(df.iloc[:, 1], format='%m/%d/%Y')
            for column in df.columns[2:]:
                if column != "Date_time":
                    idx = df.columns.get_loc(column)
                    df.iloc[:, idx] = df.iloc[:, idx]/10
                    # for x in df.iloc[:, idx]:
                    #     print("column", column,"idx", idx,"x", x)
            return df

        except pandas.errors.EmptyDataError:
            print("listToOneDataFrameConcat, input failed")
        except ValueError:
            print("listToOneDataFrameConcat, input failed")
        except:
            print("listToOneDataFrameConcat, something gone wrong")


    def obtainBeginningDate(self, df):
        try:
            if "Date" in df.columns:
                # print("in if")
                # print(df)
                # return df.iloc[0, df.columns.get_iloc('Date')]
                return df.loc[0, 'Date']
            else:
                # print("we are in else")
                # print(df)
                # print(df.iloc[0, 1])
                return df.iloc[0, 1]


                # print(df.iloc[0,1])
                # df.iloc['Date_time']
        except pandas.errors.EmptyDataError:
            pass
        except ValueError:
            pass

    def obtainEndingDate(self, df):
        try:
            if "Date" in df.columns:
                return df.iloc[-1, df.columns.get_loc('Date')]
            else:
                return df.iloc[-1, 1]

                # print(df.iloc[0,1])
                # df.iloc['Date_time']
        except pandas.errors.EmptyDataError:
            pass
        except ValueError:
            pass


ProcessDataFromDjango().process_data()


import matplotlib.pyplot as plt
import matplotlib
import matplotlib.dates as mdates
import pandas
from pandas.plotting import register_matplotlib_converters
import numpy as np


class Plotter():
    '''Two plottig functions, takes number of series and their data and plot them in one or many graphs'''
    def __init__(self):
        pass

    def autofmt_datetime_axis(self, ax, minor_ticks=False):
        """Should I seperate minor_ticks from minor_tick_labels?
        """
        # Get the xmin and xmax of the axis object
        xmin = mdates.num2date(ax.get_xlim()[0])
        xmax = mdates.num2date(ax.get_xlim()[1])

        # Convert to a datetime object
        dt = xmax - xmin
        # print(dt)
        return None


    def plotAllInOne(self, cb_checked_list_string, users_labels_name, df, graph_title_name, text=""):
        """
        :param cb_checked_list_string: possible values 'H1', 'H2', 'H3', 'H4'
        :param users_labels_name: possible values
        :param df: df with time and regions
        :param graph_title_name: title of the  graph
        :param text: text
        :return:
        """
        pandas.plotting.register_matplotlib_converters()  # conversion to matlibplot file


        strefa_name = cb_checked_list_string
        number_of_strefa = len(strefa_name)
        # print(number_of_strefa)

        number_of_separate_plots = 1
        fig, ax = plt.subplots(nrows=number_of_separate_plots, ncols=1, squeeze=False, sharex='col',
                               sharey='row')  # squeeze = False, always returns 2x2 matrix
        # plt.suptitle("Temperature")
        n = 0
        # for n in range(len(strefa_name)):
        for row in ax:
            for col in row:
                # ax.plot(df.iloc[:, 0], df.Strefa2)
                ##ax.set_xticklabels= (df.iloc[:, 0])

                for x in range(number_of_strefa):
                    # print(df.Date_time)
                    print(strefa_name[x])
                    '''pandas plot seems slow with sharex'''
                    # col.plot(df.Date_time, df[strefa_name[x]], label=users_labels_name[x])
                    '''numpy version'''
                    col.plot(df['Date_time'], df[strefa_name[x]], label=users_labels_name[x])
                ##plt.xticks(df.iloc[:, 0], rotation='vertical')

                '''pandas plot seems slow with sharex. below is code '''
                plt.xlabel(df.columns[0] + " / " + df.columns[1])  # name of x axis
                '''numpy version'''
                # plt.xlabel(df.dtype.names[0] + " / " + df.dtype.names[1])

                # plt.ylabel(strefa_name[n]) #name of y axis - with many plots give only one input

                col.set_ylabel(text)
                col.set_yticklabels = (strefa_name[n])

                self.autofmt_datetime_axis(col, False)

                col.minorticks_on()
                # this block works fine give some kind of dynamic legend
                xtick_locator = mdates.AutoDateLocator()
                xtick_formatter = mdates.ConciseDateFormatter(xtick_locator)
                col.xaxis.set_major_locator(xtick_locator)
                col.xaxis.set_major_formatter(xtick_formatter)


                for label in col.xaxis.get_minorticklabels():
                    label.set_color('black')
                    label.set_rotation(45)
                    label.set_fontsize(8)
                    label.set_ha('right')

                for label in col.xaxis.get_ticklabels():
                    # label is a Text instance
                    label.set_color('black')
                    label.set_rotation(45)
                    label.set_fontsize(8)
                    label.set_ha('right')
                n += 1

        fig.subplots_adjust(bottom=0.2)
        # fig.tight_layout()
        fig.suptitle(graph_title_name)
        # plt.legend()
        # plt.show()
        return fig

    def plot(self, cb_checked_list_string, users_labels_name, df, graph_title_name, text=""):
        pandas.plotting.register_matplotlib_converters()  # conversion to matlibplot file

        strefa_name = cb_checked_list_string
        number_of_strefa = len(strefa_name)
        print("df ", type(df))
        fig, ax = plt.subplots(nrows=number_of_strefa, ncols=1, squeeze=False, sharex='col', sharey='row') #squeeze = False, always returns 2x2 matrix
        n = 0
        for row in ax:
            for col in row:
                '''pandas plot seems slow with sharex - below panada code'''
                col.plot(df['Date_time'], df[strefa_name[n]])

                '''pandas code below'''
                '''numpy version'''
                plt.xlabel(df.dtype.names[0] + " / " + df.dtype.names[1])

                col.set_ylabel(users_labels_name[n])
                col.set_yticklabels = (strefa_name[n])



                self.autofmt_datetime_axis(col, False)

                col.minorticks_on()

                xtick_locator = mdates.AutoDateLocator()
                xtick_formatter = mdates.ConciseDateFormatter(xtick_locator)
                col.xaxis.set_major_locator(xtick_locator)
                col.xaxis.set_major_formatter(xtick_formatter)

                for label in col.xaxis.get_minorticklabels():
                    label.set_color('black')
                    label.set_rotation(45)
                    label.set_fontsize(8)
                    label.set_ha('right')

                for label in col.xaxis.get_ticklabels():
                    # label is a Text instance
                    label.set_color('black')
                    label.set_rotation(45)
                    label.set_fontsize(8)
                    label.set_ha('right')
                n += 1

        fig.subplots_adjust(bottom=0.2)
        # fig.tight_layout()
        fig.suptitle(graph_title_name + " " + text)
        plt.show()
        return

