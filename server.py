import argparse

from flask import Flask, jsonify
from flask_restful import Api, Resource, reqparse, abort
import firebase_admin
from firebase_admin import credentials, firestore
import DBUtils
from objects.Path import A11y
from objects.Utils import JsonEncoder

# TODO : clean comments and TODOs

app = Flask(__name__)
app.json_encoder = JsonEncoder
api = Api(app)
cred = credentials.Certificate('admin-key.json')
firebase_admin.initialize_app(cred)
db = firestore.client()


# images_put_args = reqparse.RequestParser()
# images_put_args.add_argument("x_pos", type=float, help="X position (0-1)", required=True)
# images_put_args.add_argument("y_pos", type=float, help="Y position (0-1)", required=True)

# class LookAround(Resource):
#     sites = {doc.id: DBUtils.des_site(doc) for doc in db.collection(u'sites').stream()}
#
#     def get(self):
#         parser = reqparse.RequestParser()
#         parser.add_argument('site_name', type=str, required=True)
#         args = parser.parse_args()
#         site_name = args['site_name']
#         if site_name not in self.sites:
#             abort(404, message=f"Site : {site_name} not found")
#
#         return jsonify(self.sites[site_name])


class App(Resource):
    sites = {doc.id: DBUtils.des_site(doc) for doc in db.collection(u'sites').stream()}

    def get(self):
        pass

    def post(self):
        pass

    def put(self):
        pass

    def delete(self):
        pass

    @app.route('/get_site', methods=['GET'])
    def get_site(self):
        parser = reqparse.RequestParser()
        parser.add_argument('site_name', type=str, required=True)
        args = parser.parse_args()
        site_name = args['site_name']
        if site_name not in self.sites:
            abort(404, message=f"Site : {site_name} not found")

        return jsonify(self.sites[site_name])

    @app.route('/shortest_path', methods=['GET'])
    def shortest_path(self):
        parser = reqparse.RequestParser()
        parser.add_argument('site_name', type=str, required=True)
        parser.add_argument('poi_start', type=str, required=True)
        parser.add_argument('poi_end', type=str, required=True)
        parser.add_argument('a11y', type=str, default=A11y.WALK.name)
        args = {}
        try:
            args = parser.parse_args()
        except argparse.ArgumentError as e:
            abort(400, message=f"Params not given properly.")

        site_name = args['site_name']
        poi_start = args['poi_start']
        poi_end = args['poi_end']

        if args['a11y'] not in A11y.__members__:
            abort(400, message=f"param {args['a11y']} is not given properly")
        a11y = A11y[args['a11y']]

        if site_name not in self.sites:
            abort(404, message=f"Site : {site_name} not found")

        site = self.sites[site_name]
        graphs = site.get_graphs()
        start_graph = next((graph for graph in graphs if poi_start in graph.get_poi_wps()), None)
        end_graph = next((graph for graph in graphs if poi_end in graph.get_poi_wps()), None)
        if not start_graph:
            abort(404, message=f"Point of interest: {poi_start} not found in {site_name}")
        if not end_graph:
            abort(404, message=f"Point of interest: {poi_end} not found in {site_name}")
        if start_graph is not end_graph:
            # TODO: handle multiple graphs
            abort(501, message=f"Point of interests found in separate locations in {site_name}, "
                               "navigation between them not implemented yet.")
        graph = start_graph
        start_id = graph.get_poi_wps()[poi_start]
        end_id = graph.get_poi_wps()[poi_end]
        short_path = graph.shortest_path(start_id, end_id, a11y)
        if not short_path:
            abort(404, message=f"Unable to find path from {poi_start} to {poi_end}")

        # for wp in short_path:
        #     print(wp)
        return jsonify(short_path)


# class Image(Resource):
#     images = db.collection(u'Images')
#
#     def get(self, image_id):
#         docs = self.images.stream()
#         for doc in docs:
#             if int(doc.id) == image_id:
#                 return doc.to_dict()
#         abort(404, message="Could not find image")
#
#     def post(self, image_id):
#         docs = self.images.stream()
#         for doc in docs:
#             if int(doc.id) == image_id:
#                 abort(404, message="Image with same ID already exists")
#         args = images_put_args.parse_args()
#         self.images.document(str(image_id)).set(args)
#         return args, 200
#
#     def put(self, image_id):
#         docs = self.images.stream()
#         for doc in docs:
#             if int(doc.id) == image_id:
#                 args = images_put_args.parse_args()
#                 self.images.document(str(image_id)).set(args)
#                 return args, 200
#         abort(404, message="Could not find image")
#
#     def delete(self, image_id):
#         docs = self.images.stream()
#         for doc in docs:
#             if int(doc.id) == image_id:
#                 self.images.document(str(image_id)).delete()
#                 return '', 204
#         abort(404, message="Could not find image")


# api.add_resource(Image, "/image/<int:image_id>")

app_instance = App.as_view('app_instance')
api.add_resource(app_instance, "/get_site", endpoint="get_site")
api.add_resource(app_instance, "/shortest_path", endpoint="shortest_path")

# api.add_resource(App)

# api.add_resource(LookAround, "/get_site")

if __name__ == "__main__":
    app.run(debug=True)
