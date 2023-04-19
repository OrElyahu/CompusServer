from objects.Area import Area
from objects.Path import Path
from objects.Waypoint import Waypoint




# db.collection(u'sites').document('Afeka').collection('graphs')\
#             .document('Campus').collection('places').document('Ficus').collection('areas')
def des_areas(col_ref):
    areas = []
    for doc in col_ref.stream():
        area = doc.to_dict()
        area['area_id'] = doc.id
        areas.append(Area(**area))
    return areas


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
