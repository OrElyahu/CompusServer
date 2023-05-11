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

    def get_site_from_col_doc(self, col, doc) -> Site:
        sites_collection = self._db.collection(col)
        site_doc_ref = sites_collection.document(doc)
        site_doc = site_doc_ref.get()
        site_data = site_doc.to_dict()
        ret_val = Site('', [], {})
        ret_val.deserialize(site_data)
        return ret_val

    def save_site_to_col(self, site_obj: Site, col):
        sites_collection = self._db.collection(col)
        saved_doc_ref = sites_collection.document(str(site_obj.get_site_name()))
        site_json = json.dumps(site_obj.serialize(), cls=objects.Utils.JsonEncoder)
        saved_doc_ref.set(json.loads(site_json))
        # Server.sites[site_obj.get_site_name()] = site_obj
        # TODO: Replace with telling the server to update its sites from DB

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

    def get_site_images(self, site_name):
        url = f'{BASE}get_site_images'
        params = {'site_name': site_name}
        response = requests.get(url, params=params)
        if response.status_code != 200:
            raise ValueError(f'error {response.status_code}\n{response.text}')

        return response.json()

    def upload_report(self, report: Report, image_path):
        url = f'{BASE}upload_report'
        params = report.serialize()
        with open(image_path, 'rb') as f:
            files = {'image': f}
            response = requests.post(url, data=params, files=files)
        if response.status_code != 200:
            raise ValueError(f'error {response.status_code}\n{response.text}')

        return response.json()

    def shortest_path(self, site_name, poi_start, poi_end, a11y=None):
        url = f'{BASE}shortest_path'
        params = {'site_name': site_name,
                  'poi_start': poi_start,
                  'poi_end': poi_end,
                  'a11y': a11y}
        response = requests.get(url, params=params)
        if response.status_code != 200:
            raise ValueError(f'error {response.status_code}\n{response.text}')

        return response.json()

    def add_wp_between(self, graph: Graph, new_wp: Waypoint, wp_1_id: str, wp_2_id: str,
                       t_from_1: int = 0, t_from_2: int = 0, a11y_from_1: List[A11y] = None,
                       a11y_from_2: List[A11y] = None):
        graph.add_wp_between(new_wp, wp_1_id, wp_2_id, t_from_1, t_from_2, a11y_from_1, a11y_from_2)

    def add_wp_images(self, site_name, graph_id, wp: Waypoint, image_path='imagesToUpload'):
        url = f'{BASE}add_wp_images'
        image_directions = ['-up', '-down', '-left', '-right']
        image_files = {}
        for direction in image_directions:
            image_file = os.path.join(image_path, wp.get_id() + direction + '.jpg')
            if not os.path.isfile(image_file):
                raise ValueError(f"Image file '{image_file}' does not exist.")
            image_files[f'image{direction}'] = open(image_file, 'rb')
        data = {
            'storage_path': f'sites/{site_name}/graphs/{graph_id}/places/{wp.get_place_id()}/areas/{wp.get_area_id()}'}
        response = requests.post(url, data=data, files=image_files)
        if response.status_code != 200:
            raise ValueError(f'error {response.status_code}\n{response.text}')

        return response.json()


res = Test()

# restore
# site = res.get_site_from_col_doc('sites_backup', 'Afeka')
# res.save_site_to_col(site, 'sites')



# get_site_from_col_doc
# site = res.get_site_from_col_doc('sites', 'Afeka')
# print(site)


# save_site_to_col
# res.save_site_to_col(site, 'sites')


# get_site
# site = res.get_site('Afekas')
# print(site)

# get_site_images
# urls = res.get_site_images('Afeka')
# print(urls)

# upload_report
# report = Report('', 'test_reporter@gmail.com', 'This is a test', '301', 2, 'Afeka')
# image_path = 'Naruto-Best-Sharingan-Users.jpg'
# response = res.upload_report(report, image_path)
# print(response)

# shortest_path
# paths = res.shortest_path('Afeka', 'Class 301', 'Gate')
# for path in paths:
#     print(path)

# add_wp_between
site = res.get_site('Afeka')
site = res.get_site_from_col_doc('sites', 'Afeka')
res.add_wp_between(graph=site.get_graphs()[0],
                   new_wp=Waypoint('stairs-outside', 'Ficus', 'Outside'),
                   wp_1_id='location-entrance',
                   wp_2_id='building-entrance')
res.add_wp_between(graph=site.get_graphs()[0],
                   new_wp=Waypoint('curb-ramps-outside', 'Ficus', 'Outside'),
                   wp_1_id='location-entrance',
                   wp_2_id='outside-left')
res.save_site_to_col(site, 'sites')
print(site)




# graph.add_connection('stairs-outside', 'curb-ramps-outside', Direction.LEFT, Path(3))
# graph.add_connection('curb-ramps-outside', 'stairs-outside', Direction.UP, Path(5))
# res.save_site_to_col(site, 'sites')


# add_wp_images
# site = res.get_site('Afeka')
# wp_new = Waypoint('stairs-outside', 'Ficus', 'Outside')
# response = res.add_wp_images('Afeka', 'Campus', wp_new)
# print(response)


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
    -) To be continued....:)

'''
