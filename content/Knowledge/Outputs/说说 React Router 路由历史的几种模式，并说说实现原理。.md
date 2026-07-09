---
date: 2025-10-09 17:33:57
updated: 2026-07-09 10:45:13
---
# 说说 React Router 路由历史的几种模式，并说说实现原理

路由的本质，是以 URL 作为状态判断，确定最终的渲染视图。React Router 所说的“路由模式”，本质上是在回答一个问题：**应用到底通过什么机制感知 URL 的变化，并把这种变化映射到界面更新上。**

 一、为什么会有“路由模式”

在传统多页应用里，点击链接会直接向服务器请求一个新页面，浏览器天然就完成了“地址变化 -> 页面切换”。

但在单页应用里，页面通常只加载一次，后续更多是前端接管视图切换。此时应用需要自己解决三件事：

1. 如何改变地址栏
2. 如何监听地址变化
3. 如何根据新地址重新匹配并渲染页面

不同的实现方式，就形成了不同的路由模式。

 二、React Router 常见的几种模式

 1. BrowserRouter

`BrowserRouter` 是最常见、也是现代 Web 应用最推荐的方案。它基于 HTML5 History API，URL 形态更自然：

```text
/posts/42
/settings/profile
```

它依赖的核心能力有：

- `history.pushState()`：向历史记录栈新增一条记录
- `history.replaceState()`：替换当前历史记录
- `popstate` 事件：用户前进、后退时触发
- `location.pathname`：读取当前路径

它的优点是：

- URL 干净，可读性强
- 更符合真实路径语义
- 更适合 SEO、SSR、分享链接等场景

它的代价是：

- 需要服务端配合，把未知路径回退到应用入口文件
- 如果服务端没有配置 rewrite，刷新深层路径时容易出现 404

 2. HashRouter

`HashRouter` 基于 URL 的 hash 部分，URL 看起来通常像这样：

```text
/#/posts/42
/#/settings/profile
```

它依赖的核心能力有：

- `location.hash`：读取 hash 内容
- `hashchange` 事件：hash 改变时触发

它的优点是：

- 不依赖服务端 rewrite
- 部署在纯静态托管或受限环境里更省心
- 刷新页面通常不会因为路径问题而 404

它的缺点是：

- URL 不如 BrowserRouter 自然
- SEO 和语义性相对较弱
- 看起来更像兼容性方案，而不是现代默认方案

 3. MemoryRouter

`MemoryRouter` 不依赖真实地址栏，而是把“历史记录”保存在内存里。它更像一个纯内存版路由器。

它适合：

- 单元测试
- Storybook
- React Native
- 非浏览器环境

它的特点是：

- 地址变化不会反映到真实浏览器 URL
- 没有可分享链接
- 更适合受控环境，而不是普通 Web 页面导航

 4. StaticRouter（补充）

严格来说，`StaticRouter` 不属于浏览器里的“历史模式”，但在 React Router 体系里也很重要。它主要用于 SSR 场景，由服务端提供当前 location，路由本身不负责监听浏览器导航。

如果把 `BrowserRouter` 理解成“浏览器驱动路由”，那么 `StaticRouter` 更接近“服务端提供路由上下文”。

 三、BrowserRouter 和 HashRouter 的本质差别

最核心的差别只有一句话：

- `BrowserRouter` 把路径放在真正的 URL path 里
- `HashRouter` 把路径放在 URL 的 hash 片段里

例如下面两个地址：

```text
BrowserRouter: https://example.com/posts/42
HashRouter:    https://example.com/#/posts/42
```

它们看起来都像“当前在 `/posts/42` 页面”，但浏览器和服务器对它们的理解完全不同：

- 对 `BrowserRouter` 而言，请求会真正指向 `/posts/42`
- 对 `HashRouter` 而言，发给服务器的其实还是 `/`，`#/posts/42` 不会被发送给服务器

这正是为什么：

- `BrowserRouter` 需要服务端配合 rewrite
- `HashRouter` 通常不需要服务端额外处理

 四、实现原理：一个路由器最少要做什么

无论是 BrowserRouter 还是 HashRouter，一个最简版前端路由器通常都要做下面几步：

1. 读取当前 URL
2. 监听 URL 变化
3. 把 URL 和路由配置做匹配
4. 找到对应组件
5. 触发重新渲染
6. 对外提供导航 API

也就是说，React Router 虽然很强大，但它最底层的思想并不复杂：**监听地址，匹配规则，渲染结果。**

 五、BrowserRouter 的实现原理

 1. 读取路径

```js
function getCurrentPath() {
  return window.location.pathname;
}
```

 2. 监听前进和后退

浏览器用户点击前进、后退按钮时，会触发 `popstate`：

```js
window.addEventListener('popstate', render);
```

 3. 主动导航时修改历史记录

```js
function navigate(to, { replace = false } = {}) {
  if (replace) {
    window.history.replaceState(null, '', to);
  } else {
    window.history.pushState(null, '', to);
  }

  render();
}
```

这里有一个很容易忽略的点：

> [!note]
> `pushState()` 和 `replaceState()` 不会自动触发 `popstate`。因此，路由器在主动导航后，通常还要自己更新内部状态或主动触发一次渲染。

 4. 根据路径匹配组件

```js
const routes = {
  '/': Home,
  '/about': About,
  '/posts': Posts,
};

function matchRoute(path) {
  return routes[path] || NotFound;
}
```

 5. 重新渲染

