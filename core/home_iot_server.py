# todo: process text and send IR signal order
import json
from abc import ABC, abstractmethod
import logging
from typing import Tuple, List, Dict

import requests

from core.prepare_settings import get_server_settings, get_signal_settings, get_irkit_settings


class GetManager(ABC):

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def run(self):
        response = {}
        return response


class PostDataManager(ABC):

    @abstractmethod
    def __init__(self, posted_data):
        pass

    @abstractmethod
    def run(self):
        response = {}
        return response


class RemoteController(PostDataManager):

    def __init__(self, posted_data=None):
        self._posted_data = posted_data

    def run(self):
        server_settings = get_server_settings()
        response = {}
        if self._posted_data['key'] != server_settings['key']:
            return response
        response['message'] = 'using valid key'
        response['text'] = self._posted_data['text'].replace(' ', '')
        logging.info(f'text: {response["text"]}')
        signal, device, order = self._send_signal(response['text'])
        logging.info(f'device: {device}')
        logging.info(f'order: {order}')
        return response

    def _send_signal(self, message: str):
        """main program recieving message and send signal.
        Returns:
            list: signal sent to IRKIT. [-1] when invalid.
        """
        signal, device, order = self._process_message(message)
        self._send_ir(signal)

        return signal, device, order

    def _process_message(self, message: str) -> Tuple[List[int], str, str]:
        """compose and return signal from message
        """
        device = self._detect_device(message)
        signal, order = self._detect_order(message, device)
        return signal, device, order

    def _detect_device(self, message: str) -> str:
        """detect device name from message
        Returns:
            str: device name, 'NA' when invalid
        """

        pattern2device_map = self._build_pattern2device_map()
        for pattern, device_name in pattern2device_map.items():
            if pattern in message:
                return device_name
        return 'NA'

    def _build_pattern2device_map(self) -> Dict[str, str]:
        signal_settings = get_signal_settings()
        pattern2device_map = {}
        for device_name, v in signal_settings.items():
            pattern2device_map.update({pat: device_name for pat in v['device_pattern']})
        return pattern2device_map

    def _detect_order(self, message: str, device: str) -> Tuple[List[int], str]:
        """returns IR signal list and order from message, using device name as suppliment information
        """
        if device == 'NA':
            return [-1], 'NA'
        pattern2signal_map, pattern2order_map = self._build_pattern2signal_map(device)
        for pattern, signal in pattern2signal_map.items():
            if pattern in message:
                return signal, pattern2order_map[pattern]
        return [-1], 'NA'

    def _build_pattern2signal_map(self, device: str) -> Tuple[Dict[str, List[int]], Dict[str, str]]:
        signal_settings = get_signal_settings()
        pattern2signal_map = {}
        pattern2order_map = {}
        for order_name, items in signal_settings[device]['orders'].items():
            for pat in items['pattern']:
                pattern2signal_map[pat] = items['signal']
                pattern2order_map[pat] = order_name
        return pattern2signal_map, pattern2order_map

    def _send_ir(self, signal: List[int]):
        irkit_settings = get_irkit_settings()
        url = f'http://{format(irkit_settings["url"])}/messages'
        message = {'format': 'raw', 'freq': 38, 'data': signal}
        message = json.dumps(message)

        headers = {
            'Content-Type': 'application/json',
            'X-Requested-With': 'python',
        }

        r = requests.post(url, headers=headers, data=message)
        return r
