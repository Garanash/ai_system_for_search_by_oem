import pandas as pd


df = pd.read_excel('./test_cases/test_case.xlsx')

def func_row_generator(filename:str):
    for index, row in df.iterrows():
        result_row = ''
        for column_name, value in row.items():
            result_row += value
        yield result_row
