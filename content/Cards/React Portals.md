---
date: 2024-10-22T10:00:50
updated: 2026-05-15 12:16:33
share: true
noteId: 1778807092476
---
React Portals 的核心作用和使用场景是什么？

---

- 组件默认会按照既定层次嵌套渲染
- 如何让组件渲染到父组件以外？
- 一些 portals 使用场景，多数处理 css 兼容性问题：
	1. 父组件 `overflow-hidden`，构造了[[./CSS BFC|CSS BFC]]
	2. 父组件 `z-index` 值太小
	3. fixed 需要放在 body 第一层级

```js
import React from "react";
import ReactDOM from "react-dom";
import "./style.css";

class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = {};
  }
  render() {
    // // 正常渲染
    // return <div className="modal">
    //     {this.props.children} {/* 类似于 vue slot */}
    // </div>

    // 使用 Portals 将model 渲染到 body 上。
    // fixed 元素要放在 body 上，有更好的浏览器兼容性。
    return ReactDOM.createPortal(
      <div className="modal">{this.props.children}</div>,
      document.body // DOM 节点
    );
  }
}
export default App;
```

```css
.modal {
  position: fixed;
  width: 300px;
  height: 100px;
  top: 100px;
  left: 50%;
  margin-left: -150px;
  background-color: #000;
  /* opacity: .2; */
  color: #fff;
  text-align: center;
}
```

