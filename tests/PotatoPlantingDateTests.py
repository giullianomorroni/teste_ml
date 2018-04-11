#!/usr/bin/env python
# -*- coding: utf-8 -*-
# encoding=utf8

from machine_learning.laboratory_A_and_L import PotatoPlantingDate
from datetime import datetime, timedelta


now = datetime.now()
now = now - timedelta(days=10)
result = PotatoPlantingDate.season_by_planting_date(now.date(), 'POTATO', 'atlantic')
print('result', result)
assert 'POTATO (ATLANTIC) (245)' == result


now = datetime.now()
result = PotatoPlantingDate.season_by_planting_date(now.date(), '', 'atlantic')
print('result', result)
assert result is None


now = datetime.now()
now = now - timedelta(days=108)
result = PotatoPlantingDate.season_by_planting_date(now.date(), 'potato', 'SHEPODY')
print('result', result)
assert 'POTATO (SHEPODY) (359)' == result

