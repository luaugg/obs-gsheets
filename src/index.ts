import adze from 'adze'
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

adze.namespace('startup').info(`OBS integration is ${wsEnabled ? 'enabled' : 'disabled'}.`)
adze.namespace('startup').info(`Filesystem integration is ${fsEnabled ? 'enabled' : 'disabled'}.`)
adze.namespace('startup').info(`Data source URI (incl. API key; unsanitized): ${uri}`)
adze.namespace('startup').info(`Update interval set to ${config.update_interval}ms.`)

if (!wsEnabled && !fsEnabled) {
  adze.namespace('startup').error('Both WebSocket (OBS) and Filesystem integrations are disabled. Nothing to do, exiting.')
  process.exit(1)
}

const obs = new OBSWebSocket()

if (wsEnabled) {
  const host = config.obs?.host ?? 'localhost'
  const port = config.obs?.port ?? 4455
  const password = config.obs?.password
  await obs.connect(`ws://${host}:${port}`, password)
  adze.namespace('startup').success('Connected to OBS WebSocket server.')
}

setInterval(async () => {
  const { status, data } = await fetchSheetData(uri)

  if (status !== 200) {
    adze.namespace('loop').error(`Error fetching sheet data: HTTP ${status} - unrecoverable, stopping further attempts.`)
    process.exit(1)
  }

  if (fsEnabled && config.fs?.cells && data) {
    for (const [key, cell] of Object.entries(config.fs.cells)) {
      const [row, col] = cellNotationToIndices(cell) ?? [NaN, NaN]
      const value = valueAtRowCol(row, col, data, config.dimension)

      if (value === undefined) {
        adze.namespace('loop').warn(`Cell ${cell} (mapped from "${key}") is out of bounds in the fetched data. Skipping.`)
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
        adze.namespace('loop').warn(`${source.sourceName} is out of bounds in the fetched data. Skipping.`)
        continue
      }

      if (isErrorValue(value)) {
        adze.namespace('loop').warn(`${source.sourceName} contains an error value ("${value}"). Skipping.`)
        continue
      }

      const settingsRequest: OBSRequestTypes['GetInputSettings'] = { inputName: source.sourceName as string }
      const response = await obs.call('GetInputSettings', settingsRequest)
      const newSettings = JSON.parse(JSON.stringify(response.inputSettings))
      switch (source.inputKind) {
        case 'xObsAsyncImageSource':
        case 'image_source':
          if (newSettings.file === value) {
            adze.namespace('loop').verbose(`Source "${source.sourceName}" image path is already up to date. Skipping.`)
            continue
          }

          newSettings.file = value
          break

        case 'text_gdiplus_v3':
        case 'text_ft2_source':
        case 'text_freetype2':
        case 'text_gdiplus':
          if (newSettings.text === value) {
            adze.namespace('loop').verbose(`Source "${source.sourceName}" text is already up to date. Skipping.`)
            continue
          }

          newSettings.text = value
          break

        case 'color_source_v3':
        case 'color_source_v2':
        case 'color_source':
          if (value === '') {
            adze.namespace('loop').warn(`Source "${source.sourceName}" has an empty color value. Skipping.`)
            continue
          }

          if (newSettings.color === convertHexToOBSColor(newSettings.color, value)) {
            adze.namespace('loop').verbose(`Source "${source.sourceName}" color is already up to date. Skipping.`)
            continue
          }

          newSettings.color = convertHexToOBSColor(newSettings.color, value)
          break

        default:
          adze.namespace('loop').warn(`Source "${source.sourceName}" has unsupported input kind "${source.inputKind}". Skipping.`)
          continue
      }

      if (JSON.stringify(response.inputSettings) === JSON.stringify(newSettings)) {
        adze.namespace('loop').verbose(`Source "${source.sourceName}" settings are already up to date. Skipping.`)
        continue
      }

      const req: OBSRequestTypes['SetInputSettings'] = {
        inputName: source.sourceName as string,
        inputSettings: newSettings
      }

      adze.namespace('loop').debug(`Updating source "${source.sourceName}" with new value: ${value}`)
      await obs.call('SetInputSettings', req)
    }
  }
}, config.update_interval)
