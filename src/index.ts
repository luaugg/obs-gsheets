import { resolve } from 'node:path'
import { sleep } from 'bun'
import { OBSWebSocket } from 'obs-websocket-js'
import { ConfigSchema } from '../types/config'
import { initLogger } from './logger'
import { fsProcessCell, updateSource } from './updater'
import { fetchSheetData, getBoundSources, requestUri } from './utils'

const configPath = resolve(process.cwd(), 'config.toml')
const configFile = Bun.file(configPath)
const rawConfig = Bun.TOML.parse(await configFile.text())
const config = ConfigSchema.parse(rawConfig)
const wsEnabled = config.obs?.enabled ?? false
const fsEnabled = config.fs?.enabled ?? false
const sanitized = config.logging?.sanitized ?? true
const uri = requestUri(config.spreadsheet_id, config.tab_name, config.range, config.api_key, config.dimension)
const logger = initLogger(config.logging?.level ?? 'log', config.logging?.format ?? 'pretty')

const safeUri = sanitized ? uri
  .replace(config.api_key, '***')
  .replace(config.spreadsheet_id, '***') : uri
const safeWsPassword = sanitized ? (config.obs?.password ? '(sanitized)' : '(none)') : (config.obs?.password ?? '(none)')

logger.info(`OBS integration is ${wsEnabled ? 'enabled' : 'disabled'}.`)
logger.info(`Filesystem integration is ${fsEnabled ? 'enabled' : 'disabled'}.`)
logger.info(`Update interval set to ${config.update_interval}ms.`)
logger.info(`Sanitization is ${sanitized ? 'enabled' : 'disabled'}. Details may be censored IF enabled.`)
logger.info(`Data source URI: ${safeUri}`)

if (!wsEnabled && !fsEnabled) {
  logger.error('Both WebSocket (OBS) and Filesystem integrations are disabled. Nothing to do, exiting.')
  process.exit(1)
}

const obs = new OBSWebSocket()
if (wsEnabled) {
  const host = config.obs?.host ?? 'localhost'
  const port = config.obs?.port ?? 4455
  const password = config.obs?.password

  try {
    await obs.connect(`ws://${host}:${port}`, password)
    logger.success(`Connected to OBS WebSocket server with host: ${host}, port: ${port}, password: ${safeWsPassword}`)
  } catch (error) {
    logger.error(`Failed to connect to OBS WebSocket server at ws://${host}:${port}, password: ${safeWsPassword}`)
    if (error instanceof Error) logger.error(`Raw error message: ${error.message}`)
    logger.alert('Exiting in 5 seconds...')
    sleep(5000)
    process.exit(1)
  }
}

setInterval(async () => {
  const { status, data } = await fetchSheetData(uri)
  switch (status) {
    case 200:
      logger.verbose('Successfully fetched sheet data.')
      break
    case 429:
      logger.warn('Rate limited when fetching sheet data. Consider increasing the update interval.');
      break
    case 403:
      logger.error('Access forbidden when fetching sheet data. Check your API key and permissions.');
      break
    case 400:
      logger.error('Bad request when fetching sheet data. Check your spreadsheet ID, tab name, and range.');
      break
    case 404:
      logger.error('Spreadsheet not found when fetching sheet data. Verify the spreadsheet ID and access rights.');
      break
    default:
      logger.error(`Unexpected error fetching sheet data: HTTP ${status}`);
      break
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
