import os

import pandas as pd
import json
import datetime

from data_manager import DataMgr as DataManager

class CalculusManager(DataManager):
    def __init__(self, data: DataManager = pd.DataFrame()):
        try:
            self.data = data.data
            self.consumption = self.data[self.data["Type"] == "consumption"]
            self.production = self.data[self.data["Type"] == "production"]
        except AttributeError:
            self.data = data
            self.consumption = None
            self.production = None

        self.calculations = {}
        self.measurement_num = 0

    def calculate_overall_consumption(self):
        self.consumption = self.data[self.data["Type"] == "consumption"]

    def calculate_overall_production(self):
        self.production = self.data[self.data["Type"] == "production"]

    def total_production(self):
        return 'Not implemented yet'

    def total_consumption(self):
        return 'Not implemented yet'

    def yearly_consumption(self):
        if self.consumption is None:
            self.calculate_overall_consumption()
        measurement = self.consumption.groupby('year')['kWh'].sum()
        self.calculations[f'measurement_{self.measurement_num}'] = {"yearly_consumption":measurement.to_dict()}
        self.measurement_num+=1
        return measurement


    def monthly_consumption(self, year):
        if self.consumption is None:
            self.calculate_overall_consumption()
        measurement = self.consumption[self.consumption['year'] == year].groupby('month')['kWh'].sum()
        self.calculations[f'measurement_{self.measurement_num}'] = {f"monthly_consumption_{year}": measurement.to_dict()}
        self.measurement_num += 1
        return measurement


    def yearly_production(self):
        if self.production is None:
            self.calculate_overall_production()
        measurement = self.production.groupby('year')['kWh'].sum()
        self.calculations[f'measurement_{self.measurement_num}'] = {"yearly_production": measurement.to_dict()}
        self.measurement_num += 1
        return measurement

    def monthly_production(self, year):
        measurement = self.production[self.production['year'] == year].groupby('month')['kWh'].sum()

        self.calculations[f'measurement_{self.measurement_num}'] = {f'monthly_production_{year}': measurement.to_dict()}
        self.measurement_num += 1
        return measurement

    def cumulative_production_sum(self, year):
        if self.production is None:
            self.calculate_overall_production()

        measurement = self.production[self.production['year'] == year].groupby('month')['kWh'].sum().cumsum()
        self.calculations[f'measurement_{self.measurement_num}'] = {f'cumulative_production_sum_{year}': measurement.to_dict()}
        self.measurement_num += 1
        return measurement

    def cumulative_consumption_sum(self, year):
        if self.consumption is None:
            self.calculate_overall_consumption()

        measurement = self.consumption[self.consumption['year'] == year].groupby('month')['kWh'].sum().cumsum()
        self.calculations[f'measurement_{self.measurement_num}'] = {f'cumulative_consumption_sum_{year}': measurement.to_dict()}
        self.measurement_num += 1

        return measurement

    def get_years(self):
        return self.data.year.unique()

    def production_between_dates(self, date_min, date_max):
        """
        e.g
        date_min = '2023-01-01 00:00:00'
        date_max = '2024-01-01 00:00:00'
        """

        measurement = self.production[self.production['Data'].between(date_min, date_max)].kWh.sum().copy()
        self.calculations[f'measurement_{self.measurement_num}'] = {f"produciton between {date_min}-{date_max}": measurement.to_dict()}
        self.measurement_num += 1
        return measurement


    def consumption_between_dates(self, date_min, date_max):
        """
        e.g
        date_min = '2023-01-01 00:00:00'
        date_max = '2024-01-01 00:00:00'
        """
        measurement = self.consumption[self.consumption['Date'].between(date_min, date_max)].kWh.sum().copy()
        self.calculations[f'measurement_{self.measurement_num}'] = {f"consumption between {date_min}-{date_max}": measurement.to_dict()}
        self.measurement_num += 1
        return measurement

    #TODO: to verify if calculations.json is already created, if yes then continue/append existing one with new results
    #TODO: in case of continuation of calculations.json reindex will be required
    def save_calculations(self):
        now = datetime.datetime.now()
        formatted_date_time = now.strftime('%d_%m_%Y_%H_%M_%S')

        with open(f"{DataManager.DATA_PATH}/calculations.json", "w") as f:
            json.dump(self.calculations, f, indent=4)

    def save_data(self):
        self.data.to_excel(f"{DataManager.DATA_PATH}{os.pathsep}data.xlsx", index=False)

if __name__ == "__main__":
    oCalc = CalculusManager()
    oCalc.load_data(r"D:\GIT\photo\photovoltaics\Data\03_10_2024_22_17_45.pickle")
