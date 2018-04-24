
import pandas as pd
from machine_learning.laboratory_A_and_L import PotatoCropCode
from sklearn.externals import joblib
from domain import elements as domain_element
from datetime import datetime

sample_type = crop_info["sample_type"]

excel = pd.read_excel('../machine_learning/laboratory_A_and_L/data/base_teste_18_000_rows.xlsx')

# Create a Pandas dataframe from some data.
df = pd.DataFrame(data=values, columns=keys)

# Create a Pandas Excel writer using XlsxWriter as the engine.
writer = pd.ExcelWriter('final_result.xlsx', engine='xlsxwriter')

# Convert the dataframe to an XlsxWriter Excel object.
df.to_excel(writer, sheet_name='Sheet1')

# Close the Pandas Excel writer and output the Excel file.
writer.save()
