import pandas as pd
import openpyxl
import os

PV_DATA = "D:\DOWNLOADED\Fotowoltaika"


class DataManager():
    def __init__(self, filepath: str):
        self.filepath = filepath

    #TODO: data validation
    def import_data(self) -> list:
        return os.listdir(self.filepath)


    def load_data(self, extention: str = "xlsx"):
        pv_dfs = list()
        for file in excel_files:
            filepath = os.path.join(self.filepath, file)
            if "xlsx" not in filepath:
                continue
            df = pd.read_excel(filepath, engine="openpyxl")
            pv_dfs.append(df)

        pv_data = pd.concat(pv_dfs)
        pv_data = pv_data.rename(columns={' Wartość kWh': 'kWh'})


if __name__ == "__main__":





excel_files =


def replace_24_to_00(df):
    df['Data'] = df['Data'].str.replace('24:00', '00:00')
    return df

pv_data = replace_24_to_00(pv_data.copy())
pv_data['Data'] = pd.to_datetime(pv_data['Data'])
pv_data['month'] = pv_data['Data'].dt.month
pv_data['year'] = pv_data['Data'].dt.year
print(pv_data)


pobor_df = pv_data[pv_data["Rodzaj"] == "pobór"]
pobor_df_yearly_sum = pobor_df.groupby('year')['kWh'].sum()
pobor_df_yearly_sum


pobor_df_2022 = pobor_df[pobor_df['year'] == 2023]
pobor_df_2022_monthly_sum = pobor_df_2022.groupby('month')['kWh'].sum()
pobor_df_2022_monthly_sum


pobor_df_2023 = pobor_df[pobor_df['year'] == 2023]
pobor_df_2023_monthly_sum = pobor_df_2023.groupby('month')['kWh'].sum()
pobor_df_2023_monthly_sum

oddanie_df = pv_data[pv_data["Rodzaj"] == "oddanie"]
oddanie_df_yearly_sum = oddanie_df.groupby('year')['kWh'].sum()
oddanie_df_yearly_sum

oddanie_df_2022 = oddanie_df[oddanie_df['year'] == 2022]
oddanie_df_2022_monthly_sum = oddanie_df_2022.groupby('month')['kWh'].sum()
oddanie_df_2022_monthly_sum



# Create a new DataFrame
oddanie_df_2022_cumulative = pd.DataFrame(oddanie_df_2022_monthly_sum)

# Add a new column with cumulative results
oddanie_df_2022_cumulative['cumulative'] = oddanie_df_2022_cumulative['kWh'].cumsum()
oddanie_df_2022_cumulative


oddanie_df_2023 = oddanie_df[oddanie_df['year'] == 2023]
oddanie_df_2023_monthly_sum = oddanie_df_2023.groupby('month')['kWh'].sum()
oddanie_df_2023_monthly_sum


# Create a new DataFrame
oddanie_df_2023_cumulative = pd.DataFrame(oddanie_df_2023_monthly_sum )

# Add a new column with cumulative results
oddanie_df_2023_cumulative['cumulative'] = oddanie_df_2023_cumulative['kWh'].cumsum()
oddanie_df_2023_cumulative



# Create a new DataFrame
pobor_df_2022_cumulative = pd.DataFrame(pobor_df_2022_monthly_sum)

# Add a new column with cumulative results
pobor_df_2022_cumulative['cumulative'] = pobor_df_2022_cumulative['kWh'].cumsum()
pobor_df_2022_cumulative


# Create a new DataFrame
pobor_df_2023_cumulative = pd.DataFrame(pobor_df_2023_monthly_sum)

# Add a new column with cumulative results
pobor_df_2023_cumulative['cumulative'] = pobor_df_2023_cumulative['kWh'].cumsum()
pobor_df_2023_cumulative


oddanie_df["kWh"].sum()


pobor_df["kWh"].sum()


oddanie_df["Data"].min()


oddanie_df["Data"].max()


date_min = '2023-01-01 00:00:00'
date_max = '2024-01-01 00:00:00'
filtered = oddanie_df[oddanie_df['Data'].between(date_min, date_max)]
filtered['kWh'].sum()


date_min = '2023-01-28 00:00:00'
date_max = '2024-01-28 00:00:00'
filtered = pobor_df[pobor_df['Data'].between(date_min, date_max)]
filtered['kWh'].sum()


date_min = '2022-09-01 00:00:00'
date_max = '2022-09-30 00:00:00'
filtered = oddanie_df[oddanie_df['Data'].between(date_min, date_max)]
filtered['kWh'].sum()