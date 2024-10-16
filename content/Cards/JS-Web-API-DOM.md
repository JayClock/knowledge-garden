---
date: 2024-10-12T18:00:52
updated: 2024-10-16T09:31:26
share: true
---
# DOM 本质
DOM 本质是一颗树，首先 [[./HTML|HTML]] 本身是一个树形的结构，HTML 是文件或者代码，DOM 是浏览器内存中初始化好的书。DOM 本质是**浏览器从 HTML 语言中解析出来的一颗树**。
# DOM 节点操作

```js
// 获取 DOM 节点
const div1 = document.getElementById('div1')
console.log('div1', div1)

const divList = document.getElementsByTagName('div') // 集合
console.log('divList.length', divList.length)
console.log('divList[1]', divList[1])

const containerList = document.getElementsByClassName('container') // 集合
console.log('containerList.length', containerList.length)
console.log('containerList[1]', containerList[1])

const pList = document.querySelectorAll('p')
console.log('pList', pList)
```
## property 和 atttribute
- property: 修改对象属性，不会体现到 html 结构中
- attribute: 修改 html 属性，会改变 html 结构
- 两者都有可能引起 DOM 重新渲染
- 尽量使用 property

```js
// DOM 节点的 propert
// property 形式 修改对象属性，不会体现到html结构中
const pList = document.querySelectorAll('p')
const p1 = pList[0]
p1.style.width = '100px'
console.log(p1.style.width)
p1.className = 'red'
console.log(p1.className)
console.log(p1.nodeName)
console.log(p1.nodeType) // 1
```

```js
// attribute 修改html属性，会改变html结构
p1.setAttribute('data-name', 'imooc')
console.log(p1.getAttribute('data-name'))
```

# DOM 结构操作

```js
const div1 = document.getElementById('div1')
const div2 = document.getElementById('div2')

// 新建节点
const newP = document.createElement('p')
newP.innerHTML = 'this is newP'

// 插入节点
div1.appendChild(newP)

// 移动节点
const p1 = document.getElementById('p1')
div2.appendChild(p1)

// 获取父元素
console.log(p1.parentNode)

// 获取子元素列表
const div1ChildNodes = div1.childNodes
console.log(div1ChildNodes)
const div1ChildNodesP = Array.prototype.slice.call(div1.childNodes).filter(child => {
    if (child.nodeType === 1) return true
    return false
})
console.log(div1ChildNodesP)

// 删除子元素
div1.removeChild(div1ChildNodesP[0])
```
# DOM 性能
- DOM 操作非常**消耗性能**，避免频繁的 DOM 操作
- 对 DOM 操作做缓存
- 将频繁操作改为一次性操作

```js
// 不缓存DOM查询结果
for (let i = 0; i < document.getElementsByTagName('p').length; i++) {
    // 每次循环，都会计算length，频繁进行DOM查询
}

// 缓存DOM查询结果
const pList = document.getElementsByTagName('p')
const length = pList.length
for (let i = 0; i < length; i++) {
    // 缓存length，只进行一次DOM查询
}
```

```js
const list = document.getElementById('list')

// 创建一个文档片段，此时还没有插入到 DOM 树中
const frag = document.createDocumentFragment()

for (let i = 0; i < 10; i++) {
    const li = document.createElement('li')
    li.innerHTML = `List item ${i}`

    // 先插入文档片段中
    frag.appendChild(li)
}

// 都完成之后，再插入到 DOM 中
list.appendChild(frag)
```

```js
// 不使用文档片段，只要循环时不触发 DOM 渲染
const node = document.createElement('div');
for (let i = 0; i < 10000; i++) {
  const liElem = document.createElement('li');
  liElem.innerHTML = i;
  node.appendChild(liElem);
}
document.body.appendChild(node);
```
