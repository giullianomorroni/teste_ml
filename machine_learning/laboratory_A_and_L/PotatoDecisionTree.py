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

    def __init__(self):
        self.df_train = None
        self.X = pd.DataFrame()
        self.y = pd.DataFrame()
        self.element_le = preprocessing.LabelEncoder()
        self.crop_le = preprocessing.LabelEncoder()

    def pre_process(self):
        self.df_train['ELEMENT'] = self.df_train['ELEMENT'].apply(str.strip)
        self.df_train['CROP_NAME'] = self.df_train['CROP_NAME'].apply(str.strip)

        iteractions = 23
        QUANTITIES = [('VERY_LOW', 'VERY_LOW_COMMENTS'),
                      ('LOW', 'LOW_COMMENTS'),
                      ('SLIGHTLY_LOW', 'SLIGHTLY_LOW_COMMENTS'),
                      ('NORMAL', 'NORMAL_COMMENTS'),
                      ('HIGH', 'HIGH_COMMENTS'),
                      ('VERY_HIGH', 'VERY_HIGH_COMMENTS')]

        target = []
        features = []
        for index, row in self.df_train.iterrows():
            for quantity in QUANTITIES:
                value = row[quantity[0]]
                value = float(value.replace(',', '.'))
                if np.isnan(value):
                    continue
                for _ in range(0, iteractions):
                    new_row = pd.Series(row)
                    value = float(value - 0.005)
                    new_row['QUANTITY'] = value
                    new_row['ORIGINAL_QUANTITY'] = row[quantity[0]]
                    new_row['QUANTITY_TYPE'] = quantity[0]
                    features.append(new_row)
                    target.append(new_row[quantity[1]])

        self.X = pd.DataFrame(data=features)
        self.y = pd.DataFrame(data=target, columns=['COMMENTS'])

    def train_encode_labels(self):
        self.element_le.fit(self.df_train['ELEMENT'])
        self.X['ELEMENT_ENCODED'] = self.element_le.transform(self.X['ELEMENT'])

        self.crop_le.fit(self.df_train['CROP_NAME'])
        self.X['CROP_NAME_ENCODED'] = self.crop_le.transform(self.X['CROP_NAME'])

    def build_model(self):
        file_name = 'data/PotatoDecisionTree_Complete.csv'
        self.df_train = pd.read_csv(file_name, sep=';')

        self.pre_process()
        self.train_encode_labels()

        X_train, X_test, y_train, y_test = train_test_split(self.X, self.y, test_size=0.25, random_state=42)

        print('df_train', len(self.df_train))
        print('X_train', len(X_train))
        print('X_test', len(X_test))
        print('Data splited, train size has {0} and test size has {1}'.format(len(X_train), len(X_test)))

        COLUMNS_NAMES = ['QUANTITY', 'ELEMENT_ENCODED', 'CROP_NAME_ENCODED']

        clf = DecisionTreeClassifier(criterion='gini', max_depth=None, max_features=3, random_state=42)
        clf.fit(X_train[COLUMNS_NAMES], y_train)
        score = clf.score(X_train[COLUMNS_NAMES], y_train)
        print('SEU SCORE PARA BASE DE TREINO FOI DE {0:.4f}'.format(float(score)))
        score = clf.score(X_test[COLUMNS_NAMES], y_test)
        print('SEU SCORE PARA BASE DE TESTE FOI DE {0:.4f}'.format(float(score)))

        print('PERSISTINDO MODELO TREINADO, PARA FUTURO REUSO')
        joblib.dump(clf, 'models/PotatoDecisionTree.pkl')
        joblib.dump(self.element_le, 'models/PotatoDecisionTree_ElementLabelEncode.pkl')
        joblib.dump(self.crop_le, 'models/PotatoDecisionTree_CropNameLabelEncode.pkl')


#model = PotatoDecisionTree()
#model.build_model()
