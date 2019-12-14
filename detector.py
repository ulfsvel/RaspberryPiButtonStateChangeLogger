import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)


class Detector:
    STATE_PRESSED = 0
    STATE_NOT_PRESSED = 1

    def __init__(self, gpio_chanel, detection_callback):
        self._gpio_chanel = gpio_chanel
        self._detection_callback = detection_callback
        self._gpio_state = None

    def run(self):
        GPIO.setup(self._gpio_chanel, GPIO.IN)
        self._gpio_state = GPIO.input(self._gpio_chanel)
        while True:
            GPIO.wait_for_edge(self._gpio_chanel, GPIO.BOTH)
            detected_state = GPIO.input(self._gpio_chanel)
            if detected_state != self._gpio_state:
                self._gpio_state = detected_state
                self._detection_callback(detected_state)
