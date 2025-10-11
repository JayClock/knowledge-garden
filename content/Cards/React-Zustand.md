---
date: 2025-10-09 16:38:22
updated: 2025-10-09 16:40:09
share: true
---
```tsx
import { create } from "zustand";

type CounterState = {
  count: number;
  name: string;
  add: () => void;
  sub: () => void;
  double: () => void;
  changeName: () => void;
};

export const useCounter = create<CounterState>((set) => ({
  count: 0,
  name: "",
  add: () => set((state) => ({ count: state.count + 1 })),
  sub: () => set((state) => ({ count: state.count - 1 })),
  double: () => set((state) => ({ count: state.count * 2 })),
  changeName: () => set(() => ({ name: "heyi" + Math.random() })),
}));
```


```tsx
import { useEffect } from "react";
import { useCounter } from "../../stores/useCounter";

const Counter = () => {
  const count = useCounter((state) => state.count);
  return <div>count: {count}</div>;
};

const Name = () => {
  const name = useCounter((state) => state.name);
  return <div>name: {name}</div>;
};

export const ZustandDemo = () => {
  const add = useCounter((state) => state.add);
  const sub = useCounter((state) => state.sub);
  const double = useCounter((state) => state.double);
  const changeName = useCounter((state) => state.changeName);

  return (
    <div>
      <Counter />
      <Name />

      <div>
        <button onClick={add}>+</button>
        <button onClick={sub}>-</button>
        <button onClick={double}>*2</button>

        <button onClick={changeName}>改变名字</button>
      </div>
    </div>
  );
};
```

