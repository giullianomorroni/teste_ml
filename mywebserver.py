#!/usr/bin/env python
# -*- coding: utf-8 -*-
# encoding=utf8


from bottle import route, run
from machine_learning.laboratory_A_and_L import PotatoDecisionTree
import threading
from service.Service import InFieldDecisionTreeService


@route('/build_models', method='POST')
def build_model():
    t = threading.Thread(target=builder)
    t.start()
    return "Models are building, it WILL take some time to be done!!!"


@route('/recommendation/<id_field_analyses>', method='POST')
def recommendation(id_field_analyses):
    t = threading.Thread(target=do_analyses, args={id_field_analyses})
    t.start()
    return "ok, your analysis will be processed."


def builder():
    model = PotatoDecisionTree.PotatoDecisionTree()
    model.build_model()


def do_analyses(id_field_analyses):
    idt = InFieldDecisionTreeService()
    idt.classify(id_field_analyses)


run(host='0.0.0.0', port=8000, debug=True)