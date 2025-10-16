import threading
import time
import atexit

try:
    import serial
except ImportError:  # pragma: no cover - guard for development hosts without pyserial
    serial = None

if serial is None:
    class SerialException(Exception):
        pass
else:
    SerialException = serial.SerialException

class DMXController:
    """Minimal DMX512 transmitter built around a UART + RS485 interface."""

    def __init__(
        self,
        port=None,
        channels=512,
        refresh_rate=30.0,
        break_time=0.00012,
        mab_time=0.000012,
    ):
        if channels < 1 or channels > 512:
            raise ValueError("DMX channel count must be between 1 and 512.")

        self.channels = channels
        self.refresh_rate = refresh_rate if refresh_rate and refresh_rate > 0 else 30.0
        self.break_time = break_time
        self.mab_time = mab_time

        if port is None:
            # Default to the primary UART device used for DMX (previously read from env)
            port = '/dev/ttyAMA0'

        self._port = port
        self._serial = None
        self._lock = threading.Lock()
        self._universe = bytearray(channels + 1)  # slot 0 reserved for start code
        self._running = True
        self._reported_error = False

        if serial is None:
            print("DMXController: pyserial not available, running in dry-run mode.")
        else:
            try:
                self._serial = serial.Serial(
                    port=self._port,
                    baudrate=250000,
                    bytesize=serial.EIGHTBITS,
                    parity=serial.PARITY_NONE,
                    stopbits=serial.STOPBITS_TWO,
                )
                self._serial.reset_output_buffer()
            except SerialException as exc:  # pragma: no cover - hardware specific
                print(f"DMXController: failed to open {self._port}: {exc}")
                self._serial = None

        self._thread = threading.Thread(target=self._tx_loop, name="DMX-TX", daemon=True)
        self._thread.start()
        atexit.register(self.stop)

    def set_channel(self, channel, value):
        if channel < 1 or channel > self.channels:
            raise ValueError(f"Channel {channel} is outside 1-{self.channels}.")

        level = max(0, min(255, int(value)))
        with self._lock:
            if self._universe[channel] != level:
                self._universe[channel] = level

    def get_channel(self, channel):
        if channel < 1 or channel > self.channels:
            raise ValueError(f"Channel {channel} is outside 1-{self.channels}.")
        with self._lock:
            return self._universe[channel]

    def blackout(self):
        with self._lock:
            for idx in range(1, self.channels + 1):
                self._universe[idx] = 0

    def stop(self):
        if not self._running:
            return
        self._running = False
        if self._thread.is_alive():
            self._thread.join(timeout=1.0)
        if self._serial is not None:
            try:
                self.blackout()
                self._send_frame(bytes(self._universe))
            except Exception:
                pass
            self._serial.close()

    def _tx_loop(self):
        period = 1.0 / self.refresh_rate if self.refresh_rate else 0.05
        next_send = time.perf_counter()

        while self._running:
            if self._serial is None:
                time.sleep(period)
                next_send = time.perf_counter() + period
                continue

            with self._lock:
                frame = bytes(self._universe)

            try:
                self._send_frame(frame)
            except SerialException as exc:  # pragma: no cover - hardware specific
                if not self._reported_error:
                    print(f"DMXController: serial error on {self._port}: {exc}")
                    self._reported_error = True
                time.sleep(1.0)
                next_send = time.perf_counter() + period
                continue

            next_send += period
            sleep_time = next_send - time.perf_counter()
            if sleep_time > 0:
                time.sleep(sleep_time)
            else:
                next_send = time.perf_counter()

    def _send_frame(self, frame):
        if self._serial is None:
            return

        self._serial.break_condition = True
        time.sleep(self.break_time)
        self._serial.break_condition = False
        time.sleep(self.mab_time)
        self._serial.write(b"\x00" + frame[1:])
        self._serial.flush()


class DMXTrigger:
    """DMX-driven replacement for the legacy GPIO Trigger class."""

    def __init__(self, controller, channel, name, on_value=255, off_value=0):
        self._controller = controller
        self._channel = channel
        self._name = name
        self._on_value = max(0, min(255, int(on_value)))
        self._off_value = max(0, min(255, int(off_value)))

        self._is_firing = False
        self._fire_time = 0
        self._fire_intervals = []
        self._fire_index = 0
        self._current_value = self._off_value

        self._set_channel(self._off_value)

    def _set_channel(self, value):
        if value != self._current_value:
            self._controller.set_channel(self._channel, value)
            self._current_value = value

    def _times_up(self, prev_time, interval):
        now = int(round(time.time() * 1000))
        if now - prev_time > interval:
            return True, now
        return False, prev_time

    def Fire(self, intervals):
        self._is_firing = True
        self._fire_index = 0
        self._fire_intervals = intervals or []
        self._fire_time = int(round(time.time() * 1000))

    def Reset(self):
        self._is_firing = False
        self._fire_intervals = []
        self._fire_index = 0
        self._set_channel(self._off_value)

    def Tick(self):
        if not self._is_firing or not self._fire_intervals:
            self._set_channel(self._off_value)
            return

        state = self._on_value if (self._fire_index % 2) == 0 else self._off_value
        self._set_channel(state)

        times_up, new_time = self._times_up(self._fire_time, self._fire_intervals[self._fire_index])
        self._fire_time = new_time

        if times_up:
            if self._fire_index >= len(self._fire_intervals) - 1:
                self._is_firing = False
                self._set_channel(self._off_value)
            else:
                self._fire_index += 1

    def isFiring(self):
        return self._is_firing
