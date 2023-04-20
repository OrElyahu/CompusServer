import firebase_admin
from firebase_admin import credentials, firestore
from google.type.latlng_pb2 import LatLng
from pyrebase import pyrebase

from DBUtils import des_places
from objects import Utils
from objects.Area import Area
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


col_places = db.collection(u'sites').document('Afeka').collection('graphs')\
            .document('Campus').collection('places')
places = des_places(col_places)
for place in places:
    print(place)


# entrances = doc_ref.get().to_dict().get('entrances')
# graph = doc_ref.collection('graphs').document('Campus')
# place = graph.collection('places').document('Ficus')
# place_fields = place.get().to_dict()
# place_subcols = {c.id: c for c in place.collections()}
# print(place_fields)
# print(place_subcols)
# if 'areas' in place_subcols:
#     areas = place.collection('areas')
#     print(areas)




# area = col_ref.document('F1').get().to_dict()
# if 'area_map' in area:
#     print("exists")
# else:
#     print("not exist")
# area_fields = area.get().to_dict()
# area_fields['area_id'] = area.id
# a = Area(**area_fields)
# print(area_fields)





