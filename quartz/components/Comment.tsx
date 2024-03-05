import { QuartzComponent, QuartzComponentProps, QuartzComponentConstructor } from "./types"
// @ts-ignore
import script from "./scripts/comment.inline"
import style from "./styles/comment.scss"

export default (() => {
  const Comment: QuartzComponent = ({ fileData }: QuartzComponentProps) => {
    const createdTimeStamp = new Date(fileData.dates?.created!).getTime().toString()
    return <div id="waline" data-path={`${createdTimeStamp}`}></div>
  }

  Comment.afterDOMLoaded = script
  Comment.css = style

  return Comment
}) satisfies QuartzComponentConstructor
