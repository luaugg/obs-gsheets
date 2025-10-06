import adze, { setup } from 'adze'

type LogLevel = 'alert' | 'error' | 'warn' | 'info' | 'fail' | 'success' | 'log' | 'debug' | 'verbose'
type LogFormat = 'pretty' | 'json' | 'common' | 'standard'

let _logger: adze<string, unknown> | undefined

export function initLogger(level: LogLevel, format: LogFormat) {
  if (!_logger) {
    setup({
      activeLevel: level,
      format: format
    })
    _logger = adze.withEmoji.timestamp.seal()
  }

  return _logger
}

export const logger = () => _logger || initLogger('info', 'pretty')
