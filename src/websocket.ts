import OBSWebSocket, { type OBSRequestTypes, type OBSResponseTypes } from 'obs-websocket-js'
import type { JsonObject } from 'type-fest'
import { mapCellToIndices } from './loader'

type SourceWithCell = {
  source: JsonObject
  row: number
  col: number
}

export const obs = new OBSWebSocket()

export const connectOBS = async (host: string, port: number, password?: string) =>
  obs.connect(`ws://${host}:${port}`, password)

export const getAllSources = async () => {
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

export const getBoundSources = async () => {
  const sources = await getAllSources()
  return sources
    .map((source) => [source.sourceName, source] as [string, JsonObject])
    .filter(([sourceName]) => sourceName.includes('|'))
    .map(([sourceName, source]) => {
      const [row, col] = mapCellToIndices(sourceName)
      return {
        source,
        row,
        col
      } as SourceWithCell
    })
}
