import sys, pytest

import pandas as pd

# sys.path('D:\GIT\photo\photovoltaics\source')

from photo.photovoltaics.source import data_manager

@pytest.fixture(scope="module")
def new_dm_instance():
    oData = data_manager.DataMgr()
    return oData

@pytest.fixture(scope="module")
def test_data(new_dm_instance):

    """
    "%Y-%m-%d %H:%M:%S"
    """
    data_list = [
        {'Date': "1992-06-10 07:30:30", "kWh": 1000, "Type": "production"},
        {'Date': "1993-10-03 11:44:44", "kWh": 1200, "Type": "consumption"}

    ]

    return new_dm_instance.add_data_manually(data_list)


def test_new_instance_wrong_filepath_ext():
    match_regex = "wrong data type of filepath"
    with pytest.raises(TypeError, match=match_regex):
        data_manager.DataMgr(filepath=1234)

def test_new_instance(new_dm_instance):
    # result = data_manager.DataMgr()
    # print(type(result.data))
    assert isinstance(new_dm_instance.data, pd.DataFrame)

def test_new_instance_columns(new_dm_instance):
    # result = data_manager.DataMgr()
    assert new_dm_instance.data.columns.to_list() == ['Date', 'kWh', 'Type', 'month', 'year']
    # ['Date', 'kWh', 'Type', 'month', 'year']

def test_new_instance_filepath(new_dm_instance):
    # result = data_manager.DataMgr()
    assert isinstance(new_dm_instance.filepath, str)

def test_empty_data_frame(new_dm_instance):
    assert len(new_dm_instance.data) == 0

def test_not_empty_data_frame(test_data):
    # print(dir(test_data))
    assert len(test_data) != 0




#
#



# def test_sys_path():
#     print("sys.path: ")
#     print("sys.path: ")
#     for p in sys.path:
#         print(p)
#     # result = run(["python", "../data_manager.py"])
#     # assert isinstance(oReport, 'photo.photovoltaics.Code.DataManager.DataManager')
#
# # def test_empty_instance():
# #     print(DataManager.create_an_empty_instance())