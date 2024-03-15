---
date: 2024-03-12T12:29:31
updated: 2024-03-15T13:28:21
share: true
---
# 如何理解接口隔离原则

> [!Quote] Interface Segregation Principle
> Clients should not be forced to depend upon interfaces that they do not use。

即接口的调用者或者使用者，不应该被强迫依赖它不需要的接口。

这个原则核心在于理解其中的“接口”二字，我们可以把“接口”理解为下面三种东西
## 一组 API 接口集合

以下代码是我们平时常见的对用户信息的处理，比如注册、登陆、根据手机号获取用户信息等。假设我们现在有一个需求，需要实现一个删除用户的功能，在不考虑接口隔离的情况下，就是直接在`UserService`中添加一个`deleteUserByCellphone` 或者`deleteUserByCellphone`，但这样会导致一个问题，所有可以调用获取信息的地方，也可以调用删除的逻辑，很有可能导致误删用户。也就是“获取用户信息接口的调用者，不应该被强迫依赖它不需要的删除用户的接口”。

```Java
public interface UserService {
  boolean register(String cellphone, String password);
  boolean login(String cellphone, String password);
  UserInfo getUserInfoById(long id);
  UserInfo getUserInfoByCellphone(String cellphone);
}
```

在接口隔离的思想下。将删除的接口独立在一个`RestrictedUserService`接口中。这样就能保证，删除的接口，只会被需要实现删除逻辑地方使用。至于用户注册的场景，并不会被强迫依赖不需要的删除接口。
```Java
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