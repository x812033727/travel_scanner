export type PlinkCount = number

declare module 'claude-code' {
  interface PluginState {
    'plink-budget': { count: PlinkCount }
  }
}
