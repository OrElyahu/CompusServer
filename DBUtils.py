from objects.Path import Path
from objects.Waypoint import Waypoint


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
