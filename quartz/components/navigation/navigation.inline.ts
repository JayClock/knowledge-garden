let preScroll = 0

document.addEventListener("scroll", () => {
  const menus = document.querySelector("#menus")
  const scrollY = window.scrollY
  if (scrollY > preScroll) {
    menus?.classList.add("show-title")
  } else {
    menus?.classList.remove("show-title")
  }

  if (scrollY > 0) {
    menus?.classList.add("white-bg")
  } else {
    menus?.classList.remove("white-bg")
  }
  preScroll = scrollY
})
