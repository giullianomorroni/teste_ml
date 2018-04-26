#!/usr/bin/env python
# -*- coding: utf-8 -*-
# encoding=utf8


def unit_measure(element):
    try:
        data = {
            'N': '%', 'P': '%', 'K': '%', 'Ca': '%', 'Mg': '%', 'S': '%', 'Mn': '%', 'Na': '%',
            'NO3N': 'PPM', 'Al': 'PPM', 'B': 'PPM', 'Cu': 'PPM', 'Fe': 'PPM', 'Zn': 'PPM'
        }
        return data[element]
    except KeyError:
        return 'NaN'


def soil(data):
    return {
        "K": data.get("S_K"), "Mg": data.get("S_MG"), "Ca": data.get("S_CA"),
        "Na": data.get("S_NA"), "S": data.get("S_S"), "Zn": data.get("S_ZN"),
        "Mn": data.get("S_MN"), "Fe": data.get("S_FE"), "Cu": data.get("S_CU"),
        "B": data.get("S_B"), "Al": data.get("S_AL"), "NO3N": data.get("S_NO3N")
    }


def leaf(data):
    return {
        "N": data.get("L_N"), "NO3N": data.get("L_NO3N"), "S": data.get("L_S"),
        "P": data.get("L_P"), "K": data.get("L_K"), "Mg": data.get("L_MG"),
        "Ca": data.get("L_CA"), "Na": data.get("L_NA"), "B": data.get("L_B"),
        "Zn": data.get("L_ZN"), "Mn": data.get("L_MN"), "Fe": data.get("L_FE"),
        "Cu": data.get("L_CU"), "Al": data.get("L_AL"), "Mo": data.get("L_MO"),
        "Cl": data.get("L_CL")
    }


def fruit(data):
    return {
        "N": data.get("F_N"), "NO3N": data.get("F_NO3N"), "S": data.get("F_S"),
        "P": data.get("F_P"), "K": data.get("F_K"), "Mg": data.get("F_MG"),
        "Ca": data.get("F_CA"), "Na": data.get("F_NA"), "B": data.get("F_B"),
        "Zn": data.get("F_ZN"), "Mn": data.get("F_MN"), "Fe": data.get("F_FE"),
        "Cu": data.get("F_CU"), "Al": data.get("F_AL")
    }
