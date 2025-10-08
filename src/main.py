import sys
import tomllib
from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog
from PySide6.QtCore import Slot
from generated import widget_ui as widget
from config import Config

class Window(QMainWindow):
    def __init__(self):
        super(Window, self).__init__()
        self.ui = widget.Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.auth_enabled.toggled.connect(lambda checked: self.ui.password.setReadOnly(not checked))
        self.ui.password.setReadOnly(not self.ui.auth_enabled.isChecked())

    @Slot()
    def on_browse_clicked(self):
        selected_file, _ = QFileDialog.getOpenFileName(self, "Open Configuration File (config.toml)", "", "TOML Files (*.toml)")
        if not selected_file:
            return
        
        with open(selected_file, "rb") as f:
            config = tomllib.load(f)
            config_obj = Config()
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
            config_obj.update_from_ui(self.ui)
            config_obj.validate()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    window.ui.start.clicked.connect(lambda: print("Started [lambda]!"))
    sys.exit(app.exec())
