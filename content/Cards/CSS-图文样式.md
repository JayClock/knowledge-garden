---
date: 2024-10-12T17:08:49
updated: 2024-10-12T17:47:10
share: true
---
# 支持小于 12px 的文字
## zoom
- `zoom: 50%`，表示缩小到原来的一半
- `zoom: 0.5`，表示缩小到原来的一半
- 需要考虑[兼容性](https://developer.mozilla.org/en-US/docs/Web/CSS/zoom)
- 缩放会改变元素占据的空间大小，触发重排

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta http-equiv="X-UA-Compatible" content="IE=edge" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Document</title>
    <style>
      .span1 {
        font-size: 20px;
        zoom: 0.5;
      }
      .span2 {
        font-size: 12px;
      }
    </style>
  </head>
  <body>
    <span class="span1">测试10px</span>
    <span class="span2">测试12px</span>
  </body>
</html>
```
## transform: scale()
- 只对可以定义宽高的元素有效
- 缩放不会改变元素占据的空间大小，页面布局不会发生变化

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta http-equiv="X-UA-Compatible" content="IE=edge" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Document</title>
    <style>
      .span1 {
        font-size: 20px;
        display: inline-block;
        transform: scale(0.5);
      }
      .span2 {
        font-size: 12px;
      }
    </style>
  </head>
  <body>
    <span class="span1">测试10px</span>
    <span class="span2">测试12px</span>
  </body>
</html>
```
# line-height 继承规则
- 写具体数值，如 `line-height: 30px`，则继承该值
- 写比例：如 `line-height: 2/15`，则继承该比例
- 写百分比：如 `line-height: 200%`，则继承计算出来的值

```html
<!DOCTYPE html>
<html>
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <meta http-equiv="X-UA-Compatible" content="ie=edge" />
    <title>line-height 继承问题</title>
    <style type="text/css">
      body {
        font-size: 20px;
        line-height: 200%;
      }

      p {
        /* 行高为40px */
        background-color: #ccc;
        font-size: 16px;
      }
    </style>
  </head>
  <body>
    <p>这是一行文字</p>
  </body>
</html>
```