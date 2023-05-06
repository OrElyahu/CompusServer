import json

import firebase_admin
from firebase_admin import credentials, firestore
import requests

import objects.Utils
from objects import Waypoint
import DBUtils

# BASE = "http://127.0.0.1:5000/"
# response = requests.get(BASE + "shortest_path?site_name=Afeka&poi_start=Class 301&poi_end=Class 302&a11y=WALK")

# print(json.dumps(response.json(), indent=2))

# response = requests.get(BASE + "shortest_path?site_name=Afeka&poi_start=Class 301&poi_end=Class 302")

# poi_start = 'Gate'
# poi_end = 'Class 304'
# response = requests.get(BASE + f"shortest_path?site_name=Afeka&poi_start={poi_start}&poi_end={poi_end}")
#
# print(json.dumps(response.json(), indent=2))


# response = requests.get(BASE + "get_site?site_name=Afeka")
# print(json.dumps(response.json(), indent=2))

# response = requests.get(BASE + "get_site_images?site_name=Afeka")
# print(json.dumps(response.json(), indent=2))


# waypoint = Waypoint("1", "place_1", "area_1")
# json_data = json.dumps({"waypoint": waypoint}, default=lambda x: x.serialize())


#
# image_to_insert = {"x_pos": 0.2, "y_pos": 0.3}
# i = 0
#
# response = requests.get(BASE + "image/" + str(i))
# print(response.json())
# response = requests.post(BASE + "image/" + str(i), image_to_insert)
# print(response.json())
# response = requests.put(BASE + "image/" + str(i), image_to_insert)
# print(response.json())
# response = requests.delete(BASE + "image/" + str(i))
# print(response)
#
#
# # Before
# data = [{"x_pos": 0.3, "y_pos": 0.1},
#         {"x_pos": 0.7, "y_pos": 0.2},
#         {"x_pos": 0.1, "y_pos": 0.1}]
#
# for i in range(len(data)):
#     response = requests.post(BASE + "image/" + str(i), data[i])
#     print(response.json())
#
#
# val = data[0]
# val["x_pos"] = 0.5
#
# input()
# response = requests.put(BASE + "image/0", val)
# print(response.json())
#
# input()
# response = requests.delete(BASE + "image/0")
# print(response)
#
# input()
# response = requests.get(BASE + "image/2")
# print(response.json())

# cred = credentials.Certificate('admin-key.json')
# firebase_admin.initialize_app(cred)
# db = firestore.client()
# site_doc = db.collection(u'sites').document('Afeka').get()
# site = DBUtils.des_site(site_doc)
# graph = site.get_graphs().__getitem__(0)
# poi_wps = graph.get_poi_wps()
# # start_id = poi_wps['F2 Bathroom']
# # end_id = poi_wps['Class 304']
# short_path = graph.shortest_path('outside-left', '301')
# for wp in short_path:
#     print(wp)
from objects.Graph import Graph
from objects.Site import Site
from google.type.latlng_pb2 import LatLng


class Test:

    def __init__(self):
        self._cred = credentials.Certificate('admin-key.json')
        firebase_admin.initialize_app(self._cred)
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
        # print(site_json)
        saved_doc_ref.set(json.loads(site_json))


res = Test()
site = res.get_site_from_col_doc('sites_test', 'Afeka')
res.save_site_to_col(site, 'sites_ser_test')



# res.save_site_from_col_doc(site, 'sites_ser_test')

# DBUtils.export_site(site, db)

# site_json = json.dumps(site.__dict__(), cls=objects.Utils.JsonEncoder)
# # print(site_json)
# doc_ref_site = db.collection('sites_test').document(str(site.get_site_name()))
# doc_ref_site.set(json.loads(site_json))
# graphs = site.get_graphs()
# for graph in graphs:
#     doc_ref_graph = doc_ref_site.collection('graphs').document(graph.get_graph_name())
#     graph_json = json.dumps(graph.__dict__(), cls=objects.Utils.JsonEncoder)
#     doc_ref_graph.set(json.loads(graph_json))

# TODO: implements
'''
***********************
Rules To Validate:
***********************
    -) All POIS are unique, even with multiple graphs
    -) To be continue....:)

'''
