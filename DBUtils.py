from firebase_admin import firestore
from google.cloud import firestore as db

from objects.Area import Area
from objects.Path import Path
from objects.Place import Place
from objects.Waypoint import Waypoint


# db.collection(u'sites').document('Afeka').collection('graphs')\
#             .document('Campus').collection('places').document('Ficus').collection('areas')
def des_places(col_ref):
    return [des_place(doc) for doc in col_ref.stream()]


def des_place(place_doc: db.DocumentSnapshot):
    place_ref = place_doc.reference
    place = {'place_name': place_doc.id}
    if 'areas' in [c.id for c in place_ref.collections()]:
        place['areas'] = des_areas(place_ref.collection('areas'))
    return Place(**place)


def des_areas(col_ref):
    return [des_area(doc) for doc in col_ref.stream()]


def des_area(area_doc: db.DocumentSnapshot):
    if not area_doc.exists:  # an Area object must have an area_map image
        return None
    area = area_doc.to_dict()
    area['area_id'] = area_doc.id
    return Area(**area)


# db.collection(u'sites').document('Afeka').collection('graphs')\
#             .document('Campus')
def des_wp_neighs(doc_refs):
    return doc_refs.get().to_dict()['wp_neighs']


# db.collection(u'sites').document('Afeka').collection('graphs')\
#             .document('Campus')
def des_poi_wps(doc_refs):
    return doc_refs.get().to_dict()['poi_wps']


# db.collection(u'sites').document('Afeka').collection(u'graphs'). \
#     document('Campus').collection('wps')
def des_wps(doc_refs):
    return {doc.id: des_wp(doc) for doc in doc_refs}


def des_wp(doc_ref):
    dic_doc = doc_ref.to_dict()
    dic_doc['_id'] = dic_doc.id
    return Waypoint(**dic_doc)


# col_ref = db.collection(u'sites').document('Afeka').collection(u'graphs'). \
#     document('Campus').collection('paths')
def des_paths(doc_refs):
    return {doc.id: des_path(doc) for doc in doc_refs}


def des_path(doc_ref):
    dic_doc = doc_ref.to_dict()
    return Path(**dic_doc)
