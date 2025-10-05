import type { JsonObject } from 'type-fest'

export type Sheet = string[][]
export type Cell = [number, number]
export type Dimension = 'ROWS' | 'COLUMNS'
export type ErrorValue = '#N/A' | '#VALUE!' | '#REF!' | '#DIV/0!' | '#NUM!' | '#NAME?' | '#NULL!' | '#ERROR!'
export type Handler = { types: readonly string[]; update: (settings: JsonObject, value: string) => boolean }

export type Result = {
  status: number
  data: Sheet | null
}

export type SourceWithCell = {
  source: JsonObject
  row: number
  col: number
}
