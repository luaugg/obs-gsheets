class Config:
    def __init__(self):
        self.api_key = None
        self.spreadsheet_id = None
        self.tab_name = None
        self.range = None
        self.update_interval = None
        self.dimension = None
        self.obs_host = None
        self.obs_port = None
        self.auth_enabled = False
        self.obs_password = None

    def update_from_ui(self, ui):
        self.api_key = ui.api_key.text()
        self.spreadsheet_id = ui.spreadsheet_id.text()
        self.tab_name = ui.tab_name.text()
        self.range = ui.range.text()
        self.update_interval = int(ui.update_interval.text().replace("ms", "").strip())
        self.dimension = ui.dimension.currentText().upper()
        self.obs_host = ui.server.text()
        self.obs_port = int(ui.port.text())
        self.obs_password = ui.password.text()
        self.auth_enabled = ui.auth_enabled.isChecked()

    def validate(self):
        if not self.api_key:
            raise ValueError("API key is required")
        if not self.spreadsheet_id:
            raise ValueError("Spreadsheet ID is required")
        if not self.tab_name:
            raise ValueError("Tab name is required")
        if not self.range:
            print("Range not specified, defaulting to A1:Z1000")
            self.range = "A1:Z1000"
        if not self.update_interval:
            print("Update interval not specified, defaulting to 1500ms")
            self.update_interval = 1500
        if self.dimension and str(self.dimension).upper() not in ["ROWS", "COLUMNS"]:
            raise ValueError("Dimension must be either 'ROWS' or 'COLUMNS'")
        if not self.obs_host:
            print("OBS host not specified, defaulting to localhost")
            self.obs_host = "localhost"
        if not self.obs_port:
            print("OBS port not specified, defaulting to 4455")
            self.obs_port = 4455
        if not self.auth_enabled:
            self.obs_password = None
        elif self.auth_enabled and not self.obs_password:
            raise ValueError("OBS password is required if authentication is enabled")
        if self.auth_enabled and self.obs_password is None:
            print("OBS password not specified, defaulting to no password")
            self.obs_password = None
