---
date: 2025-05-10T22:08:09
updated: 2026-05-16 19:29:22
share: true
noteId: 1778930948018
---
JS 事件委托的核心机制是什么？

---

事件委托是利用了[[./JS 事件流的核心机制是什么？|JS 事件流的核心机制是什么？]] 冒泡阶段机制，由父节点的监听函数统一处理多个子元素的事件，避免重复绑定事件，性能高，适合动态加载的场景。

比如在**无限下拉加载图片的页面，如何给每个图片绑定 click 事件？**
```html
<div id="image-container" style="height: 400px; overflow-y: scroll; border: 1px solid #ccc;">
  <!-- 加载图片 -->
</div>

<script>
  const container = document.getElementById('image-container')

  // 模拟 API 请求加载图片
  let page = 1 // 当前加载的页码
  const loadImages = () => {
    for (let i = 1; i <= 10; i++) {
      const img = document.createElement('img')
      img.src = `https://via.placeholder.com/150?text=Image+${(page - 1) * 10 + i}`
      img.style.margin = '10px'
      img.alt = `Image ${(page - 1) * 10 + i}`
      img.className = 'image-item' // 添加统一的类名
      container.appendChild(img)
    }
    page++
  }

  // 绑定父容器的 click 事件
  container.addEventListener('click', (event) => {
    if (event.target.tagName === 'IMG') {
      alert(`You clicked on ${event.target.alt}`)
    }
  })

  // 监听滚动事件，实现无限加载
  container.addEventListener('scroll', () => {
    if (container.scrollTop + container.clientHeight >= container.scrollHeight) {
      loadImages() // 加载更多图片
    }
  })

  // 初次加载图片
  loadImages()
</script>
```
