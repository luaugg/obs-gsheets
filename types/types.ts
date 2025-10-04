import type { JsonObject } from 'type-fest'

export type Result = {
  status: number
  data: string[][] | null
}

export type SourceWithCell = {
  source: JsonObject
  row: number
  col: number
}

export type Sheet = string[][]
export type Cell = [number, number]
export type Dimension = 'ROWS' | 'COLUMNS'
export type ErrorValue = '#N/A' | '#VALUE!' | '#REF!' | '#DIV/0!' | '#NUM!' | '#NAME?' | '#NULL!' | '#ERROR!'

export function isErrorValue(value: string): value is ErrorValue {
  return ['#N/A', '#VALUE!', '#REF!', '#DIV/0!', '#NUM!', '#NAME?', '#NULL!', '#ERROR!'].includes(value)
}
