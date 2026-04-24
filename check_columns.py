import pandas as pd

df = pd.read_excel('excel files/PK233 MANIFEST EXCEL.xlsx')
print('Columns:', df.columns.tolist())
print('\nFirst 15 rows - showing first 3 columns:')
for i in range(15):
    col0 = df.iloc[i, 0]
    col1 = df.iloc[i, 1]
    col2 = df.iloc[i, 2]
    print(f'{i}: [{col0}] | [{col1}] | [{col2}]')
