from abc import ABC, abstractmethod
import logging
from typing import Dict
from utils.input_data import INPUT_DATA
from utils.inputs import inputs

inputs

class Controller(ABC):
    values: Dict[str,INPUT_DATA]
    @abstractmethod
    def read(self) -> INPUT_DATA:
        pass


def get_controller() -> Controller:
    controller: Controller
    inputs.rescan_devices()
    try:
        controller = Gamepad(inputs.devices.gamepads[0])
    except (IndexError, FileNotFoundError):
        logging.info("No gamepad plugged in. Fallback to keyboard...")
        controller = Keyboard(inputs.devices.keyboards[0])
    return controller


class Keyboard(Controller):
    values = {
        'KEY_A': INPUT_DATA.A,
        'KEY_B': INPUT_DATA.B,
        'KEY_X': INPUT_DATA.X,
        'KEY_Y': INPUT_DATA.Y,
        'KEY_UP': INPUT_DATA.UP,
        'KEY_DOWN': INPUT_DATA.DOWN,
        'KEY_LEFT': INPUT_DATA.LEFT,
        'KEY_RIGHT': INPUT_DATA.RIGHT
    }
    def __init__(self, keyboard: inputs.Keyboard) -> None:
        super().__init__()
        self.keyboard_instance = keyboard

    def read(self) -> INPUT_DATA:
        while True:
            event = self.keyboard_instance.read()[0]
            if event.code in ('SYN_REPORT', 'MSC_SCAN') or event.state == 0:
                continue
            try:
                return self.values[event.code]
            except KeyError:
                logging.info('Key currently not supported.')

class Gamepad(Controller):
    values = {
        'BTN_SOUTH': INPUT_DATA.A,
        'BTN_EAST': INPUT_DATA.B,
        'BTN_WEST': INPUT_DATA.X,
        'BTN_NORTH': INPUT_DATA.Y,
    }
    def __init__(self, gamepad: inputs.GamePad) -> None:
        self.gamepad_instance = gamepad
        self.gamepad_instance.set_vibration(1,1,250)
        self.gamepad_instance.set_vibration(0,0,1)

    def dpad_decode(self, event: inputs.InputEvent) -> INPUT_DATA:
        match((event.code, event.state)):
            case ('ABS_HAT0X', -1):
                return INPUT_DATA.LEFT
            case ('ABS_HAT0X', 1):
                return INPUT_DATA.RIGHT
            case ('ABS_HAT0Y', -1):
                return INPUT_DATA.UP
            case _:
                return INPUT_DATA.DOWN

    def read(self) -> INPUT_DATA:
        while True:
            try:
                event = self.gamepad_instance.read()[0]
            except inputs.UnknownEventCode:
                logging.info('Something is strange with the current implementation of inputs.')
                continue
            if event.code == 'SYN_REPORT' or event.state == 0:
                continue
            try:
                key = self.values[event.code]
            except KeyError:
                if 'ABS_HAT0' not in event.code:
                    logging.info('Key currently not supported.')
                    continue
                return self.dpad_decode(event)
            else:
                return key



