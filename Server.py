import argparse
import json
import os
import uuid

import firebase_admin

import socket
from objects.Path import A11y
from objects.Site import Site
from objects.Utils import JsonEncoder
from flask import Flask, jsonify, request, abort
from flask_restful import Api, reqparse
from firebase_admin import credentials, firestore, storage

app = Flask(__name__)
app.json_encoder = JsonEncoder
api = Api(app)
cred = credentials.Certificate('admin-key.json')
firebase_admin.initialize_app(cred)
db = firestore.client()
bucket = storage.bucket('navigate-a1e16.appspot.com')

sites = {}
for doc in db.collection('sites').stream():
    site_json = doc.to_dict()
    val = Site('', [], {})
    val.deserialize(site_json)
    sites[doc.id] = val


@app.route('/rename_wp', methods=['PUT'])
def rename_wp():
    global sites
    parser = reqparse.RequestParser()
    parser.add_argument('site_name', type=str, required=True)
    parser.add_argument('graph_name', type=str, required=True)
    parser.add_argument('wp_old', type=str, required=True)
    parser.add_argument('wp_new', type=str, required=True)
    args = parser.parse_args()
    site_name = args['site_name']
    graph_name = args['graph_name']
    wp_old = args['wp_old']
    wp_new = args['wp_new']
    if site_name not in sites:
        abort(404, f"Site : {site_name} not found")
    site = sites[site_name]
    graph = site.get_graph_by_name(graph_name)
    if not graph:
        abort(404, f"Graph : {graph_name} not found")
    graph.rename_wp(wp_old, wp_new)
    wp = graph.get_wps()[wp_new]
    # storage_path = f'sites/{site_name}/graphs/{graph_name}/places/{wp.get_place_id()}/areas/{wp.get_area_id()}'
    # directions = ['down', 'up', 'left', 'right']
    # for direction in directions:
    #     old_file_path = os.path.join(storage_path, f'{wp_old}-{direction}.jpg')
    #     new_file_path = os.path.join(storage_path, f'{wp_new}-{direction}.jpg')
    #     if os.path.exists(old_file_path):
    #         os.rename(old_file_path, new_file_path)

    for doc in db.collection('sites_test').stream():
        if doc.id == site.get_site_name():
            sites[doc.id] = site
            return {'success': f'Site {doc.id} refreshed successfully'}, 200

    abort(404, f"Site : {site_name} not found")


@app.route('/refresh_sites', methods=['PUT'])
def refresh_sites():
    global sites
    parser = reqparse.RequestParser()
    parser.add_argument('site_name', type=str, required=True)
    args = parser.parse_args()
    site_name = args['site_name']
    for doc in db.collection('sites_test').stream(): # TODO change to sites
        if doc.id == site_name:
            site_data = doc.to_dict()
            site = Site('', [], {})
            site.deserialize(site_data)
            sites[doc.id] = site
            return {'success': f'Site {site_name} refreshed successfully'}, 200

    abort(404, f"Site '{site_name}' not found")


@app.route('/upload_report', methods=['POST'])
def upload_report():
    parser = reqparse.RequestParser()
    report_id = str(uuid.uuid4())
    parser.add_argument('reporter_email', type=str, required=True)
    parser.add_argument('description', type=str, required=True)
    parser.add_argument('wp_id', type=str, required=True)
    parser.add_argument('direction', type=int, required=True)
    parser.add_argument('site_name', type=str, required=True)
    image_file = request.files['image']
    extension = os.path.splitext(image_file.filename)[1]
    if extension not in ['.jpg', '.jpeg', '.png']:
        abort(400, f"File with extension : {extension} is invalid. Must be jpeg/jpg/png.")

    args = parser.parse_args()

    # save image to Storage under 'reports' section
    blob = bucket.blob(f'reports/{report_id}.{extension}')
    blob.upload_from_file(image_file, content_type='image/jpeg')
    url = blob.public_url

    report_ref = db.collection('reports')
    report_data = {'reporter_email': args['reporter_email'],
                   'description': args['description'],
                   'wp_id': args['wp_id'],
                   'direction': args['direction'],
                   'site_name': args['site_name']}

    # add the document to the collection with the report_id as the document ID
    report_ref.document(report_id).set(report_data)

    return {'success': 'Report added successfully'}, 200


@app.route('/get_site_images', methods=['GET'])
def get_site_images():
    parser = reqparse.RequestParser()
    parser.add_argument('site_name', type=str, required=True)
    args = parser.parse_args()
    site_name = args['site_name']
    if site_name not in sites:
        abort(404, f"Site : {site_name} not found")

    folder_name = f'sites/{site_name}/graphs/'
    return jsonify({os.path.splitext(os.path.basename(blob.name))[0]: blob.public_url
                    for blob in bucket.list_blobs(prefix=folder_name)
                    if blob.name.endswith(('jpg', 'jpeg', 'png'))})


@app.route('/get_site', methods=['GET'])
def get_site():
    parser = reqparse.RequestParser()
    parser.add_argument('site_name', type=str, required=True)
    args = parser.parse_args()
    site_name = args['site_name']
    if site_name not in sites:
        abort(404, f"Site : {site_name} not found")

    return jsonify(sites[site_name])


@app.route('/shortest_path', methods=['GET'])
def shortest_path():
    parser = reqparse.RequestParser()
    parser.add_argument('site_name', type=str, required=True)
    parser.add_argument('poi_start', type=str, required=True)
    parser.add_argument('poi_end', type=str, required=True)
    parser.add_argument('a11y', type=str, default=A11y.WALK.name)
    args = {}
    try:
        args = parser.parse_args()
    except argparse.ArgumentError as e:
        abort(400, f"Params not given properly.")

    site_name = args['site_name']
    poi_start = args['poi_start']
    poi_end = args['poi_end']

    if args['a11y'] not in A11y.__members__:
        abort(400, f"param {args['a11y']} is not given properly")
    a11y = A11y[args['a11y']]

    if site_name not in sites:
        abort(404, f"Site {site_name} not found")

    site = sites[site_name]
    graphs = site.get_graphs()
    start_graph = next((graph for graph in graphs if poi_start in graph.get_poi_wps()), None)
    end_graph = next((graph for graph in graphs if poi_end in graph.get_poi_wps()), None)
    if not start_graph:
        abort(404, f"Point of interest: {poi_start} not found in {site_name}")
    if not end_graph:
        abort(404, f"Point of interest: {poi_end} not found in {site_name}")
    if start_graph is not end_graph:
        # TODO: handle multiple graphs
        abort(501, f"Point of interests found in separate locations in {site_name}, "
                   f"navigation between them not implemented yet.")
    graph = start_graph
    start_id = graph.get_poi_wps()[poi_start]
    end_id = graph.get_poi_wps()[poi_end]
    short_path = graph.shortest_path(start_id, end_id, a11y)
    if not short_path:
        abort(404, f"Unable to find path from {poi_start} to {poi_end}")
    return jsonify(short_path)


if __name__ == "__main__":
    hostname = socket.gethostname()
    if hostname == "DESKTOP-A651GUV":
        app.run(debug=True, host=socket.gethostbyname(hostname), port=5000)
    else:
        app.run(debug=True, port=5000)
