import { QuartzComponent, QuartzComponentProps, QuartzComponentConstructor } from "./types"
// @ts-ignore
import script from "./scripts/comment.inline"
import style from "./styles/comment.scss"

export default (() => {
  const Comment: QuartzComponent = ({ fileData }: QuartzComponentProps) => {
    return <div id="waline" created-time={`${fileData.dates?.created}`}></div>
  }

  Comment.afterDOMLoaded = script
  Comment.css = style

  return Comment
}) satisfies QuartzComponentConstructor
