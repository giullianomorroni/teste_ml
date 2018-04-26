#!/usr/bin/env python
# -*- coding: utf-8 -*-
# encoding=utf8

import pandas as pd
import numpy as np
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.externals import joblib


class PotatoDecisionTree:

    interactions = 500
    file_name = 'machine_learning/laboratory_A_and_L/data/PotatoDecisionTree_Complete.xlsx'

    column_names = ['ELEMENT_ENCODED', 'QUANTITY', 'CROP_NAME_ENCODED']

    QUANTITIES = [
        ('VERY_LOW', 'VERY_LOW_COMMENTS', 'VL'),
        ('LOW', 'LOW_COMMENTS', 'L'),
        ('SLIGHTLY_LOW', 'SLIGHTLY_LOW_COMMENTS', 'SL'),
        ('NORMAL', 'NORMAL_COMMENTS', 'N'),
        ('HIGH', 'HIGH_COMMENTS', 'H')
    ]

    NEXT_QUANTITIES = {
        'VERY_LOW': 'LOW',
        'LOW': 'SLIGHTLY_LOW',
        'SLIGHTLY_LOW': 'NORMAL',
        'NORMAL': 'HIGH',
        'HIGH': ''
    }

    def __init__(self):
        self.df_train = None
        self.X = pd.DataFrame()
        self.y = pd.DataFrame()
        self.element_le = preprocessing.LabelEncoder()
        self.crop_le = preprocessing.LabelEncoder()

    def pre_process(self):
        target = []
        features = []

        for index, row in self.df_train.iterrows():
            print(row[['CROP_NAME', 'ELEMENT']])
            for quantity in self.QUANTITIES:
                try:
                    value = row[quantity[0]]
                    if np.isnan(value):
                        continue

                    if quantity[0] == 'HIGH':
                        max_value = value + 1
                    else:
                        max_value = row[self.NEXT_QUANTITIES[quantity[0]]]
                        if np.isnan(max_value):
                            max_value = value + 1

                    for i in range(0, 2):
                        copy_row = pd.Series(row).copy()
                        copy_row['QUANTITY'] = value
                        copy_row['ORIGINAL_QUANTITY'] = copy_row[quantity[0]]
                        copy_row['QUANTITY_TYPE'] = quantity[0]

                        target_value = quantity[2] + ';' + copy_row[quantity[1]]

                        target.append(target_value)
                        features.append(copy_row)

                        value = max_value - 0.01
                except Exception as e:
                    print(row)
                    print(e)

        self.X = pd.DataFrame(data=features)
        self.y = pd.DataFrame(data=target, columns=['COMMENTS'])

    def train_encode_labels(self):
        self.element_le.fit(self.df_train['ELEMENT'])
        self.X['ELEMENT_ENCODED'] = self.element_le.transform(self.X['ELEMENT'])

        self.crop_le.fit(self.df_train['CROP_NAME'])
        self.X['CROP_NAME_ENCODED'] = self.crop_le.transform(self.X['CROP_NAME'])

    def build_model(self):
        print('start building model')
        self.df_train = pd.read_excel(self.file_name)

        self.pre_process()
        self.train_encode_labels()

        clf = DecisionTreeClassifier(criterion='gini', max_depth=None, max_features=1, random_state=42)
        clf.fit(self.X[self.column_names], self.y)

        score = clf.score(self.X[self.column_names], self.y)
        print('SEU SCORE PARA BASE DE TREINO FOI DE {0:.4f}'.format(float(score)))

        print('PERSISTINDO MODELO TREINADO, PARA FUTURO REUSO')
        joblib.dump(clf, 'machine_learning/laboratory_A_and_L/models/PotatoDecisionTree.pkl')
        joblib.dump(self.element_le, 'machine_learning/laboratory_A_and_L/models/PotatoDecisionTree_ElementLabelEncode.pkl')
        joblib.dump(self.crop_le, 'machine_learning/laboratory_A_and_L/models/PotatoDecisionTree_CropNameLabelEncode.pkl')
        print('model built')
