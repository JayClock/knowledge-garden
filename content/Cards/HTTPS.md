---
date: 2025-05-10T22:45:27
updated: 2025-05-12T22:25:13
share: true
---
- HTTP协议采用**明文传输**信息，存在**信息窃听**、**信息篡改**和**信息劫持**的风险，而协议TLS/SSL具有**身份验证**、**信息加密**和**完整性校验**的功能，可以避免此类问题发生。
	![HTTP VS HTTPS](https://knowledge-garden.oss-cn-shanghai.aliyuncs.com/images/HTTP%20VS%20HTTPS.png)
- 如何加解密：
	- 对称加密的密钥需要明文传输
	- 非对称加密性能不够
	- 最终采用将对称加密的密钥使⽤⾮对称加密的公钥进⾏加密，然后发送出去，接收⽅使⽤私钥进⾏解密得到对称加密的密钥，然后双⽅可以使⽤对称加密来进⾏沟通
	![完整的 HTTPS 请求流程](https://knowledge-garden.oss-cn-shanghai.aliyuncs.com/images/%E5%AE%8C%E6%95%B4%E7%9A%84%20HTTPS%20%E8%AF%B7%E6%B1%82%E6%B5%81%E7%A8%8B.png)
- 另一个问题：黑客通过 DNS 劫持将访问地址换成了黑客地址，需要服务器向浏览器证明“我就是我”
	- 数字证书用于**服务器向浏览器证明身份**和传递公钥