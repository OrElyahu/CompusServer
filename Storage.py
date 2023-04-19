import firebase_admin
from firebase_admin import credentials, firestore
from pyrebase import pyrebase
from geopy.point import Point

from objects import Utils
from objects.ImageRef import ImageRef

# firebase = pyrebase.initialize_app(Utils.get_config('config.json'))
# _storage = firebase.storage()

# uploading
# _storage.child("area_map/301-down.jpg").put("301-down.jpg")

# get URL
# print(_storage.child("area_map/301-down.jpg").get_url(None))

# download
# _storage.child("area_map/301-left.jpg").download("301-left.jpg")

# read / show
# local_file_path = _storage.child("area_map/301-down.jpg").get_url(None)
# image = ImageRef("301", local_file_path)
# image.show_img()


# OLD stuff---------------------------------------------

# cred = credentials.Certificate('admin-key.json')
# firebase_admin.initialize_app(cred)
#
# db = firestore.client()
# data = [{"x_pos": 0.5, "y_pos": 0.1},
#         {"x_pos": 0.7, "y_pos": 0.2},
#         {"x_pos": 0.1, "y_pos": 0.1}]

# Put / Post
# for record in data:
#     doc_ref = db.collection(u'Images').document(record['image_id'])
#     doc_ref.set(record)
# for i in range(len(data)):
#     doc_ref = db.collection(u'Images').document(str(i))
#     doc_ref.set(data[i])

# Get
# images_ref = db.collection(u'Images')
# docs = images_ref.stream()
# for doc in docs:
#     print(f'{doc.id} => {doc.to_dict()}')


# Try to read _wps dict
from objects.Path import Path
from objects.Waypoint import Waypoint

cred = credentials.Certificate('admin-key.json')
firebase_admin.initialize_app(cred)
db = firestore.client()

doc_ref = db.collection(u'sites').document('Afeka')

entrances = doc_ref.get().to_dict().get('entrances')
for entrance in entrances:
    lat, lng = entrances[entrance].latitude, entrances[entrance].longitude
    point = Point(latitude=lat, longitude=lng)

#     lat = entrances['location-entrance'].latitude
#     lng = entrances['location-entrance'].longitude
#     print(f'wp_id={wp_id}, [lat,lng]={lat},{lng}')
# print(entrances['location-entrance'])
# lat = entrances['location-entrance'].latitude
# print(lat)
# lng = entrances['location-entrance'].longitude
# print(lng)
