import { QuartzComponent } from "../types"
import style from "./page-info.scss"
// @ts-ignore
import script from "./page-info.inline"
import { formatDate } from "../Date"
import readingTime from "reading-time"

export default () => {
  const PageInfo: QuartzComponent = ({ fileData, cfg }) => {
    const title = fileData.frontmatter?.title
    let created = ""
    let modified = ""
    let minutes = 0
    let words = 0
    if (fileData.dates) {
      created = formatDate(fileData.dates.created, cfg.locale)
      modified = formatDate(fileData.dates.modified, cfg.locale)
    }

    if (fileData.text) {
      const readingInfo = readingTime(fileData.text)
      minutes = Math.ceil(readingInfo.minutes)
      words = readingInfo.words
    }

    const createdTimeStamp = new Date(fileData.dates?.created!).getTime().toString()

    return (
      <div class="page-info relative -z-10 px-16">
        <div class="flex flex-col justify-center h-full">
          <div id="page-info">
            <div class="page-title">{title}</div>
            <div class="flex items-center meta">
              <div class="mr-2">创建时间：{created}</div>
              <div>最后编辑时间：{modified}</div>
            </div>
            <div class="flex items-center meta">
              <div class="mr-2">字数统计：{words}</div>
              <div class="mr-2">阅读时长：{minutes} 分钟</div>
              <div class="mr-2">
                阅读量：<span class="waline-pageview-count" data-path={createdTimeStamp}></span>
              </div>
              <div class="mr-2">
                评论数：
                <span class="waline-comment-count" data-path={createdTimeStamp} />
              </div>
            </div>
          </div>
        </div>
        <section class="main-hero-waves-area waves-area">
          <svg
            class="waves-svg"
            xmlns="http://www.w3.org/2000/svg"
            xlink:href="http://www.w3.org/1999/xlink"
            viewBox="0 24 150 28"
            preserveAspectRatio="none"
            shape-rendering="auto"
          >
            <defs>
              <path
                id="gentle-wave"
                d="M-160 44c30 0 58-18 88-18s58 18 88 18 58-18 88-18 58 18 88 18v44h-352Z"
              ></path>
            </defs>
            <g class="parallax">
              <use href="#gentle-wave" x="48" y="0"></use>
              <use href="#gentle-wave" x="48" y="3"></use>
              <use href="#gentle-wave" x="48" y="5"></use>
              <use href="#gentle-wave" x="48" y="7"></use>
            </g>
          </svg>
        </section>
      </div>
    )
  }

  PageInfo.css = style
  PageInfo.afterDOMLoaded = script

  return PageInfo
}
