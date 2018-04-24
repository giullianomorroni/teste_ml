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

    interactions = 27
    file_name = 'machine_learning/laboratory_A_and_L/data/PotatoDecisionTree_Complete.xlsx'

    column_names = ['ELEMENT_ENCODED', 'CROP_NAME_ENCODED', 'QUANTITY']

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
            for quantity in self.QUANTITIES:
                try:
                    value = row[quantity[0]]
                    if np.isnan(value):
                        continue

                    if quantity[0] == 'HIGH':
                        max_value = value + 10
                    else:
                        max_value = row[self.NEXT_QUANTITIES[quantity[0]]]

                    for _ in range(0, self.interactions):
                        copy_row = pd.Series(row).copy();
                        copy_row['QUANTITY'] = value
                        copy_row['ORIGINAL_QUANTITY'] = copy_row[quantity[0]]
                        copy_row['QUANTITY_TYPE'] = quantity[0]

                        target_value = quantity[2] + ';' + copy_row[quantity[1]]

                        target.append(target_value)
                        features.append(copy_row)

                        value = float(value + 0.005)
                        if value >= max_value:
                            break
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

        writer = pd.ExcelWriter('aqui.xlsx', engine='xlsxwriter')
        self.X.to_excel(writer, sheet_name='Sheet1')
        writer.save()


    def build_model(self):
        print('start building model')
        self.df_train = pd.read_excel(self.file_name)

        self.pre_process()
        self.train_encode_labels()

        X_train, X_test, y_train, y_test = train_test_split(self.X, self.y, test_size=0.25, random_state=42)

        print('df_train', len(self.df_train))
        print('X_train', len(X_train))
        print('X_test', len(X_test))
        print('Data split, train size has {0} and test size has {1}'.format(len(X_train), len(X_test)))

        clf = DecisionTreeClassifier(criterion='gini', max_depth=None, max_features=3, random_state=42)
        clf.fit(X_train[self.column_names], y_train)

        '''
        for index, row in X_test.iterrows():
            predict = clf.predict([row[self.column_names]])
            print(predict)
            print(row[['ELEMENT', 'QUANTITY_TYPE', 'QUANTITY']])
            print('\n')
        '''

        score = clf.score(X_train[self.column_names], y_train)
        print('SEU SCORE PARA BASE DE TREINO FOI DE {0:.4f}'.format(float(score)))

        score = clf.score(X_test[self.column_names], y_test)
        print('SEU SCORE PARA BASE DE TESTE FOI DE {0:.4f}'.format(float(score)))

        print('PERSISTINDO MODELO TREINADO, PARA FUTURO REUSO')
        joblib.dump(clf, 'machine_learning/laboratory_A_and_L/models/PotatoDecisionTree.pkl')
        joblib.dump(self.element_le, 'machine_learning/laboratory_A_and_L/models/PotatoDecisionTree_ElementLabelEncode.pkl')
        joblib.dump(self.crop_le, 'machine_learning/laboratory_A_and_L/models/PotatoDecisionTree_CropNameLabelEncode.pkl')
        print('model built')
