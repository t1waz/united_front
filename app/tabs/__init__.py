import requests
from kivy.uix.label import Label
from kivy.uix.popup import Popup

from cache import CACHE


class APIHandler:
    REQUEST_METHOD = {
        'get': requests.get,
        'post': requests.post,
    }

    def get_response(self, method, url, data=None, is_authenticated=False):
        request_kwargs = {'data': data or {}}
        if is_authenticated:
            request_kwargs['headers'] = self.auth_headers

        request_method = self.REQUEST_METHOD.get(method.lower())
        if not request_method:
            raise ValueError('invalid method')

        return request_method(url, **request_kwargs)

    @property
    def auth_headers(self):
        return {'Authorization': f"Bearer {CACHE.get('access_token')}"}


class BaseTab:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._robot_data_process = None

    @staticmethod
    def display_error_popup(message):
        error_popup = Popup(
            title='ERROR',
            size=(800, 800),
            size_hint=(None, None),
            content=Label(text=message),
        )
        error_popup.open()

    def terminate_robot_data_process(self):
        if self._robot_data_process:
            self._robot_data_process.kill()

    def _get_response(self, method, url, data=None, is_authenticated=False):
        try:
            return APIHandler().get_response(method, url, data, is_authenticated)
        except requests.RequestException:
            self.display_error_popup(message='external error')
            return

    @property
    def is_logged(self):
        return bool(CACHE.get('access_token'))

    @property
    def is_robot_selected(self):
        return bool(CACHE.get('robot_uuid'))
