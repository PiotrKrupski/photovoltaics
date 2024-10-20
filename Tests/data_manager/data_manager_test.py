import pytest
import pandas as pd
from .photovoltaics.source import data_manager


def test_new_instance_wrong_filepath_ext():
    match_regex = "wrong data type of filepath"
    with pytest.raises(TypeError, match=match_regex):
        data_manager.DataMgr(filepath=1234)

def test_unspecified_arguments_for_DataMgr_init():
    data_manager.DataMgr('abc', abc=1)

def test_new_instance(new_dm_instance):
    assert isinstance(new_dm_instance.data, pd.DataFrame)

def test_new_instance_columns(new_dm_instance):
    assert new_dm_instance.data.columns.to_list() == ['Date', 'kWh', 'Type', 'month', 'year']

def test_new_instance_filepath(new_dm_instance):
    assert isinstance(new_dm_instance.filepath, str)

def test_empty_data_frame(new_dm_instance):
    assert len(new_dm_instance.data) == 0

def test_negative_validate_date_format(new_dm_instance):
    match_regex = "Wrong format of data"
    with pytest.raises(TypeError, match=match_regex):
        data_list = [
            {'Date': "1992-06-10 07:30:30", "kWh": 1000, "Type": "production"},
            {'Date': "1993:10:03-11:44:44", "kWh": 1200, "Type": "consumption"}]
        new_dm_instance.add_data_manually(data_list)


def test_not_empty_data_frame(ok_test_data):
    assert len(ok_test_data) != 0

def test_tmp_path(tmp_path):
    """function scope by default"""
    file = tmp_path / "file.txt"
    print(file)
    file.write_text("Hello")
    assert file.read_text() == "Hello"

def test_tmp_path_factory(tmp_path_factory):
    """session scope by default"""
    path = tmp_path_factory.mktemp("sub")
    print(path)
    file = path / "file.txt"
    file.write_text("Hello")
    assert file.read_text() == "Hello"

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