---
date: 2025-05-03T10:02:39
updated: 2026-05-15 09:35:34
share: true
noteId: 1778807091820
---
JS Symbol 的核心机制是什么？

---

- 背景/作用：在 JS 中，创建唯一一个标识符，用于对象属性名的命名，常量的定义等场景。
- 例子：

```ts
const s1 = Symbol();
const s2 = Symbol();
const obj = {
 [s1]: 'hello',
 [s2]: 'world'
};
console.log(obj[s1]); // "hello"console.log(obj[s2]); // "world"
```
- 注意点：Symbol 不会出现在 for...in、for...of、Object.keys()、Object.getOwnPropertyName
