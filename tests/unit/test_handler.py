import pandas as pd

from src.alumnifinder.excel.handler import Handler


class TestHandler:
    def test_xlsx_has_headers(self, xlsx_file):
        headers = Handler(xlsx_file).check_headers()
        assert type(headers) is list
        assert len(headers) > 0

    def test_split_data(self, xls_file):
        h = Handler(xls_file)
        num = h.find_divisor()
        assert num > 0
        sections = h.split_data(num)
        assert type(sections) is list
        for data_frame in sections:
            assert type(data_frame) is not None
            assert type(data_frame) is pd.DataFrame

    def test_iter(self, xls_file):
        h = Handler(xls_file)
        for index, row in h.data.iterrows():
            if index == 0:
                pass
