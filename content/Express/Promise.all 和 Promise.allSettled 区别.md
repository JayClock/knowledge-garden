---
date: 2025-05-03T17:49:24
updated: 2025-05-03T19:13:25
share: true
---
- 总览：Promise.all 在需要所有 Promise 都成功的情况下使用，而 Promise.allSettled 则适用于知道每个 Promise 的执行结果的情况下使用。  
- Promise.all 方法返回的 Promise 对象咋所有的 Promise 对象都 resolve 之后，才会 resolve 并返回有所有 Promise 返回值组成的数组。如果其中有一个 Promise 被 reject，则会立即 reject 并返回相应的错误信息。
- Promise.allSettled 方法返回的 Promise 对象在所有的 Promise 对象都 resolve 或 reject 之后，才会 resolve 并返回一个由所有 Promise 状态对象组成的数组，每个状态对象包含一个 status 表示 resolve 或 reject，和一个 value 或者 reason 字段表示 Promise 的返回值或错误信息。