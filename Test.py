import json
import os
from typing import List

import firebase_admin
import requests
import socket

import Server
import objects.Utils
from firebase_admin import firestore, credentials
from objects.Graph import Graph, Direction
from objects.Path import A11y, Path
from objects.Report import Report
from objects.Site import Site
from objects.Waypoint import Waypoint

IP = 'localhost'
hostname = socket.gethostname()
if hostname == "DESKTOP-A651GUV":
    IP = socket.gethostbyname(hostname)
PORT = '5000'
BASE = f'http://{IP}:{PORT}/'


class Test:

    def __init__(self):
        # In case server is running -> commit the cred initiation
        # self._cred = credentials.Certificate('admin-key.json')
        # firebase_admin.initialize_app(self._cred)
        self._db = firestore.client()

    def get_site(self, site_name) -> Site:
        url = f'{BASE}get_site'
        params = {'site_name': site_name}
        response = requests.get(url, params=params)
        if response.status_code != 200:
            raise ValueError(f'error {response.status_code}\n{response.text}')

        site_data = response.json()
        ret_val = Site('', [], {})
        ret_val.deserialize(site_data)
        return ret_val

    def shortest_path(self, site_name, wp_id_src, wp_id_dst, a11y=None):
        url = f'{BASE}shortest_path'
        params = {'site_name': site_name,
                  'wp_id_src': wp_id_src,
                  'wp_id_dst': wp_id_dst,
                  'a11y': a11y}
        response = requests.get(url, params=params)
        if response.status_code != 200:
            raise ValueError(f'error {response.status_code}\n{response.text}')

        return response.json()

    def get_sites_list(self):
        url = f'{BASE}get_site_list'
        response = requests.get(url)
        if response.status_code != 200:
            raise ValueError(f'error {response.status_code}\n{response.text}')

        return response.json()



res = Test()
sites = res.get_sites_list()
print(sites)
# TODO: implement the following tests:
'''
***********************
Rules To Validate:
***********************
    -) All POIS and WP_ids are unique, even with multiple graphs
    -) All reports have images in Storage with the same name as the report id
    -) All waypoints, according to neighbors, have the required paths
    -) All waypoints show up in both their graph's wps, and in area's wps, and the WP obj details the right area+place
    -) Path names are in format : 'wpId1_wpId2'
    -) All waypoints can not contain the symbols underscore ('_')
    -) Save objects -> direct to DB (no URLS)

'''
