BACKEND_URL = '127.0.0.1:8000'

LOGIN_URL = f'http://{BACKEND_URL}/users/obtain_token/'

ME_URL = f'http://{BACKEND_URL}/users/me'

ROBOT_STATUS_WS = f'ws://{BACKEND_URL}/users/robot_status'

COMMAND_URL = f'http://{BACKEND_URL}/robots/robot/command'
