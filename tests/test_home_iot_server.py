import pytest
from core.home_iot_server import RemoteController
from core.prepare_settings import get_signal_settings

settings = get_signal_settings()


class TestDetectDevice:

    @pytest.mark.parametrize('message, result', [
        ('ライト', 'room_light'),
        ('ライトを付けて', 'room_light'),
        ('電気オン', 'room_light'),
        ('えーと電気をつけて', 'room_light'),
    ])
    def test_detect_device(self, message, result):
        remote_controller = RemoteController()
        assert remote_controller._detect_device(message) == result

    @pytest.mark.parametrize('message, result', [
        ('', 'NA'),
        ('デンキ', 'NA'),
        ('落雷と', 'NA'),
        ('発電機', 'NA'),
    ])
    def test_false_detect_device(self, message, result):
        remote_controller = RemoteController()
        assert remote_controller._detect_device(message) == result


class TestDetectOrder:

    @pytest.mark.parametrize('message, device, result', [
        ('ライトを付けて', 'room_light', settings['room_light']['orders']['turn_on']['signal']),
        ('ライトを着けて', 'room_light', settings['room_light']['orders']['turn_on']['signal']),
        ('うーんと電気をつけて', 'room_light', settings['room_light']['orders']['turn_on']['signal']),
        ('あかりを音', 'room_light', settings['room_light']['orders']['turn_on']['signal']),
        ('あかりを消して', 'room_light', settings['room_light']['orders']['turn_off']['signal']),
    ])
    def test_valid_order(self, message, device, result):
        remote_controller = RemoteController()
        assert remote_controller._detect_order(message, device)[0] == result

    @pytest.mark.parametrize('message, device, result', [
        ('雲を付けて', 'NA', [-1]),
    ])
    def test_false_order(self, message, device, result):
        remote_controller = RemoteController()
        assert remote_controller._detect_order(message, device)[0] == result


class TestProcessMessage:

    @pytest.mark.parametrize('message, signal, device, order', [
        ('ライトを付けて', settings['room_light']['orders']['turn_on']['signal'], 'room_light', 'turn_on'),
        ('えーっと電気をつけて', settings['room_light']['orders']['turn_on']['signal'], 'room_light', 'turn_on'),
    ])
    def test_valid_message(self, message, signal, device, order):
        remote_controller = RemoteController()
        assert remote_controller._process_message(message) == (signal, device, order)


class TestSendIR:

    @pytest.mark.parametrize('signal', [
        settings['room_light']['orders']['turn_on']['signal'],
    ])
    @pytest.mark.skip(reason='pytestskip')
    def test_turn_on_light_send_ir(self, signal):
        remote_controller = RemoteController()
        assert remote_controller._send_ir(signal).status_code == 200

    @pytest.mark.parametrize('signal', [
        settings['room_light']['orders']['turn_off']['signal'],
    ])
    @pytest.mark.skip(reason='pytestskip')
    def test_turn_off_light_send_ir(self, signal):
        remote_controller = RemoteController()
        assert remote_controller._send_ir(signal).status_code == 200


class TestSendSignal:

    @pytest.mark.parametrize('message', [
        '電気をつけて',
    ])
    @pytest.mark.skip(reason='pytestskip')
    def test_turn_on_light_send_signal(self, message):
        remote_controller = RemoteController()
        assert remote_controller._send_signal(message)[0] == settings['room_light']['orders']['turn_on']['signal']

    @pytest.mark.parametrize('message', [
        '電気を消して',
    ])
    @pytest.mark.skip(reason='pytestskip')
    def test_turn_off_light_send_signal(self, message):
        remote_controller = RemoteController()
        assert remote_controller._send_signal(message)[0] == settings['room_light']['orders']['turn_off']['signal']

    @pytest.mark.parametrize('message', [
        '変な文字列',
        '電気を壊して',
        '雲をつけて',
    ])
    def test_false_send_signal(self, message):
        remote_controller = RemoteController()
        assert remote_controller._send_signal(message)[0] == [-1]
