import rawConfig from '../config.toml'
import { ConfigSchema } from '../types/config'
import { fetchSheetData, mapCellToIndices, requestUri } from './loader'

const config = ConfigSchema.parse(rawConfig)

const wsEnabled = config.obs?.enabled ?? false
const fsEnabled = config.fs?.enabled ?? false
const uri = requestUri(
  config.spreadsheet_id,
  config.tab_name,
  config.range,
  config.api_key,
  config.dimension
)

console.log(
  `WebSocket (OBS) integration is ${wsEnabled ? 'enabled' : 'disabled'}.`
)
console.log(`Filesystem integration is ${fsEnabled ? 'enabled' : 'disabled'}.`)
console.log(`Data source URI (incl. API key; unsanitized): ${uri}`)
console.log(`Update interval set to ${config.update_interval}ms.`)

if (!wsEnabled && !fsEnabled) {
  console.error(
    'Both WebSocket (OBS) and Filesystem integrations are disabled. Nothing to do, exiting.'
  )
  process.exit(1)
}

const id = setInterval(async () => {
  const { status, data } = await fetchSheetData(uri)

  if (status !== 200) {
    console.error(
      `Error fetching sheet data: HTTP ${status} - unrecoverable, stopping further attempts.`
    )
    clearInterval(id)
    return
  }

  if (fsEnabled && config.fs?.cells && data) {
    for (const [key, cell] of Object.entries(config.fs.cells)) {
      const [row, col] = mapCellToIndices(cell)
      const value =
        config.dimension === 'ROWS'
          ? data[row]
            ? data[row][col]
            : undefined
          : data[col]
            ? data[col][row]
            : undefined

      if (value === undefined) {
        console.warn(
          `Cell ${cell} (mapped from "${key}") is out of bounds in the fetched data. Skipping.`
        )
        continue
      }

      const path = `./files/${key}.txt`
      await Bun.write(path, value)
    }
  }
}, config.update_interval)
