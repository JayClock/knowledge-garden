---
date: 2025-05-05T22:28:45
updated: 2026-05-15 12:16:33
share: true
noteId: 1778807092271
---
React 受控组件的核心作用和使用场景是什么？

---

在 React 中，受控组件（Controlled Component） 是指表单元素（如 `<input>`、`<textarea>`、`<select>` 等）的值由 React 的状态（state）控制，而不是由 DOM 自身管理。换句话说，表单元素的值通过 value 属性绑定到 React 的状态，并通过 onChange 事件处理函数来更新状态。

这是一个简单的受控组件示例：

```tsx
function ControlledInput() {
  const [value, setValue] = useState('')

  const handleChange = (event) => {
    setValue(event.target.value) // 更新状态
  }

  return (
    <div>
      <input
        type="text"
        value={value} // 绑定状态
        onChange={handleChange} // 监听输入变化
      />
      <p>Current value: {value}</p>
    </div>
  )
}
```

受控组件的优点：

1. 完全控制表单数据：React 状态是表单数据的唯一来源，可以轻松地对数据进行验证、格式化或处理。
2. 实时响应输入：可以在用户输入时实时更新 UI 或执行其他操作（如搜索建议）。
3. 易于集成：与其他 React 状态和逻辑无缝集成。
