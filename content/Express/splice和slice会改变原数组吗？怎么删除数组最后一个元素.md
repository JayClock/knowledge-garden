---
date: 2025-05-03T22:54:31
updated: 2025-05-03T22:54:52
share: true
---
splice() 和 slice() 是 JavaScript 数组的方法，两者作用不同。
1. splice() 方法可以在数组中添加、删除或替换元素，并返回被删除的元素，它会改变原数组。
2. slice() 方法是从原数组中返回指定开始和结束位置的元素组成的新数组，它不会改变原数组。
所以，使用 splice() 方法可能会改变原数组，而 slice() 方法则不会。
要删除数组中的最后一个元素，有几种方法：
3. 使用 pop() 方法删除并返回数组的最后一个元素，即可删除数组的最后一个元素：
```ts
const arr = [1, 2, 3, 4];
const lastElement = arr.pop(); // 返回被删除的元素 4console.log(arr); // [1, 2, 3]
```


4. 使用 splice() 方法删除数组的最后一个元素：
const arr = [1, 2, 3, 4];
arr.splice(-1, 1); // 从倒数第一个位置开始删除一个元素console.log(arr); // [1, 2, 3]

3. 使用 slice() 方法和展开运算符 (...) 创建一个新的数组，包含除了最后一个元素以外的所有元素：
const arr = [1, 2, 3, 4];
const newArr = [...arr.slice(0, -1)];
console.log(newArr); // [1, 2, 3]

需要注意的是，以上方法都会改变或创建一个新的数组，原数组不会被保留最后一个元素。如果要仅仅取得最后一个元素，可以使用下标或者数组方法 slice()：
const arr = [1, 2, 3, 4];
const lastElement = arr[arr.length - 1]; // 4const lastElement2 = arr.slice(-1)[0]; // 4

