import json
import requests
import objects.Utils
from firebase_admin import firestore
from objects.Report import Report
from objects.Site import Site

IP = 'localhost'
PORT = '5000'
BASE = f'http://{IP}:{PORT}/'


class Test:

    def __init__(self):
        # In case server is running -> commit the cred initiation
        # self._cred = credentials.Certificate('admin-key.json')
        # firebase_admin.initialize_app(self._cred)
        self._db = firestore.client()

    def get_site_from_col_doc(self, col, doc) -> Site:
        sites_collection = self._db.collection(col)
        site_doc_ref = sites_collection.document(doc)
        site_doc = site_doc_ref.get()
        site_data = site_doc.to_dict()
        ret_val = Site('', [], {})
        ret_val.deserialize(site_data)
        return ret_val

    def save_site_to_col(self, site_obj: Site, col):
        sites_collection = self._db.collection(col)
        saved_doc_ref = sites_collection.document(str(site_obj.get_site_name()))
        site_json = json.dumps(site_obj.serialize(), cls=objects.Utils.JsonEncoder)
        # print(site_json)
        saved_doc_ref.set(json.loads(site_json))

    def get_site(self, site_name) -> Site:
        url = f'{BASE}get_site'
        params = {'site_name': site_name}
        response = requests.get(url, params=params)
        if response.status_code != 200:
            raise ValueError(f'error {response.status_code}\n{response.text}')

        site_data = response.json()
        ret_val = Site('', [], {})
        ret_val.deserialize(site_data)
        return ret_val

    def get_site_images(self, site_name):
        url = f'{BASE}get_site_images'
        params = {'site_name': site_name}
        response = requests.get(url, params=params)
        if response.status_code != 200:
            raise ValueError(f'error {response.status_code}\n{response.text}')

        return response.json()

    def upload_report(self, ip, port, report: Report, image_path):
        url = f'{BASE}upload_report'
        params = report.serialize()
        with open(image_path, 'rb') as f:
            files = {'image': f}
            response = requests.post(url, data=params, files=files)
        if response.status_code != 200:
            raise ValueError(f'error {response.status_code}\n{response.text}')

        return response.json()

    def shortest_path(self, site_name, poi_start, poi_end, a11y=None):
        url = f'{BASE}shortest_path'
        params = {'site_name': site_name,
                  'poi_start': poi_start,
                  'poi_end': poi_end,
                  'a11y': a11y}
        response = requests.get(url, params=params)
        if response.status_code != 200:
            raise ValueError(f'error {response.status_code}\n{response.text}')

        return response.json()


res = Test()
# get_site_from_col_doc
# site = res.get_site_from_col_doc('sites', 'Afeka')
# print(site)


# get_site
# site = res.get_site('Afekas')
# print(site)

# get_site_images
# urls = res.get_site_images('Afeka')
# print(urls)

# upload_report
# report = Report('', 'test_reporter@gmail.com', 'This is a test', '301', 2, 'Afeka')
# image_path = 'Naruto-Best-Sharingan-Users.jpg'
# response = res.upload_report(report, image_path)
# print(response)

# shortest_path
# paths = res.shortest_path('Afeka', 'Class 301', 'Gate')
# for path in paths:
#     print(path)


# TODO: implement the following tests:
'''
***********************
Rules To Validate:
***********************
    -) All POIS are unique, even with multiple graphs
    -) To be continued....:)

'''
