---
date: 2025-01-02T16:16:07
updated: 2026-05-15 12:16:33
share: true
source: https://martinfowler.com/bliki/StranglerFigApplication.html
noteId: 1778807093360
---
Strangler fig 的核心思想和适用场景是什么？

---

- 背景：
 软件变更通常伴随着大量临时化的补丁，而这些补丁每一个都难以应对未来的变化。直到有一天，人们发现已经难以通过打补丁的方式去更新软件（也就是我们平时所说的**屎山代码**），必须得进行对遗留系统进行优化。
- 来源：
 [Martin Fowler](https://martinfowler.com/)在旅游时，发现一种被称为 Strangler fig 的藤蔓。这种藤蔓寄生在树上，不断吸取树木的养分，直到长到可以自我进行光合作用。在多年的生长过后，这种藤蔓会杀死自己的宿主，完成“谋权篡位”。游戏《最后生还者》中也是这么个设定。
-
