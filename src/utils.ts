/** biome-ignore-all lint/style/noNonNullAssertion: false positive regex match */

import type { OBSRequestTypes, OBSResponseTypes, OBSWebSocket } from 'obs-websocket-js'
import type { JsonObject } from 'type-fest'
import type { Cell, Dimension, Result, Sheet, SourceWithCell } from '../types/types'

export async function fetchSheetData(uri: string): Promise<Result> {
  const headers = { 'Content-Type': 'application/json' }
  const response = await fetch(uri, { headers })
  const result = { status: response.status }
  if (!response.ok) return { ...result, data: null }

  const { values } = (await response.json()) as { values: Sheet }
  return { ...result, data: values }
}

export function cellNotationToIndices(cell: string): Cell | null {
  const match = cell.match(/\|\s*([A-Z])([0-9]+)$/i)
  if (!match || !match[1] || !match[2]) return null

  const col = match[1].toUpperCase().charCodeAt(0) - 65
  const row = parseInt(match[2], 10) - 1
  return [row, col]
}

export function convertHexToOBSColor(previous: number, hex: string): number {
  const match = hex.match(/^#?([0-9A-F]{2})([0-9A-F]{2})([0-9A-F]{2})$/i)
  if (!match) return previous

  return parseInt(`ff${match[3]!}${match[2]}${match[1]}`, 16)
}

export function requestUri(
  sheetId: string,
  tabName: string,
  range: string,
  apiKey: string,
  dimension: Dimension
): string {
  return `https://sheets.googleapis.com/v4/spreadsheets/${sheetId}/values/${tabName}!${range}?key=${apiKey}&majorDimension=${dimension}`
}

export function valueAtRowCol(row: number, col: number, data: Sheet, dimension: Dimension): string | undefined {
  return dimension === 'ROWS' ? (data[row] ? data[row][col] : undefined) : data[col] ? data[col][row] : undefined
}

async function getAllSources(obs: OBSWebSocket) {
  const sceneList: OBSResponseTypes['GetSceneList'] = await obs.call('GetSceneList')
  const groupList: OBSResponseTypes['GetGroupList'] = await obs.call('GetGroupList')
  const sceneNames = sceneList.scenes.map((scene) => scene.sceneName as string)

  const scenePromises = sceneNames.map(async (sceneName) => {
    const req: OBSRequestTypes['GetSceneItemList'] = { sceneName }
    const res: OBSResponseTypes['GetSceneItemList'] = await obs.call('GetSceneItemList', req)
    return res.sceneItems
  })

  const groupPromises = groupList.groups.map(async (group) => {
    const req: OBSRequestTypes['GetGroupSceneItemList'] = { sceneName: group }
    const res: OBSResponseTypes['GetGroupSceneItemList'] = await obs.call('GetGroupSceneItemList', req)
    return res.sceneItems
  })

  const results = await Promise.all([...scenePromises, ...groupPromises])
  const sources = results.flat()
  return sources
}

export async function getBoundSources(obs: OBSWebSocket) {
  const sources = await getAllSources(obs)

  return sources
    .map((source) => [source.sourceName, source] as [string, JsonObject])
    .filter(([sourceName]) => sourceName.includes('|'))
    .map(([sourceName, source]) => {
      const [row, col] = cellNotationToIndices(sourceName) ?? [NaN, NaN]
      return {
        source,
        row,
        col
      } as SourceWithCell
    })
}
