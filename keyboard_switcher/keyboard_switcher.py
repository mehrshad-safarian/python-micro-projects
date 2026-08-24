import ctypes
import psutil

import win32gui
import win32process

from PySide6.QtCore import QObject, QTimer, Signal


class WindowMonitor(QObject):
    application_changed = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.last_process = None

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.check_window)

    def start(self):
        self.timer.start(500)

    def stop(self):
        self.timer.stop()

    def check_window(self):
        hwnd = win32gui.GetForegroundWindow()

        if not hwnd:
            return

        try:
            _, pid = win32process.GetWindowThreadProcessId(hwnd)
            process = psutil.Process(pid)
            process_name = process.name()

        except (psutil.NoSuchProcess, psutil.AccessDenied):
            return

        if process_name != self.last_process:
            self.last_process = process_name
            self.application_changed.emit(process_name)


def switch_keyboard(language):
    if language == "en-US":
        layout = "00000409"

    elif language == "fa-IR":
        layout = "00000429"

    else:
        return False

    hwnd = win32gui.GetForegroundWindow()

    if not hwnd:
        return False

    result = ctypes.windll.user32.PostMessageW(
        hwnd,
        0x0050,
        0,
        int(layout, 16),
    )

    return bool(result)