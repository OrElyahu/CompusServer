import pickle


class Report:
    def __init__(self):
        self._reporter_email = None
        self._text = None
        self._uploaded_img_name = None
        self._waypoint_id = None
        self._direction = None

    # setter
    def set_reporter_email(self, reporter_email):
        self._reporter_email = reporter_email

    def set_text(self, text):
        self._text = text

    def set_image_name(self, image_name):
        self._uploaded_img_name = image_name

    def set_waypoint_id(self, waypoint_id):
        self._waypoint_id = waypoint_id

    def set_direction(self, direction):
        self._direction = direction

    # getter
    def get_reporter_email(self):
        return self._reporter_email

    def get_text(self):
        return self._text

    def get_image_name(self):
        return self._uploaded_img_name

    def get_waypoint_id(self):
        return self._waypoint_id

    def get_direction(self):
        return self._direction

    # serialization
    def serialize(self):
        return pickle.dumps(self)

    @staticmethod
    def deserialize(serialized_data):
        return pickle.loads(serialized_data)
