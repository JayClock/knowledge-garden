---
date: 2024-10-12T16:32:06
updated: 2024-10-12T17:46:57
share: true
---
# 盒模型宽度计算
- offsetWidth = (内容宽度 + 内边距 + 边框)，无外边距
- offsetWidth = 100 + 20 + 2 = 122
```css
#div1 {
  width: 100px;
  padding: 10px;
  border: 1px solid #ccc;
  margin: 10px;
  box-sizing: border-box; // offsetWidth 为100
}
```
# margin 纵向重叠问题
- 相邻元素的 margin-top 和 margin-bottom 会发生重叠
- 空白内容的 `<p></p>` 也会重叠
- AAA 和 BBB 之间相距 15px

```html
<!DOCTYPE html>
<html>
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <meta http-equiv="X-UA-Compatible" content="ie=edge" />
    <title>margin 纵向重叠</title>
    <style type="text/css">
      p {
        font-size: 16px;
        line-height: 1;
        margin-top: 10px;
        margin-bottom: 15px;
      }
    </style>
  </head>
  <body>
    <p>AAA</p>
    <p></p>
    <p></p>
    <p></p>
    <p>BBB</p>
  </body>
</html>
```
# margin 负值问题
- margin-top 和 margin-left 负值、元素向上、向左移动
- margin-right 负值，右侧元素左移，自身不受影响
- margin-bottom 负值，下方元素上移，自身不受影响

```html
<!DOCTYPE html>
<html>
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <meta http-equiv="X-UA-Compatible" content="ie=edge" />
    <title>margin 负值</title>
    <style type="text/css">
      body {
        margin: 20px;
      }
      .float-left {
        float: left;
      }
      .clearfix:after {
        content: '';
        display: table;
        clear: both;
      }
      .container {
        border: 1px solid #ccc;
        padding: 10px;
      }
      .container .item {
        width: 100px;
        height: 100px;
      }
      .container .border-blue {
        border: 1px solid blue;
      }
      .container .border-red {
        border: 1px solid red;
      }
    </style>
  </head>
  <body>
    <p>用于测试 margin top bottom 的负数情况</p>
    <div class="container">
      <div class="item border-blue">this is item 1</div>
      <div class="item border-red">this is item 2</div>
    </div>

    <p>用于测试 margin left right 的负数情况</p>
    <div class="container clearfix">
      <div class="item border-blue float-left">this is item 3</div>
      <div class="item border-red float-left">this is item 4</div>
    </div>
  </body>
</html>
```
