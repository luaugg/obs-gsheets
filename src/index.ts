import { type OBSRequestTypes, OBSWebSocket } from 'obs-websocket-js'
import rawConfig from '../config.toml'
import { ConfigSchema } from '../types/config'
import { isErrorValue } from '../types/types'
import {
  cellNotationToIndices,
  convertHexToOBSColor,
  fetchSheetData,
  getBoundSources,
  requestUri,
  valueAtRowCol
} from './utils'

const config = ConfigSchema.parse(rawConfig)
const wsEnabled = config.obs?.enabled ?? false
const fsEnabled = config.fs?.enabled ?? false
const uri = requestUri(config.spreadsheet_id, config.tab_name, config.range, config.api_key, config.dimension)

console.log(`WebSocket (OBS) integration is ${wsEnabled ? 'enabled' : 'disabled'}.`)
console.log(`Filesystem integration is ${fsEnabled ? 'enabled' : 'disabled'}.`)
console.log(`Data source URI (incl. API key; unsanitized): ${uri}`)
console.log(`Update interval set to ${config.update_interval}ms.`)

if (!wsEnabled && !fsEnabled) {
  console.error('Both WebSocket (OBS) and Filesystem integrations are disabled. Nothing to do, exiting.')
  process.exit(1)
}

const obs = new OBSWebSocket()

if (wsEnabled) {
  const host = config.obs?.host ?? 'localhost'
  const port = config.obs?.port ?? 4455
  const password = config.obs?.password
  await obs.connect(`ws://${host}:${port}`, password)
  console.log('Connected to OBS WebSocket server.')
}

setInterval(async () => {
  const { status, data } = await fetchSheetData(uri)

  if (status !== 200) {
    console.error(`Error fetching sheet data: HTTP ${status} - unrecoverable, stopping further attempts.`)
    process.exit(1)
  }

  if (fsEnabled && config.fs?.cells && data) {
    for (const [key, cell] of Object.entries(config.fs.cells)) {
      const [row, col] = cellNotationToIndices(cell) ?? [NaN, NaN]
      const value = valueAtRowCol(row, col, data, config.dimension)

      if (value === undefined) {
        console.warn(`Cell ${cell} (mapped from "${key}") is out of bounds in the fetched data. Skipping.`)
        continue
      }

      const path = `./files/${key}.txt`
      await Bun.write(path, value)
    }
  }

  if (wsEnabled && data) {
    const boundSources = await getBoundSources(obs)

    for (const { source, row, col } of boundSources) {
      const value = valueAtRowCol(row, col, data, config.dimension)

      if (value === undefined) {
        console.warn(`${source.sourceName} is out of bounds in the fetched data. Skipping.`)
        continue
      }

      if (isErrorValue(value)) {
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
          if (value === '' || newSettings.color === convertHexToOBSColor(newSettings.color, value)) {
            continue
          }

          newSettings.color = convertHexToOBSColor(newSettings.color, value)
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
