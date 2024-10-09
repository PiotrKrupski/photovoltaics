from data_manager import DataMgr as DataManager

class CalculusManager:
    def __init__(self, data: DataManager):
        self.data = data.data
        self.consumption  = self.data[self.data["Type"] == "consumption"]
        self.production = self.data[self.data["Type"] == "production"]

    def calculate_overall_consumption(self):
        self.consumption = self.data[self.data["Type"] == "consumption"]

    def calculate_overall_production(self):
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
