
import pandas as pd
from domain.decision_tree import InFieldDecisionTree
import json

files = [
    'base_test_potato_norland.xlsx',
    'base_test_potato_onaway.xlsx',
    'base_test_potato_shepody.xlsx'
]

for file in files:
    excel = pd.read_excel('../machine_learning/laboratory_A_and_L/data/test_files/{0}'.format(file))
    print('reading file {0}'.format(file))

    recommendations = []
    recommendations_per_element = []

    for idx in range(0, len(excel)):
        records = json.loads(excel.loc[idx].to_json(orient='columns'))
        analyses = InFieldDecisionTree().process_analyses(records)

        for idx2, value in enumerate(analyses['recommendations']):
            analyses['recommendations'][idx2]['crop_name'] = records['CROPNAME']
            analyses['recommendations'][idx2]['crop_code'] = records['CROPCODE']

        aux = [x for x in analyses['recommendations']]
        recommendations.extend(aux)
        recommendations_per_element.extend([list(x.values()) for x in recommendations])

    # Create a Pandas dataframe from some data.
    df = pd.DataFrame(data=recommendations_per_element, columns=recommendations[0].keys())

    # Create a Pandas Excel writer using XlsxWriter as the engine.
    writer = pd.ExcelWriter('final_result_{0}.xlsx'.format(file.split('.')[0]), engine='xlsxwriter')

    # Convert the dataframe to an XlsxWriter Excel object.
    df.to_excel(writer, sheet_name='Sheet1')

    # Close the Pandas Excel writer and output the Excel file.
    writer.save()
