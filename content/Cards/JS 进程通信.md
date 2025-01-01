---
date: 2024-10-27T10:44:12
updated: 2024-12-31T18:12:59
share: true
tags:
  - review
---
- 为何需要多进程
	- 多核 CPU，更适合处理多进程
	- 内存较大，多个进程才能更好的利用（单进程有内存上限）
	- “压榨”机器资源，更快，更节省
- 如何开启多进程并通信
	- 使用 `child_process.fork`
		```js
		// 主进程
		const http = require('http')
		const fork = require('child_process').fork
		
		const server = http.createServer(req, res) => {
			if(req.url === '/get-sum') {
				console.info('主进程 id', process.id)
				// 开启子进程
				const computeProcess = fork('./compute.js')
				computeProcess.send('开始计算')
				computeProcess.on('message', data => {
					console.log('主进程接收到的信息：'， data)
					res.send('sum is ' + data)
				})
				conmputeProcess.on('close', () => {
					console.info('子进程因报错而退出')
					computeProcess.kill()
				})		
			}
		}
		```
		
		```js
		// 子进程 compute.js
		function getSum() {
			let sum = 0;
			for (let i = 0; i < 1000000; i++) {
				sum += 1
			}
			return sum
		}
		
		process.on('message', (data) => {
			console.log('子进程 id', process.id)
			console.log('子进程接收到的信息: ', data)
			const sum = getSum()
			// 发送消息给主进程
			process.on(sum)
		})
		```
	- 使用 `cluster`
		```js
		const http = require('http')
		const cpuCoreLength = require('os').cpus().length
		const cluster = require('cluster')
		
		if (cluster.isMaster) {
			for (let i = 0; i< cpuCoreLength; i++) {
				cluster.fork() // 开启子进程
			}
			cluster.on('exit', worker => {
				console.log('子进程')
				cluster.fork() // 进程守护
			})
		} else {
			// 多个子进程会共享一个 TCP 连接，提供一份网络服务
			const server = http.createServer((req, res) => {
				res.writeHead(200)
				res.send('done')
			})
			server.listen(3000)
		}
		```
- 实际工作中使用 [PM2 ](https://www.npmjs.com/package/pm2)


