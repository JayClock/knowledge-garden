import { init } from "@waline/client"

document.addEventListener("nav", () => {
  const walineElement = document.getElementById("waline")
  const dataPath = walineElement?.getAttribute("data-path")!
  const walineInstance = init({
    el: walineElement,
    serverURL: "https://comment.jayclock-garden.top",
    comment: true,
    pageview: true,
    login: "force",
    path: dataPath,
    copyright: false,
  })
  window.addCleanup(() => walineInstance?.destroy())
})
