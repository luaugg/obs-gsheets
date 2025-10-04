import type { OBSRequestTypes } from 'obs-websocket-js'
import rawConfig from '../config.toml'
import { ConfigSchema } from '../types/config'
import { fetchSheetData, mapCellToIndices, requestUri } from './loader'
import { connectOBS, getBoundSources, obs } from './websocket'

const config = ConfigSchema.parse(rawConfig)
const wsEnabled = config.obs?.enabled ?? false
const fsEnabled = config.fs?.enabled ?? false

const errorValues = new Set(['#N/A', '#DIV/0!', '#NAME?', '#NULL!', '#NUM!', '#REF!', '#VALUE!', '#ERROR!'])
const uri = requestUri(config.spreadsheet_id, config.tab_name, config.range, config.api_key, config.dimension)

console.log(`WebSocket (OBS) integration is ${wsEnabled ? 'enabled' : 'disabled'}.`)
console.log(`Filesystem integration is ${fsEnabled ? 'enabled' : 'disabled'}.`)
console.log(`Data source URI (incl. API key; unsanitized): ${uri}`)
console.log(`Update interval set to ${config.update_interval}ms.`)

if (!wsEnabled && !fsEnabled) {
  console.error('Both WebSocket (OBS) and Filesystem integrations are disabled. Nothing to do, exiting.')
  process.exit(1)
}

if (wsEnabled) {
  await connectOBS(config.obs?.host ?? 'localhost', config.obs?.port ?? 4455, config.obs?.password)
  console.log('Connected to OBS WebSocket server.')
}

const cellValue = (row: number, col: number, data: string[][], dimension: 'ROWS' | 'COLUMNS') => {
  return dimension === 'ROWS' ? (data[row] ? data[row][col] : undefined) : data[col] ? data[col][row] : undefined
}

const convertColorToOBS = (hex: string) => {
  const match = hex.match(/^#?([0-9A-F]{2})([0-9A-F]{2})([0-9A-F]{2})$/i)
  if (!match) {
    return 0
  }

  // biome-ignore lint/style/noNonNullAssertion: false positive
  return parseInt(`ff${match[3]!}${match[2]}${match[1]}`, 16)
}

setInterval(async () => {
  const { status, data } = await fetchSheetData(uri)

  if (status !== 200) {
    console.error(`Error fetching sheet data: HTTP ${status} - unrecoverable, stopping further attempts.`)
    process.exit(1)
  }

  if (fsEnabled && config.fs?.cells && data) {
    for (const [key, cell] of Object.entries(config.fs.cells)) {
      const [row, col] = mapCellToIndices(cell)
      const value = cellValue(row, col, data, config.dimension)

      if (value === undefined) {
        console.warn(`Cell ${cell} (mapped from "${key}") is out of bounds in the fetched data. Skipping.`)
        continue
      }

      const path = `./files/${key}.txt`
      await Bun.write(path, value)
    }
  }

  if (wsEnabled && data) {
    const boundSources = await getBoundSources()

    for (const { source, row, col } of boundSources) {
      const value = cellValue(row, col, data, config.dimension)

      if (value === undefined) {
        console.warn(`${source.sourceName} is out of bounds in the fetched data. Skipping.`)
        continue
      }

      if (errorValues.has(value)) {
        console.warn(`${source.sourceName} contains an error value ("${value}"). Skipping.`)
        continue
      }

      const settingsRequest: OBSRequestTypes['GetInputSettings'] = { inputName: source.sourceName as string }
      const response = await obs.call('GetInputSettings', settingsRequest)
      const newSettings = JSON.parse(JSON.stringify(response.inputSettings))

      switch (source.inputKind) {
        case 'xObsAsyncImageSource':
        case 'image_source':
          if (newSettings.file === value) {
            continue
          }

          newSettings.file = value
          break
        case 'text_gdiplus_v3':
        case 'text_ft2_source':
        case 'text_freetype2':
        case 'text_gdiplus':
          if (newSettings.text === value) {
            continue
          }

          newSettings.text = value
          break
        case 'color_source_v3':
        case 'color_source_v2':
        case 'color_source':
          if (value === '') {
            continue
          }

          if (!/^#([0-9A-F]{6}|[0-9A-F]{8})$/i.test(value)) {
            console.warn(`${source.sourceName} does not contain a valid hex color ("${value}"). Skipping.`)
            continue
          }

          if (newSettings.color === convertColorToOBS(value)) {
            continue
          }

          newSettings.color = convertColorToOBS(value)
          break
        default:
          console.warn(`Source "${source.sourceName}" has unsupported input kind "${source.inputKind}". Skipping.`)
          continue
      }

      if (JSON.stringify(response.inputSettings) === JSON.stringify(newSettings)) {
        continue
      }

      const req: OBSRequestTypes['SetInputSettings'] = {
        inputName: source.sourceName as string,
        inputSettings: newSettings
      }

      await obs.call('SetInputSettings', req)
    }
  }
}, config.update_interval)
