#!/usr/bin/env python
# -*- coding: utf-8 -*-
# encoding=utf8


from machine_learning import DecisionTreeVersion
from database.repository import DatabaseRepository
from domain.decision_tree import InFieldDecisionTree


class InFieldDecisionTreeService:

    def __init__(self):
        self.repository = DatabaseRepository()

    def classify(self, id_field_analyses):
        self.repository.database_connect()
        records = self.repository.retrieve_data(id_field_analyses)

        recommendation = InFieldDecisionTree().process_analyses(records)

        _version = DecisionTreeVersion.CURRENT_VERSION['laboratory_A_and_L']
        model_version = _version['potato']['version']
        model_name = _version['potato']['name']

        self.repository.save_recommendation(id_field_analyses, recommendation, model_version, model_name)
        self.repository.database_disconnect()
