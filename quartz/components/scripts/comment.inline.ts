import { init } from "@waline/client"

document.addEventListener("nav", () => {
  const walineElement = document.getElementById("waline")
  const date = new Date(walineElement?.getAttribute("created-time")!)
  const walineInstance = init({
    el: walineElement,
    serverURL: "https://comment.jayclock-garden.top",
    comment: true,
    login: "force",
    path: date.getTime().toString(),
  })
  window.addCleanup(() => walineInstance?.destroy())
})
