import asyncio
import json
from multiprocessing import (
    Queue,
    Process,
)

import websockets
from kivy.clock import Clock

import constants
from cache import CACHE
from tabs import BaseTab


data_queue = Queue()


async def read_robot_status(q, access_token, robot_uuid):
    async with websockets.connect(
        constants.ROBOT_STATUS_WS,
        extra_headers={'robot': robot_uuid, 'authentication': access_token},
    ) as websocket:
        while True:
            data = await websocket.recv()
            try:
                api_data = json.loads(data)
            except (ValueError, AttributeError):
                continue

            q.put(api_data)


def start_read_robot_status(q, access_token, robot_uuid):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(read_robot_status(q, access_token, robot_uuid))


class ControlTab(BaseTab):
    HANDLE_DATA_QUEUE_INTERVAL = 0.25

    def control_tab_click(self):
        if not self.is_logged:
            self.display_error_popup(message='login first')
            return

        if not self.is_robot_selected:
            self.display_error_popup(message='setup robot first')
            return

        self.terminate_robot_data_process()
        self._setup_robot_data_process()

    def _reset_control_labels(self):
        self.ids.control_mode_label.text = ''
        self.ids.control_speed_label.text = ''
        self.ids.control_pos_x_label.text = ''
        self.ids.control_pos_y_label.text = ''

    def _setup_robot_data_process(self):
        self._reset_control_labels()
        self._robot_data_process = Process(
            target=start_read_robot_status,
            args=(data_queue, CACHE.get('access_token'), CACHE.get('robot_uuid')),
        )
        self._robot_data_process.start()

        Clock.schedule_interval(self.handle_data_queue, self.HANDLE_DATA_QUEUE_INTERVAL)

    def _send_command(self, command):
        response = self._get_response(
            method='post',
            url=constants.COMMAND_URL,
            is_authenticated=True,
            data={
                'command': command,
                'robot_uuid': CACHE.get('robot_uuid'),
            },
        )

        if not response or response.status_code != 201:
            self.display_error_popup(message='external error')

    def handle_data_queue(self, *args, **kwargs):
        if data_queue.empty():
            return

        data_frame = data_queue.get()

        self.ids.control_mode_label.text = data_frame.get('state', '')
        self.ids.control_speed_label.text = str(data_frame.get('speed'))
        self.ids.control_pos_x_label.text = str(data_frame.get('position_x'))
        self.ids.control_pos_y_label.text = str(data_frame.get('position_y'))

    def control_go_auto(self):
        self._send_command(command='auto')

    def control_go_idle(self):
        self._send_command(command='idle')

    def control_go_manual(self):
        self._send_command(command='manual')

    def control_go_error(self):
        self._send_command(command='error')
