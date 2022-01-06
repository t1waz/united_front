import requests
from kivy.uix.label import Label
from kivy.uix.popup import Popup

from cache import CACHE


class BaseTab:
    REQUEST_METHOD = {
        'get': requests.get,
        'post': requests.post,
    }

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
        request_kwargs = {'data': data or {}}
        if is_authenticated:
            request_kwargs['headers'] = self.auth_headers

        request_method = self.REQUEST_METHOD.get(method.lower())
        if not request_method:
            raise ValueError('invalid method')

        try:
            return request_method(url, **request_kwargs)
        except requests.RequestException:
            CACHE['access_token'] = None
            self.display_error_popup(message='external error')
            return

    @property
    def auth_headers(self):
        return {'Authorization': f"Bearer {CACHE.get('access_token')}"}
