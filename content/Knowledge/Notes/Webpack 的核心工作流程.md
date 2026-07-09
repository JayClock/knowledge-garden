---
date: 2026-06-02 14:41:07
noteId: 1780397909204
updated: 2026-07-09 20:21:41
---
Webpack 的核心工作流程是怎样的？Loader 和 Plugin 的区别是什么

---
Webpack 主要流程取决于一个或者多个 entry 入口文件。Webpack 基于代码中的 import 和 require 构建出所有模块的依赖图。

在构建过程中，Loader 主要承担翻译官的角色。Webpack 本身只能理解 JS 和 JSON 文件。当遇到如 `scss` `tsx` `png` 等非 js 文件类型，loader 的职责就是就是将文件转换成 Webpack 能理解和处理的有效模块。比如 `babel-loader` 将 es6 往上的模块转化为es5，`css-loader` 用于解析 css 文件。

在所有模块被 Loader 翻译后。Plugin 则是负责在打包的各个过程中，在特定时刻对打包结果进行优化。比如 `htmlwebpackplugin`是在打包结束后自动生成一个 html 文件。`terserwebpackplugin` 则负责在最终输出前对代码进行压缩。