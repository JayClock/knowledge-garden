---
date: 2024-10-17T14:28:42
updated: 2024-10-17T15:38:04
share: true
---
在 TypeScript 中，即使两个 `enum` 的成员完全一致，它们仍然是不同的类型。这是因为 `enum` 在 TypeScript 中是命名空间的一部分，每个 `enum` 都有自己的命名空间。因此，即使它们的成员相同，也不能互相替代。
### 示例

```typescript
enum Color1 {
  Red,
  Green,
  Blue
}

enum Color2 {
  Red,
  Green,
  Blue
}

let color1: Color1 = Color1.Red;
let color2: Color2 = Color2.Red;

// 以下代码会报错，因为 Color1 和 Color2 是不同的类型
// color1 = color2; // Error: Type 'Color2' is not assignable to type 'Color1'.
// color2 = color1; // Error: Type 'Color1' is not assignable to type 'Color2'.
```

### 解决方案

#### 1. 使用联合类型
如果你希望两个 `enum` 能够互相替代，可以将它们转换为联合类型。

```typescript
enum Color1 {
  Red,
  Green,
  Blue
}

enum Color2 {
  Red,
  Green,
  Blue
}

type Color = Color1 | Color2;

let color1: Color = Color1.Red;
let color2: Color = Color2.Red;

color1 = color2; // 现在可以互相替代
color2 = color1; // 现在可以互相替代
```

#### 2. 使用字符串枚举
如果你不介意使用字符串枚举，可以考虑使用字符串枚举，因为字符串枚举的值是字符串，而不是数字，因此更容易进行类型转换。

```typescript
enum Color1 {
  Red = "Red",
  Green = "Green",
  Blue = "Blue"
}

enum Color2 {
  Red = "Red",
  Green = "Green",
  Blue = "Blue"
}

let color1: Color1 = Color1.Red;
let color2: Color2 = Color2.Red;

// 现在可以互相替代
color1 = color2;
color2 = color1;
```

#### 3. 使用常量枚举
如果你希望 `enum` 的值在编译时被内联，可以使用常量枚举（const enum）。

```typescript
const enum Color1 {
  Red,
  Green,
  Blue
}

const enum Color2 {
  Red,
  Green,
  Blue
}

let color1: Color1 = Color1.Red;
let color2: Color2 = Color2.Red;

// 现在可以互相替代
color1 = color2;
color2 = color1;
```

### 总结
- **联合类型**：适用于需要将两个 `enum` 互相替代的情况。
- **字符串枚举**：适用于希望 `enum` 的值是字符串的情况。
- **常量枚举**：适用于希望 `enum` 的值在编译时被内联的情况。

根据你的需求选择合适的方法即可。