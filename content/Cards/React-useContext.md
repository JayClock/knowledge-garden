---
date: 2025-04-17T16:36:54
updated: 2025-09-30 23:03:50
up:
  - "[[React Hooks|React Hooks]]"
related:
  - "[[React-Redux|redux]]"
share: true
---
- 背景：props 属性只能在 react 父子组件进行状态的传递，需要一种跨层次，或者同层组件之间需要进行数据的共享。除了 [[React-Redux|redux]] 外，可以选择使用 useContext。
- 机制详情：context 让所有在某个组件开始的组件树上创建一个 Context。那么这个组件树上所有的组件，就都能访问和修改这个 Context 了。
```tsx
const themes = {
  light: {
    foreground: "#000000",
    background: "#eeeeee"
  },
  dark: {
    foreground: "#ffffff",
    background: "#222222"
  }
};
// 创建一个 Theme 的 Context

const ThemeContext = React.createContext(themes.light);
function App() {
  // 使用 state 来保存 theme 从而可以动态修改
  const [theme, setTheme] = useState("light");

  // 切换 theme 的回调函数
  const toggleTheme = useCallback(() => {
    setTheme((theme) => (theme === "light" ? "dark" : "light"));
  }, []);

  const theme = useContext(ThemeContext)

  return (
    // 使用 theme state 作为当前 Context
    <ThemeContext.Provider value={themes[theme]}>
      <button onClick={toggleTheme}>Toggle Theme</button>
      <Toolbar />
    </ThemeContext.Provider>
  );
}

// 在 Toolbar 组件中使用一个会使用 Theme 的 Button
function Toolbar(props) {
  return (
    <div>
      <ThemedButton />
    </div>
  );
}

// 在 Theme Button 中使用 useContext 来获取当前的主题
function ThemedButton() {
  const theme = useContext(ThemeContext);
  return (
    <button style={{
      background: theme.background,
      color: theme.foreground
    }}>
      I am styled by theme context!
    </button>
  );
}
```
