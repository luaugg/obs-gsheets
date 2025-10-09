import logging

from PySide6.QtCore import QObject, QThread, Slot

from websocket import OBSConnection


class Worker(QObject):
    def __init__(self, config, log_level=logging.INFO):
        super().__init__()
        self.config = config
        self.running = False
        self.obs = None
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(log_level)

    @Slot()
    def start(self):
        self.running = True
        self.obs = OBSConnection(
            host=self.config["obs_host"],
            port=self.config["obs_port"],
            password=self.config["obs_password"],
            sheet_id=self.config["sheet_id"],
            tab_name=self.config["tab_name"],
            range=self.config["range"],
            api_key=self.config["api_key"],
            dimension=self.config["dimension"],
            log_level=logging.DEBUG,
        )

        self.logger.info("Worker started.")
        while self.running:
            data = self.obs.fetch_sheet_data()
            if data:
                self.obs.update_sources(data, self.config["dimension"])

            QThread.msleep(self.config["update_interval"])

    @Slot()
    def stop(self):
        self.running = False
        self.logger.info("Worker stopped.")
