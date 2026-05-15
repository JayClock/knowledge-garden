---
date: 2025-05-19T08:30:17
updated: 2026-05-15 09:35:34
share: true
noteId: 1778807092618
---
React useTimer 用来解决什么问题，核心用法是什么？

---

```ts
import { act, renderHook } from '@testing-library/react';
import { useTimer } from './use-timer';

describe('useTimer', () => {
  beforeAll(() => {
    jest.useFakeTimers();
  });

  it('should initialize with 0', () => {
    const { result } = renderHook(() => useTimer());
    expect(result.current.count).toEqual(0);
  });

  it('should increase count every second', () => {
    const { result } = renderHook(() => useTimer());
    for (let i = 1; i <= 10; i++) {
      act(() => jest.advanceTimersByTime(1000));
      expect(result.current.count).toEqual(i);
    }
  });

  afterAll(() => {
    jest.useRealTimers();
  });
});
```

```ts
import { useEffect, useState } from 'react';

export const useTimer = () => {
  const [count, setCount] = useState(0);
  useEffect(() => {
    const timer = setInterval(() => {
      setCount((prev) => prev + 1);
    }, 1000);
    return () => clearInterval(timer);
  }, []);
  return { count };
};
```
