import json
import os
import io
from typing import List
import socket

import firebase_admin
import requests

import objects.Utils
from firebase_admin import credentials, firestore, storage
from objects.Path import A11y
from objects.Site import Site
from objects.Waypoint import Waypoint

IP = 'localhost'
hostname = socket.gethostname()
if hostname == "DESKTOP-A651GUV":
    IP = socket.gethostbyname(hostname)
PORT = '5000'
BASE = f'http://{IP}:{PORT}/'


class Admin:

    def __init__(self):
        self._cred = credentials.Certificate('admin-key.json')
        firebase_admin.initialize_app(self._cred)
        self._db = firestore.client()
        self.bucket = storage.bucket('navigate-a1e16.appspot.com')

    '''''
    @param: collection name, document name
    @return: deserialized Site object
    '''''

    def get_site_from_col_doc(self, col, doc) -> Site:
        sites_collection = self._db.collection(col)
        site_doc_ref = sites_collection.document(doc)
        site_doc = site_doc_ref.get()
        site_data = site_doc.to_dict()
        ret_val = Site('', [], {})
        ret_val.deserialize(site_data)
        return ret_val

    ''''
    @param: Site object, collection name
    @output: refreshed serialized Site object stored in the DB
    '''''

    def save_site_to_col(self, site_obj: Site, col):
        sites_collection = self._db.collection(col)
        saved_doc_ref = sites_collection.document(str(site_obj.get_site_name()))
        site_json = json.dumps(site_obj.serialize(), cls=objects.Utils.JsonEncoder)
        saved_doc_ref.set(json.loads(site_json))

    ''''
    @param: Site object, collection name, graph name, Waypoint object,
            wp_id_1, wp_id_2, time_from_1_to_2, time_from_2_to_1, a11y_from_1_to_2,
            a11y_from_2_to_1
    @output: connect a new Waypoint between wp_1 to wp_2, and stored in the DB
    '''''

    def add_wp_between(self, site_obj: Site, col, graph_name, new_wp: Waypoint, wp_1_id: str, wp_2_id: str,
                       t_from_1: int = 0, t_from_2: int = 0, a11y_from_1: List[A11y] = None,
                       a11y_from_2: List[A11y] = None):
        graph = site_obj.get_graph_by_name(graph_name)
        if not graph:
            return 'Graph not found'
        graph.add_wp_between(new_wp, wp_1_id, wp_2_id, t_from_1, t_from_2, a11y_from_1, a11y_from_2)
        self.save_site_to_col(site_obj, col)
        # TODO: refresh site in Server objects in sites

    ''''
    @param: Site name, Graph name, Waypoint object, image folder path - where images stored
    @output: save 4 images in format {image_name}-{direction}.jpg to Storage
    '''''

    def add_wp_images(self, site_name, graph_id, wp: Waypoint, image_path='imagesToUpload'):
        image_directions = ['-up', '-down', '-left', '-right']
        allowed_extensions = '.jpg'
        images = {}

        for direction in image_directions:
            image_file = os.path.join(image_path, wp.get_id() + direction + allowed_extensions)
            if not os.path.isfile(image_file):
                return f"Image file '{image_file}' does not exist"
            images[f'image{direction}'] = open(image_file, 'rb')

        bucket_path = f'sites/{site_name}/graphs/{graph_id}/places/{wp.get_place_id()}/areas/{wp.get_area_id()}'
        for image_name, image in images.items():
            self.bucket.blob(f'{bucket_path}/{image_name}').upload_from_file(image, content_type='image/jpeg')

    def rename_wp(self, site_obj, col, graph_name, wp_old, wp_new):
        graph = site_obj.get_graph_by_name(graph_name)
        if not graph:
            return 'Graph not found'
        wp = graph.get_wps()[wp_old]
        graph.rename_wp(wp_old, wp_new)
        self.save_site_to_col(site_obj, col)

        # refresh site in Server objects in sites
        url = f'{BASE}refresh_sites'
        response = requests.put(url, params={'site_name': site_obj.get_site_name()})
        if response.status_code != 200:
            return f'error {response.status_code}\n{response.text}'
        storage_path = f'sites/{site_obj.get_site_name()}/graphs/{graph_name}/places/{wp.get_place_id()}/areas/{wp.get_area_id()}'
        directions = ['down', 'up', 'left', 'right']
        for direction in directions:
            old_file_path = f'{storage_path}/{wp_old}-{direction}.jpg'
            new_file_path = f'{storage_path}/{wp_new}-{direction}.jpg'
            old_file_blob = self.bucket.blob(old_file_path)
            new_file_blob = self.bucket.blob(new_file_path)
            if old_file_blob.exists():
                new_file_blob.upload_from_file(io.BytesIO(old_file_blob.download_as_bytes()),
                                               content_type=old_file_blob.content_type, rewind=True)
                old_file_blob.delete()


db = Admin()
site = db.get_site_from_col_doc('sites_test', 'Afeka')
graph_name = 'Campus'
wp_old = '3301'
wp_new = '301'
res = db.rename_wp(site, 'sites_test', graph_name, wp_old, wp_new)
if isinstance(res, str):
    print(f'Error : {res}')

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
    -) All waypoints can not contain the symbols underscore ('_')
    -) Save objects -> direct to DB (no URLS)

'''
