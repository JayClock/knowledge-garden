---
date: 2024-10-12T18:02:01
updated: 2024-10-16T09:52:48
share: true
---
# 核心 API - XMLHttpRequest

| xhr.readyState | 描述                                                                 |
|----------------|----------------------------------------------------------------------|
| 0              | (未初始化) 还没有调用 `send()` 方法                                  |
| 1              | (载入) 已调用 `send()` 方法，正在发送请求                            |
| 2              | (载入完成) `send()` 方法执行完成，已经接收到全部的响应内容          |
| 3              | (交互) 正在解析响应内容                                              |
| 4              | (完成) 响应内容解析完成，可以在客户端调用                            |

| xhr.status | 描述                          |
| ---------- | --------------------------- |
| 2xx        | 表示成功处理请求，如 200              |
| 3xx        | 需要重定向，浏览器直接跳转，如 301 302 304 |
| 4xx        | 客户端错误请求，如 404 403           |
| 5xx        | 服务端错误                       |

```js
// GET请求
const xhr = new XMLHttpRequest()
xhr.open('GET', '/data/test.json', true)
xhr.onreadystatechange = function () {
  if (xhr.readyState === 4) {
    if (xhr.status === 200) {
      // console.log(
      //     JSON.parse(xhr.responseText)
      // )
      alert(xhr.responseText)
    } else if (xhr.status === 404) {
      console.log('404 not found')
    }
  }
}
xhr.send(null)
```
# 同源策略

- ajax 请求时，浏览器要求当前网页和 server 必须同源（安全）
- 同源：协议、域名、端口，三者必须一致

## 加载图片 css js 可无视同源策略

- `<img src=跨域的图片地址 />`
- `<link href=跨域的css地址 />`
- `<script src=跨域的js地址 />`
- `<img />` 可用于统计打点，可使用第三方统计服务
- `<link><script>` 可使用 CDN，CDN一般都是外域
- `<script>` 可实现 JSONP

## JSONP

- `<script>` 可绕过跨域限制
- 服务端可以任意动态拼接数据返回，只要符合 html 格式要求
- `<script>` 可以获得跨域的数据，只要服务端愿意返回

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <meta http-equiv="X-UA-Compatible" content="ie=edge" />
    <title>jsonp 演示</title>
  </head>
  <body>
    <p>一段文字 1</p>

    <script>
      window.abc = function (data) {
        console.log(data)
      }
    </script>
    <script src="http://localhost:8002/jsonp.js?username=xxx&callback=abc"></script>
  </body>
</html>
```

```js
const generateUrl = () => {
    let dataSrc = ''
    for (let key in params) {
      if (params.hasOwnProperty(key)) {
        dataSrc += `${key}=${params[key]}&`
      }
    }
    dataSrc += `callback=${callbackName}`
    return `${url}?${dataSrc}`
  }
  const scriptEl = document.createElement('script')
  scriptEl.src = generateUrl()
  return new Promise((resolve, reject) => {
    document.body.appendChild(scriptEl)
    window[callbackName] = (res) => {
      delete window[callbackName]
      document.body.removeChild(scriptEl)
      if (res) {
        resolve(res)
      } else {
        reject('没有数据')
      }
    }
  })
}
```

