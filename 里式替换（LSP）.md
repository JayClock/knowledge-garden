---
date: 2024-03-08T07:40:32
updated: 2024-03-15T11:43:43
---
# 如何理解里式替换原则
Liskov Substitution Principle ——
If S is a subtype if T, then objects of type T may be replaced with objects of type S, without breaking the program. / Functions that use pointers of references to base classes must be able to use objects of derived classes without knowing it。

即子类对象能够替换程序中的父类对象出现的任何地方，并且保证原来程序的逻辑行为不变级正确性不被破坏。
