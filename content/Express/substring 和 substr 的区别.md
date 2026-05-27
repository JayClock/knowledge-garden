---
date: 2025-05-03T19:13:30
updated: 2025-05-03T22:29:30
share: true
---
- substring 方法接收两个参数，起始位置和结束位置。如果没有第二个参数，则截取至字符串结束。
- substr 方法接收两个参数，起始位置和截取长度。如果没有第二个参数，则截取至字符串结束。

```ts
const str = 'hello world'
str.substring(0, 5); // "hello"
str.substring(6); // "world"
str.substr(0, 5); // "hello"
str.substr(6); // "world"
```
