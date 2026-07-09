---
date: 2025-11-01 17:19:35
noteId: 1778807091278
updated: 2026-07-09 11:00:29
---
JavaScript 事件循环与渲染阻塞的关键机制是什么？

---

 核心概念

JavaScript 的事件循环（Event Loop）是浏览器运行时环境的核心调度机制，它决定了代码的执行顺序、异步任务的处理时机，以及**最关键**的——何时进行页面渲染。

 事件循环的基本模型

```javascript
// 简化的事件循环伪代码
while (true) {
  // 1. 执行一个宏任务
  const macroTask = macroTaskQueue.dequeue();
  if (macroTask) {
    macroTask.execute();
  }
  
  // 2. 执行所有微任务
  while (!microTaskQueue.isEmpty()) {
    const microTask = microTaskQueue.dequeue();
    microTask.execute();
  }
  
  // 3. 检查是否需要渲染
  if (shouldRender()) {
    // 4. 执行渲染相关任务
    executeAnimationFrames(); // requestAnimationFrame 回调
    render();                 // 样式计算、布局、绘制
  }
}
```

 任务队列的优先级

 执行顺序演示

```javascript
console.log('脚本开始'); // 同步任务 - 第一执行

// 微任务 - 第三执行（在同一个宏任务结束后立即执行）
Promise.resolve().then(() => {
  console.log('Promise 微任务');
});

// 宏任务 - 第四执行（下一个事件循环）
setTimeout(() => {
  console.log('setTimeout 宏任务');
}, 0);

// 同步任务 - 第二执行
console.log('脚本结束');

// 输出顺序：
// 脚本开始
// 脚本结束  
// Promise 微任务
// setTimeout 宏任务
```

 完整的队列类型示例

```javascript
console.log('Start');

// 宏任务
setTimeout(() => console.log('Timeout'), 0);
setInterval(() => console.log('Interval'), 1000);

// 微任务
Promise.resolve().then(() => console.log('Promise'));

// 动画帧回调（在渲染前执行）
requestAnimationFrame(() => console.log('rAF'));

// 渲染后的回调
requestIdleCallback(() => console.log('Idle Callback'));

console.log('End');
```

 渲染阻塞的根本原因

 问题：长时间同步任务阻塞渲染

```javascript
function blockingOperation() {
  console.log('开始阻塞操作');
  const start = Date.now();
  
  // 模拟 2 秒的密集计算
  while (Date.now() - start < 2000) {
    // 空循环阻塞主线程
  }
  
  console.log('阻塞操作结束');
}

// 测试渲染阻塞
document.getElementById('calculate').addEventListener('click', () => {
  // 在阻塞期间：
  // - 页面无法响应点击事件
  // - 动画卡顿
  // - 输入无响应
  blockingOperation();
});

// 验证渲染被阻塞
let animationProgress = 0;
function updateAnimation() {
  animationProgress = (animationProgress + 1) % 100;
  document.getElementById('progress').style.width = animationProgress + '%';
  requestAnimationFrame(updateAnimation);
}
updateAnimation();

// 当 blockingOperation 执行时，动画会完全停止
```

 渲染时机的可视化理解

```
[宏任务开始]
  ↓
执行 JavaScript 代码
  ↓
[检查微任务队列] → 执行所有微任务
  ↓
[检查是否需要渲染] → 是 → 执行渲染管线
  ↓
[下一个宏任务]
```

**关键点**：渲染发生在宏任务之间。如果一个宏任务执行时间过长，就会延迟渲染。

 实际应用中的渲染阻塞场景

 场景 1：大数据列表处理

```javascript
// ❌ 错误方式：同步处理大数据，阻塞渲染
function processLargeDataSync(data) {
  const results = [];
  for (let i = 0; i < data.length; i++) {
    // 复杂的计算
    const result = expensiveCalculation(data[i]);
    results.push(result);
    
    // 如果 data 有 10,000 条，用户会看到页面卡死 2-3 秒
  }
  return results;
}

// ✅ 正确方式：使用时间分片，避免阻塞
async function processLargeDataAsync(data) {
  const results = [];
  const chunkSize = 100; // 每次处理 100 条
  
  for (let i = 0; i < data.length; i += chunkSize) {
    const chunk = data.slice(i, i + chunkSize);
    
    // 使用 setTimeout 或 requestIdleCallback 让出主线程
    await new Promise(resolve => {
      setTimeout(() => {
        for (const item of chunk) {
          results.push(expensiveCalculation(item));
        }
        resolve();
      }, 0);
    });
    
    // 更新进度条，让用户看到进度
    updateProgress((i / data.length) * 100);
  }
  return results;
}
```

 场景 2：DOM 批量操作

