---
date: 2025-10-11 18:09:59
updated: 2025-10-11 18:29:31
share: true
---
Babel 是一个 JavaScript 编译器，主要用于现代 JavaScript 代码（包括 ES6 及更高版本的语法）转换为向后兼容的 JavaScript 代码，以确保在旧版本浏览器或环境中也能运行。

1. **词法转换**：将现代 JavaScript 语法（如箭头函数、类、模板字符串等）转换为 ES5 兼容的语法。
2. **Polyfills**：通过使用工具如 `@babel/ployfill`，可以为缺失的 JavaScript 功能（如 `Promise`、`Array.includes` 等）添加兼容性支持。
3. **插件化机制**：Babel 使用插件来拓展功能，可以根据项目需求加载不同的插件。
4. **代码优化和压缩**：Babel 虽然主要用于转换不同的语法，Babel 也可以与其他工具（如 Terser）集成，以优化和压缩代码。