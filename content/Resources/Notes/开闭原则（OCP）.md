---
date: 2024-03-08T07:22:14
updated: 2024-03-08T07:39:31
share: true
---
# 如何理解开闭原则
Open Closed Principle —— software entities (modules, classes, functions, etc) should be open for extension, but closed for modification.

即在添加一个新功能时，尽量避免已有的代码基础上进行拓展（添加类、函数、模块等），而非修改已有代码。核心目标是，以最小修改代码的代价，来完成新功能的开发。

开闭原则重点在于提高代码拓展性，体现开闭原则的设计思想有：多态、依赖注入、基于接口而非实现编程，设计模式里的装饰器模式、策略模式、职责链模式等。

# 如何做到“对拓展开放、修改关闭”？
时刻具备拓展意识、[[抽象（Abstraction）| 抽象]]意识、[[封装（Encapsulation）|封装]]意识。为未来的可能性变更预留好拓展点，方便未来的自己和他人，以最小代价实现新的功能。