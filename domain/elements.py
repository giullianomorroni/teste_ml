#!/usr/bin/env python
# -*- coding: utf-8 -*-
# encoding=utf8


def soil(data):
    return {
        "K": data["S_K"], "MG": data["S_MG"], "CA": data["S_CA"], "NA": data["S_NA"],
        "S": data["S_S"], "ZN": data["S_ZN"], "MN": data["S_MN"], "FE": data["S_FE"],
        "CU": data["S_CU"], "B": data["S_B"], "AL": data["S_AL"], "NO3N": data["S_NO3N"]
    }


def leaf(data):
    # TODO VALIDATE THIS ELEMENTS
    return {
        "N": data["L_N"], "NO3N": data["L_NO3N"], "S": data["L_S"], "P": data["L_P"],
        "K": data["L_K"], "MG": data["L_MG"], "CA": data["L_CA"], "NA": data["L_NA"],
        "B": data["L_B"], "ZN": data["L_ZN"], "MN": data["L_MN"], "FE": data["L_FE"],
        "CU": data["L_CU"], "AL": data["L_AL"], "MO": data["L_MO"], "CL": data["L_CL"]
    }


def fruit(data):
    # TODO VALIDATE THIS ELEMENTS
    return {
        "N": data["F_N"], "NO3N": data["F_NO3N"], "S": data["F_S"], "P": data["F_P"],
        "K": data["F_K"], "MG": data["F_MG"], "CA": data["F_CA"], "NA": data["F_NA"],
        "B": data["F_B"], "ZN": data["F_ZN"], "MN": data["F_MN"], "FE": data["F_FE"],
        "CU": data["F_CU"], "AL": data["F_AL"]
    }
