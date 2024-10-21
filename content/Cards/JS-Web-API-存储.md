---
date: 2024-10-16T09:55:21
updated: 2024-10-16T09:55:37
share: true
---
# cookie

## 定义

- 本身用于浏览器和 server 通讯
- 被“借用”到本地存储来
- 可用 document.cookie = '...' 来修改
## 缺点

- 存储大小，最大 4KB
- http 请求时需要发送到服务端，增加请求量
- 只能用 document.cookie 来修改，太过简陋
# localStorage 和 sessionStorage

- [[./HTML|HTML]]5 专门为存储而设计，最大可存5M
- API 简单易用 setItem getItem
- 不会随着 http 请求被发出去
- localStorage 数据会永久存储，除非代码手动删除
- sessionStorage 数据只存在于当前会话，浏览器关闭则清空
- 一般 localStorage 会更多一些