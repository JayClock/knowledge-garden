---
date: 2026-03-12 16:40:25
updated: 2026-05-15 12:17:48
share: true
aliases:
  - React-Router
noteId: 1778807092715
---
React Router 的核心作用和使用场景是什么？

---

# React Router

> [!abstract]
> React Router 的核心可以概括为一句话：把 URL 当成状态，把路由树当成 UI 结构，把导航当成状态切换。

 它是什么

React Router 是 React 生态里最重要的客户端路由库，用于根据当前 location 渲染不同的页面与布局。它不只是处理页面跳转，还负责：

- 匹配 URL 与组件
- 组织嵌套路由与布局
- 管理参数、查询串、导航状态
- 在现代写法中承担数据加载、表单提交、错误处理

 为什么重要

- 单页应用需要在不整页刷新的前提下切换视图
- URL 需要可分享、可回退、可收藏
- 页面结构往往天然是嵌套的，路由树正好映射 UI 树
- 路由常常是代码分割和渐进加载的边界

 核心心智模型

1. URL 是状态
2. 路由树是 UI 树
3. 嵌套路由对应嵌套布局
4. 导航本质是 location 变化
5. params、search、state 是从 location 派生的输入
6. 数据路由把导航和数据读取、提交放进同一套模型里

 路由模式

 BrowserRouter

- 基于 HTML5 History API
- URL 干净，例如 `/users/42`
- 需要服务端把未知路径回退到应用入口，否则刷新会出现 404

 HashRouter

- 基于 hash 变化
- URL 形如 `/#/users/42`
- 不依赖服务端重写，适合静态托管或受限环境
- 可读性和 SEO 相对较差

 MemoryRouter

- 不写入真实地址栏
- 常用于测试、Storybook、React Native 等非浏览器主路由场景

 两套常见写法

 1. 组件式路由

适合入门和简单应用，常见于 `BrowserRouter + Routes + Route`。

```tsx
import { BrowserRouter, Routes, Route } from "react-router-dom";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/posts" element={<Posts />} />
        <Route path="/posts/:postId" element={<PostDetail />} />
      </Routes>
    </BrowserRouter>
  );
}
```

 2. 数据路由

适合中大型应用，常见于 `createBrowserRouter + RouterProvider`。它把路由、数据加载、提交、错误处理放到同一处定义。

```tsx
import {
  createBrowserRouter,
  RouterProvider,
} from "react-router-dom";

const router = createBrowserRouter([
  {
    path: "/",
    element: <RootLayout />,
    children: [
      { index: true, element: <Home /> },
      {
        path: "posts",
        element: <Posts />,
        children: [
          {
            path: ":postId",
            loader: postLoader,
            element: <PostDetail />,
          },
        ],
      },
    ],
  },
]);

export default function App() {
  return <RouterProvider router={router} />;
}
```

 核心组成

| 能力 | 常用 API | 作用 |
| --- | --- | --- |
| 路由容器 | `BrowserRouter` `HashRouter` `RouterProvider` | 提供路由上下文 |
| 路由声明 | `Routes` `Route` `createBrowserRouter` | 定义路径与页面映射 |
| 布局嵌套 | `Outlet` | 在父路由中渲染子路由 |
| 声明式导航 | `Link` `NavLink` | 生成可回退、可预期的导航 |
| 命令式导航 | `useNavigate` | 在逻辑里跳转 |
| 读取位置 | `useLocation` | 获取 pathname、search、state |
| 路径参数 | `useParams` | 读取 `:id` 这类动态片段 |
| 查询参数 | `useSearchParams` | 读取和更新 URL 查询串 |
| 数据加载 | `loader` `useLoaderData` | 路由进入前读取数据 |
| 表单提交 | `action` `Form` | 路由级提交与变更 |
| 错误处理 | `errorElement` | 路由级错误边界 |

 嵌套路由与布局

React Router 最重要的设计之一，是把路由树映射为 UI 树。父路由通常负责布局，子路由负责填充内容区域，这就是 `<Outlet />` 的意义。

