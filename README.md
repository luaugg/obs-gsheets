# sheet-importer

Imports Google Sheets values in a way OBS can deal with. Either as files as [SheetsIO](https://github.com/GrandyB/SheetsIO) does,
or by communicating over OBS's WebSocket Server as [obs-google-sheets-importer](https://github.com/DaBenjamins/obs-google-sheet-importer/) and [Companion](https://bitfocus.io/companion) do.

# Running the project
Download the latest release and uncompress it. Modify `config.toml` to suit your needs. The configuration is validated through [Zod](https://zod.dev/) upon startup; you'll get helpful messages if you've messed it up in some way.

The only mandatory requirements of any config:
- An API key with Google Sheets API access.
- A spreadsheet & tab name.
- Poll rate / update interval must be > 1000ms (defaults to 1500ms).

Once saved and good to go, you can just run the batch script. Don't execute the .exe directly as you'll be oblivious to the console messages, nor any convenient way to end the process.

# Contributing
You'll need a recent version of [Bun](https://bun.com), 1.2+.
All changes must be tested, and I'll only merge changes that have been formatted and linted through the associated [Biome](https://biomejs.dev/) config. An example command to do this:
`bunx --bun biome check --write`

If you want to run the project in a development setting, you can use:
`bun run src/index.ts`

If you want to bundle the project into a single production executable, use this command:
`bun build --compile src/index.ts --outfile server.exe`

# Will you add support for \[some feature\]?
Open an issue with your feature request and I'll see.