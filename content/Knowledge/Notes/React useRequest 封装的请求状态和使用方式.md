---
date: 2025-05-19T09:47:18
noteId: 1778930949893
updated: 2026-07-09 11:00:29
---
React useRequest 适合封装什么请求状态，如何使用？

---

```ts
import { useState, useEffect } from 'react'

function useRequest(url) {
  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    const fetchData = async () => {
      setLoading(true)
      setError(null)

      try {
        const response = await fetch(url)
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`)
        }
        const result = await response.json()
        setData(result)
      } catch (e) {
        setError(e)
      } finally {
        setLoading(false)
      }
    }

    fetchData()
  }, [url])

  return { data, loading, error }
}

export default useRequest
```
