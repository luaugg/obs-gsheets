import sys
import tomllib

from PySide6.QtCore import Slot
from PySide6.QtWidgets import QApplication, QFileDialog, QMainWindow

from config import Config
from generated import widget_ui as widget


class Window(QMainWindow):
    def __init__(self):
        super(Window, self).__init__()
        self.ui = widget.Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.auth_enabled.toggled.connect(lambda checked: self.ui.password.setReadOnly(not checked))
        self.ui.password.setReadOnly(not self.ui.auth_enabled.isChecked())
        self.config = Config()

    @Slot()
    def on_browse_clicked(self):
        selected_file, _ = QFileDialog.getOpenFileName(
            self, "Open Configuration File (config.toml)", "", "TOML Files (*.toml)"
        )
        if not selected_file:
            return

        with open(selected_file, "rb") as f:
            config = tomllib.load(f)
            password = config.get("obs.password")
            self.ui.api_key.setText(config.get("api_key"))
            self.ui.spreadsheet_id.setText(config.get("spreadsheet_id"))
            self.ui.tab_name.setText(config.get("tab_name"))
            self.ui.range.setText(config.get("range", "A1:Z1000"))
            self.ui.update_interval.setValue(int(config.get("update_interval", 1500)))
            self.ui.dimension.setCurrentText(str(config.get("dimension", "ROWS")).upper())
            self.ui.server.setText(config.get("obs.host", "localhost"))
            self.ui.port.setValue(int(config.get("obs.port", 4455)))
            self.ui.auth_enabled.setChecked(bool(password))
            self.ui.password.setText(password)
            self.config.update_from_ui(self.ui)

    @Slot()
    def on_start_clicked(self):
        self.config.validate()
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
        self.ui.status.setText("Started!")

    @Slot()
    def on_stop_clicked(self):
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
        self.ui.status.setText("Stopped.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    window.ui.start.clicked.connect(lambda: print("Started [lambda]!"))
    sys.exit(app.exec())
