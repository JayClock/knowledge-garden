---
date: 2024-10-19T16:09:56
updated: 2024-10-19T18:40:12
share: true
---
# 基本使用
 
- 异步回调会带来 callback hell
- [[./JS-Promise|Promise]] 通过 then、catch 链式调用，一定程度上会解决了回调函数的问题
- 结束 async&await，可以把异步函数转化为同步形式，彻底消除回调函数

```js
function loadImg(src) {
    const promise = new Promise((resolve, reject) => {
        const img = document.createElement('img')
        img.onload = () => {
            resolve(img)
        }
        img.onerror = () => {
            reject(new Error(`图片加载失败 ${src}`))
        }
        img.src = src
    })
    return Promise.race([promise, timeout()])
}

function timeout() {
  return new Promise((resolve, reject) => {
    setTimeout(() => {
      reject('图片请求超时')
    }，500)
  })
}


async function loadImg1() {
    const src1 = 'http://www.imooc.com/static/img/index/logo_new.png'
    const img1 = await loadImg(src1)
    return img1
}

async function loadImg2() {
    const src2 = 'https://avatars3.githubusercontent.com/u/9583120'
    const img2 = await loadImg(src2)
    return img2
}

(async function () {
    // 注意：await 必须放在 async 函数中，否则会报错
    try {
        // 加载第一张图片
        const img1 = await loadImg1()
        console.log(img1)
        // 加载第二张图片
        const img2 = await loadImg2()
        console.log(img2)
    } catch (ex) {
        console.error(ex)
    }
})()
```
# 和  Promise 的关系

async 函数返回结果都是 [[./JS-Promise|Promise]] 对象（如果函数没返回 Promise，则自动封装一下）

```js
async function fn1() {
    return 100
}
console.log( fn1() ) // 相当于 Promise.resolve(100)
```

async 后面跟 Promise 对象：会阻断后续代码，等待状态为 resolved，才获取结果并继续执行

```js
(async function () {
    const p1 = new Promise(() => {})
    await p1
    console.log('p1') // 不会执行，一直处于 pending
})()

(async function () {
    const p2 = Promise.resolve(100)
    const res = await p2
    console.log(res) // 100
})()

(async function () {
    const res = await 100
    console.log(res) // 100
})()

(async function () {
    const p3 = Promise.reject('some err')
    const res = await p3
    console.log(res) // 不会执行
})()
```

try...catch 捕获 rejected 状态

```js
(async function () {
    const p4 = Promise.reject('some err')
    try {
        const res = await p4
        console.log(res)
    } catch (ex) {
        console.error(ex)
    }
})()
```
# 更复杂的例子

```js
async function async1 () {
  console.log('async1 start') // 2
  await async2()
  // 关键在这一步，它相当于放在 callback 中，即异步
  console.log('async1 end') 
}

async function async2 () {
  console.log('async2') // 3
}

console.log('script start') // 1
async1()
console.log('script end') // 4
```

