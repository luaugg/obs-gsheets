import { z } from 'zod'

export const ConfigSchema = z.object({
  api_key: z.string(),
  spreadsheet_id: z.string(),
  tab_name: z.string(),
  range: z.string().default('A1:Z1000'),
  dimension: z.enum(['ROWS', 'COLUMNS']).default('ROWS'),
  update_interval: z
    .number()
    .min(1000, 'Update interval must be at least 1000ms - recommend 1500ms')
    .default(1500),
  obs: z
    .object({
      enabled: z.boolean().default(true),
      host: z.string().default('localhost'),
      port: z.number().default(4455),
      password: z.string().optional()
    })
    .optional()
    .default({ enabled: false, host: 'localhost', port: 4455 }),
  fs: z
    .object({
      enabled: z.boolean().default(true),
      cells: z.record(z.string(), z.string()).default({})
    })
    .optional()
    .default({ enabled: false, cells: {} })
})

export type Config = z.infer<typeof ConfigSchema>
