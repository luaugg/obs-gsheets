import logging
import re

import obsws_python as obs
import requests


class OBSConnection:
    def __init__(self, config):
        self.obs_client = obs.ReqClient(
            host=config.obs_host, port=config.obs_port, password=config.obs_password, timeout=3
        )
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        self.req_path = f"https://sheets.googleapis.com/v4/spreadsheets/{config.spreadsheet_id}/values/{config.tab_name}!{config.range}?key={config.api_key}&majorDimension={config.dimension}"

    def fetch_sheet_data(self):
        self.logger.debug("Fetching sheet data...")
        response = requests.get(self.req_path)
        data = None
        match response.status_code:
            case 101:
                self.logger.error("Error 101: Invalid API key or access denied.")
            case 200:
                data = response.json().get("values", [[]])
                self.logger.debug("Sheet data fetched successfully.")
            case _:
                self.logger.error(f"Failed to fetch sheet data: {response.status_code}")

        return data

    def value_of_indices(self, data, row, col, dimension):
        match dimension:
            case "ROWS" if row < len(data) and col < len(data[row]):
                return data[row][col]
            case "COLUMNS" if col < len(data) and row < len(data[col]):
                return data[col][row]
            case _:
                self.logger.debug(f"Cell at ({row}, {col}) for dimension `{dimension}` not found in data.")
                return None

    def source_name_to_indices(self, source_name):
        matched = re.search(r"\|\s*([A-Za-z])([0-9]+)$", source_name)
        if not matched:
            return None

        col = ord(matched.group(1).upper()) - ord("A")
        row = int(matched.group(2)) - 1
        return (row, col)

    def map_cell_color(self, cell_color):
        matched = re.match(r"^#?([0-9a-fA-F]{2})([0-9a-fA-F]{2})([0-9a-fA-F]{2})([0-9a-fA-F]{2})?$", cell_color)
        if not matched:
            return None

        alpha = matched.group(4) or "FF"
        blue = matched.group(3)
        green = matched.group(2)
        red = matched.group(1)
        return int(alpha + blue + green + red, 16)

    def get_source_types(self):
        scenes = [json["sceneName"] for json in self.obs_client.get_scene_list().scenes]
        groups = self.obs_client.get_group_list().groups
        sources = {}
        for scene in scenes:
            for item in self.obs_client.get_scene_item_list(scene).scene_items:
                sources[item["sourceName"]] = item["inputKind"]

        for group in groups:
            for item in self.obs_client.get_group_scene_item_list(group).scene_items:
                sources[item["sourceName"]] = item["inputKind"]

        return sources

    def get_sources_types_with_cells(self):
        sources = self.get_source_types()
        for name, input_kind in sources.items():
            match self.source_name_to_indices(name):
                case (row, col):
                    yield (name, input_kind, row, col)
                case _:
                    continue

    def update_sources(self, data, dimension):
        sources = self.get_sources_types_with_cells()
        for name, input_kind, row, col in sources:
            old_settings = self.obs_client.get_input_settings(name).input_settings
            match self.value_of_indices(data, row, col, dimension):
                case None:
                    # Not continuing here to allow clearing sources if needed
                    self.logger.debug(f"No data found for source '{name}' at ({row}, {col}).")
                case value if value in ["#N/A", "#VALUE!", "#REF!", "#DIV/0!", "#NUM!", "#NAME?", "#NULL!", "#ERROR!"]:
                    self.logger.debug(f"Warning: Error value for source '{name}' at ({row}, {col}): '{value}'")
                    continue
                case value:
                    match input_kind:
                        case "image_source" | "xObsAsyncImageSource":
                            old_value = old_settings.get("file", None)
                            if old_value == value:
                                continue

                            self.obs_client.set_input_settings(name, {"file": value}, True)
                            self.logger.debug(f"Updated image source '{name}' to '{value}'.")
                        case input_kind if input_kind.startswith("text_"):
                            old_value = old_settings.get("text", None)
                            if old_value == value:
                                continue

                            self.obs_client.set_input_settings(name, {"text": value}, True)
                            self.logger.debug(f"Updated text source '{name}' to '{value}'.")
                        case input_kind if input_kind.startswith("color_source"):
                            color = self.map_cell_color(value)
                            old_value = old_settings.get("color", None)
                            if old_value == color:
                                continue
                            elif color is not None:
                                self.obs_client.set_input_settings(name, {"color": color}, True)
                                self.logger.debug(f"Updated color source '{name}' to '{value}'.")
                            else:
                                self.logger.warning(
                                    f"Invalid color format '{value}' for source '{name}'. Expected hex format like '#RRGGBB' or '#AARRGGBB'."
                                )
                        case input_kind if input_kind.startswith("browser_source"):
                            old_value = old_settings.get("url", None)
                            if old_value == value:
                                continue

                            self.obs_client.set_input_settings(name, {"url": value}, True)
                            self.logger.debug(f"Updated browser source '{name}' to '{value}'.")
                        case input_kind if input_kind.startswith("media_source"):
                            old_value = old_settings.get("input", None)
                            if old_value == value:
                                continue

                            if re.match(r"^https?://", value):
                                self.obs_client.set_input_settings(name, {"input": value}, True)
                                self.logger.debug(f"Updated media source '{name}' to '{value}'.")
                            elif re.match(r"^[a-zA-Z]:\\", value) or value.startswith("/"):
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
