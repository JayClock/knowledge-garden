---
date: 2024-10-21T11:41:29
updated: 2026-05-16 19:29:22
share: true
noteId: 1778930948589
---
如何实现 lodash.isEqual？

---

```js
// 判断是否是对象或数组
function isObject(obj) {
  return typeof obj === 'object' && obj != null
}
// 全相等（深度）
function isEqual(obj1, obj2) {
  if (!isObject(obj1) || !isObject(obj2)) {
    return obj1 === obj2
  }
  if (obj1 === obj2) {
    return true
  }
  // 两个都是对象或数组，而且不相等
  // 1. 先取出 obj1 和 obj2 的 keys ，比较个数
  const obj1Keys = Object.keys(obj1)
  const obj2Keys = Object.keys(obj2)
  if (obj1Keys.length !== obj2Keys.length) {
    return false
  }
  for (let key in obj1Keys) {
    const res = isEqual(obj1[key], obj2[key])
    if (!res) return false
  }
  return true
}
```
