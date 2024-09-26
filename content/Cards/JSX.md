---
date: 2024-09-24T17:02:14
updated: 2024-09-24T18:09:31
share: true
source: https://facebook.github.io/jsx/
---
- JSX 就是 React?
	- 不是。JSX 只是 React 其中一个 API，`createElement` 函数的语法糖 
- JSX 就是 React 组件？
	- 不是。JSX 是 React 组件渲染方法返回值的一部分，React 组件还有其他的功能
- JSX 就是另一种 HTML?
	- 不是。JSX 本质还是 JS，只是在最终渲染时才创建修改 DOM
- JSX 既能声明视图，又能混入 JS 表达式，那是不是可以把所有逻辑都写在 JSX 里？
	- 可以是可以，但毕竟不能在 JSX 里使用命令式语句，能做的事情很有限。
# 命名规则
1. 自定义组件名称需要大写字母开头
```tsx
function MyApp() {
//_______^
  return (<div></div>);
}
const KanbanCard = () => (
//____^
  <div></div>
);
```
2. props 属性名称使用驼峰命名（camelCase），区分大小写
```tsx 
<FileCard filename="文件名" fileName="另一个文件名" />
```
以上代码中，两个 filename 和 fileName 时不同的文件名
# JSX 组件为什么要包裹在括号里
为了避免陷入 JS 自动加分号的陷阱；例如源代码

```tsx
function Component() {
  return 
    <div>{/*假设这行JSX语句很长，为了提升一些代码可读性才特地换行*/}</div>;
}
```
会编译成

```tsx
function Component() {
  return;
  React.createElement("div", null);
}
```
在这种场景下， 根本不会执行到 `React.createElement("div", null);`语句。加上括号以后

```tsx
function Component() {
  return (
    <div>{/*假设这行JSX语句很长，为了提升一些代码可读性，特地换行*/}</div>
  );
}
```
重新编译：

```tsx
function Component() {
  return React.createElement("div", null);
}
```
