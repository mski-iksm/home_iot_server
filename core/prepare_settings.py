import yaml


def get_server_settings():
    with open('yamls/secret_server_setting.yml', 'r') as yf:
        server_settings = yaml.load(yf)
        return server_settings


def get_signal_settings():
    with open('yamls/secret_signal_settings.yml', 'r') as yf:
        signal_settings = yaml.load(yf)
        return signal_settings


def get_irkit_settings():
    with open('yamls/secret_irkit_setting.yml', 'r') as yf:
        irkit_settings = yaml.load(yf)
        return irkit_settings
