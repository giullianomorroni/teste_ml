from django.http import HttpResponse
from machine_learning.laboratory_A_and_L import PotatoDecisionTree
import threading
from domain.decision_tree import InFieldDecisionTree


def builder():
    model = PotatoDecisionTree.PotatoDecisionTree()
    model.build_model()


def do_analyses(id_field_analyses):
    idt = InFieldDecisionTree()
    idt.process_analyses(id_field_analyses)


def build_model():
    t = threading.Thread(target=builder)
    t.start()
    return HttpResponse("Models are building, it WILL take some time to be done!!!")


def recommendation(request, id_field_analyses):
    print(id_field_analyses)
    t = threading.Thread(target=do_analyses, args={id_field_analyses})
    t.start()
    return HttpResponse("ok, your analysis will be processed.")

