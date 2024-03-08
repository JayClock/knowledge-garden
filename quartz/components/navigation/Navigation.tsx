import { QuartzComponent, QuartzComponentConstructor, QuartzComponentProps } from "../types"
import style from "./navigation.scss"
// @ts-ignore
import script from "./navigation.inline"

const Navigation: QuartzComponent = ({ fileData }: QuartzComponentProps) => {
  const title = fileData.frontmatter?.title
  return (
    <div id="nav" class="navigation">
      {title}
    </div>
  )
}

Navigation.css = style
Navigation.afterDOMLoaded = script

export default (() => Navigation) satisfies QuartzComponentConstructor