```javascript
// ❌ 错误方式：频繁操作 DOM，导致多次重排重绘
function addManyItemsBad(container, count) {
  for (let i = 0; i < count; i++) {
    const element = document.createElement('div');
    element.textContent = `Item ${i}`;
    container.appendChild(element); // 每次都会触发重排
  }
}

// ✅ 正确方式：使用 DocumentFragment 批量操作
function addManyItemsGood(container, count) {
  const fragment = document.createDocumentFragment();
  
  for (let i = 0; i < count; i++) {
    const element = document.createElement('div');
    element.textContent = `Item ${i}`;
    fragment.appendChild(element);
  }
  
  container.appendChild(fragment); // 只触发一次重排
}
```

 性能监控与调试

 检测长任务

```javascript
// 使用 PerformanceObserver 监控长任务
const observer = new PerformanceObserver((list) => {
  for (const entry of list.getEntries()) {
    if (entry.duration > 50) { // 超过 50ms 被认为是长任务
      console.warn('长任务 detected:', entry);
      
      // 报告到监控系统
      reportLongTask({
        duration: entry.duration,
        startTime: entry.startTime,
        name: entry.name
      });
    }
  }
});

observer.observe({ entryTypes: ['longtask'] });

// 手动检测代码块执行时间
function measurePerformance(fn, name) {
  const start = performance.now();
  fn();
  const duration = performance.now() - start;
  
  if (duration > 50) {
    console.warn(`函数 ${name} 执行了 ${duration.toFixed(2)}ms`);
  }
  
  return duration;
}
```

 渲染性能分析

```javascript
// 监控帧率
let frameCount = 0;
let lastTime = performance.now();

function checkFPS() {
  frameCount++;
  const currentTime = performance.now();
  
  if (currentTime - lastTime >= 1000) {
    const fps = Math.round((frameCount * 1000) / (currentTime - lastTime));
    console.log(`当前 FPS: ${fps}`);
    
    if (fps < 30) {
      console.warn('低帧率警告！可能存在渲染阻塞');
    }
    
    frameCount = 0;
    lastTime = currentTime;
  }
  
  requestAnimationFrame(checkFPS);
}

checkFPS();
```

 解决方案与最佳实践

 1. 任务分片

```javascript
function createChunkedProcessor(chunkSize = 100) {
  return function processInChunks(items, processFn, onProgress) {
    let index = 0;
    
    function processNextChunk() {
      const chunk = items.slice(index, index + chunkSize);
      
      // 处理当前分片
      for (const item of chunk) {
        processFn(item);
      }
      
      index += chunkSize;
      
      // 更新进度
      if (onProgress) {
        onProgress((index / items.length) * 100);
      }
      
      // 如果还有数据，安排下一个分片
      if (index < items.length) {
        setTimeout(processNextChunk, 0);
      }
    }
    
    processNextChunk();
  };
}
```

 2. Web Workers 处理 CPU 密集型任务

```javascript
// 主线程
const worker = new Worker('heavy-task-worker.js');

worker.postMessage({ data: largeData });

worker.onmessage = (event) => {
  const results = event.data;
  updateUI(results);
};

// heavy-task-worker.js
self.onmessage = (event) => {
  const data = event.data.data;
  const results = expensiveCalculation(data); // 不会阻塞主线程
  self.postMessage(results);
};
```

 3. 使用 requestIdleCallback

```javascript
function scheduleLowPriorityWork(work) {
  if ('requestIdleCallback' in window) {
    requestIdleCallback((deadline) => {
      while ((deadline.timeRemaining() > 0 || deadline.didTimeout) && work.hasMore()) {
        work.doNext();
      }
      
      if (work.hasMore()) {
        scheduleLowPriorityWork(work);
      }
    }, { timeout: 1000 }); // 最多等待 1 秒
  } else {
    // 降级方案
    setTimeout(work.doAll, 0);
  }
}
```

 总结

**JavaScript 事件循环与渲染阻塞的关键点**：

1. **单线程模型**：JavaScript 在主线程运行，与渲染、布局共享同一线程
2. **任务队列**：宏任务 → 微任务 → 渲染的固定顺序
3. **渲染时机**：渲染发生在宏任务之间，长任务会延迟渲染
4. **阻塞表现**：长时间同步代码导致页面卡顿、无响应
5. **解决方案**：任务分片、Web Workers、异步操作、批量 DOM 操作

理解事件循环是优化 Web 应用性能、实现流畅用户体验的基础，也是理解 React Fiber 等现代框架并发特性的前提。

## 拆分卡片

- [[事件循环决定的 JavaScript 运行时机]]
- [[微任务会影响浏览器渲染时机的原因]]
- [[长任务会阻塞浏览器渲染和用户输入响应的原因]]
- [[任务分片和 Web Worker 缓解渲染阻塞的方法]]
