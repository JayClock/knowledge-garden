---
date: 2025-10-13 00:16:28
updated: 2025-11-11 21:29:17
share: true
---
以协同文档为例，我们首先要考虑的是，可能影响用户正常使用的错误。

这种错误使用 `window.onerror` 捕获同步错误（比如在 ui 渲染前就调用了 ui 的实例）和 `window.onunhandledrejection` 捕获未被 catch 的异常。

比如在协同文档中，有一个自动保存的功能。用户可能因为网络异常 `reject` 或者后端返回 500 而 reject。如果没有 `catch` 并进行 ui 上的提示，