```js
function render() {
  const path = getCurrentPath();
  const Component = matchRoute(path);
  mount(Component);
}
```

把这些组合起来，一个非常简化的 Browser History 路由器大概就是这样：

```js
function getCurrentPath() {
  return window.location.pathname;
}

function render() {
  const path = getCurrentPath();
  const Component = matchRoute(path);
  mount(Component);
}

function navigate(to, { replace = false } = {}) {
  if (replace) {
    window.history.replaceState(null, '', to);
  } else {
    window.history.pushState(null, '', to);
  }

  render();
}

window.addEventListener('popstate', render);
window.addEventListener('load', render);
```

当然，真正的 React Router 还会处理：

- 动态路由，如 `:postId`
- 嵌套路由
- 相对路径
- 查询参数
- 错误边界
- 数据加载与提交

但底层思路并没有变化。

 六、HashRouter 的实现原理

Hash 模式比 Browser History 更“直接”，因为它本来就是围绕 `location.hash` 工作的。

 1. 读取 hash 路径

```js
function getCurrentPath() {
  return window.location.hash.slice(1) || '/';
}
```

 2. 监听 hash 变化

```js
window.addEventListener('hashchange', render);
```

 3. 主动导航

```js
function navigate(to) {
  window.location.hash = to;
}
```

当 `hash` 变化后，浏览器会自动触发 `hashchange`，于是路由器重新匹配并渲染：

```js
function render() {
  const path = getCurrentPath();
  const Component = matchRoute(path);
  mount(Component);
}

window.addEventListener('hashchange', render);
window.addEventListener('load', render);
```

和 Browser History 相比，Hash 模式的实现更简单，原因就在于：它不需要真的“改路径并欺骗服务器”，而只是借用了 URL 中不会提交给服务端的 hash 片段，作为前端自己的状态容器。

 七、为什么 BrowserRouter 刷新会 404，而 HashRouter 不会

这是面试和实际部署里都非常常见的问题。

假设当前页面地址为：

```text
https://example.com/posts/42
```

如果你使用的是 `BrowserRouter`，那么用户刷新页面时，浏览器会向服务器请求 `/posts/42`。如果服务器没有这个真实资源，也没有把它 rewrite 到 `index.html`，就会返回 404。

而如果地址是：

```text
https://example.com/#/posts/42
```

浏览器发给服务器的其实仍然只是：

```text
/
```

`#/posts/42` 是前端自己消费的状态，所以服务器不会因为深层路径而报 404。

因此：

- `BrowserRouter` 的问题不是 React Router 本身，而是部署时缺少服务端回退配置
- `HashRouter` 的优势不是功能更强，而是天然绕开了这个部署问题

 八、怎么选这几种模式

| 模式 | 地址形态 | 依赖浏览器能力 | 是否需要服务端配合 | 常见场景 |
| --- | --- | --- | --- | --- |
| `BrowserRouter` | `/posts/42` | History API | 是 | 常规 Web 应用、SSR、现代项目 |
| `HashRouter` | `/#/posts/42` | hash + `hashchange` | 否 | 静态托管、旧系统、受限部署环境 |
| `MemoryRouter` | 不显示在地址栏 | 内存状态 | 否 | 测试、Storybook、React Native |
| `StaticRouter` | 由服务端提供 | 服务端上下文 | 不适用 | SSR |

经验上可以这样理解：

- 能控制服务端时，优先选 `BrowserRouter`
- 无法配置 rewrite 时，可以退而求其次使用 `HashRouter`
- 不需要真实地址栏时，使用 `MemoryRouter`
- 服务端渲染时，使用 `StaticRouter`

 九、常见误区

 1. 以为 `pushState()` 会触发 `popstate`

不会。`popstate` 主要发生在用户前进、后退时。主动调用 `pushState()` 后，路由器要自己更新状态。

 2. 以为 HashRouter 只是“老旧”，所以完全没必要

不完全对。它确实不是现代默认方案，但在无法控制服务端、只能静态部署、或者需要快速兼容的场景里，依然很实用。

 3. 以为前端路由只是“页面切换”

实际上它还影响：

- 布局嵌套
- 参数设计
- 查询串建模
- 懒加载边界
- 数据加载时机
- 服务端部署方式

 4. 只会背概念，不理解浏览器事件

真正决定路由模式差异的，不是 React Router 的 API 名字，而是背后的浏览器能力：

- `popstate`
- `hashchange`
- `pushState`
- `replaceState`
- `location.pathname`
- `location.hash`

 十、总结

React Router 的几种模式，本质上是在回答“前端应用如何把 URL 变化转换为视图变化”。

- `BrowserRouter`：基于 History API，URL 干净，但需要服务端配合
- `HashRouter`：基于 hash，部署简单，但 URL 不够自然
- `MemoryRouter`：基于内存，适合测试和非浏览器环境
- `StaticRouter`：用于 SSR，由服务端提供 location

如果再压缩成一句话，可以这样记：

**BrowserRouter 用真实路径做状态，HashRouter 用 hash 做状态，MemoryRouter 用内存做状态，而 React Router 的工作就是把这些状态变化映射成组件树的重新渲染。**

 相关笔记

- React Router：React Router 的总览知识卡片与学习主线。
- Suspense 与渐进式加载：从路由切换进一步理解懒加载与 fallback。
- 微前端的渐进式集成：理解路由如何从页面导航扩展到应用装配。
- 渐进式集成：从浏览器渲染到框架设计的统一哲学：把路由模式放回更大的前端演进背景中理解。