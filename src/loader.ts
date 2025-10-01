export type Result = {
    status: number,
    data: string[][] | null
}

export type Cell = [number, number]

const requestUri = (sheetId: string, tabName: string, range: string, apiKey: string, dimension: string) =>
    `https://sheets.googleapis.com/v4/spreadsheets/${sheetId}/values/${tabName}!${range}?key=${apiKey}&majorDimension=${dimension}`

const fetchSheetData = async (uri: string): Promise<Result> => {
    const headers = { 'Content-Type': 'application/json' }
    const response = await fetch(uri, { headers })
    const result = { status: response.status }

    if (!response.ok) {
        return { ...result, data: null }
    }
    
    const { values } = await response.json() as { values: string[][] }
    return { ...result, data: values }
}

const mapCellToIndices = (cell: string): Cell => {
    const match = cell.toUpperCase().match(/^([A-Z])([0-9]+)$/)
    
    if (!match || !match[1] || !match[2]) {
        throw new Error(`Invalid cell format: "${cell}". Expected format like "A1".`)
    }

    const col = match[1].charCodeAt(0) - 65 // 'A' is 65 in ASCII
    const row = parseInt(match[2], 10) - 1   // Convert to 0-based index
    return [row, col]
}

export { requestUri, fetchSheetData, mapCellToIndices }