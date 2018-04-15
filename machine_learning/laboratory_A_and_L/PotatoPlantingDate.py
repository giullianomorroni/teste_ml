#!/usr/bin/env python
# -*- coding: utf-8 -*-
# encoding=utf8

from datetime import datetime, timedelta

potatos = [
    ('POTATO', 'SUPERIOR', '253', '0-59'),
    ('POTATO', 'SUPERIOR', '265', '70-79'),
    ('POTATO', 'SUPERIOR', '286', '60-69'),
    ('POTATO', 'SUPERIOR', '296', '80-89'),
    ('POTATO', 'SUPERIOR', '312', '90-99'),
    ('POTATO', 'SUPERIOR', '363', '100-109'),
    ('POTATO', 'SUPERIOR', '372', '110-139'),
    ('POTATO', 'SUPERIOR', '381', '140-999'),

    ('POTATO', 'KENNEBEC', '248', '0-59'),
    ('POTATO', 'KENNEBEC', '258', '70-79'),
    ('POTATO', 'KENNEBEC', '279', '60-69'),
    ('POTATO', 'KENNEBEC', '289', '80-89'),
    ('POTATO', 'KENNEBEC', '300', '90-99'),
    ('POTATO', 'KENNEBEC', '355', '100-109'),
    ('POTATO', 'KENNEBEC', '364', '110-139'),
    ('POTATO', 'KENNEBEC', '373', '140-999'),

    ('POTATO', 'NORKOTA', '253', '0-59'),
    ('POTATO', 'NORKOTA', '265', '70-79'),
    ('POTATO', 'NORKOTA', '286', '60-69'),
    ('POTATO', 'NORKOTA', '296', '80-89'),
    ('POTATO', 'NORKOTA', '312', '90-99'),
    ('POTATO', 'NORKOTA', '363', '100-109'),
    ('POTATO', 'NORKOTA', '372', '110-139'),
    ('POTATO', 'NORKOTA', '381', '140-999'),

    ('POTATO', 'NORLAND', '247', '140-999'),
    ('POTATO', 'NORLAND', '260', '60-69'),
    ('POTATO', 'NORLAND', '281', '0-59'),
    ('POTATO', 'NORLAND', '291', '70-79'),
    ('POTATO', 'NORLAND', '306', '80-89'),
    ('POTATO', 'NORLAND', '357', '90-99'),
    ('POTATO', 'NORLAND', '366', '100-109'),
    ('POTATO', 'NORLAND', '375', '140-999'),

    ('POTATO', 'ONAWAY', '252', '0-59'),
    ('POTATO', 'ONAWAY', '261', '70-79'),
    ('POTATO', 'ONAWAY', '282', '60-69'),
    ('POTATO', 'ONAWAY', '292', '80-89'),
    ('POTATO', 'ONAWAY', '307', '90-99'),
    ('POTATO', 'ONAWAY', '362', '100-109'),
    ('POTATO', 'ONAWAY', '371', '110-139'),
    ('POTATO', 'ONAWAY', '380', '140-999'),

    ('POTATO', 'R. BURBANK', '0-59'),
    ('POTATO', 'R. BURBANK', '262', '70-79'),
    ('POTATO', 'R. BURBANK', '283', '60-69'),
    ('POTATO', 'R. BURBANK', '293', '80-89'),
    ('POTATO', 'R. BURBANK', '308', '90-99'),
    ('POTATO', 'R. BURBANK', '360', '100-109'),
    ('POTATO', 'R. BURBANK', '369', '110-139'),
    ('POTATO', 'R. BURBANK', '378', '140-999'),

    ('POTATO', 'ATLANTIC', '245', '0-59'),
    ('POTATO', 'ATLANTIC', '257', '70-79'),
    ('POTATO', 'ATLANTIC', '278', '60-69'),
    ('POTATO', 'ATLANTIC', '288', '80-89'),
    ('POTATO', 'ATLANTIC', '299', '90-99'),
    ('POTATO', 'ATLANTIC', '356', '100-109'),
    ('POTATO', 'ATLANTIC', '365', '110-139'),
    ('POTATO', 'ATLANTIC', '374', '140-999'),

    ('POTATO', 'SHEPODY', '249', '0-59'),
    ('POTATO', 'SHEPODY', '263', '70-79'),
    ('POTATO', 'SHEPODY', '284', '60-69'),
    ('POTATO', 'SHEPODY', '294', '80-89'),
    ('POTATO', 'SHEPODY', '309', '90-99'),
    ('POTATO', 'SHEPODY', '359', '100-109'),
    ('POTATO', 'SHEPODY', '368', '110-139'),
    ('POTATO', 'SHEPODY', '377', '140-999'),

    ('POTATO', 'SNOWDEN', '251', '0-59'),
    ('POTATO', 'SNOWDEN', '264', '70-79'),
    ('POTATO', 'SNOWDEN', '285', '60-69'),
    ('POTATO', 'SNOWDEN', '295', '80-89'),
    ('POTATO', 'SNOWDEN', '311', '90-99'),
    ('POTATO', 'SNOWDEN', '361', '100-109'),
    ('POTATO', 'SNOWDEN', '370', '110-139'),
    ('POTATO', 'SNOWDEN', '379', '140-999'),

    ('POTATO', 'GENERIC', '244', '0-59'),
    ('POTATO', 'GENERIC', '277', '70-79'),
    ('POTATO', 'GENERIC', '255', '60-69'),
    ('POTATO', 'GENERIC', '274', '80-89'),
    ('POTATO', 'GENERIC', '298', '90-99'),
    ('POTATO', 'GENERIC', '297', '100-109'),
    ('POTATO', 'GENERIC', '313', '110-139'),
    ('POTATO', 'GENERIC', '287', '140-999'),
]


def season_by_planting_date(planting_date, crop, variety):
    crop = crop.upper()
    variety = variety.upper()
    now = datetime.now().date()

    days_after_planting = 0

    while now >= planting_date:
        now = now - timedelta(days=1)
        days_after_planting += 1

    for potato in potatos:
        if potato[0] == crop and potato[1] == variety:
            begin = int(potato[3].split('-')[0])
            end = int(potato[3].split('-')[1])
            if begin <= days_after_planting <= end:
                return '{0} ({1}) ({2})'.format(potato[0], potato[1], potato[2])
    return None
