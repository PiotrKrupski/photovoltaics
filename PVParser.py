


class ReportManager:
    pass

if __name__ == "__main__":


    oReport = DataManager()

    # Example usage
    data_list = [
        {'Date': "1992-06-10 07:30:30", "kWh": 1000, "Type": "production"},
        {'Date': "1993-10-03 11:44:44", "kWh": 1200, "Type": "consumption"}

    ]
    oReport.add_data_manually(data_list)

    # collected_data = oReport.import_data()
    # oReport.load_xlsx_data(collected_data)
    # # oReport.save_dataframe_as_pickle()
    # oReport.column_value_modification('Data', 'Date')
    # oReport.row_clean('Date', '24:00', '00:00')
    #
    # # oReport.convert_to_datetime()
    #
    # oReport.column_value_modification(' Wartość kWh', 'kWh')
    # oReport.column_value_modification('Rodzaj', 'Type')
    # oReport.row_clean('Type', 'oddanie', 'production')
    # oReport.row_clean('Type', 'pobór', 'consumption')
    # oReport.load_most_recent_data()
    # oReport.convert_to_datetime()
    # # oReport.save_dataframe_as_pickle()
    # oReport.save_dataframe_as_pickle()


    oCalculus = CalculusManager(oReport)
