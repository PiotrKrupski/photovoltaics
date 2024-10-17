import datetime

import pandas as pd
import os

class DataMgr:

    DATA_PATH = r"D:\GIT\photo\photovoltaics\Data"

    def __init__(self, filepath: str = DATA_PATH):
        if not isinstance(filepath, str):
            raise TypeError("wrong data type of filepath")
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
        if 'Data' in temp_df.columns:
            temp_df.rename(columns={'Data': 'Date'}, inplace=True)
        if ' Wartość kWh' in temp_df.columns:
            temp_df.rename(columns={' Wartość kWh': 'kWh'}, inplace=True)
        if 'Rodzaj' in temp_df.columns:
            temp_df.rename(columns={'Rodzaj': 'Type'}, inplace=True)

            # Row cleaning (ensure these values exist before replacing)
        if 'Type' in temp_df.columns:
            temp_df.loc[temp_df['Type'] == 'oddanie', 'Type'] = 'production'
            temp_df.loc[temp_df['Type'] == 'pobór', 'Type'] = 'consumption'

            # Date conversion
        temp_df['Date'] = temp_df['Date'].str.replace('24:00', '00:00')
        temp_df['Date'] = pd.to_datetime(temp_df['Date'])
        temp_df['month'] = temp_df['Date'].dt.month
        temp_df['year'] = temp_df['Date'].dt.year

        # Concatenate with existing data (handle empty self.data)
        self.data = pd.concat([self.data, temp_df], ignore_index=True)

    #TODO to add validation for Type & kWh as well
    def add_data_manually(self, new_rows):
        if self.validate_date_format(new_rows):
            new_rows = pd.DataFrame(new_rows)
            new_rows = new_rows.reindex(columns=self.data.columns, fill_value=None)
            self.data = pd.concat([self.data, new_rows], ignore_index=True)
        else:
            raise TypeError("Wrong format of data")

        self.data['Date'].str.replace('24:00', '00:00')
        self.data['Date'] = pd.to_datetime(self.data['Date'])
        self.data['month'] = self.data['Date'].dt.month
        self.data['year'] = self.data['Date'].dt.year


        return self.data


    @staticmethod
    def validate_date_format(new_rows, date_format="%Y-%m-%d %H:%M:%S"):
        """Validates a date string against a given format.

        Args:
        date_str: The date string to validate.
        format: The expected date format.

        Returns:
        True if the date string matches the format, False otherwise.
        """
        if len(new_rows)>1:
            try:
                for row in new_rows:
                    datetime.datetime.strptime(row['Date'], date_format)
            except ValueError:
                return False
            return True
        elif len(new_rows) == 1:
            try:
                datetime.datetime.strptime(new_rows['Date'], date_format)
                return True
            except ValueError:
                return False
        else:
            return False

    def save_dataframe_as_pickle(self):
        now = datetime.datetime.now()
        formatted_date_time = now.strftime('%d_%m_%Y_%H_%M_%S')
        self.data.to_pickle(DataMgr.DATA_PATH + os.path.sep + f"{formatted_date_time}.pickle")

    # @staticmethod
    def load_most_recent_data(self, extension: str = ".pickle"):
        most_recent_file = None
        most_recent_timestamp = None
        for file in os.listdir(DataMgr.DATA_PATH):
            if file.endswith(extension):
                timestamp_str = file[:-7]  # Remove the ".pickle" extension
                timestamp = datetime.datetime.strptime(timestamp_str, "%d_%m_%Y_%H_%M_%S")
                if most_recent_file is None or timestamp > most_recent_timestamp:
                    most_recent_file = file
                    most_recent_timestamp = timestamp

        if most_recent_file:
            self.data = pd.read_pickle(DataMgr.DATA_PATH + os.path.sep + most_recent_file)
        else:
            print('There is no saved data to be loaded')

    def load_data(self, data_filepath: str):
        self.data = pd.read_pickle(data_filepath)


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

if __name__ == "__main__":
    oData = DataMgr()

    data_list = [
        {'Date': "1992-06-10 07:30:30", "kWh": 2000, "Type": "production"},
        {'Date': "1992-06-10 11:44:44", "kWh": 1000, "Type": "consumption"},
        {'Date': "1992-06-10 07:30:30", "kWh": 2000, "Type": "production"},
        {'Date': "1992-06-10 11:44:44", "kWh": 1000, "Type": "consumption"},
        {'Date': "1992-06-10 07:30:30", "kWh": 2000, "Type": "production"},
        {'Date': "1992-06-10 11:44:44", "kWh": 1000, "Type": "consumption"},
        {'Date': "1992-06-10 07:30:30", "kWh": 2000, "Type": "production"},
        {'Date': "1992-06-10 11:44:44", "kWh": 1000, "Type": "consumption"},
        {'Date': "1992-06-10 07:30:30", "kWh": 2000, "Type": "production"},
        {'Date': "1992-06-10 11:44:44", "kWh": 1000, "Type": "consumption"},
        {'Date': "1992-06-10 07:30:30", "kWh": 2000, "Type": "production"},
        {'Date': "1992-06-10 11:44:44", "kWh": 1000, "Type": "consumption"},
        {'Date': "1992-07-10 07:30:30", "kWh": 2000, "Type": "production"},
        {'Date': "1992-07-10 11:44:44", "kWh": 1000, "Type": "consumption"},
        {'Date': "1992-07-10 07:30:30", "kWh": 2000, "Type": "production"},
        {'Date': "1992-07-10 11:44:44", "kWh": 1000, "Type": "consumption"},
        {'Date': "1992-07-10 07:30:30", "kWh": 2000, "Type": "production"},
        {'Date': "1992-07-10 11:44:44", "kWh": 1000, "Type": "consumption"},
        {'Date': "1992-07-10 07:30:30", "kWh": 2000, "Type": "production"},
        {'Date': "1992-07-10 11:44:44", "kWh": 1000, "Type": "consumption"},
    ]

    oData.add_data_manually(data_list)
