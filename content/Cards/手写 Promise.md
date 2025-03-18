---
date: 2024-10-21T10:53:57
updated: 2025-02-19T10:50:36
share: true
tags:
  - review
---
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