```tsx
import { Outlet } from "react-router-dom";

function DashboardLayout() {
  return (
    <div>
      <Sidebar />
      <main>
        <Outlet />
      </main>
    </div>
  );
}
```

常见几种子路由：

- `index` 路由：父路径的默认内容
- 动态路由：如 `:postId`
- 通配路由：如 `*`
- 布局路由：不一定自己对应页面内容，但负责包裹子树

 匹配规则里最常见的几个概念

- 静态片段：`/about`
- 动态片段：`/users/:userId`
- 查询串：`/search?keyword=react`
- 哈希：`/docs#api`
- 通配符：`/docs/*`
- 相对路径：子路由通常相对于父路由书写

一个常见例子：

```tsx
<Route path="posts" element={<PostsLayout />}>
  <Route index element={<PostList />} />
  <Route path="new" element={<NewPost />} />
  <Route path=":postId" element={<PostDetail />} />
</Route>
```

它对应的路径分别是：

- `/posts`
- `/posts/new`
- `/posts/:postId`

 导航的两种方式

 声明式导航

更适合 UI 层，推荐优先使用。

```tsx
<Link to="/posts">文章列表</Link>
<NavLink to="/settings">设置</NavLink>
```

`NavLink` 适合导航栏，因为它可以根据当前匹配状态添加激活样式。

 命令式导航

更适合提交成功、鉴权跳转、向后返回等逻辑场景。

```tsx
import { useNavigate } from "react-router-dom";

function LoginSuccess() {
  const navigate = useNavigate();

  function handleDone() {
    navigate("/dashboard");
  }

  return <button onClick={handleDone}>进入后台</button>;
}
```

常见写法：

- `navigate("/path")`
- `navigate(-1)` 返回上一页
- `navigate("/login", { replace: true })` 替换历史记录
- `navigate("/checkout", { state: { from: "cart" } })` 传递导航状态

 参数、查询串与状态

 路径参数

适合表达资源标识，例如文章详情页、用户详情页。

```tsx
import { useParams } from "react-router-dom";

function PostDetail() {
  const { postId } = useParams();
  return <div>{postId}</div>;
}
```

 查询参数

适合表达筛选、排序、分页等可分享状态。

```tsx
import { useSearchParams } from "react-router-dom";

function SearchPage() {
  const [searchParams, setSearchParams] = useSearchParams();
  const keyword = searchParams.get("keyword") ?? "";

  function setKeyword(nextKeyword: string) {
    setSearchParams({ keyword: nextKeyword });
  }

  return <div>{keyword}</div>;
}
```

 location state

适合一次性导航上下文，不适合长期可分享状态。

```tsx
navigate("/confirm", { state: { orderId: "123" } });
```

经验上：

- 可分享、可刷新后恢复的状态，优先放 URL
- 只在本次跳转中临时使用的状态，可以放 `state`

 数据路由要点

现代 React Router 的重要升级，是把数据读取和路由匹配结合起来。这样做的好处是，页面进入前就能声明依赖，减少组件内部到处写请求逻辑。

 loader

用于进入路由前加载数据。

```tsx
export async function postLoader({ params }) {
  const res = await fetch(`/api/posts/${params.postId}`);
  if (!res.ok) throw new Response("Not Found", { status: 404 });
  return res.json();
}
```

```tsx
import { useLoaderData } from "react-router-dom";

function PostDetail() {
  const post = useLoaderData();
  return <article>{post.title}</article>;
}
```

 action

用于处理路由级表单提交、创建、删除、更新。

```tsx
export async function createPostAction({ request }) {
  const formData = await request.formData();
  await fetch("/api/posts", {
    method: "POST",
    body: formData,
  });
  return redirect("/posts");
}
```

 errorElement

让错误处理跟着路由层级走，而不是让整个页面一起崩。

 React Router 与 Suspense、懒加载

React Router 经常和 `lazy`、`Suspense` 一起出现，因为路由天然就是代码分割边界。常见场景是：

- 页面组件按路由懒加载
- 次级面板、图表、评论区延迟加载
- 在导航后先展示骨架屏，再逐步展示内容

这部分可以结合 [[./Suspense 与渐进式加载|Suspense 与渐进式加载]] 一起理解。一个简单例子：

