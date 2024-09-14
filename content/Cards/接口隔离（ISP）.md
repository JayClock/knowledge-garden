---
date: 2024-03-12T12:29:31
updated: 2024-09-14T10:56:53
share: true
---
# 如何理解接口隔离原则

> [!Quote] Interface Segregation Principle
> Clients should not be forced to depend upon interfaces that they do not use。

即接口的调用者或者使用者，不应该被强迫依赖它不需要的接口。

这个原则核心在于理解其中的“接口”二字，我们可以把“接口”理解为下面三种类型
## 一组 API 接口集合

以下代码是我们平时常见的对用户信息的处理，比如注册、登陆、根据手机号获取用户信息等。假设我们现在有一个需求，需要实现一个删除用户的功能，在不考虑接口隔离的情况下，就是直接在`UserService`中添加一个`deleteUserByCellphone` 或者`deleteUserByCellphone`，但这样会导致一个问题，所有可以调用获取信息的地方，也可以调用删除的逻辑，很有可能导致误删用户。也就是“获取用户信息接口的调用者，不应该被强迫依赖它不需要的删除用户的接口”。

```java
public interface UserService {
  boolean register(String cellphone, String password);
  boolean login(String cellphone, String password);
  UserInfo getUserInfoById(long id);
  UserInfo getUserInfoByCellphone(String cellphone);
}
```

在接口隔离的思想下。将删除的接口独立在一个`RestrictedUserService`接口中。这样就能保证，删除的接口，只会被需要实现删除逻辑地方使用。至于用户注册的场景，并不会被强迫依赖不需要的删除接口。
```java
public interface UserService {
  boolean register(String cellphone, String password);
  boolean login(String cellphone, String password);
  UserInfo getUserInfoById(long id);
  UserInfo getUserInfoByCellphone(String cellphone);
}

public interface RestrictedUserService {
  boolean deleteUserByCellphone(String cellphone);
  boolean deleteUserById(long id);
}

public class UserServiceImpl implements UserService, RestrictedUserService {
  // ...省略实现代码...
}
```
## 单个 API 接口或函数
在这样的场景下，函数的设计要功能单一，不要将多个不同的功能逻辑在一个函数中实现。
```java
public class Statistics {
  private Long max;
  private Long min;
  private Long average;
  private Long sum;
  private Long percentile99;
  private Long percentile999;
  //...省略constructor/getter/setter等方法...
}

public Statistics count(Collection<Long> dataSet) {
  Statistics statistics = new Statistics();
  //...省略计算逻辑...
  return statistics;
}
```

上面这个函数解决的是统计需求，假设在统计时，Statistics 中的所有属性都用到了，那么 count 就是一个功能单一的接口。但假设统计信息有的只涉及到 max、min，有的只涉及到 average、sum。那么 count 的职责就不算单一。应该拆分成更小粒度的函数。
```java
public Long max(Collection<Long> dataSet) { //... }
public Long min(Collection<Long> dataSet) { //... } 
public Long average(Colletion<Long> dataSet) { //... }
// ...省略其他统计函数...
```

接口隔离和[[./设计原则：单一职责（SRP）|单一职责]]的区别在于，[[./设计原则：单一职责（SRP）|单一职责]]针对的是模块、类、接口的设计。而接口隔离原则相对于单一职责原则，更加侧重于接口的设计。它提供了一种评判接口是否单一的标准：通过调用者如何使用接口来间接地判定。**如果调用者只使用部分接口或接口的部分功能，那接口的设计就不够职责单一**
## OOP 中的接口概念
