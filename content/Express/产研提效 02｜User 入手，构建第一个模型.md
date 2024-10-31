---
date: 2024-10-09T15:30:30
updated: 2024-10-31T09:54:14
share: true
title: 产研提效 02｜User 入手，构建第一个模型
categories:
  - 产研提效
  - ai
---
# User：熟悉的陌生人

在前端开发中，用户基本信息接口是一个核心组件，用于承载和管理用户的个人信息。由于用户的个人基本信息变更频率较低，频繁的网络请求不仅会增加服务器的负担，还会影响用户体验。因此，前端开发人员通常会在初次请求后将用户信息存储在本地缓存中，如LocalStorage或SessionStorage，以减少后续请求的次数。只有在用户进行个人信息变更时，才会触发更新本地数据的逻辑。

在一开始的时候，User 里一般只有用户名、手机号、邮箱等基础信息，后来我们为了给用户划分等级，来满足不同类型客户的需求，User 接口里就有了权限相关信息。再后来我们为了让客户能够帮我们宣传产品，我们便有了邀请机制，User 信息里便通过 `isInvited` 区分是否被邀请。随着功能的累加，User 接口变膨胀为了巨型对象。比如下面这种：

```json
{
  "beingBlackEmail": false,
  "beingDisableExpiryRemind": false,
  "beingExpand": true,
  "beingInvited": false,
  "beingLangFollowBrowser": false,
  "beingOldVersion": false,
  "beingPrivacyPolicy": true,
  "beingSandBoxSuperAdmin": false,
  "collectUserInfo": true,
  "createTime": "2022-09-05T10:00:19",
  "csShow": false,
  "desktopRemind": true,
  "email": "uat@qingflow.com",
  "firstLogin": false,
  "hasPwdLoggedIn": true,
  "havePassword": true,
  "headImg": "https://osstest.oalite.com/documents/user/icon/126B7CD/0dbf8e37-72b7-43c9-a18f-6d74ccf33d53.jpeg",
  "lang": "cn",
  "lastWsInfo": {
    "accepted": null,
    "accountLevel": 40,
    "auth": 2,
    "beingCustomizedAppSync": false,
    "beingDevelopManagement": false,
    "beingHideHelpDocument": false,
    "beingSandbox": false,
    "beingUseExternalMemberFunction": true,
    "beingWatermark": false,
    "biAuth": "NORMAL",
    "canWorkWx": false,
    "contactEnableNum": 82,
    "contactNum": 85,
    "dataRelatedStatus": "NEW",
    "departs": [
      [
        {
          "beingCanEdit": null,
          "departName": "1",
          "deptId": 279395,
          "ordinal": "-100000000",
          "userPost": 0
        },
        {
          "beingCanEdit": null,
          "departName": "89",
          "deptId": 279396,
          "ordinal": "-99965375",
          "userPost": 0
        },
        {
          "beingCanEdit": null,
          "departName": "90",
          "deptId": 279401,
          "ordinal": "-100000000",
          "userPost": 0
        },
        {
          "beingCanEdit": null,
          "departName": "54",
          "deptId": 279408,
          "ordinal": "-100002000",
          "userPost": 0
        },
        {
          "beingCanEdit": null,
          "departName": "64",
          "deptId": 279413,
          "ordinal": "-100001000",
          "userPost": 0
        },
        {
          "beingCanEdit": null,
          "departName": "79",
          "deptId": 279418,
          "ordinal": "-100001000",
          "userPost": 0
        }
      ],
      [
        {
          "beingCanEdit": null,
          "departName": "轻流",
          "deptId": 212545,
          "ordinal": "0",
          "userPost": 0
        },
        {
          "beingCanEdit": null,
          "departName": "研发部门",
          "deptId": 212546,
          "ordinal": "0",
          "userPost": 0
        }
      ],
      [
        {
          "beingCanEdit": null,
          "departName": "轻流",
          "deptId": 212545,
          "ordinal": "0",
          "userPost": 0
        }
      ],
      [
        {
          "beingCanEdit": null,
          "departName": "逐级审批部门1",
          "deptId": 279769,
          "ordinal": "9",
          "userPost": 0
        },
        {
          "beingCanEdit": null,
          "departName": "逐级审批子1",
          "deptId": 279771,
          "ordinal": "0",
          "userPost": 0
        },
        {
          "beingCanEdit": null,
          "departName": "逐级审批子2",
          "deptId": 279772,
          "ordinal": "0",
          "userPost": 1
        }
      ],
      [
        {
          "beingCanEdit": null,
          "departName": "逐级审批部门1",
          "deptId": 279769,
          "ordinal": "9",
          "userPost": 0
        },
        {
          "beingCanEdit": null,
          "departName": "逐级审批子1",
          "deptId": 279771,
          "ordinal": "0",
          "userPost": 0
        },
        {
          "beingCanEdit": null,
          "departName": "逐级审批子2",
          "deptId": 279772,
          "ordinal": "0",
          "userPost": 1
        }
      ],
      [
        {
          "beingCanEdit": null,
          "departName": "逐级审批部门1",
          "deptId": 279769,
          "ordinal": "9",
          "userPost": 0
        },
        {
          "beingCanEdit": null,
          "departName": "逐级审批子1",
          "deptId": 279771,
          "ordinal": "0",
          "userPost": 0
        },
        {
          "beingCanEdit": null,
          "departName": "逐级审批子2",
          "deptId": 279772,
          "ordinal": "0",
          "userPost": 1
        }
      ],
      [
        {
          "beingCanEdit": null,
          "departName": "逐级审批部门1",
          "deptId": 279769,
          "ordinal": "9",
          "userPost": 0
        },
        {
          "beingCanEdit": null,
          "departName": "逐级审批子1",
          "deptId": 279771,
          "ordinal": "0",
          "userPost": 0
        },
        {
          "beingCanEdit": null,
          "departName": "逐级审批子2",
          "deptId": 279772,
          "ordinal": "0",
          "userPost": 1
        }
      ],
      [
        {
          "beingCanEdit": null,
          "departName": "逐级审批部门1",
          "deptId": 279769,
          "ordinal": "9",
          "userPost": 0
        },
        {
          "beingCanEdit": null,
          "departName": "逐级审批子1",
          "deptId": 279771,
          "ordinal": "0",
          "userPost": 0
        },
        {
          "beingCanEdit": null,
          "departName": "逐级审批子2",
          "deptId": 279772,
          "ordinal": "0",
          "userPost": 1
        },
        {
          "beingCanEdit": null,
          "departName": "逐级审批子3",
          "deptId": 279773,
          "ordinal": "0",
          "userPost": 0
        }
      ],
      [
        {
          "beingCanEdit": null,
          "departName": "打印部门",
          "deptId": 279803,
          "ordinal": "13",
          "userPost": 0
        }
      ]
    ],
    "dynamic": null,
    "exId": "tAeLHd46LCKx944sDqug/A==",
    "exUserId": "1148377",
    "exWsId": "5yCfIToEVUXBj0fUn6rgWg",
    "expireDate": 1745574727000,
    "externalMemberId": null,
    "hideCopyright": false,
    "identity": "INTERIOR",
    "logoutConfig": {
      "logOutToSso": false,
      "serverName": null,
      "ssoType": null
    },
    "memberId": 1196687,
    "openConnectorList": [],
    "openPluginList": [
      2,
      3,
      4,
      6,
      7,
      8,
      9,
      11,
      12,
      13,
      14,
      15,
      16,
      17,
      18,
      19,
      20,
      21,
      22,
      23,
      24,
      25,
      26,
      27,
      28,
      29,
      33,
      34,
      35,
      36,
      37,
      38,
      39,
      41,
      42,
      43,
      44,
      45,
      46,
      -2,
      32,
      30
    ],
    "permissionStatus": false,
    "pluginClickList": [
      4,
      6,
      14,
      19,
      26,
      30,
      36,
      39,
      40,
      503,
      504,
      505,
      506
    ],
    "pluginLimitDetail": {
      "dashAllVisiableLimit": 4,
      "dashAllVisiableNum": 9
    },
    "publicAccessAuthVO": {
      "beingAttachmentQuestion": true,
      "beingPublicLink": true
    },
    "remark": "1",
    "showContact": true,
    "trial": true,
    "trialDays": "784",
    "trialNotice": true,
    "type": "workwx",
    "useScheduledSync": false,
    "watermarkConfig": {
      "showDate": true,
      "showDeparts": true,
      "showExUserId": true,
      "showName": true,
      "showPhoneNumber": true,
      "showWsName": true
    },
    "wsDomain": null,
    "wsFunction": "platform",
    "wsId": 110184,
    "wsLimitDetail": {
      "canDashNum": -1,
      "canFormNum": -1,
      "canPackageNum": -1,
      "currentDashNum": -1,
      "currentFormNum": -1,
      "currentPackageNum": -1
    },
    "wsName": "hp最大的工作区"
  },
  "mobile": "13091870868",
  "nickName": "灭霸堂堂来袭",
  "npsCollect": false,
  "promoCode": "f1d25a24a",
  "randomEmail": false,
  "recordedNewGuidePop": [
    1,
    2,
    3,
    4,
    5,
    6,
    7,
    9,
    10,
    11
  ],
  "showProcessPersonal": false,
  "signatureUrl": "https://osstest.oalite.com/documents/form/signature/126B7CD/22e2adbf-9939-4246-943f-e6ea0a00186a.png",
  "source": "offical_noPage_undefined",
  "status": true,
  "uid": 1148377
}
```

