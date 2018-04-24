
import pandas as pd
from machine_learning.laboratory_A_and_L import PotatoCropCode
from sklearn.externals import joblib
from domain import elements as domain_element
from datetime import datetime

excel = pd.read_excel('../machine_learning/laboratory_A_and_L/data/base_teste_18_000_rows.xlsx')

elements = ['N', 'NO3N', 'S', 'P', 'K', 'Mg', 'Ca', 'Na', 'B', 'Zn', 'Mn', 'Fe', 'Cu']

clf = joblib.load('../machine_learning/laboratory_A_and_L/models/PotatoDecisionTree.pkl')
element_le = joblib.load('../machine_learning/laboratory_A_and_L/models/PotatoDecisionTree_ElementLabelEncode.pkl')
crop_le = joblib.load('../machine_learning/laboratory_A_and_L/models/PotatoDecisionTree_CropNameLabelEncode.pkl')

errors = []
final_result = []

start = datetime.now()

for index in excel.index:
    crop_code = excel['CROPCODE'][index]
    crop_info = PotatoCropCode.code[crop_code]
    crop = crop_info["crop"]
    variety = crop_info["variety"]
    crop_name = '{0} ({1}) ({2})'.format(crop.upper(), variety.upper(), crop_code)
    sample_type = crop_info["sample_type"]

    for element in elements:
        try:
            quantity = excel[element][index]
            element_encoded = element_le.transform([element])
            crop_name_encoded = crop_le.transform([crop_name])
            predict = clf.predict([[element_encoded[0], crop_name_encoded[0], quantity]])

            values = predict[0].split(';')

            level = values.pop(0)
            comments = values.pop(0)

            products = []
            for v in values:
                products.append({
                    "product": values.pop(0),
                    "product_liters_per_hectare": values.pop(0),
                    "water_liters_per_hectare": values.pop(0),
                    "suggestion": values.pop(0)
                })

            final_result.append(
                {
                    "crop": crop_name,
                    "sample_type": sample_type,
                    "element": element,
                    "level": level,
                    "quantity": quantity,
                    "unit_measure": domain_element.unit_measure(element),
                    "comments": comments,
                    "products": products
                })
        except Exception as e:
            errors.append(e)

values = []
for result in final_result:
    values.append(list(result.values()))

keys = final_result[0].keys()

# Create a Pandas dataframe from some data.
df = pd.DataFrame(data=values, columns=keys)

# Create a Pandas Excel writer using XlsxWriter as the engine.
writer = pd.ExcelWriter('final_result.xlsx', engine='xlsxwriter')

# Convert the dataframe to an XlsxWriter Excel object.
df.to_excel(writer, sheet_name='Sheet1')

# Close the Pandas Excel writer and output the Excel file.
writer.save()


for error in list(set(errors)):
    print(error)

print('started at {0} and finished at {1}'.format(start, datetime.now()))
