#!/usr/bin/env python
# -*- coding: utf-8 -*-
# encoding=utf8


def unit_measure(element):
    try:
        data = {
            'N': '%', 'P': '%', 'K': '%', 'Ca': '%', 'Mg': '%', 'S': '%', 'Mn': '%', 'Na': '%',
            'NO3N': 'PPM', 'Al': 'PPM', 'B': 'PPM', 'Cu': 'PPM', 'Fe': 'PPM', 'Zn': 'PPM'
        }
        return data[element.upper()]
    except KeyError:
        return 'NaN'


def soil(data):
    return {
        "K": data["S_K"], "Mg": data["S_MG"], "Ca": data["S_CA"], "Na": data["S_NA"],
        "S": data["S_S"], "Zn": data["S_ZN"], "Mn": data["S_MN"], "Fe": data["S_FE"],
        "Cu": data["S_CU"], "B": data["S_B"], "Al": data["S_AL"], "NO3N": data["S_NO3N"]
    }


def leaf(data):
    return {
        "N": data["L_N"], "NO3N": data["L_NO3N"], "S": data["L_S"], "P": data["L_P"],
        "K": data["L_K"], "Mg": data["L_MG"], "Ca": data["L_CA"], "Na": data["L_NA"],
        "B": data["L_B"], "Zn": data["L_ZN"], "Mn": data["L_MN"], "Fe": data["L_FE"],
        "Cu": data["L_CU"], "Al": data["L_AL"], "Mo": data["L_MO"], "Cl": data["L_CL"]
    }


def fruit(data):
    return {
        "N": data["F_N"], "NO3N": data["F_NO3N"], "S": data["F_S"], "P": data["F_P"],
        "K": data["F_K"], "Mg": data["F_MG"], "Ca": data["F_CA"], "Na": data["F_NA"],
        "B": data["F_B"], "Zn": data["F_ZN"], "Mn": data["F_MN"], "Fe": data["F_FE"],
        "Cu": data["F_CU"], "Al": data["F_AL"]
    }
