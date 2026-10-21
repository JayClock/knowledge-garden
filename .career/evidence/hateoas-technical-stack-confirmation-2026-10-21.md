# HATEOAS 技术栈表述确认｜2026-10-21

## 用户确认与同步授权

用户针对 `content/Knowledge/Outputs/项目介绍：HATEOAS.md` 明确要求：

> 技术栈改为 TypeScript、React Hooks、HAL / HAL-FORMS、Zod、Nx + pnpm、Vite、Vitest、MSW、Testing Library、TypeDoc，所有相关的都更新一下。

## 当前表述

技术栈统一为：**TypeScript、React Hooks、HAL / HAL-FORMS、Zod、Nx + pnpm、Vite、Vitest、MSW、Testing Library、TypeDoc**。

项目介绍、职业经历及已有 Markdown 简历中的清单和相关正文同步采用这一表述。字段校验按“从服务端动作模板生成 Zod 校验规则，在提交前验证数据”表达，保留 JSON Schema 表单描述与运行时校验机制。

本轮属于技术选材与表达更新：Inversify、Immer、Standard Schema 和 vite-plugin-dts 不再作为当前材料的技术栈列项或叙事重点；不据此断言参考源码从未使用这些依赖。原始源码、依赖配置和 2026-10-20 静态核对记录原样保留。

## 同步范围

- 更新 `hateoas.technical-stack` 与运行时字段校验相关表述，保留各自职责、完成状态及已有验证范围。
- 同步 Vault 项目介绍、职业经历、通用 Markdown 简历、HouseSigma Markdown 简历及审核包中的 HATEOAS Markdown 副本。
- 更新相关依赖记录。用户后续追加删除构建工具表述并同步所有素材的要求后，进一步同步现有审核版 Word 和压缩包的技术表述；通用 Word 正在打开，保留原文件并标记待关闭后同步。
- 不改变项目原稿中的其他人工修改、量化成果待核对项、其他项目或历史练习记录；本轮未执行 SDK 构建、测试或性能验证。
