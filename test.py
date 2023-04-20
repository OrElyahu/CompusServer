import firebase_admin
from firebase_admin import credentials, firestore
import requests
import DBUtils


# BASE = "http://127.0.0.1:5000/"
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

cred = credentials.Certificate('admin-key.json')
firebase_admin.initialize_app(cred)
db = firestore.client()
site_doc = db.collection(u'sites').document('Afeka').get()
site = DBUtils.des_site(site_doc)
graph = site.get_graphs().__getitem__(0)
poi_wps = graph.get_poi_wps()
# start_id = poi_wps['F2 Bathroom']
# end_id = poi_wps['Class 304']
short_path = graph.shortest_path('outside-left', '301')
for wp in short_path:
    print(wp)
