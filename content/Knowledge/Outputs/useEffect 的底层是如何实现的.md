---
date: 2025-05-06T22:49:44
updated: 2026-07-09 10:45:13
---
useEffect 是 React 用于管理副作用的 Hook，它在 commit 阶段统一执行，确保副作用不会影响渲染。在 React 码中，useEffect 通过 Fiber 机制在 commit 阶段进行处理：
