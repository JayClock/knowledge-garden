---
date: 2024-03-17T15:49:04
updated: 2024-03-17T15:58:43
share: true
---
# 如何理解依赖反转原则
> [!Quote] Dependency Inversion Prin
> High-level modules shouldn’t depend on low-level modules. Both modules should depend on abstractions. In addition, abstractions shouldn’t depend on details. Details depend on abstractions.

即高层模块不要依赖低层模块。高层模块和低层模块应该通过[[抽象（Abstraction）|抽象（Abstraction）]]来互相依赖，除此之外，抽象不要依赖具体的实现细节，具体实现细节依赖抽象。

简单来说，在调用链上，调用者属于高层，被调用者属于低层。这个原则主要用于指导框架设计。
# angular 中的例子
```ts
import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class SomeService {
  constructor() { }
  
  doSomething() {
    // Implementation...
  }
}

import { Component } from '@angular/core';
import { SomeService } from './some.service';

@Component({
  selector: 'app-some-component',
  templateUrl: './some.component.html',
  styleUrls: ['./some.component.css']
})
export class SomeComponent {
  constructor(private someService: SomeService) {}

  useService() {
    this.someService.doSomething();
  }
}

```
在上面的例子中，`Someponent`类不直接实例化`SomeService`，而是通过其构造的参数来接收一个`SomeService`的实例，这个实例的创建和提供是由 angular 的依赖注入容器决定的。`SomeComponent`实现了依赖于抽象而不是具体的实例化，遵循了依赖反转原则。

Angular 的 DI 容器在幕后处理所有的依赖关系的解析和注入，使得组件或服务之间的耦合度降低，提高了代码的模块化和可测试性。