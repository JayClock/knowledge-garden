---
date: 2024-10-19T14:19:16
updated: 2024-10-21T10:37:48
share: true
---
# 三种状态

- pending resolved rejected
- pending -> reolved 或 pending -> rejected
- 变化不可逆

```js
// 刚定义时，状态默认为 pending
const p1 = new Promise((resolve, reject) => {})

// 执行 resolve() 后，状态变成 resolved
const p2 = new Promise((resolve, reject) => {
    setTimeout(() => {
        resolve()
    })
})

// 执行 reject() 后，状态变成 rejected
const p3 = new Promise((resolve, reject) => {
    setTimeout(() => {
        reject()
    })
})
```

# 状态表现
- pending 状态，不会触发 then 和 catch
- resolved 状态，会触发后续的 then 回调函数
- rejected 状态，会触发后续的 catch 回调函数
# then 和 catch 改变状态
- then 正常返回 resolved，里面有报错则返回 rejected
- catch 正常返回 resolved，里面有报错则返回 rejected

```js
// then() 一般正常返回 resolved 状态的 promise
Promise.resolve().then(() => {
    return 100
})

// then() 里抛出错误，会返回 rejected 状态的 promise
Promise.resolve().then(() => {
    throw new Error('err')
})

// catch() 不抛出错误，会返回 resolved 状态的 promise
Promise.reject().catch(() => {
    console.error('catch some error')
})

// catch() 抛出错误，会返回 rejected 状态的 promise
Promise.reject().catch(() => {
    console.error('catch some error')
    throw new Error('err')
})
```


```js
// 第一题
Promise.resolve().then(() => {
    console.log(1)
}).catch(() => {
    console.log(2)
}).then(() => {
    console.log(3)
})

// 1, 3

// 第二题
Promise.resolve().then(() => { // 返回 rejected 状态的 promise
    console.log(1)
    throw new Error('erro1')
}).catch(() => { // 返回 resolved 状态的 promise
    console.log(2)
}).then(() => {
    console.log(3)
})
// 1, 2, 3

// 第三题
Promise.resolve().then(() => { // 返回 rejected 状态的 promise
    console.log(1)
    throw new Error('erro1')
}).catch(() => { // 返回 resolved 状态的 promise
    console.log(2)
}).catch(() => {
    console.log(3)
})
// 1, 2
```

# 手写 Promise

```ts
import { MyPromise } from './my-promise';

describe('MyPromise', () => {
  it('should resolve with a given value', (done) => {
    const promise = new MyPromise((resolve) => {
      resolve('Hello world');
    });

    promise.then((value) => {
      expect(value).toBe('Hello world');
      done();
    });
  });

  it('should handle asynchronous resolution', (done) => {
    const promise = new MyPromise((resolve) => {
      setTimeout(() => {
        resolve('Async Hello, World!');
      }, 100);
    });

    promise.then((value) => {
      expect(value).toBe('Async Hello, World!');
      done();
    });
  });

  it('should handle rejection', (done) => {
    const promise = new MyPromise((resolve, reject) => {
      reject(new Error('Rejected'));
    });

    promise.catch((error) => {
      expect(error).toEqual(new Error('Rejected'));
      done();
    });
  });

  it('should handle async rejection', (done) => {
    const promise = new MyPromise((resolve, reject) => {
      setTimeout(() => {
        reject(new Error('Rejected'));
      }, 100);
    });

    promise.catch((error) => {
      expect(error).toEqual(new Error('Rejected'));
      done();
    });
  });

  it('should support chaining with .then', (done) => {
    const promise = new MyPromise((resolve) => {
      resolve(1);
    });

    promise
      .then((value) => value + 1)
      .then((value) => {
        expect(value).toBe(2);
        done();
      });
  });
});
```

```ts
/* eslint-disable @typescript-eslint/no-explicit-any */
export class MyPromise {
  private state: 'pending' | 'fulfilled' | 'rejected' = 'pending';
  private value = undefined; // 成功后的值
  private reason = undefined; // 失败后的原因

  private onResolveCallbacks = []; // pending 状态下，存储成功的回调
  private onRejectCallbacks = []; // pending 状态下，存储失败的回调

  constructor(
    executor: (
      resolve: (value: unknown) => void,
      reject: (reason?: any) => void
    ) => void
  ) {
    const resolve = (value: any) => {
      if (this.state === 'pending') {
        this.state = 'fulfilled';
        this.value = value;
        this.onResolveCallbacks.forEach((fn) => fn(this.value));
      }
    };

    const reject = (reason: any) => {
      if (this.state === 'pending') {
        this.state = 'rejected';
        this.reason = reason;
        this.onRejectCallbacks.forEach((fn) => fn(this.reason));
      }
    };

    try {
      executor(resolve, reject);
    } catch (error) {
      reject(error);
    }
  }

  then(onFulfilled: (value: any) => void, onRejected?: (reason: any) => void) {
    return new MyPromise((resolve, reject) => {
      if (this.state === 'fulfilled') {
        const result = onFulfilled(this.value);
        resolve(result);
      }

      if (this.state === 'pending') {
        this.onResolveCallbacks.push(onFulfilled);
        this.onRejectCallbacks.push(onRejected);
      }

      if (this.state === 'rejected') {
        const result = onRejected(this.reason);
        reject(result);
      }
    });
  }

  catch(onRejected?: (reason: any) => void) {
    this.then(null, onRejected);
  }
}

```
