from flask import Flask
from flask_restful import Api, Resource, reqparse, abort
import firebase_admin
from firebase_admin import credentials, firestore

app = Flask(__name__)
api = Api(app)
cred = credentials.Certificate('admin-key.json')
firebase_admin.initialize_app(cred)
db = firestore.client()

images_put_args = reqparse.RequestParser()
images_put_args.add_argument("x_pos", type=float, help="X position (0-1)", required=True)
images_put_args.add_argument("y_pos", type=float, help="Y position (0-1)", required=True)


class Image(Resource):
    images = db.collection(u'Images')

    def get(self, image_id):
        docs = self.images.stream()
        for doc in docs:
            if int(doc.id) == image_id:
                return doc.to_dict()
        abort(404, message="Could not find image")

    def post(self, image_id):
        docs = self.images.stream()
        for doc in docs:
            if int(doc.id) == image_id:
                abort(404, message="Image with same ID already exists")
        args = images_put_args.parse_args()
        self.images.document(str(image_id)).set(args)
        return args, 200

    def put(self, image_id):
        docs = self.images.stream()
        for doc in docs:
            if int(doc.id) == image_id:
                args = images_put_args.parse_args()
                self.images.document(str(image_id)).set(args)
                return args, 200
        abort(404, message="Could not find image")

    def delete(self, image_id):
        docs = self.images.stream()
        for doc in docs:
            if int(doc.id) == image_id:
                self.images.document(str(image_id)).delete()
                return '', 204
        abort(404, message="Could not find image")


api.add_resource(Image, "/image/<int:image_id>")

if __name__ == "__main__":
    app.run(debug=True)