```tsx
import { lazy, Suspense } from "react";

const SettingsPage = lazy(() => import("./SettingsPage"));

function AppRoutes() {
  return (
    <Suspense fallback={<div>加载中...</div>}>
      <SettingsPage />
    </Suspense>
  );
}
```

 React Router 与架构设计

当应用变大后，React Router 会自然延伸到更高一层的架构问题：

- 哪个页面需要首屏直出
- 哪个页面适合懒加载
- 哪个区域应该做嵌套布局
- 哪个子系统应该以路由为边界拆分
- 微前端之间如何基于路由装配
- 浏览器地址、服务端重写、SSR、缓存策略如何协同

因此，React Router 并不只是组件库层面的工具，它还会影响：

- 应用的信息架构
- 页面间跳转体验
- 代码分割策略
- 数据获取方式
- 资源加载优先级

延伸阅读：

- [[./微前端的渐进式集成|微前端的渐进式集成]]
- [[../Express/渐进式集成：从浏览器渲染到框架设计的统一哲学|渐进式集成：从浏览器渲染到框架设计的统一哲学]]

 最小实践建议

如果是新项目，可以按下面的顺序建立心智模型：

1. 先会写 `BrowserRouter`、`Routes`、`Route`
2. 再掌握 `<Outlet />`、嵌套路由、`index` 路由
3. 再掌握 `Link`、`NavLink`、`useNavigate`
4. 再掌握 `useParams`、`useSearchParams`
5. 再理解 `loader`、`action`、`errorElement`
6. 最后把路由放进懒加载、SSR、微前端这些更大的问题里看

 常见坑

> [!warning]
> 下面这些问题，几乎是 React Router 初学和落地时最常见的坑。

- `BrowserRouter` 部署后刷新 404：服务端没有把未知路径回退到入口 HTML
- 父路由写了 `children`，但父组件里忘了放 `<Outlet />`
- 把筛选条件、分页、排序放在组件本地 state，结果无法分享链接
- 嵌套路由和 UI 结构不一致，导致路由表越来越难维护
- 过度使用命令式导航，本来可以用 `Link` 的地方写成了事件逻辑
- 把数据请求全塞进组件 `useEffect`，导致进入页面后再瀑布式加载

 学习路线

这篇知识卡片可以和下面几篇一起看：

1. [[说说 React Router 路由历史的几种模式，并说说实现原理。|说说 React Router 路由历史的几种模式，并说说实现原理。]]
2. [[./Suspense 与渐进式加载|Suspense 与渐进式加载]]
3. [[./微前端的渐进式集成|微前端的渐进式集成]]
4. [[../Express/渐进式集成：从浏览器渲染到框架设计的统一哲学|渐进式集成：从浏览器渲染到框架设计的统一哲学]]

 一句话总结

React Router 的核心学习路径是：先理解 URL 如何映射视图，再理解路由如何组织布局与加载，最后理解路由如何成为应用拆分和架构演进的入口。

 相关笔记

- [[说说 React Router 路由历史的几种模式，并说说实现原理。|React Router 的几种路由模式]]：从 history 模式理解路由基础。
- [[./Suspense 与渐进式加载|Suspense 与渐进式加载]]：从路由级懒加载理解渐进式渲染。
- [[./微前端的渐进式集成|微前端的渐进式集成]]：理解路由如何成为模块装配与预加载入口。
- [[../Express/渐进式集成：从浏览器渲染到框架设计的统一哲学|渐进式集成：从浏览器渲染到框架设计的统一哲学]]：从 SPA、SSR 与渐进增强角度看 React Router 的架构位置。

## 拆分卡片

- [[../Cards/React Router 把 URL 当成应用状态|React Router 把 URL 当成应用状态]]
- [[../Cards/React Router 的路由树对应 UI 布局树|React Router 的路由树对应 UI 布局树]]
- [[../Cards/React Router 数据路由把导航和数据读写放进同一模型|React Router 数据路由把导航和数据读写放进同一模型]]
- [[../Cards/React Router 中路径参数查询参数和导航状态用途不同|React Router 中路径参数查询参数和导航状态用途不同]]
