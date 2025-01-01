---
date: 2024-10-23T09:24:20
updated: 2024-12-31T18:14:20
share: true
tags:
  - review
---
```js
import React from 'react'

const ContextDemo = React.lazy(() => import('./ContextDemo'))

class App extends React.Component {
    constructor(props) {
        super(props)
    }
    render() {
        return <div>
            <p>引入一个动态组件</p>
            <hr />
            <React.Suspense fallback={<div>Loading...</div>}>
                <ContextDemo/>
            </React.Suspense>
        </div>

        // 1. 强制刷新，可看到 Loading...（看不到就限制一下 chrome 网速）
        // 2. 看 network 的 js 加载
    }
}

export default App
```
