#!/usr/bin/env python
# -*- coding: utf-8 -*-
# encoding=utf8


from sklearn.externals import joblib
from machine_learning.laboratory_A_and_L import PotatoPlantingDate
from machine_learning import DecisionTreeVersion
from database.repository import DatabaseRepository
from domain import elements as domain_element


class InFieldDecisionTree:

    def __init__(self):
        self.repository = DatabaseRepository()
        self.elements = {}

    def process_analyses(self, id_field_analyses):
        self.repository.database_connect()
        records = self.repository.retrieve_data(id_field_analyses)

        recommendations = []
        for data in records:
            id_field_analyses = data[0]
            #id_field = data[1]
            #id_laboratory = data[2]
            json_lab_analyses = data[3]
            variety = data[4]
            crop = data[5]
            planting_date = data[6]

            sample_type = json_lab_analyses["SAMPLETYPE"]
            crop_name = PotatoPlantingDate.season_by_planting_date(planting_date, crop, variety)

            if crop_name is None:
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

            CURRENT_VERSION = DecisionTreeVersion.CURRENT_VERSION['laboratory_A_and_L']
            model_version = CURRENT_VERSION['potato']['version']
            model_name = CURRENT_VERSION['potato']['name']
            try:
                for element in self.elements.keys():
                    quantity = self.elements[element]
                    element_encoded = element_le.transform([element])
                    crop_name_encoded = crop_le.transform([crop_name])
                    predict = clf.predict([[element_encoded[0], crop_name_encoded[0], quantity]])

                    values = predict[0].split('#')

                    level = values[0]
                    #comments = values[1]
                    product = values[2]
                    product_liters_per_hectare = values[3]
                    water_liters_per_hectare = values[4]
                    suggestion = values[5]

                    recommendations.append(
                        {
                            "element": element,
                            "level": level,
                            "quantity": self.elements[element],
                            "unit_measure": domain_element.unit_measure(element),
                            "product": product,
                            "product_liters_per_hectare": product_liters_per_hectare,
                            "water_liters_per_hectare": water_liters_per_hectare,
                            "suggestion": suggestion
                        }
                    )
                self.repository.save_recommendation(id_field_analyses, recommendations, model_version, model_name)
            except Exception as e:
                print(e)
        self.repository.database_disconnect()
