---
date: 2024-09-24T16:45:14
updated: 2024-10-12T10:53:27
share: true
---
# 生命周期

> 组件生命周期并不等同于类组件的生命周期方法。组件生命周期时一组抽象概念，类组件生命周期方法和 Hooks API 时这组概念的对外接口。

## 组件生命周期

```tsx
class LegacyKanbanCard extends React.Component {
  constructor(props) {
    super(props);
    // ...省略
  }

  componentDidMount() {
    // ...省略
  }

  // ...其他生命周期方法

  componentWillUnmount() {
    // ...省略
  }

  render() {
    return (<div>KanbanCard {this.props.title}</div>);
  }
}
```










