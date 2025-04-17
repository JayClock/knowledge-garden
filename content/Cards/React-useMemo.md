---
date: 2025-04-17T10:36:30
updated: 2025-04-17T11:08:30
up:
  - "[[React-Hooks|React-Hooks]]"
share: true
---
- 背景：如果某个数据时通过其它数据得到的，那么只有当用到的数据，也就是依赖的数据发生变化时，才应该需要重新计算。
	```tsx
	import React, { useState, useEffect } from "react";
	
	export default function SearchUserList() {
	  const [users, setUsers] = useState(null);
	  const [searchKey, setSearchKey] = useState("");
	
	  useEffect(() => {
	    const doFetch = async () => {
	      // 组件首次加载时发请求获取用户数据
	      const res = await fetch("https://reqres.in/api/users/");
	      setUsers(await res.json());
	    };
	    doFetch();
	  }, []);
	  let usersToShow = null;
	
	  if (users) {
	    // 无论组件为何刷新，这里一定会对数组做一次过滤的操作
	    usersToShow = users.data.filter((user) =>
	      user.first_name.includes(searchKey),
	    );
	  }
	
	  return (
	    <div>
	      <input
	        type="text"
	        value={searchKey}
	        onChange={(evt) => setSearchKey(evt.target.value)}
	      />
	      <ul>
	        {usersToShow &&
	          usersToShow.length > 0 &&
	          usersToShow.map((user) => {
	            return <li key={user.id}>{user.first_name}</li>;
	          })}
	      </ul>
	    </div>
	  );
	}
	```
- 如何使用：
	无论组件为何要进行一次重新渲染，实际上都需要进行一次过滤的操作。但其实你只需要在 users 或者 searchKey 这两个状态中的某一个发生变化时，重新计算获得需要展示的数据就行了。
	```tsx
	// 使用 userMemo 缓存计算的结果
	const usersToShow = useMemo(() => {
	    if (!users) return null;
	    return users.data.filter((user) => {
	      return user.first_name.includes(searchKey));
	    }
	  }, [users, searchKey]);
	//...
	```
- 使用 [[./React-useCallback|React-useCallback]] 复现
	```tsx
	 const myEventHandler = useMemo(() => {
	   // 返回一个函数作为缓存结果
	   return () => {
	     // 在这里进行事件处理
	   }
	 }, [dep1, dep2]);
	```
