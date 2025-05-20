---
date: 2025-05-20T15:40:00
updated: 2025-05-20T15:50:52
share: true
---
![避开重排和重绘](https://knowledge-garden.oss-cn-shanghai.aliyuncs.com/images/%E9%81%BF%E5%BC%80%E9%87%8D%E6%8E%92%E5%92%8C%E9%87%8D%E7%BB%98.png)

在上图中，我们使用了 CSS 的 transform 来实现动画效果，这可以避开[[./HTML 重排|重排]]和[[./HTML 重绘|重绘]]阶段，直接在非主线程上执行合成动画操作。这样的效率是最高的，因为是在非主线程上合成，并没有占用主线程的资源，另外也避开了布局和绘制两个子阶段，所以相对于重绘和重排，合成能大大提升绘制效率。