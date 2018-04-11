#!/usr/bin/env python
# -*- coding: utf-8 -*-
# encoding=utf8
import json

from bottle import route, run
import os
from sklearn.externals import joblib
import psycopg2
from machine_learning.laboratory_A_and_L import PotatoDecisionTree, PotatoPlantingDate
import threading


def builder(message):
    model = PotatoDecisionTree()
    model.build_model()


def do_analyses():
    idt = InFieldDecisionTree()
    idt.process_analyses()


@route('/build_models', method='POST')
def build_model():
    t = threading.Thread(target=builder)
    t.start()
    return "Models are building, it WILL take some time to be done!!!"


@route('/recommendation', method='POST')
def recommendation():
    t = threading.Thread(target=do_analyses)
    t.start()
    return "ok, all Analyses will be processed."


class InFieldDecisionTree:

    def __init__(self):
        #TODO PASSAR ESSAS VARIAVEIS PRO SERVICO DA AZURE
        os.environ['DATABASE_HOST'] = 'infield-dev.postgres.database.azure.com'
        os.environ['DATABASE_NAME'] = 'infield_dev'
        os.environ['DATABASE_USER'] = 'infield_dev@infield-dev.postgres.database.azure.com'
        os.environ['DATABASE_PASSWORD'] = 'tHkNgTss6BAysE5r'

        self.conn_string = "host='{0}' dbname='{1}' user='{2}' password='{3}'".format(
            os.environ['DATABASE_HOST'],
            os.environ['DATABASE_NAME'],
            os.environ['DATABASE_USER'],
            os.environ['DATABASE_PASSWORD']
        )
        self.connection = None
        self.elements = {}

    def database_connect(self):
        try:
            print("Connecting to database\n {0}".format(self.conn_string))
            # get a connection, if a connect cannot be made an exception will be raised here
            self.connection = psycopg2.connect(self.conn_string)
        except Exception as e:
            print("Couldn't connect to database")
            print(e)

    def retrieve_data(self):
        self.database_connect()
        try:
            cursor = self.connection.cursor()
            cursor.execute(
                'select '
                '   field_analyses.id_field_analyses,'
                '   field_analyses.id_field,'
                '   field_analyses.id_laboratory,'
                '   field_analyses.lab_analyses, '
                '   varieties.name,'
                '   crops.name, '
                '   fields.planting_date '
                'from field_analyses as field_analyses ' 
                '   inner join fields as fields on fields.id_field = field_analyses.id_field '
                '   inner join crops as crops on crops.id_crop = fields.id_crop '\
                '   inner join varieties as varieties on varieties.id_crop = fields.id_crop '
                'where 1=1 '
                '   and field_analyses.processed = false and field_analyses.id_field_analyses = 248')
            records = cursor.fetchall()
            return records
        except Exception as e:
            print("Couldn't fetch data")
            print(e)

    def process_analyses(self):
        records = self.retrieve_data()
        for data in records:
            id_field_analyses = data[0]
            id_field = data[1]
            id_laboratory = data[2]
            json_lab_analyses = data[3]
            variety = data[4]
            crop = data[5]
            planting_date = data[6]

            sample_type = json_lab_analyses["SAMPLETYPE"]
            crop_name = PotatoPlantingDate.season_by_planting_date(planting_date, crop, variety)

            if sample_type.lower() == 'soil':
                self.soil(json_lab_analyses)
            elif sample_type.lower() == 'leaf':
                self.soil(json_lab_analyses)
            elif sample_type.lower() == 'fruit':
                self.fruit(json_lab_analyses)

            clf = joblib.load('machine_learning/laboratory_A_and_L/models/PotatoDecisionTree.pkl')
            element_le = joblib.load('machine_learning/laboratory_A_and_L/models/PotatoDecisionTree_ElementLabelEncode.pkl')
            crop_le = joblib.load('machine_learning/laboratory_A_and_L/models/PotatoDecisionTree_CropNameLabelEncode.pkl')

            try:
                for element in self.elements.keys():
                    quantity = self.elements[element]
                    element_encoded = element_le.transform([element])
                    crop_name_encoded = crop_le.transform([crop_name])
                    predict = clf.predict([[ quantity, element_encoded[0], crop_name_encoded[0] ]])
                    print(predict)
            except Exception as e:
                print(e)

    def soil(self, data):
        self.elements = {"K": data["S_K"], "MG": data["S_MG"], "CA": data["S_CA"], "NA": data["S_NA"],
                         "S": data["S_S"], "ZN": data["S_ZN"], "MN": data["S_MN"], "FE": data["S_FE"],
                         "CU": data["S_CU"], "B": data["S_B"], "AL": data["S_AL"], "NO3N": data["S_NO3N"]}

    def leaf(self, data):
        #TODO VALIDATE THIS ELEMENTS
        self.elements = {"N": data["L_N"], "NO3N": data["L_NO3N"], "S": data["L_S"], "P": data["L_P"],
                  "K": data["L_K"], "MG": data["L_MG"], "CA": data["L_CA"], "NA": data["L_NA"],
                  "B": data["L_B"], "ZN": data["L_ZN"], "MN": data["L_MN"], "FE": data["L_FE"],
                  "CU": data["L_CU"], "AL": data["L_AL"], "MO": data["L_MO"], "CL": data["L_CL"]}

    def fruit(self, data):
        # TODO VALIDATE THIS ELEMENTS
        self.elements = {"N": data["F_N"], "NO3N": data["F_NO3N"], "S": data["F_S"], "P": data["F_P"],
                  "K": data["F_K"], "MG": data["F_MG"], "CA": data["F_CA"], "NA": data["F_NA"],
                  "B": data["F_B"], "ZN": data["F_ZN"], "MN": data["F_MN"], "FE": data["F_FE"],
                  "CU": data["F_CU"], "AL": data["F_AL"]}


run(host='0.0.0.0', port=8080, debug=True)