在整个 user 接口膨胀的过程中，承载了几十上百页的需求、设计文档。在当年任务开发的阶段，这些的确能准确描述当时的系统状态。然而随着时间的更迭、需求的研发，不同阶段的文档往往无法很好地保存下来，最终造成了业务知识的缺失。

即使所有文档都保存完好，也很难有人能完完整整地阅读下来。虽然现在有 AI 了，但是没有人能保证系统的实现和文档描述是完全吻合的。错误的业务知识传递，可能在 AI 的情况下比过去更加严重。
# 隐性概念显性化，降低认知负载

我们最优先应该做的，其实是把代码库中，被埋藏在历史长河中的概念提取出来，使其变得可读。这里我举一个用户权限的例子。软件开发中，权限体系是和 user 绑定的至关重要的一环，我们经常会根据全局信息，判断当前用户是否有权限。在常规情况下，我们会在每一个获取权限的地方，进行逻辑上的判断。比如下面这种形式：

```js
const wsInfo = this.rootStore.workspaceInfo();
const auth = wsInfo?.auth;

return auth === UserWsAuth.ADMIN || auth === UserWsAuth.CREATOR;
```
由或者是。
```js
this.personalWorkSpace = res.filter(ws => ws.auth === UserWsAuth.CREATOR);
this.otherWorkSpace = res.filter(ws => ws.auth !== UserWsAuth.CREATOR);
```

