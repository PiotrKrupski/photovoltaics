import pytest, time

from .photovoltaics.source import data_manager

@pytest.fixture(scope="module")
def new_cm_instance():
    oCalculus = data_manager.DataMgr()
    return oCalculus

# @pytest.fixture(scope="function")
# def ok_test_data(new_dm_instance):
#     """
#     Provides simple dataset"
#     """
#     data_list = [
#         {'Date': "1992-06-10 07:30:30", "kWh": 1000, "Type": "production"},
#         {'Date': "1993-10-03 11:44:44", "kWh": 1200, "Type": "consumption"}
#
#     ]
#
#     return new_dm_instance.add_data_manually(data_list)

# def nok_test_data(new_dm_instance):
#
#     data_list = [
#         {'Date': "1992-06-10 07:30:30", "kWh": 1000, "Type": "production"},
#         {'Date': "1993:10:03-11:44:44", "kWh": 1200, "Type": "consumption"}]
#
#     return new_dm_instance.add_data_manually(data_list)

# @pytest.fixture(autouse=True, scope="session")
# def footer_session_scope():
#     """Report the time at the end of a session."""
#     yield
#     now = time.time()
#     print("--")
#     print(
#     "finished : {}".format(
#     time.strftime("%d %b %X", time.localtime(now))
#     )
#     )
#     print("-----------------")
