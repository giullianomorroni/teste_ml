#!/usr/bin/env python
# -*- coding: utf-8 -*-
# encoding=utf8


from sklearn.externals import joblib
from machine_learning.laboratory_A_and_L import PotatoCropCode
from domain import elements as domain_element


class InFieldDecisionTree:

    def __init__(self):
        self.elements = {}

    def process_analyses(self, json_lab_analyses):
        crop_code = json_lab_analyses["CROPCODE"]
        crop_code = 290

        crop_info = PotatoCropCode.code[crop_code]
        crop = crop_info["crop"]
        phase_code = crop_info["phase_code"]

        variety = crop_info["variety"]
        crop_name = '{0} ({1}) ({2})'.format(crop.upper(), variety.upper(), crop_code)

        sample_type = crop_info["sample_type"]
        sample_type = 'soil'
        if crop is None:
            return

        if sample_type.lower() == 'soil':
            self.elements = domain_element.soil(json_lab_analyses)
        elif sample_type.lower() == 'leaf' or sample_type.lower() == 'petiole' or sample_type.lower() == 'plant':
            self.elements = domain_element.leaf(json_lab_analyses)
        elif sample_type.lower() == 'fruit':
            self.elements = domain_element.fruit(json_lab_analyses)

        models_path = 'machine_learning/laboratory_A_and_L/models/'

        clf = joblib.load('{0}PotatoDecisionTree.pkl'.format(models_path))
        element_le = joblib.load('{0}PotatoDecisionTree_ElementLabelEncode.pkl'.format(models_path))
        crop_le = joblib.load('{0}PotatoDecisionTree_CropNameLabelEncode.pkl'.format(models_path))

        try:
            elements_analyses = []
            products = []
            for element in self.elements.keys():
                quantity = self.elements[element]
                if quantity is None:
                    continue
                element_encoded = element_le.transform([element])
                crop_name_encoded = crop_le.transform([crop_name])
                predict = clf.predict([[element_encoded[0], quantity, crop_name_encoded[0]]])

                values = predict[0].split(';')
                level = values.pop(0)
                comments = values.pop(0)

                for _ in values:
                    product = values.pop(0)
                    if len(product) == 0:
                        continue
                    already_contains = [x for x in products if x['product'] == product]
                    if len(already_contains) > 0:
                        del values[0:3]
                        continue
                    products.append({
                        "product": product,
                        "product_liters_per_hectare": values.pop(0),
                        "water_liters_per_hectare": values.pop(0),
                        "suggestion": values.pop(0)
                    })

                #products = list(set(products))
                elements_analyses.append({
                        "element": element,
                        "level": level,
                        "quantity": self.elements[element],
                        "unit_measure": domain_element.unit_measure(element),
                    }
                )
            return {'phase_code': phase_code, 'elements_analyses': elements_analyses, 'products': products}
        except Exception as e:
            print(e)
            return {'phase_code': 0, 'recommendations': []}

