import { formatDate, getDate } from "./Date"
import { QuartzComponentConstructor, QuartzComponentProps } from "./types"
import readingTime from "reading-time"
import { classNames } from "../util/lang"
import { i18n } from "../i18n"
import { JSX } from "preact"
import style from "./styles/contentMeta.scss"

interface ContentMetaOptions {
  /**
   * Whether to display reading time
   */
  showReadingTime: boolean
  showComma: boolean
}

const defaultOptions: ContentMetaOptions = {
  showReadingTime: true,
  showComma: true,
}

export default ((opts?: Partial<ContentMetaOptions>) => {
  // Merge options with defaults
  const options: ContentMetaOptions = { ...defaultOptions, ...opts }

  function ContentMetadata({ cfg, fileData, displayClass }: QuartzComponentProps) {
    const text = fileData.text

    if (text) {
      const segments: (string | JSX.Element)[] = []

      const timeInfo: string[] = []
      const articaleInfo: string[] = []
      if (fileData.dates) {
        timeInfo.push(`创建时间：${formatDate(fileData.dates.created, cfg.locale)}`)
        timeInfo.push(`最后编辑时间：${formatDate(fileData.dates.modified, cfg.locale)}`)
      }

      // Display reading time if enabled
      if (options.showReadingTime) {
        const { minutes, words: _words } = readingTime(text)
        const displayedTime = i18n(cfg.locale).components.contentMeta.readingTime({
          minutes: Math.ceil(minutes),
        })
        const wordCounts = `📖本文约 ${_words} 字`
        articaleInfo.push(wordCounts)
        articaleInfo.push(displayedTime)
      }

      return (
        <div>
          <p class={classNames(displayClass, "content-meta")}>{timeInfo.join("、")}</p>
          <p class={classNames(displayClass, "content-meta")}>{articaleInfo.join("，")}</p>
        </div>
      )
    } else {
      return null
    }
  }

  ContentMetadata.css = style;
  return ContentMetadata
}) satisfies QuartzComponentConstructor
