---
date: 2025-05-03T22:40:35
updated: 2025-05-03T22:46:30
share: true
---
- for...in 循环用于遍历对象的可枚举属性，它会将对象的每个 key 作为迭代变量来遍历，比如：
	```ts
	const obj = { a: 1, b: 2, c: 3 };
	for (const key in obj) {
	 console.log(key, obj[key]);
	 // a 1
	 // b 2
	 // c 3
	}
	```
- for...of 循环用于遍历可迭代对象的元素，它会将每个元素作为迭代变量来遍历，比如：
	```ts
	const arr = [1, 2, 3];
	for (const item of arr) {
	 console.log(item);
	 // 1
	 // 2
	 // 3
	}
	```
