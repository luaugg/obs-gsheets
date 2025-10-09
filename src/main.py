import sys
import tomllib

from PySide6.QtCore import QThread, Slot
from PySide6.QtWidgets import QApplication, QFileDialog, QMainWindow

from config import Config
from generated import widget_ui as widget
from worker import Worker


class Window(QMainWindow):
    def __init__(self):
        super(Window, self).__init__()
        self.ui = widget.Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.auth_enabled.toggled.connect(lambda checked: self.ui.password.setReadOnly(not checked))
        self.ui.password.setReadOnly(not self.ui.auth_enabled.isChecked())
        self.config = Config()
        self.worker = None
        self.worker_thread = None

    @Slot()
    def on_browse_clicked(self):
        selected_file, _ = QFileDialog.getOpenFileName(
            self, "Open Configuration File (config.toml)", "", "TOML Files (*.toml)"
        )
        if not selected_file:
            return

        with open(selected_file, "rb") as f:
            config = tomllib.load(f)
            obs_config = config.get("obs", {})
            password = obs_config.get("password", None)
            self.ui.api_key.setText(config.get("api_key"))
            self.ui.spreadsheet_id.setText(config.get("spreadsheet_id"))
            self.ui.tab_name.setText(config.get("tab_name"))
            self.ui.range.setText(config.get("range", "A1:Z1000"))
            self.ui.update_interval.setValue(int(config.get("update_interval", 1500)))
            self.ui.dimension.setCurrentText(str(config.get("dimension", "ROWS")).upper())
            self.ui.server.setText(obs_config.get("host", "localhost"))
            self.ui.port.setValue(int(obs_config.get("port", 4455)))
            self.ui.auth_enabled.setChecked(bool(password))
            self.ui.password.setText(password)
            self.config.update_from_ui(self.ui)

    @Slot()
    def on_start_clicked(self):
        self.config.validate()
        self.worker = Worker(self.config)
        self.worker_thread = QThread()
        self.worker.moveToThread(self.worker_thread)
        self.worker_thread.started.connect(self.worker.start)
        self.worker_thread.start()
        self.ui.start.setEnabled(False)
        self.ui.browse.setEnabled(False)
        self.ui.api_key.setReadOnly(True)
        self.ui.spreadsheet_id.setReadOnly(True)
        self.ui.tab_name.setReadOnly(True)
        self.ui.range.setReadOnly(True)
        self.ui.update_interval.setReadOnly(True)
        self.ui.dimension.setEnabled(False)
        self.ui.server.setReadOnly(True)
        self.ui.port.setReadOnly(True)
        self.ui.auth_enabled.setEnabled(False)
        self.ui.password.setReadOnly(True)

    @Slot()
    def on_stop_clicked(self):
        self.worker.stop()
        self.worker_thread.quit()
        self.worker_thread.wait()
        self.worker = None
        self.worker_thread = None
        self.ui.start.setEnabled(True)
        self.ui.browse.setEnabled(True)
        self.ui.api_key.setReadOnly(False)
        self.ui.spreadsheet_id.setReadOnly(False)
        self.ui.tab_name.setReadOnly(False)
        self.ui.range.setReadOnly(False)
        self.ui.update_interval.setReadOnly(False)
        self.ui.dimension.setEnabled(True)
        self.ui.server.setReadOnly(False)
        self.ui.port.setReadOnly(False)
        self.ui.auth_enabled.setEnabled(True)
        self.ui.password.setReadOnly(not self.ui.auth_enabled.isChecked())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec())
