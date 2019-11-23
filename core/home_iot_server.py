# todo: process text and send IR signal order
import json
import requests
import yaml

with open('yamls/secret_settings.yml', 'r') as yf:
    settings = yaml.load(yf)

with open('yamls/secret_irkit_setting.yml', 'r') as yf:
    irkit_settings = yaml.load(yf)


def make_signal(message):
    """main program recieving message and send signal.

    Args:
        message (str): recieved message

    Returns:
        list: signal sent to IRKIT. [-1] when invalid.
    """
    signal, device, order = process_message(message)
    send_ir(signal)

    return signal, device, order


def process_message(message):
    """compose and return signal from message

    Args:
        message (str): spoken message

    Returns:
        list: Signal sent to IRKIT. [-1] when invalid.
        str: device name. 'NA' when invalid.
        str: order name. 'NA' when invalid.
    """

    # process message and detect device
    device = detect_device(message)

    # process message and detect order
    signal, order = detect_order(message, device)

    return signal, device, order


def detect_device(message):
    """detect device name from message

    Args:
        message (str): input messgae

    Returns:
        str: device name, 'NA' when invalid
    """
    device = 'NA'
    for k, v in settings.items():
        for pat in v['device_pattern']:
            if pat in message:
                device = k
                break
        else:
            continue
        break
    return device


def detect_order(message, device):
    """returns IR signal list and order from message, using device name as suppliment information

    Args:
        message (str): [description]
        device (str): [description]

    Returns:
        list: IR signal. list of Int. [-1] when invalid.
        str: order str. 'NA' when invalid.
    """
    signal = [-1]
    order = 'NA'

    if device != 'NA':
        for k, v in settings[device]['orders'].items():
            for pat in v['pattern']:
                if str(pat) in message:
                    signal = v['signal']
                    order = k
                    break
            else:
                continue
            break
    return signal, order


def send_ir(signal):
    url = f'http://{format(irkit_settings['url'])}/messages'
    message = {'format': 'raw', 'freq': 38,
               'data': signal}
    message = json.dumps(message)

    headers = {
        'Content-Type': 'application/json',
        'X-Requested-With': 'python',
    }

    r = requests.post(url, headers=headers, data=message)
    return r
