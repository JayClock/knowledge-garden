---
date: 2024-10-25T16:37:42
updated: 2026-05-15 12:16:33
share: true
noteId: 1778807088646
---
如何实现 cloneDeep？

---

- 判断类型，正则和日期直接返回新对象
- 空或者非对象类型，直接返回原值
- 考虑循环引用，判断如果hash中含有直接返回hash中的值
- 新建一个相应的new obj.constructor加入hash
- 遍历对象递归（普通key和key是symbol情况）

```js
function deepClone(obj, hash = new WeakMap()) {
  if (obj instanceof RegExp) return new RegExp(obj)
  if (obj instanceof Date) return new Date(obj)
  if (obj === null || typeof obj !== 'object') return obj
  //循环引用的情况
  if (hash.has(obj)) {
    return hash.get(obj)
  }
  //new 一个相应的对象
  //obj为Array，相当于new Array()
  //obj为Object，相当于new Object()
  let constr = new obj.constructor()
  hash.set(obj, constr)
  for (let key in obj) {
    if (obj.hasOwnProperty(key)) {
      constr[key] = deepClone(obj[key], hash)
    }
  }
  //考虑symbol的情况
  let symbolObj = Object.getOwnPropertySymbols(obj)
  for (let i = 0; i < symbolObj.length; i++) {
    if (obj.hasOwnProperty(symbolObj[i])) {
      constr[symbolObj[i]] = deepClone(obj[symbolObj[i]], hash)
    }
  }
  return constr
}
```