尽管我们可以将判断逻辑抽象至一个  util 函数中，比如 `authUtil.isCreater(auth)`（实际上大部分企业都是这么做的）。但这个方式治标不治本。对于功能描述为“当用户是管理员时，用户可以编辑数据”，直观的描述应该是：
```js
if (user.isCreater()) {
	user.editData()
}
```
而不是：
```js
if (AuthUtil.isCreater(user.auth)) {
	user.editData()
}
```

第二种方法中 `AuthUtil` 它本身只是一些静态方法的集合，这种方法虽然实现了功能，但是并没有明确表达出**用户权限**这个业务概念。而且每一个初次上手代码库的人，不仅需要知道 user 中有权限相关的参数，还需要明确知道代码库中有一个专门叫 `AuthUtil` 来判断权限的类。一旦在人员变动交付的过程中，没有传递好信息，立马就会出现，**不同的人，在不同的地方，用不同的方式写了相同的功能**。即使大家都统一调用工具类方法，也依旧导致业务逻辑分散在各个地方，变成我们平时所说的屎山代码。

我们可以基于 DDD 的思想，构造一个叫做 `UserAuth` 的值对象，将各种判断条件写入值对象中，这样在实现层就不需要写大量的判断了。

```ts
enum UserAuthEnum {
  MEMBER,
  ADMIN,
  CREATOR,
  DATA_MANAGER,
}

export class UserAuth {
  private constructor(private params: { label: string; value: UserAuthEnum }) {}

  readonly label = this.params.label;

  readonly value = this.params.value;

  isMember(): boolean {
    return this.value === UserAuthEnum.MEMBER;
  }

  isAdmin(): boolean {
    return this.value === UserAuthEnum.ADMIN;
  }

  isCreater(): boolean {
    return this.value === UserAuthEnum.CREATOR;
  }

  static readonly MEMBER = new UserAuth({ label: '成员', value: UserAuthEnum.MEMBER });

  static readonly ADMIN = new UserAuth({ label: '管理元', value: UserAuthEnum.ADMIN });

  static readonly CREATOR = new UserAuth({ label: '创建者', value: UserAuthEnum.CREATOR });

  static values(): UserAuth[] {
    return Object.values(this).filter(item => item instanceof UserAuth);
  }

  static valueOf(value: UserAuthEnum): UserAuth {
    const userAuth = this.values().find(item => item.value === value);
    if (!userAuth) {
      throw new Error(`未知的用户权限 ${value}`);
    }
    return userAuth;
  }
}
```

接下去我们在构造 user 实体时，使用 `userAuth` 值对象，在 user 中的权限数据就变为了：

```ts
export interface BackendUser {
  auth: UserAuthEnum;
}

class User {
  constructor(private backendUser: BackendUser) {}

  auth = UserAuth.valueOf(this.backendUser.auth);

  isCreater = this.auth.isCreater();

  isAdmin = this.auth.isAdmin();

  isMemer = this.auth.isMember();
}
```
在这样的设计下，我们对 user 的调用逻辑就变为了：

```ts
// 拿到 user 权限在前端显示的名称
user.auth.label
// 判断用户是否是管理员
user.isAdmin()
```
