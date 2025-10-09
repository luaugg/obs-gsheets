import http
import logging

import obsws_python as obs
import regex


class OBSConnection:
    def __init__(self, host, port, password, sheet_id, tab_name, range, api_key, dimension, log_level=logging.INFO):
        self.obs_client = obs.ReqClient(host=host, port=port, password=password, timeout=3)
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(log_level)
        self.req_path = f"https://sheets.googleapis.com/v4/spreadsheets/{sheet_id}/values{tab_name}!{range}?key={api_key}&majorDimension={dimension}"

    def fetch_sheet_data(self):
        self.logger.debug("Fetching sheet data...")
        response = http.client.get(self.req_path)
        data = None
        match response.status_code:
            case 101:
                self.logger.error("Error 101: Invalid API key or access denied.")
            case 200:
                data = response.json()
                self.logger.debug("Sheet data fetched successfully.")
            case _:
                self.logger.error(f"Failed to fetch sheet data: {response.status_code}")

        return data

    def value_of_indices(self, data, row, col, dimension):
        match dimension:
            case "ROWS":
                return data.get(row, []).get(col, None)
            case "COLUMNS":
                return data.get(col, []).get(row, None)
            case _:
                self.logger.error(f"Invalid dimension: {dimension}")
                return None

    def source_name_to_indices(self, source_name):
        matched = regex.match(r"\|\s*([A-Za-z])([0-9]+)$", source_name)
        if not matched:
            return None

        col = ord(matched.group(1).upper()) - ord("A")
        row = int(matched.group(2)) - 1
        return (row, col)

    def map_cell_color(self, cell_color):
        matched = regex.match(r"^#?([0-9a-fA-F]{2})([0-9a-fA-F]{2})([0-9a-fA-F]{2})([0-9a-fA-F]{2})?$", cell_color)
        if not matched:
            return None

        alpha = matched.group(4) or "FF"
        blue = matched.group(3)
        green = matched.group(2)
        red = matched.group(1)
        return int(alpha + blue + green + red, 16)

    def get_source_types(self):
        scenes = [json["sceneName"] for json in self.obs_client.get_scene_list()]
        groups = self.obs_client.get_group_list().groups
        sources = {}
        for scene in scenes:
            for item in self.obs_client.get_scene_item_list(scene).scene_items:
                sources[item["sourceName"]] = item["inputKind"]

        for group in groups:
            for item in self.obs_client.get_group_scene_item_list(group).scene_items:
                sources[item["sourceName"]] = item["inputKind"]

        return sources

    def get_sources_with_cells(self):
        sources = self.get_sources()
        for name, input_kind in sources.items():
            match self.source_name_to_indices(name):
                case (row, col):
                    yield (name, input_kind, row, col)
                case _:
                    continue

    def update_sources(self, data, dimension):
        sources = self.get_sources_with_cells()
        for name, input_kind, row, col in sources:
            match self.value_of_indices(data, row, col, dimension):
                case None:
                    self.logger.warning(f"No data found for source '{name}' at ({row}, {col}).")
                    continue
                case value:
                    match input_kind:
                        case "image_source" | "xObsAsyncImageSource":
                            self.obs_client.set_input_settings(name, {"file": value}, True)
                            self.logger.debug(f"Updated image source '{name}' to '{value}'.")
                        case input_kind if input_kind.startswith("text_"):
                            self.obs_client.set_input_settings(name, {"text": value}, True)
                            self.logger.debug(f"Updated text source '{name}' to '{value}'.")
                        case input_kind if input_kind.startswith("color_source"):
                            color = self.map_cell_color(value)
                            if color is not None:
                                self.obs_client.set_input_settings(name, {"color": color}, True)
                                self.logger.debug(f"Updated color source '{name}' to '{value}'.")
                            else:
                                self.logger.warning(
                                    f"Invalid color format '{value}' for source '{name}'. Expected hex format like '#RRGGBB' or '#AARRGGBB'."
                                )
                        case input_kind if input_kind.startswith("browser_source"):
                            self.obs_client.set_input_settings(name, {"url": value}, True)
                            self.logger.debug(f"Updated browser source '{name}' to '{value}'.")
                        case input_kind if input_kind.startswith("media_source"):
                            if regex.match(r"^https?://", value):
                                self.obs_client.set_input_settings(name, {"input": value}, True)
                                self.logger.debug(f"Updated media source '{name}' to '{value}'.")
                            elif regex.match(r"^[a-zA-Z]:\\", value) or value.startswith("/"):
                                self.obs_client.set_input_settings(name, {"input": value}, True)
                                self.logger.debug(f"Updated media source '{name}' to '{value}'.")
                            else:
                                self.logger.warning(
                                    f"Invalid media source URL or path '{value}' for source '{name}'. Must be a valid URL or absolute file path."
                                )
                        case _:
                            self.logger.warning(
                                f"Unsupported source type '{input_kind}' for source '{name}'. Consider opening an issue to request support for this type."
                            )
