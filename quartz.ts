import * as ExternalPlugin from "./.quartz/plugins"
import { loadQuartzConfig, loadQuartzLayout } from "./quartz/plugins/loader/config-loader"

ExternalPlugin.Explorer({
  filterFn: (node) => !["tags", "assets"].includes(node.slugSegment ?? ""),
} satisfies Partial<ExternalPlugin.ExplorerOptions>)

const config = await loadQuartzConfig()
export default config
export const layout = await loadQuartzLayout()
