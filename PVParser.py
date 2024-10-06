import datetime

import pandas as pd
import openpyxl
import os
from tinydb import TinyDB, Query

from astropy.io.fits import append

DATA_PATH = "D:/DOWNLOADED/Fotowoltaika"
STORAGE_DB = ""

class DataManager:

    def __init__(self, filepath: str = DATA_PATH):
        self.filepath = filepath
        self.data = pd.DataFrame(columns=['Date', 'kWh', 'Type', 'month', 'year'])

    def import_data(self) -> list:
        return os.listdir(self.filepath)

    #TODO: raise ValueError("No objects to concatenate")
    #TODO ValueError: No objects to concatenate
    def load_xlsx_data(self, files: list):
        pv_dfs = list()

        for file in files:
            fpath = os.path.join(self.filepath, file)
            if 'xlsx' not in fpath:
                continue
            df = pd.read_excel(fpath, engine="openpyxl")
            pv_dfs.append(df)

        temp_df = pd.concat(pv_dfs)
        oReport.column_value_modification('Data', 'Date', temp_df)
        oReport.row_clean('Date', '24:00', '00:00', temp_df)
        oReport.column_value_modification(' Wartość kWh', 'kWh', temp_df)
        oReport.column_value_modification('Rodzaj', 'Type', temp_df)
        oReport.row_clean('Type', 'oddanie', 'production', temp_df)
        oReport.row_clean('Type', 'pobór', 'consumption', temp_df)
        oReport.convert_to_datetime(temp_df)
        self.data = pd.concat([self.data, temp_df])


    def add_data_manually(self):
        pass


    def save_dataframe_as_pickle(self):
        now = datetime.datetime.now()
        formatted_date_time = now.strftime('%d_%m_%Y_%H_%M_%S')
        self.data.to_pickle(DATA_PATH + os.path.sep + f"{formatted_date_time}.pickle")

    # @staticmethod
    def load_most_recent_data(self, extension: str = ".pickle"):
        most_recent_file = None
        most_recent_timestamp = None
        for file in os.listdir(self.filepath):
            if file.endswith(extension):
                timestamp_str = file[:-7]  # Remove the ".pickle" extension
                timestamp = datetime.datetime.strptime(timestamp_str, "%d_%m_%Y_%H_%M_%S")
                if most_recent_file is None or timestamp > most_recent_timestamp:
                    most_recent_file = file
                    most_recent_timestamp = timestamp

        if most_recent_file:
            self.data = pd.read_pickle(DATA_PATH + os.path.sep + most_recent_file)
        else:
            print('There is no saved data to be loaded')

    #TODO: dodac walidacje w przypadku gdy dane juz są przetworzone
    #TODO: gdy
    def column_value_modification(self, column: str, new_column: str, opt_dataframe = None):
        a =5
        if opt_dataframe is not None:
            opt_dataframe.rename(columns={column: new_column}, inplace=True)
        else:
            if self.data.empty:
                raise TypeError("Data is still not loaded")
            else:
                self.data.rename(columns={column: new_column}, inplace=True)

    def row_clean(self, column: str, row_value: str, new_value: str, opt_dataframe = None):
        if opt_dataframe is not None:
            opt_dataframe[column] = opt_dataframe[column].str.replace(row_value, new_value)
        else:
            if self.data.empty:
                raise TypeError("Data is still not loaded")
            else:
                self.data[column] = self.data[column].str.replace(row_value, new_value)

    #TODO: dodac validacje w przypadku gdy dane są juz przetworzone
    #TODO: z racji, ze dochodzi tu do pracy nad typami to sprawdzic czy dane nie sa juz typu datetime. Jesli tak to skip
    def convert_to_datetime(self, opt_dataframe=None):
        if opt_dataframe is not None:
            opt_dataframe['Date'] = pd.to_datetime(opt_dataframe['Date'])
            opt_dataframe['month'] = opt_dataframe['Date'].dt.month
            opt_dataframe['year'] = opt_dataframe['Date'].dt.year
        else:
            if self.data.empty:
                raise TypeError("Data is still not loaded")
            else:
                self.data['Date'] = pd.to_datetime(self.data['Date'])
                self.data['month'] = self.data['Date'].dt.month
                self.data['year'] = self.data['Date'].dt.year

class CalculusManager:
    def __init__(self, data: DataManager):
        self.data = data.data
        self.consumption  = self.data[self.data["Type"] == "consumption"]
        self.production = self.data[self.data["Type"] == "production"]

    def yearly_consumption(self):
        return self.consumption.groupby('year')['kWh'].sum()

    def monthly_consumption(self, year):
        return self.consumption[self.consumption['year'] == year].groupby('month')['kWh'].sum()

    def yearly_production(self):
        return self.production.groupby('year')['kWh'].sum()

    def monthly_production(self, year):
        return self.production[self.production['year'] == year].groupby('month')['kWh'].sum()

    def cumulative_production_sum(self, year):
        return self.monthly_production(year).cumsum()

    def cumulative_consumption_sum(self, year):
        return self.monthly_consumption(year).cumsum()

    def get_years(self):
        return self.data.year.unique()

    def production_between_dates(self, date_min, date_max):
        """
        e.g
        date_min = '2023-01-01 00:00:00'
        date_max = '2024-01-01 00:00:00'
        """
        return self.production[self.production['Data'].between(date_min, date_max)].kWh.sum().copy()

    def consumption_between_dates(self, date_min, date_max):
        """
        e.g
        date_min = '2023-01-01 00:00:00'
        date_max = '2024-01-01 00:00:00'
        """
        return self.consumption[self.consumption['Date'].between(date_min, date_max)].kWh.sum().copy()


class ReportManager:
    pass

if __name__ == "__main__":


    oReport = DataManager()
    collected_data = oReport.import_data()
    oReport.load_xlsx_data(collected_data)
    oCalculus = CalculusManager(oReport)

