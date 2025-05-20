---
date: 2025-05-05T11:14:49
updated: 2025-05-20T22:36:51
share: true
---
1. **Fiber 架构的本质与设计目标**：Fiber 是 React 16+ 的**核心算法重写**，本质是**基于链表的增量式协调模型**。其核心目标并非单纯提升性能，而是重构架构以实现：  
	- **改进了协调算法**：React Fiber 使用的是基于优先级的协调算法，将任务分解为多个小任务，并根据任务的优先级来调度任务的执行，从而提高了应用的性能。
	- **支持增量渲染**：React Fiber 支持增量渲染，即在处理任务时可以中断任务，并优先处理更高优先级的任务，从而使得用户能够更快地看到页面的变化。
	- **可中断和恢复**：React Fiber 允许开发者在组件渲染的过程中对任务进行中断和恢复，从而支持更细粒度的控制，提高了应用的性能和响应速度。
	- **支持并发模式**：React Fiber 的设计是支持并发模式的，可以在多个线程中同时执行任务，从而提高了应用的性能。
	- **向后兼容**：React Fiber 的设计是向后兼容的，可以在不影响旧的应用的情况下逐步升级到新的版本，从而使得 React 应用的升级变得更加容易。
	- **支持错误边界**：React Fiber 支持错误边界机制，当组件发生错误时，可以通过错误边界机制来捕获错误并展示友好的错误信息，从而提高了应用的健壮性和用户体验。
2. **Fiber 节点的核心设计**：每个组件对应一个 **Fiber 节点**，构成**双向链表树结构**，包含以下关键信息：  
	```ts
	type Fiber = {
	  // ---- Fiber类型 ----
	
	  /** 工作类型，枚举值包括：函数组件、类组件、HTML元素、Fragment等 */
	  tag: WorkTag,
	  /** 就是那个子元素列表用的key属性 */
	  key: null | string,
	  /** 对应React元素ReactElmement.type属性 */
	  elementType: any,
	  /** 函数组件对应的函数或类组件对应的类 */
	  type: any,
	
	  // ---- Fiber Tree树形结构 ----
	
	  /** 指向父FiberNode的指针 */
	  return: Fiber | null,
	  /** 指向子FiberNode的指针 */
	  child: Fiber | null,
	  /** 指向平级FiberNode的指针 */
	  sibling: Fiber | null,
	  
	  // ---- Fiber数据 ----
	
	  /** 经本次渲染更新的props值 */  
	  pendingProps: any,
	  /** 上一次渲染的props值 */
	  memoizedProps: any,
	  /** 上一次渲染的state值，或是本次更新中的state值 */
	  memoizedState: any,
	  /** 各种state更新、回调、副作用回调和DOM更新的队列 */
	  updateQueue: mixed,
	  /** 为类组件保存对实例对象的引用，或为HTML元素保存对真实DOM的引用 */
	  stateNode: any,
	
	  // ---- Effect副作用 ----
	
	  /** 副作用种类的位域，可同时标记多种副作用，如Placement、Update、Callback等 */
	  flags: Flags,
	  /** 指向下一个具有副作用的Fiber的引用，在React 18中貌似已被弃用 */
	  nextEffect: Fiber | null,
	
	  // ---- 异步性/并发性 ----
	  
	  /** 当前Fiber与成对的进行中Fiber的双向引用 */
	  alternate: Fiber | null,
	  /** 标记Lane车道模型中车道的位域，表示调度的优先级 */
	  lanes: Lanes
	};
	```
