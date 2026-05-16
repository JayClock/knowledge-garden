---
date: 2025-05-14T11:02:16
updated: 2026-05-16 19:29:21
share: true
noteId: 1778930947241
---
FCP 衡量什么，如何优化？

---

![FCP Values](https://knowledge-garden.oss-cn-shanghai.aliyuncs.com/images/FCP%20Values.svg)
- **概念**：[首次内容绘制 (FCP)](https://web.dev/articles/fcp) 衡量的是从页面加载到页面的一部分内容呈现在屏幕上的时间。通俗来说，这个指标显示了用户从输入链接到看到第一个画面的时间。首次内容绘制可以有效降低跳出率
- **计算公式**：FCP ≈ [[./TTFB 的衡量与优化|TTFB 的衡量与优化]] + ResourceDownloadTime + HandleDomTime + RenderTime
- **优化策略**：
	- 避免 JavaScript 阻塞 HTML 的解析
 - 尽量将 JavaScript 文件放在body的最后
 - 使用 defer 或者 async 属性，延迟加载 script 脚本
 - 使用 npm 引入而不是 script 引入
	- 移除未使用的 CSS 和 JavaScript 代码
	- 避免网络负载庞大
 - 图片格式使用 WebP 等格式，而非 JPEG 或 PNG 格式
 - 对视频等媒体类文件，改为延迟加载，通过占位符等方式预留播放位置。
	- 采用高效的[[./浏览器缓存的整体流程是什么？|缓存]]策略来提供静态资源
	- 最大限度地缩短关键请求资源深度
	- 尽量减少请求数量，减少传输大小
	- 确保文本在网页字体加载期间保持可见状态
