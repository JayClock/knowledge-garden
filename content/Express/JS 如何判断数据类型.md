---
date: 2025-05-03T22:47:17
updated: 2026-05-15 10:03:23
share: true
---
1. 使用 typeof 操作符，除了 null 以外均可处理；

| **类型** | **返回值** | **备注** |
| --------------------- | ------------- | ------------------------------------ |
| **Undefined** | `"undefined"` | 当变量未被定义或未赋值时，返回此值。 |
| **Null** | `"object"` | 历史遗留问题，`null` 被错误地识别为对象。 |
| **Boolean** | `"boolean"` | 适用于 `true` 或 `false` 值。 |
| **Number** | `"number"` | 适用于整数和浮点数（包括特殊值 `NaN` 和 `Infinity`）。 |
| **String** | `"string"` | 适用于字符串（例如 `"hello"`）。 |
| **BigInt** | `"bigint"` | 适用于任意大的整数（例如 `10n`）。 |
| **Symbol** | `"symbol"` | 适用于 `Symbol` 类型。 |
| **Function（classes）** | `"function"` | 适用于可调用的对象（如函数和类定义）。 |
| **其他对象** | `"object"` | 包括数组、普通对象、日期对象、正则表达式等非函数对象。 |

2. 使用 instanceof 操作符
3. 使用 Object.prototype.toString 方法
	```ts
	Object.prototype.toString.call(undefined); // "[object Undefined]"
	Object.prototype.toString.call(null); // "[object Null]"
	Object.prototype.toString.call(true); // "[object Boolean]"
	Object.prototype.toString.call(123); // "[object Number]"
	Object.prototype.toString.call("abc"); // "[object String]"
	Object.prototype.toString.call(Symbol("foo")); // "[object Symbol]"
	Object.prototype.toString.call({}); // "[object Object]"
	Object.prototype.toString.call(function () {}); // "[object Function]"
	Object.prototype.toString.call([]); // "[object Array]"
	Object.prototype.toString.call(new Date()); // "[object Date]"
	Object.prototype.toString.call(/abc/); // "[object RegExp]"
	```
