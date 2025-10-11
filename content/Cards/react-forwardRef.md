---
date: 2025-10-09 10:03:29
updated: 2025-10-09 10:07:06
share: true
---
允许父组件访问子组件的 DOM 节点或者组件实例。常用于封装第三方 ui 库组件或实现高阶组件。

```tsx
interface InputProps {
	value?: string;
}

const Input = forwardRef<HTMLInputElement, InputProps>((props, ref) => {
  return <input ref={ref} />;
});
```

在 react 19 以后，直接在 props 中使用即可

```tsx
interface InputProps {
  value?: string;
  ref?: Ref<HTMLInputElement>;
}
const Input: React.FC<InputProps> = ({ ref }) => {
  return (
    <div>
      <input ref={ref} />
    </div>
  );
};
```
