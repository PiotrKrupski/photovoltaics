import pandas as pd
from typing import Union, List
from photo.photovoltaics.source.data_manager import DataMgr
from photo.photovoltaics.source.calculus_manager import CalculusManager

class ReportMgr(DataMgr,CalculusManager):

    @property
    def columns(self):
        return self.data.columns

    def add_new_column(self, cols: Union[str, List[str]]):
        if isinstance(cols, str):
            self.data[cols] = []
        if isinstance(cols, list):
            for col in cols:
                self.data[col] = []

if __name__ == "__main__":
    oReport = ReportMgr()
