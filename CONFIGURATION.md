# Configuration
There must be a file named `config.toml` in the same directory of the executable.

All configuration expects these three options:
- `api_key`: Your Google Sheets API key.
- `spreadsheet_id`: The ID of your Google Sheet.
- `tab_name`: The name of the tab to read from.

Without any of these, you'll receive a Zod validation error upon startup and the application will exit.
On top of this, at least one of `obs` and `fs` must be enabled. They are implicitly assumed to be enabled if you pass any other config options into them.

# Minimal configuration

The most minimal possible `config.toml` is:
```toml
api_key = "API Key"
spreadsheet_id = "Spreadsheet ID"
tab_name = "Sheet1"

[obs]
enabled = true
```

This assumes:
- your sheet is organised in rows
- you don't want to interact with OBS over WebSocket
- you want to poll Google Sheets every 1500ms
- you wish to enable the OBS integration
- that you're interested in the range `A1:Z1000`

# Specification / complete example

Here's the full set of options you can use:
```toml
api_key = "API Key"                 # An API Key with permissions to read from your Google Sheet.
spreadsheet_id = "Spreadsheet ID"   # The spreadsheet - must be viewable by anyone with a link.
tab_name = "Sheet1"                 # What tab to read from.
dimension = "ROWS"                  # Or COLUMNS. Don't change this without good reason.
update_interval = 1500              # Lowest this can go is 1000ms.
range = "A1:Z1000"                  # What range to collect values from. Best left alone.

[obs]
enabled = true                      # Enable the OBS WebSocket client?
host = "localhost"                  # What OBS server to connect to?
port = 4455                         # What port is the OBS WebSocket server running on?
password = ""                       # What is the password required to connect?

[fs]
enabled = true                      # Enable writing cell values to disk?

[fs.cells]
some_file_name = "A1"               # Save `files/some_file_name.txt` with the contents of whatever is in cell A1.

[logging]
level = "log"                       # How important do logs have to be to pass the filter?
format = "pretty"                   # How do we want to format logs?
sanitized = true                    # Do we want to filter out the API key & spreadsheet URI?

# Log level can be:
# alert     - fatal
# error     - errors
# warn      - warnings
# info      - generic info messages
# fail      - generic fail messages
# success   - generic success messages
# log       - generic logs
# debug     - debugging logs
# verbose   - ridiculous amount of logs

# Log format can be:
# pretty    - human readable, pretty logs
# json      - machine readable, structured JSON (javascript object notation) logs
# common    - conforming to the Common Log Format
# standard  - human readable but formatted for console / terminal output
```