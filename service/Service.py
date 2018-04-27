#!/usr/bin/env python
# -*- coding: utf-8 -*-
# encoding=utf8


from machine_learning import DecisionTreeVersion
from database.repository import DatabaseRepository
from domain.decision_tree import InFieldDecisionTree
import requests
import os


class InFieldDecisionTreeService:

    def __init__(self):
        self.repository = DatabaseRepository()

    def classify(self, id_field_analyses):
        _version = DecisionTreeVersion.CURRENT_VERSION['laboratory_A_and_L']
        model_version = _version['potato']['version']
        model_name = _version['potato']['name']

        self.repository.database_connect()
        records = self.repository.retrieve_data(id_field_analyses)

        for record in records:
            recommendation = InFieldDecisionTree().process_analyses(record[0])
            self.repository.save_recommendation(id_field_analyses, recommendation, model_version, model_name)

        self.repository.database_disconnect()
        stakeholders_emails = self.get_recommendation_stakeholders(id_field_analyses)
        self.send_email(stakeholders_emails)

    @staticmethod
    def send_email(emails):
        if os.environ.get('IFA_ENVIRONMENT') == 'develop':
            return

        if emails is None:
            return

        key = 'ZL8C7rao8bsFZ1SF3wKMAzhn4R91tUaY9KMiHETKcaDWXruQWLWX/A=='
        route = 'recommendationReady'
        url = 'https://infield-dev.azurewebsites.net/api/mailer/{0}?code={1}'.format(route, key)
        r = requests.post(url=url, json={'emails': emails})
        print('recommendation email sent...http code', r.status_code)

    @staticmethod
    def get_recommendation_stakeholders(id_field_analyses):
        if os.environ.get('IFA_ENVIRONMENT') == 'develop':
            return

        key = 'ZL8C7rao8bsFZ1SF3wKMAzhn4R91tUaY9KMiHETKcaDWXruQWLWX/A=='
        route = 'listRecommendationStakeHolders'
        url = 'https://infield-dev.azurewebsites.net/api/mailer/{0}?code={1}'.format(route, key)
        r = requests.post(url=url, json={'id_field_analyses': id_field_analyses})
        if r.status_code == 201:
            return None

        r_json = r.json()
        if 'emails' not in r_json:
            return None

        emails_list = r_json['emails']
        emails = ''
        for email in emails_list:
            emails += (email + ',')
        return emails
