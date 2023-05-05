import json
from typing import List

from firebase_admin import firestore
from google.cloud import firestore as db
from google.type.latlng_pb2 import LatLng

from objects.Area import Area
from objects.Graph import Graph
from objects.Path import Path, A11y
from objects.Place import Place
from objects.Site import Site
from objects.Waypoint import Waypoint
from objects.Utils import JsonEncoder


def export_site(site: Site, db: firestore):
    doc_ref = db.collection('sites_test').document(str(site.get_site_name()))
    site_json = json.dumps(site.__dict__(), cls=JsonEncoder)
    doc_ref.set(json.loads(site_json))
    graphs = site.get_graphs()
    graphs_collection = doc_ref.collection('graphs')
    export_graphs(graphs, graphs_collection)


def export_graphs(graphs: List[Graph], graphs_collection: firestore):
    for graph in graphs:
        export_graph(graph, graphs_collection)

def export_graph(graph: Graph, graphs_collection: firestore):
    doc_ref_graph = graphs_collection.document(graph.get_graph_name())
    graph_json = json.dumps(graph.__dict__(), cls=JsonEncoder)
    doc_ref_graph.set(json.loads(graph_json))
    paths_collection = graphs_collection.collection('paths')
    paths = graph.get_paths()
    places_collection = graphs_collection.collection('paths')
    wps_collection = graphs_collection.collection('paths')

# def export_paths(paths, paths_collection: firestore):
#
# def export_path(path, paths_collection: firestore):



def des_site(site_doc: db.DocumentSnapshot):
    site_ref = site_doc.reference
    site = site_doc.to_dict()
    if 'graphs' not in [c.id for c in site_ref.collections()]:
        return None
    if 'entrances' not in site:
        return None

    site = {'site_name': site_doc.id,
            'graphs': des_graphs(site_ref.collection('graphs')),
            'entrances': {wp_id: LatLng(latitude=geo.latitude, longitude=geo.longitude)
                          for wp_id, geo in site['entrances'].items()}}  # convert values from Geo to LatLng
    return Site(**site)


def des_graphs(col_ref: db.CollectionReference):
    return [des_graph(doc) for doc in col_ref.stream()]


def des_graph(graph_doc: db.DocumentSnapshot):
    graph_ref = graph_doc.reference
    sub_cols = [c.id for c in graph_ref.collections()]
    graph = graph_doc.to_dict()
    if not all(sc in sub_cols for sc in ['places', 'paths', 'wps']):
        return None
    if not all(f in graph for f in ['wp_neighs', 'poi_wps']):
        return None

    graph = {'graph_name': graph_doc.id,
             'places': des_places(graph_ref.collection('places')),
             'wps': des_wps(graph_ref.collection('wps')),
             'paths': des_paths(graph_ref.collection('paths')),
             'wp_neighs': des_wp_neighs(graph_ref),
             'poi_wps': des_poi_wps(graph_ref)}
    return Graph(**graph)


# db.collection(u'sites').document('Afeka').collection('graphs')\
#             .document('Campus').collection('places').document('Ficus').collection('areas')
def des_places(col_ref: db.CollectionReference):
    return [des_place(doc) for doc in col_ref.stream()]


def des_place(place_doc: db.DocumentSnapshot):
    place_ref = place_doc.reference
    place = {'place_name': place_doc.id}
    if 'areas' in [c.id for c in place_ref.collections()]:
        place['areas'] = des_areas(place_ref.collection('areas'))
    return Place(**place)


def des_areas(col_ref: db.CollectionReference):
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
def des_wps(col_ref: db.CollectionReference):
    return {doc.id: des_wp(doc) for doc in col_ref.stream()}


def des_wp(wp_doc: db.DocumentSnapshot):
    dic_doc = wp_doc.to_dict()
    dic_doc['_id'] = wp_doc.id
    return Waypoint(**dic_doc)


# col_ref = db.collection(u'sites').document('Afeka').collection(u'graphs'). \
#     document('Campus').collection('paths')
def des_paths(col_ref: db.CollectionReference):
    return {doc.id: des_path(doc) for doc in col_ref.stream()}


def des_path(doc_ref):
    dic_doc = doc_ref.to_dict()
    dic_doc['a11y'] = [A11y(val) for val in dic_doc['a11y']]
    return Path(**dic_doc)
