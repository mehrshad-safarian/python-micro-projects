import psutil
from keyboard_switcher import WindowMonitor, switch_keyboard

from PySide6.QtWidgets import (
    QComboBox,
    QFrame,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


def get_running_applications():
    applications = {}

    for process in psutil.process_iter(["name"]):
        try:
            process_name = process.info["name"]

            if not process_name:
                continue

            key = process_name.lower()

            if key not in applications:
                applications[key] = {
                    "name": process_name,
                    "process": process_name,
                }

        except (
            psutil.NoSuchProcess,
            psutil.AccessDenied,
            psutil.ZombieProcess,
        ):
            continue

    return sorted(
        applications.values(),
        key=lambda application: application["name"].lower(),
    )


class ProfileCard(QFrame):
    def __init__(
        self,
        profile_name,
        applications,
        parent=None,
    ):
        super().__init__(parent)

        self.setObjectName("profileCard")

        layout = QVBoxLayout(self)

        title = QLabel(profile_name)
        title.setObjectName("profileTitle")

        application_label = QLabel(
            "Application"
        )

        self.application_combo = QComboBox()

        self.application_combo.addItem(
            "Select application",
            None,
        )

        for application in applications:
            self.application_combo.addItem(
                application["name"],
                application["process"],
            )

        language_label = QLabel(
            "Keyboard Language"
        )

        self.language_combo = QComboBox()

        self.language_combo.addItem(
            "Select language",
            None,
        )

        self.language_combo.addItem(
            "English (United States)",
            "en-US",
        )

        self.language_combo.addItem(
            "Persian",
            "fa-IR",
        )

        layout.addWidget(title)
        layout.addWidget(application_label)
        layout.addWidget(self.application_combo)
        layout.addWidget(language_label)
        layout.addWidget(self.language_combo)

    def get_selected_application(self):
        return self.application_combo.currentData()

    def get_selected_language(self):
        return self.language_combo.currentData()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Keyboard Switcher")
        self.resize(700, 650)

        applications = get_running_applications()

        self.setup_ui(applications)
        self.setup_monitor()
        self.setup_connections()
        self.apply_styles()

    def setup_ui(self, applications):
        central_widget = QWidget()

        self.setCentralWidget(
            central_widget
        )

        main_layout = QVBoxLayout(
            central_widget
        )

        title = QLabel(
            "Keyboard Switcher"
        )

        title.setObjectName(
            "mainTitle"
        )

        subtitle = QLabel(
            "Automatically switch keyboard "
            "language when you change applications."
        )

        subtitle.setObjectName(
            "subtitle"
        )

        profiles_layout = QHBoxLayout()

        self.profile_a = ProfileCard(
            "Profile A",
            applications,
        )

        self.profile_b = ProfileCard(
            "Profile B",
            applications,
        )

        profiles_layout.addWidget(
            self.profile_a
        )

        profiles_layout.addWidget(
            self.profile_b
        )

        status_layout = QHBoxLayout()

        self.status_label = QLabel(
            "● Monitoring inactive"
        )

        self.status_label.setObjectName(
            "statusLabel"
        )

        self.start_button = QPushButton(
            "Start Monitoring"
        )

        self.stop_button = QPushButton(
            "Stop"
        )

        self.stop_button.setEnabled(
            False
        )

        status_layout.addWidget(
            self.status_label
        )

        status_layout.addStretch()

        status_layout.addWidget(
            self.start_button
        )

        status_layout.addWidget(
            self.stop_button
        )

        main_layout.addWidget(title)
        main_layout.addWidget(subtitle)

        main_layout.addSpacing(20)

        main_layout.addLayout(
            profiles_layout
        )

        main_layout.addStretch()

        main_layout.addLayout(
            status_layout
        )

    def setup_monitor(self):
        self.monitor = WindowMonitor(
            parent=self,
        )

        self.monitor.application_changed.connect(
            self.on_application_changed
        )

    def setup_connections(self):
        self.start_button.clicked.connect(
            self.start_monitoring
        )

        self.stop_button.clicked.connect(
            self.stop_monitoring
        )

    def start_monitoring(self):
        profile_a = self.get_profile_data(
            self.profile_a
        )

        profile_b = self.get_profile_data(
            self.profile_b
        )

        if profile_a is None:
            self.status_label.setText(
                "● Profile A is incomplete"
            )
            return

        if profile_b is None:
            self.status_label.setText(
                "● Profile B is incomplete"
            )
            return

        print()
        print("Monitoring started")
        print("------------------")

        print("Profile A:")
        print(
            "Application:",
            profile_a["application"],
        )
        print(
            "Language:",
            profile_a["language"],
        )

        print()

        print("Profile B:")
        print(
            "Application:",
            profile_b["application"],
        )
        print(
            "Language:",
            profile_b["language"],
        )

        print("------------------")

        self.monitor.start()

        self.status_label.setText(
            "● Monitoring active"
        )

        self.start_button.setEnabled(
            False
        )

        self.stop_button.setEnabled(
            True
        )

    def stop_monitoring(self):
        self.monitor.stop()

        self.status_label.setText(
            "● Monitoring inactive"
        )

        self.start_button.setEnabled(
            True
        )

        self.stop_button.setEnabled(
            False
        )

        print("Monitoring stopped")

    def get_profile_data(self, profile):
        application = (
            profile.get_selected_application()
        )

        language = (
            profile.get_selected_language()
        )

        if not application or not language:
            return None

        return {
            "application": application,
            "language": language,
        }

    def on_application_changed(self, process_name):
        app_a = self.profile_a.get_selected_application()
        lang_a = self.profile_a.get_selected_language()

        app_b = self.profile_b.get_selected_application()
        lang_b = self.profile_b.get_selected_language()

        if app_a and process_name.lower() == app_a.lower():
            print("Profile A")
            print("Language:", lang_a)

            switch_keyboard(lang_a)

            return

        if app_b and process_name.lower() == app_b.lower():
            print("Profile B")
            print("Language:", lang_b)

            switch_keyboard(lang_b)

            return

    def apply_styles(self):
        self.setStyleSheet(
            """
            QMainWindow {
                background-color: #111827;
            }

            QLabel {
                color: #E5E7EB;
            }

            #mainTitle {
                font-size: 28px;
                font-weight: bold;
            }

            #subtitle {
                color: #9CA3AF;
                font-size: 13px;
            }

            #profileCard {
                background-color: #1F2937;
                border: 1px solid #374151;
                border-radius: 12px;
                padding: 10px;
            }

            #profileTitle {
                font-size: 18px;
                font-weight: bold;
            }

            QComboBox {
                background-color: #111827;
                color: #E5E7EB;
                border: 1px solid #4B5563;
                border-radius: 6px;
                padding: 8px;
            }

            QComboBox:hover {
                border: 1px solid #2563EB;
            }

            QPushButton {
                background-color: #2563EB;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 9px 16px;
            }

            QPushButton:hover {
                background-color: #1D4ED8;
            }

            QPushButton:disabled {
                background-color: #374151;
                color: #9CA3AF;
            }

            #statusLabel {
                color: #9CA3AF;
            }
            """
        )