3. **Fiber 协调流程（两阶段提交）**  
	 - **阶段 1：Reconciliation（协调/渲染阶段）**  
		- **可中断的增量计算**： React 将组件树遍历拆解为多个 Fiber 工作单元，通过**两层循环进行深度优先遍历**（而非递归）逐个处理。  
			- 每次循环执行一个 Fiber 节点，生成子 Fiber 并连接成树。  
			- 通过 `requestIdleCallback`（或 Scheduler 包）在浏览器空闲时段执行，避免阻塞主线程。  
		- **对比策略**：根据 `key` 和 `type` 复用节点，标记 `Placement`（新增）、`Update`（更新）、`Deletion`（删除）等副作用。  
		- **执行流程**：
			-  当 state 或者 context 更新时，react 会进入渲染阶段，Fiber 协调引擎会从根部开始遍历，快速跳过已处理的节点
			- 对有变化的节点，引擎会为 `Current` **（当前）节点**克隆一个 WorkInProgress **（进行中）节点**，将这两个 FiberNode 的 alternate 属性分别指向对方，并把更新都记录在在 WorkInProgress 上
			- 我们可以理解为有两颗树，一棵 `Current` 树，对应着目前已经渲染到页面上的内容；另一棵是 `WorkInProgress` 树，记录着即将发生的修改。
			- 将 [[../Knowledges/React Hooks|Hooks]] 按照顺序构造形成由 `Hook.next` 属性连接的单向链表，并挂载至 `FiberNode.memoizedState` 上。每次对比都会一一对比单向链表，React 会收集所有优先级相同的更新，合并它们，然后生成最终的更新计划（[[./React batchUpdate|React 批处理]]）
			- 对于 [[./React useEffect|useEffect]] 这种会产生副作用的 Hooks，会额外创建与 `Hook` 对象一一对应的 `Effect` 对象，赋值给 Hook.memoizedState 属性，此外，也会在 `FiberNode.updateQueue` 属性上，维护一个由 `Effect.next` 属性连接的单向链表，并把这个 `Effect` 对象加入到链表末尾。
			- 当 Fiber 树所有节点都完成工作后，`WorkInProgress` 节点会被改称为 `FinishedWork`（已完成）节点，`WorkInProgress` 树也会被改称为 `FinishedWork树`。这时 React 会进入提交阶段（Commit Phase），这一阶段主要是同步执行的。Fiber 协调引擎会把 `FinishedWork` 节点上记录的所有修改，按一定顺序提交并体现在页面上。
	- **阶段 2：Commit（提交阶段）**  
		- **不可中断的 DOM 更新**：  
		  同步执行所有标记的副作用（如 [[./JS Web-API-DOM|DOM]] 操作、生命周期调用），确保 UI 一致性。  
		- **副作用分类**：  
		  - **BeforeMutation**：`getSnapshotBeforeUpdate`。  
		  - **Mutation**：DOM 插入/更新/删除。  
		  - **Layout**：`useLayoutEffect`、`componentDidMount`/`Update`。 
4. **优先级调度机制** ：React 通过 **Lane 模型** 管理任务优先级（共 31 个优先级车道）：  
	- **事件优先级**：  
	```javascript  
	  // 优先级从高到低  
	  ImmediatePriority（用户输入）  
	  UserBlockingPriority（悬停、点击）  
	  NormalPriority（数据请求）  
	  LowPriority（分析日志）  
	  IdlePriority（非必要任务）  
	  ```
	- **调度策略**：  
		- 高优先级任务可抢占低优先级任务的执行权。  
		- 过期任务（如 Suspense 回退）会被强制同步执行。  
5. **Fiber 架构的优势与局限性**  
	- **优势**  	  
		- **流畅的用户体验**：异步渲染避免主线程阻塞，保障高优先级任务即时响应。  
		- **复杂场景优化**：支持大规模组件树的高效更新（如虚拟滚动、动画串联）。  
		- **未来特性基础**：为并发模式（Concurrent Mode）、离线渲染（SSR）提供底层支持。  
	- **局限性**   
		- **学习成本高**：开发者需理解底层调度逻辑以优化性能。  
		- **内存开销**：Fiber 树的双向链表结构比传统虚拟 DOM 占用更多内存。  
6. **与旧架构的关键差异** 

| 特性        | Stack Reconciler（React 15-）       | Fiber Reconciler（React 16+） |     |
| --------- | --------------------------------- | --------------------------- | --- |
| **遍历方式**  | 递归（不可中断）                          | 循环（可中断 + 恢复）                |     |
| **任务调度**  | 同步执行，阻塞主线程                        | 异步分片，空闲时段执行                 |     |
| **优先级控制** | 无                                 | 基于 Lane 模型的优先级抢占            |     |
| **数据结构**  | [[./虚拟 DOM（Virtual DOM）\|虚拟 DOM]] 树 | Fiber 链表树（含调度信息）            |     |
