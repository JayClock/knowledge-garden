import { QuartzComponent, QuartzComponentProps, QuartzComponentConstructor } from "./types"
// @ts-ignore
import script from "./scripts/comment.inline"
import style from "./styles/comment.scss"

export default (() => {
  const Comment: QuartzComponent = ({ fileData }: QuartzComponentProps) => {
    if (fileData.dates?.created) {
      const createdTimeStamp = new Date(fileData.dates?.created!).getTime().toString()
      return (
        <div>
          <hr />
          <div id="waline" data-path={`${createdTimeStamp}`}></div>
        </div>
      )
    }
    return null
  }

  Comment.afterDOMLoaded = script
  Comment.css = style

  return Comment
}) satisfies QuartzComponentConstructor
