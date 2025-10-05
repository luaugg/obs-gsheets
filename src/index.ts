import { resolve } from 'node:path'
import adze from 'adze'
import { OBSWebSocket } from 'obs-websocket-js'
import { ConfigSchema } from '../types/config'
import { fsProcessCell, updateSource } from './updater'
import { fetchSheetData, getBoundSources, requestUri } from './utils'

const configPath = resolve(process.cwd(), 'config.toml')
const configFile = Bun.file(configPath)
const rawConfig = Bun.TOML.parse(await configFile.text())
const config = ConfigSchema.parse(rawConfig)
const wsEnabled = config.obs?.enabled ?? false
const fsEnabled = config.fs?.enabled ?? false
const uri = requestUri(config.spreadsheet_id, config.tab_name, config.range, config.api_key, config.dimension)

adze.namespace('startup').info(`OBS integration is ${wsEnabled ? 'enabled' : 'disabled'}.`)
adze.namespace('startup').info(`Filesystem integration is ${fsEnabled ? 'enabled' : 'disabled'}.`)
adze.namespace('startup').info(`Data source URI (incl. API key; unsanitized): ${uri}`)
adze.namespace('startup').info(`Update interval set to ${config.update_interval}ms.`)

if (!wsEnabled && !fsEnabled) {
  adze
    .namespace('startup')
    .error('Both WebSocket (OBS) and Filesystem integrations are disabled. Nothing to do, exiting.')
  process.exit(1)
}

const obs = new OBSWebSocket()
if (wsEnabled) {
  const host = config.obs?.host ?? 'localhost'
  const port = config.obs?.port ?? 4455
  const password = config.obs?.password

  //adze.namespace('DEBUG').alert(`Connecting to OBS WebSocket server at ws://${host}:${port} WITH password ${password ? 'set' : 'NOT set'}`)

  await obs.connect(`ws://${host}:${port}`, password)
  adze.namespace('startup').success('Connected to OBS WebSocket server.')
}

setInterval(async () => {
  const { status, data } = await fetchSheetData(uri)

  if (status !== 200) {
    adze
      .namespace('loop')
      .error(`Error fetching sheet data: HTTP ${status} - unrecoverable, stopping further attempts.`)
    process.exit(1)
  }

  if (fsEnabled && config.fs?.cells && data) {
    await Promise.all(
      Object.entries(config.fs.cells).map(([key, cell]) => fsProcessCell(data, key, cell, config.dimension))
    )
  }

  if (wsEnabled && data) {
    const boundSources = await getBoundSources(obs)
    await Promise.all(boundSources.map((source) => updateSource(obs, data, source, config.dimension)))
  }
}, config.update_interval)
