---
date: 2024-10-12T17:57:32
updated: 2024-10-15T14:32:44
share: true
---
# 为什么继承需要调用 super()

在子类 `constructor` 中必须调用 `super` 方法，因为子类没有自己的 `this` 对象，而是继承在父类的 `this` 对象，然后对其进行加工，而 `super` 就代表了父类的构造函数。

在下面的例子中，super 虽然代表了父类 A 的构造函数，但是返回的是子类 B 的实例，即 super 内部的 this 指的是 B，因此 super() 在这里相当于`A.prototype.constructor.call(this, props)`。

```ts
// 父类
class People {
    constructor(name) {
        this.name = name
    }
    eat() {
        console.log(`${this.name} eat something`)
    }
}

// 子类
class Student extends People {
    constructor(name, number) {
        super(name)
        this.number = number
    }
    sayHi() {
        console.log(`姓名 ${this.name} 学号 ${this.number}`)
    }
}

// 子类
class Teacher extends People {
    constructor(name, major) {
        super(name)
        this.major = major
    }
    teach() {
        console.log(`${this.name} 教授 ${this.major}`)
    }
}

// 实例
const xialuo = new Student('夏洛', 100)
console.log(xialuo.name)
console.log(xialuo.number)
xialuo.sayHi()
xialuo.eat()

// 实例
const wanglaoshi = new Teacher('王老师', '语文')
console.log(wanglaoshi.name)
console.log(wanglaoshi.major)
wanglaoshi.teach()
wanglaoshi.eat()
```

# 原型

`JavaScript` 常被描述为一种基于原型的语言 —— 每个对象都有一个原型对象。

当试图访问一个对象属性时，它不仅仅在该对象上搜寻，还会搜寻该对象的原型，以及该对象原型的原型，依次层层向上搜索，直到找到一个名字匹配的属性或到达原型链的末尾。

%% 准确地说，这些属性和方法定义在Object的构造器函数（constructor functions）之上的prototype属性上，而非实例对象本身 %%

1. 每个 class 都有一个显示原型 `prototype`
2. 每个实例都有隐式原型 `_proto_`
3. 每个 `_proto_` 指向对应 class 的 `prototype`

# 基于原型的执行规则
1. 获取属性 xialuo.name 或执行方法 xialuo.sayHi() 时
2. 先在自身属性和方法寻找
3. 如果找不到则自动去 `_proto_` 中查找
![[../images/基于原型的执行规则.png|基于原型的执行规则.png]]
# 原型链
原型对象也可能拥有原型，并从中继承方法和属性，一层一层、依次类推。这种关系常常被称为原型链（prototype chain），它解释了为何一个对象会拥有定义在其它对象中的属性和方法。
![[../images/原型和原型链.png|原型和原型链.png]]
# 实现一个 new 操作符
- 创建一个新的对象 obj
- 将对象与构造函数通过原型链连接起来
- 将构造函数中的 this 绑定到新建的对象上 obj 上
- 根据构造函数的返回类型作判断，如果是原始值则被忽略，如果是返回对象，需要正常处理


```ts
function newFn(fn, ...args) {
	// 创建一个新对象
  const obj = {}
  // 新对象的原型指向构造函数原型对象
  obj.__proto__ = fn.prototype
  // 将构造函数的this指向新对象
  let res = fn.apply(obj, args)
  // 根据返回值判断
  return res instanceof Object ? res : obj
}
```
# instanceOf 的本质是原型链

```ts
function instanceOf(left, right) {
  let proto = left.__proto__
  while (true) {
    if (proto == null) return false
    if (proto === right.prototype) {
      return true
    }
    proto = proto.__proto__
  }
}
```
