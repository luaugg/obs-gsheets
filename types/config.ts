import { z } from 'zod';

// Define and validate the structure of your TOML configuration using Zod
export const ConfigSchema = z.object({
  api_key: z.string(),
  spreadsheet_id: z.string(),
  tab_name: z.string(),
  range: z.string().default('A1:Z1000'),
  dimension: z.enum(['ROWS', 'COLUMNS']).default('ROWS'),
  update_interval: z.number().min(1000, 'Update interval must be at least 1000ms - recommend 1500ms'),
  obs: z.object({
    enabled: z.boolean(),
    host: z.string().default('localhost').optional(),
    port: z.number().default(4455).optional(),
    password: z.string().optional(),
  }).optional().default({ enabled: true }),
  fs: z.object({
    enabled: z.boolean(),
    cells: z.record(z.string(), z.string()).optional(),
  }).optional().default({ enabled: false }),
});

// Infer TypeScript type from Zod schema
export type Config = z.infer<typeof ConfigSchema>;