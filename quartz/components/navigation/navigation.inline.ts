document.addEventListener("scroll", () => {
  const nav = document.querySelector("#nav")
  if (window.scrollY > 0) {
    nav?.classList.add("fixed")
  } else {
    nav?.classList.remove("fixed")
  }
})
