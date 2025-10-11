---
date: 2025-10-11 18:29:53
updated: 2025-10-11 18:40:50
share: true
---
Babel 插件和预设都用于配置 Babel 的行为，但它们有不同的用途和方式：
- **插件（Plugins）**：插件是 Babel 的基本转换单元，负责特定的代码转换任务。例如，将箭头函数转换为普通函数的插件 `@bable/plugin-transform-arrow-functions`。
- **预设（Presets）**：预设是多个插件的集合，用于简化配置。例如，`@babel/preset-env` 预设包含了一系列插件，能够根据目标环境自动环境选择和加载所需的插件，以实现 ES6+ 到 ES5 的转换。

**使用示例**

在项目中，通常会创建一个 `.babelrc` 文件进行配置：

```json
{
	"presets":["@babel/preset-env"],
	"plugins":["@babel/plugin-transform-runtime"]
}
```

这里，`@babel/preset-env` 预设负责将现代 JavaScript 语法转换为兼容的版本，而 `@babel/plugin-transform-runtime` 插件则处理一些辅助代码的转换，避免全局污染。