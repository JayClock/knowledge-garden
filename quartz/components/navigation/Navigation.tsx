import { QuartzComponent, QuartzComponentConstructor, QuartzComponentProps } from "../types"
import style from "./navigation.scss"
// @ts-ignore
import script from "./navigation.inline"

const Navigation: QuartzComponent = ({ fileData }: QuartzComponentProps) => {
  const title = fileData.frontmatter?.title
  return (
    <div id="nav" class="navigation h-16 overflow-hidden">
      <div id="menus" class="menus font-bold">
        <div class="flex items-center justify-center h-16">menus</div>
        <div class="flex items-center justify-center h-16">{title}</div>
      </div>
    </div>
  )
}

Navigation.css = style
Navigation.afterDOMLoaded = script

export default (() => Navigation) satisfies QuartzComponentConstructor
