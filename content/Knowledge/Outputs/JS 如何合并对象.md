---
date: 2025-05-04T21:08:26
updated: 2026-07-09 20:21:41
---
1. 使用 Object.assign() 合并对象
	```ts
	const obj1 = { a: 1, b: 2 };
	const obj2 = { c: 3, d: 4 };
	const mergedObj = Object.assign({}, obj1, obj2);
	console.log(mergedObj); // { a: 1, b: 2, c: 3, d: 4 }
	```
2. 使用拓展运算符 ... 合并对象
	```ts
	const obj1 = { a: 1, b: 2 };
	const obj2 = { c: 3, d: 4 };
	const mergedObj = { ...obj1, ...obj2 };
	console.log(mergedObj); // { a: 1, b: 2, c: 3, d: 4 }
	```
