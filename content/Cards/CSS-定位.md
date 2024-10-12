---
date: 2024-10-12T16:45:03
updated: 2024-10-12T17:05:13
share: true
---
# absolute 和 relateive 分别依据什么定位
- relative 依据自身定位
- absolute 依据最近一层的 positive / relative 定位

```html
<!DOCTYPE html>
<html>
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <meta http-equiv="X-UA-Compatible" content="ie=edge" />
    <title>absote relative 定位问题</title>
    <style type="text/css">
      body {
        margin: 20px;
      }
      .relative {
        position: relative;
        width: 400px;
        height: 200px;
        border: 1px solid #ccc;
        top: 20px;
        left: 50px;
      }
      .absolute {
        position: absolute;
        width: 200px;
        height: 100px;
        border: 1px solid blue;
        top: 20px;
        left: 50px;
      }
    </style>
  </head>
  <body>
    <p>absolute 和 relative 定位问题</p>
    <div class="relative">
      <div class="absolute">this is absolute</div>
    </div>
  </body>
</html>
```
# 居中对齐的实现方式
## 水平居中
- inline 元素：`text-align: center`
- block 元素：`margin: auto`
- absolute 元素：`left: 50% + margin-left 负值`

```html
<!DOCTYPE html>
<html>
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <meta http-equiv="X-UA-Compatible" content="ie=edge" />
    <title>水平对齐</title>
    <style type="text/css">
      .container {
        border: 1px solid #ccc;
        margin: 10px;
        padding: 10px;
      }
      .item {
        background-color: #ccc;
      }

      .container-1 {
        text-align: center;
      }

      .container-2 .item {
        width: 500px;
        margin: auto;
      }

      .container-3 {
        position: relative;
        height: 100px;
      }
      .container-3 .item {
        width: 300px;
        height: 100px;
        position: absolute;
        left: 50%;
        margin-left: -150px;
      }
    </style>
  </head>
  <body>
    <div class="container container-1">
      <span>一段文字</span>
    </div>

    <div class="container container-2">
      <div class="item">this is block item</div>
    </div>

    <div class="container container-3">
      <div class="item">this is absolute item</div>
    </div>
  </body>
</html>
```
## 垂直居中
- inline 元素：line-height 的值等于 height 值
- absolute 元素：top: 50% + margin-top 负值
- absolute 元素：`transform: translate(-50%,-50%)`
- absolute 元素：top,left,bottom,right = 0 + margin: auto

```html
<!DOCTYPE html>
<html>
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <meta http-equiv="X-UA-Compatible" content="ie=edge" />
    <title>垂直对齐</title>
    <style type="text/css">
      .container {
        border: 1px solid #ccc;
        margin: 10px;
        padding: 10px;
        height: 200px;
      }
      .item {
        background-color: #ccc;
      }

      .container-1 {
        text-align: center;
        line-height: 200px;
        height: 200px;
      }

      .container-2 {
        position: relative;
      }
      .container-2 .item {
        width: 300px;
        height: 100px;
        position: absolute;
        left: 50%;
        margin-left: -150px;
        top: 50%;
        margin-top: -50px;
      }

      .container-3 {
        position: relative;
      }
      .container-3 .item {
        width: 200px;
        height: 80px;
        position: absolute;
        left: 50%;
        top: 50%;
        transform: translate(-50%, -50%);
      }

      .container-4 {
        position: relative;
      }
      .container-4 .item {
        width: 100px;
        height: 50px;
        position: absolute;
        top: 0;
        left: 0;
        bottom: 0;
        right: 0;
        margin: auto;
      }
    </style>
  </head>
  <body>
    <div class="container container-1">
      <span>一段文字</span>
    </div>

    <div class="container container-2">
      <div class="item">this is item</div>
    </div>

    <div class="container container-3">
      <div class="item">this is item</div>
    </div>

    <div class="container container-4">
      <div class="item">this is item</div>
    </div>
  </body>
</html>
```
