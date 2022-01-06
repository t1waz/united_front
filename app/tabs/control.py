import asyncio
from multiprocessing import Process, Queue
import constants
import json
import websockets

from tabs import BaseTab
from kivy.clock import Clock


data_queue = Queue()


async def read_robot_status(q):
    async with websockets.connect(constants.ROBOT_STATUS_WS) as websocket:
        while True:
            data = await websocket.recv()
            try:
                api_data = json.loads(data)
            except (ValueError, AttributeError):
                continue

            q.put(api_data)


def start_read_robot_status(app):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(read_robot_status(app))


class ControlTab(BaseTab):
    HANDLE_DATA_QUEUE_INTERVAL = 0.25

    def control_tab_click(self):
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
            target=start_read_robot_status, args={data_queue}
        )
        self._robot_data_process.start()

        Clock.schedule_interval(self.handle_data_queue, self.HANDLE_DATA_QUEUE_INTERVAL)

    def handle_data_queue(self, *args, **kwargs):
        if data_queue.empty():
            return

        data_frame = data_queue.get()

        self.ids.control_mode_label.text = data_frame.get('mode', '')
        self.ids.control_speed_label.text = str(data_frame.get('speed'))
        self.ids.control_pos_x_label.text = str(data_frame.get('position_x'))
        self.ids.control_pos_y_label.text = str(data_frame.get('position_y'))
