---
date: 2024-10-23T09:35:47
updated: 2024-10-27T10:41:46
share: true
---
# 背景

在 React 中，只要父组件更新了，子组件不管是否发生变化都要更新。每一个组件都有一个默认  SCU 生命周期。

```js
shouldComponentUpdate(nextProps, nextState) {
  return true;
}
```
# 基本使用

在下面的代码中，我通过深度比较 list，如果两个 list `deepEqual`，则渲染组件。

```js
shouldComponentUpdate(nextProps, nextState) {
  // _.isEqual 做对象或者数组的深度比较（一次性递归到底）
  if (_.isEqual(nextProps.list, this.props.list)) {
  // 相等，则不重复渲染
    return false;
  }
  return true; // 不相等，则渲染
}
```

如果不配合[[./React setState|state不可变值]]规范去写，比如下面的代码

```js
this.state.list.push({
  id: `id-${Date.now()}`,
  title,
});
this.setState({
  list: this.state.list,
});
```

我们先对 `state.list` 进行了 push 操作，此时 list 内容已经发生了变化。而 `shouldComponentUpdate` 是 `setState` 后才会触发，这里就会导致，`isEqual` 下的 list，不论怎样都相等。正确的用法应该按照**不可变值规范**去写。

```js
// 正确的用法
this.setState({ 
  list: this.state.list.concat({
	id: `id-${Date.now()}`,
	title,
  }),
});
```