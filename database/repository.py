#!/usr/bin/env python
# -*- coding: utf-8 -*-
# encoding=utf8

import os
import psycopg2
import json
from django.conf import settings


class DatabaseRepository:

    def __init__(self):
        databases = settings.DATABASES['default']
        self.conn_string = "host='{0}' dbname='{1}' user='{2}' password='{3}'".format(
            databases['HOST'],
            databases['NAME'],
            databases['USER'],
            databases['PASSWORD']
        )
        self.connection = None

    def database_connect(self):
        try:
            print("Connecting to database\n {0}".format(self.conn_string))
            # get a connection, if a connect cannot be made an exception will be raised here
            self.connection = psycopg2.connect(self.conn_string)
        except Exception as e:
            print("Couldn't connect to database")
            print(e)

    def database_disconnect(self):
        try:
            self.connection.close
        except Exception as e:
            print("Couldn't disconnect from database")
            print(e)

    def save_recommendation(self, id_field_analyses, recommendations):
        try:
            cursor = self.connection.cursor()
            insert_statement = 'insert into recommendation_analyses ' \
                               '(id_field_analyses, recommendation_analyses) values (%s, %s)'
            cursor.execute(insert_statement, (id_field_analyses, json.dumps({"recommendation": recommendations})))
            self.connection.commit()
            cursor.close()
        except Exception as e:
            print("Couldn't save recommendation to database")
            print(e)

    def retrieve_data(self, id_field_analyses):
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
                '   inner join crops as crops on crops.id_crop = fields.id_crop '
                '   inner join varieties as varieties on varieties.id_variety = fields.id_variety '
                'where 1=1 '
                '   and field_analyses.processed = false and field_analyses.id_field_analyses = {0}'
                .format(id_field_analyses))
            records = cursor.fetchall()
            cursor.close()
            return records
        except Exception as e:
            print("Couldn't fetch data")
            print(e)
