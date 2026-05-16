---
date: 2025-10-09 16:46:26
updated: 2026-05-16 19:29:22
share: true
noteId: 1778930949315
---
React Jotai 的核心作用和使用场景是什么？

---

```tsx
import { useAtomValue, useSetAtom } from "jotai";
import { ageAtom } from "../../atom/AgeAtom";
import { nameAtom } from "../../atom/NameAtom";
import { infoAtom } from "../../atom/InfoAtom";

const Age = () => {
  const age = useAtomValue(ageAtom);
  return <div>age: {age}</div>;
};

const Name = () => {
  const name = useAtomValue(nameAtom);
  return <div>name: {name} </div>;
};

const Info = () => {
  const info = useAtomValue(infoAtom);
  return <div>{JSON.stringify(info)}</div>;
};

export const JotaiDemo = () => {
  const setAge = useSetAtom(ageAtom);
  const setName = useSetAtom(nameAtom);
  return (
    <div>
      <Age />
      <Name />
      <Info />

      <div>
        <button onClick={() => setAge((s) => s + 1)}>+</button>
        <button onClick={() => setAge((s) => s - 1)}>-</button>
        <input onChange={(ev) => setName(ev.target.value)} />
      </div>
    </div>
  );
};

```
