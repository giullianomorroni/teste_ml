#!/usr/bin/env python
# -*- coding: utf-8 -*-
# encoding=utf8


from sklearn.externals import joblib
from machine_learning.laboratory_A_and_L import PotatoCropCode
from domain import elements as domain_element


class InFieldDecisionTree:

    def __init__(self):
        self.elements = {}

    def process_analyses(self, records):
        recommendations = []
        for data in records:
            json_lab_analyses = data[3]

            #este codigo veio da A&L...futuramente vamos ter q trocar
            crop_code = json_lab_analyses["CROPCODE"]

            crop_info = PotatoCropCode.code[crop_code]
            crop = crop_info["crop"]
            phase_code = crop_info["phase_code"]

            variety = crop_info["variety"]
            crop_name = '{0} ({1}) ({2})'.format(crop.upper(), variety.upper(), crop_code)

            sample_type = crop_info["sample_type"]

            if crop is None:
                return

            if sample_type.lower() == 'soil':
                self.elements = domain_element.soil(json_lab_analyses)
            elif sample_type.lower() == 'leaf' or sample_type.lower() == 'petiole' or sample_type.lower() == 'plant':
                self.elements = domain_element.leaf(json_lab_analyses)
            elif sample_type.lower() == 'fruit':
                self.elements = domain_element.fruit(json_lab_analyses)

            clf = joblib.load('machine_learning/laboratory_A_and_L/models/PotatoDecisionTree.pkl')
            element_le = joblib.load('machine_learning/laboratory_A_and_L/models/PotatoDecisionTree_ElementLabelEncode.pkl')
            crop_le = joblib.load('machine_learning/laboratory_A_and_L/models/PotatoDecisionTree_CropNameLabelEncode.pkl')

            try:
                for element in self.elements.keys():
                    quantity = self.elements[element]
                    element_encoded = element_le.transform([element])
                    crop_name_encoded = crop_le.transform([crop_name])
                    predict = clf.predict([[element_encoded[0], crop_name_encoded[0], quantity]])

                    values = predict[0].split(';')
                    level = values.pop(0)
                    comments = values.pop(0)

                    products = []
                    for _ in values:
                        products.append({
                            "product": values.pop(0),
                            "product_liters_per_hectare": values.pop(0),
                            "water_liters_per_hectare": values.pop(0),
                            "suggestion": values.pop(0)
                        })

                    recommendations.append(
                        {
                            "element": element,
                            "level": level,
                            "quantity": self.elements[element],
                            "unit_measure": domain_element.unit_measure(element),
                            "products": products
                        }
                    )
                recommendation = {'phase_code': phase_code, 'recommendations': recommendations}
                return recommendation
            except Exception as e:
                print(e)
