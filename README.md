# obs-gsheets

OBS Google Sheets reader/poller. Allows you to save files to disk and directly update matching sources in OBS over its built-in WebSocket server.
This project is in beta, meaning that there can be breaking changes between commits, though I'll do my best to minimise them and document them where necessary.

# Initial setup
You'll need:
- The [pre-built binary for your system](https://github.com/luaugg/obs-gsheets/releases/latest), or the source code and [Bun](https://bun.com/) if you wish to build it yourself.
- A `config.toml` file in the same directory as the application. [An example config + specification can be found here.](CONFIGURATION.md)

# Feature requests
Open an issue or, if you'd like to add functionality yourself, feel free to open a PR.

You'll need Bun to build this project and you'll need to both test and format your changes if you want them merged upstream.
You can format your code with the following command:

`bunx --bun biome check --write`

To start a dev server:

`bun run src/index.ts`

To bundle into a single-file executable:

`bun build --compile src/index.ts --outfile dist/obs-gsheets.exe`

# Shoutouts
Special thanks to:
- the creators of [SheetsIO](https://github.com/GrandyB/SheetsIO) for a list of all Google Sheets error values.
- the creators of [obs-google-sheet-importer](https://github.com/DaBenjamins/obs-google-sheet-importer) for some of the OBS WebSocket logic.
