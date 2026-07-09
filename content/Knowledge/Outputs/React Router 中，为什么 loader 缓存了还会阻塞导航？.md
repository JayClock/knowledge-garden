---
date: 2026-03-28 16:10:00
updated: 2026-07-09 10:45:13
---
# React Router 中，为什么 loader 缓存了还会阻塞导航？

关联主题：React-Router

 结论
缓存了 rootState，并不代表导航不会阻塞。

真正决定导航是否要等待的，不是有没有命中缓存，而是登录校验逻辑仍然放在 route loader 里。只要它还是 data router 的 async loader，React Router 就会先等待它 resolve，再提交导航。

 在 Team AI 里的表现
当前 Web 端使用 React Router data router。排查时可以观察到：

1. 点击路由链接后，地址栏不会立刻变化。
2. 只有等到受保护路由上的登录校验完成，导航才真正提交。
3. 因此会表现成 Outlet 里的 loading 结束后，浏览器地址才变化。

 根因
父级受保护路由使用了 protectedRouteLoader 做登录校验，内部会调用 getRootResource().get()。

即使 get 返回的是缓存命中的 Promise，它对 React Router 来说依然是一个需要等待的 loader Promise。缓存只能减少网络请求，不能消除 route loader 对导航提交流程的阻塞。

 为什么缓存不能解决这个问题
需要区分两个维度：

- 缓存：决定要不要发新的网络请求。
- loader：决定导航是不是要先等待。

也就是说：

- 命中缓存，可以让数据更快 resolve。
- 但只要校验逻辑还在 loader 里，React Router 还是会在提交导航前等它完成。

所以它只是变快了，不是变成非阻塞了。

 更好的实现方式
 1. 用 ProtectedRoute 组件替代 protectedRouteLoader
- 让受保护路由改成 ProtectedRoute 包裹 route element。
- 组件内部读取并缓存 auth state。
- 首次进入受保护区域时显示 loading。
- 未登录时重定向到 login 或 signup，并保留 return_to。
- 后续子路由切换时不再阻塞地址栏变化。

 2. 让 401 middleware 做兜底
对于会话过期这种情况，不需要每次路由切换都预检。

更合理的做法是：页面先正常导航，真正发业务请求时如果返回 401，再由统一 auth middleware 跳登录页。

 与 layout 的关系
 主内容
主内容区可以允许 loading，因为它本来就是当前路由的主体内容。

 Sidebar
Sidebar 不适合每次导航都骨架屏。更合理的是首次骨架，后续保留旧数据，等新数据回来再替换。

 Breadcrumb
Breadcrumb 属于导航框架信息。可以先用 pathname fallback，再渐进增强为服务端 breadcrumb，不应完全等主内容加载结束后才出现。

 一句话总结
缓存解决的是请求成本，loader 决定的是导航时机。

只要登录校验还放在 route loader 里，命中缓存也只是更快，并不会让导航变成真正的非阻塞。