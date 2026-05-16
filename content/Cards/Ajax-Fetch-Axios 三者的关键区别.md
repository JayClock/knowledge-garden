---
date: 2024-10-12T15:57:33
updated: 2026-05-16 19:29:21
share: true
noteId: 1778930946541
---
Ajax-Fetch-Axios 三者有哪些关键区别？

---

三者都用于网络请求，但是不同纬度
- Ajax（Asynchronous Javascript and XML）一种技术统称
- Fetch 一个具体的 API
	- 浏览器原生 API，用于网络请求
	- 和 XMLHttpRequest 都是原生 API
	- 相比于 XMLHttpRequest，Fetch 语法更加简洁易用、支持 Promise
- Axios 一个第三方库
	- 由 Fetch XMLHttpRequest 去实现的 lib

重点：lib 和 api 之间的区别，平时尽量用 lib 而非 api
