import type OBSWebSocket from 'obs-websocket-js'
import type { OBSRequestTypes } from 'obs-websocket-js'
import type { JsonObject } from 'type-fest'
import type { Dimension, Handler, Sheet, SourceWithCell } from '../types/types'
import { logger } from './logger'
import { cellNotationToIndices, convertHexToOBSColor, isErrorValue, valueAtRowCol } from './utils'

export async function fsProcessCell(sheet: Sheet, key: string, cell: string, dimension: Dimension) {
  const [row, col] = cellNotationToIndices(cell) ?? [NaN, NaN]
  const value = valueAtRowCol(row, col, sheet, dimension)

  if (value === undefined) {
    logger().warn(`Cell ${cell} (mapped from "${key}") is out of bounds in the fetched data.`)
    return
  }

  const path = `./files/${key}.txt`
  await Bun.write(path, value)
}

export async function updateSource(
  obs: OBSWebSocket,
  sheet: Sheet,
  { source, row, col }: SourceWithCell,
  dimension: Dimension
) {
  const value = valueAtRowCol(row, col, sheet, dimension)
  if (value === undefined) {
    logger().debug(`${source.sourceName} is out of bounds in the fetched data. Skipping.`)
    return
  }

  if (isErrorValue(value)) {
    logger().debug(`${source.sourceName} contains an error value ("${value}"). Skipping.`)
    return
  }

  const settingsRequest: OBSRequestTypes['GetInputSettings'] = { inputName: source.sourceName as string }
  const response = await obs.call('GetInputSettings', settingsRequest)
  const newSettings = JSON.parse(JSON.stringify(response.inputSettings)) as JsonObject
  const handler = Object.values(sourceHandlers).find((handler: Handler) => {
    return handler.types.includes(source.inputKind as string)
  })

  if (!handler) {
    logger().warn(`No handler found for source kind "${source.inputKind}".`)
    return
  }

  if (!handler.update(newSettings, value)) {
    logger().verbose(`No changes made for source kind "${source.inputKind}".`)
    return
  }

  const updateRequest: OBSRequestTypes['SetInputSettings'] = {
    inputName: source.sourceName as string,
    inputSettings: newSettings
  }

  logger().info(`Updating source "${source.sourceName}" with new value.`)
  await obs.call('SetInputSettings', updateRequest)
}

const sourceHandlers = {
  image: {
    types: ['image_source', 'xObsAsyncImageSource'] as const,
    update: (settings: JsonObject, value: string) => {
      if (settings.file === value) return false
      settings.file = value
      return true
    }
  },
  text: {
    types: ['text_gdiplus_v3', 'text_ft2_source', 'text_freetype2', 'text_gdiplus'] as const,
    update: (settings: JsonObject, value: string) => {
      if (settings.text === value) return false
      settings.text = value
      return true
    }
  },
  color: {
    types: ['color_source_v3', 'color_source_v2', 'color_source'] as const,
    update: (settings: JsonObject, value: string) => {
      if (settings.color === '') return false
      const convertedValue = convertHexToOBSColor(settings.color as number, value)
      if (settings.color === convertedValue) return false

      settings.color = convertedValue
      return true
    }
  }
} satisfies Record<string, Handler>
