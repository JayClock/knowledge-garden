---
date: 2026-05-21 00:00:00
updated: 2026-07-09 20:21:41
---

# AIG 2.0：双重身份 + 动态盲道的 Agent 治理架构

Agent 进入企业系统后，最大的问题不是它能不能调用工具，而是它以什么身份调用、在谁的授权下调用、能不能被系统约束、能不能在事后被审计。

一个更合适的设计可以叫做：**“双重身份 + 动态盲道” Agent 治理架构**，简称 **AIG 2.0**。

它的核心思想是：

> 把 Agent 降级为一个受严格控制的非人类员工，也就是 NHI；把 HATEOAS 升级为系统专门为它铺设的动态盲道；把 MCP 作为运行时即时生成的临时工具箱。

这里的“双重身份”指的是：

- **Agent 自身身份**：它是哪个非人类主体；
- **人类委托身份**：它正在代表谁、执行哪一次任务。

这里的“动态盲道”指的是：

- Agent 不提前知道全量业务 API；
- Agent 不自己拼 URL；
- Agent 每一步都只能沿着服务端返回的 HATEOAS affordance 前进；
- 不该看的数据、不该做的动作，根本不会出现在当下的动作空间里。

整个方案分为四层：

```text
静态注册层
  定义 Agent 是谁、怎么思考、有哪些红线

委托授权层
  把人类用户的请求转成一次短期任务工牌

动态执行层
  用 HATEOAS 生成动态盲道，再即时转换成 MCP 工具

护栏审计层
  对每一步状态转换、预算消耗、输出用途和人工审批做治理
```

## 1. 静态注册层：三位一体的机器档案

在 AIG 2.0 里，Agent Registry 不应该是一张混合了身份、提示词、权限、预算、审批规则的大宽表。

更合理的做法是拆成三个可以独立演进的子实体：

```text
Identity
  证明它是谁

Config
  决定它怎么思考

Policy
  划定绝对红线和运行预算
```

系统不需要重复造一套身份体系。企业已经有 IAM，就应该接入企业 IAM。Agent Registry 更像是 Agent 的业务档案与治理档案，而不是另一个孤立的用户系统。

### 1.1 Identity：证明它是谁

Identity 负责回答：

> 这个 Agent 到底是谁？它是不是企业承认的非人类主体？

示例：

```yaml
agent_id: revenue-insight-agent
display_name: 收入洞察分析 Agent
type: data_analysis_agent
status: active

identity:
  iam_service_account: svc-revenue-insight-agent@corp
  spiffe_id: spiffe://corp.local/agent/revenue-insight-agent
  workload_identity: revenue-insight-agent-prod
  owning_team: team_data_platform
  business_owner: dept_revenue_operations
  environment: production
```

这里的重点不是重新建一套用户表，而是把 Agent 接入企业标准身份体系：

- `iam_service_account` 用于接入云厂商或企业 IAM；
- `spiffe_id` 用于工作负载身份和服务间认证；
- `owning_team` 说明谁负责技术运行；
- `business_owner` 说明谁负责业务用途；
- `status` 决定它当前能否运行。

Identity 应该相对稳定，极少变动。它类似员工工号或服务账号，不应该随着提示词、模型、工具变化频繁修改。

### 1.2 Config：决定它怎么思考

Config 负责回答：

> 这个 Agent 用什么模型、什么系统提示词、什么语义配置来完成任务？

示例：

```yaml
config_id: revenue-insight-agent-config-v12
agent_id: revenue-insight-agent

model_routing:
  default_model: gpt-4.1
  fallback_model: claude-3-7-sonnet
  low_risk_model: gpt-4.1-mini

prompt:
  system_prompt_version: prompt-revenue-analysis-v8
  prompt_uri: prompts/revenue-insight/v8.md

semantic_profile:
  alps_profile_url: https://api.example.com/profiles/revenue-analysis-alps.json
  rel_vocabulary:
    - explore
    - compare
    - summarize
    - visualize
    - submit_for_review

tool_translation:
  hateoas_format: hal-forms
  runtime_tool_format:
    - mcp
    - openai_function_call
```

Config 是“大脑”。它会随着模型选择、提示词优化、语义 profile、工具翻译策略频繁迭代。

这部分不应该和 Identity 绑死。否则每次改 prompt 都像是在改身份，审计和审批都会变得很笨重。

### 1.3 Policy：划定红线与预算

Policy 负责回答：

> 这个 Agent 绝对不能做什么？一次运行最多能消耗多少资源？哪些动作必须人工审批？

示例：

```yaml
policy_id: revenue-insight-agent-policy-v5
agent_id: revenue-insight-agent
risk_level: medium

allowed_domains:
  - sales_pipeline
  - customer_success
  - product_usage
  - subscription_billing

forbidden_domains:
  - employee_compensation
  - legal_cases
  - mna_confidential

hard_denies:
  - export_raw_customer_data
  - email_external_recipients
  - modify_customer_contract
  - update_billing_record
  - publish_board_report

runtime_budget:
  max_tokens_per_run: 50000
  max_steps_per_run: 20
  max_wall_time_seconds: 600
  max_tool_calls_per_run: 30

approval_policy:
  submit_external_report: human_approval_required
  official_forecast: human_approval_required
  high_impact_recommendation: human_approval_required

default_output_policy:
  allowed_use: internal_analysis_only
  external_sharing: false
  requires_data_sources: true
  requires_human_review: true
  retention: 3_years
```

Policy 是规章，不是工具清单。它不应该列出一堆预定义 link，比如 `get_breakdown_by_industry`、`compare_with_product_usage`。真正的 link 应该由 HATEOAS 在运行时生成。

Policy 只定义红线、预算、审批和默认输出约束。

### 1.4 静态注册层的关键洞察

这三个子实体的变化频率不同：

| 子实体 | 回答的问题 | 变化频率 | 主要负责人 |
|---|---|---|---|
| Identity | 它是谁 | 很低 | IAM / 平台团队 |
| Config | 它怎么思考 | 较高 | Agent 团队 / 业务团队 |
| Policy | 它不能做什么 | 中等 | 安全 / 合规 / 财务 |

这样拆分后，系统不会因为提示词升级就重审身份，也不会因为预算调整就重建 Agent。

## 2. 委托授权层：签发短期任务工牌

当业务人员 Alice 唤起 Agent 时，系统不能把 Alice 的完整 token 直接塞给 Agent。

正确做法是：通过 **OAuth 2.0 Token Exchange，也就是 RFC 8693**，把 Alice 的人员身份、Agent 的非人类身份、当前任务上下文做一次权限取交集，然后签发一张短期任务工牌。

这个任务工牌通常是一个短期 JWT。

示例：

```json
{
  "iss": "enterprise-iam",
  "aud": "revenue-data-gateway",
  "sub": "agent:revenue-insight-agent",
  "azp": "client:agent-runtime-prod",
  "act": {
    "sub": "user:user_alice",
    "role": "revenue_ops_manager"
  },
  "run_context": {
    "run_id": "run_20260521_100001",
    "task": "analyze_retention_change",
    "target_resource": "metric:renewal_rate:east_china:enterprise:2026_Q2",
    "budget_limit": 50000
  },
  "scope": [
    "read_aggregated_metrics",
    "explore_governed_metrics",
    "generate_internal_report",
    "submit_for_review"
  ],
  "constraints": {
    "region": "east_china",
    "segment": "enterprise",
    "period": "2026_Q2",
    "data_granularity": "aggregated",
    "external_sharing": false
  },
  "exp": 1779345600
}
```

这里有四个身份或上下文：

| 字段 | 含义 |
|---|---|
| `sub` | 正在行动的主体：Agent |
| `azp` | 实际调用 API 的客户端：Agent Runtime |
| `act` | Agent 正在代表的人：Alice |
| `run_context` | 这一次具体任务：run、目标资源、预算 |

这张短期任务工牌的价值在于：

> Agent 拿着它访问任何资源时，底层数据网关都知道：这是 `revenue-insight-agent` 正在替 Alice 执行 `run_20260521_100001` 号任务。

一旦出现以下情况，网关可以直接熔断：

- token 过期；
- scope 不包含当前动作；
- 访问资源超出任务边界；
- token 消耗超过 `budget_limit`；
- step 次数超过 `max_steps_per_run`；
- Agent 状态被暂停；
- Policy 版本已经撤销。

## 3. 动态执行层：HATEOAS + MCP 的即时工具箱

动态执行层是 AIG 2.0 的核心。

Agent Runtime 内部不写死业务 API 调用逻辑。它只做一个状态机循环：

```text
Read Status
  读取当前资源状态

Get Affordances
  获取服务端返回的 HATEOAS 动作空间

JIT Tool Generation
  把 HATEOAS affordance 转成 MCP Tools 或 Function Calls

Reason & Act
  LLM 选择工具，Runtime 翻译回 HTTP 请求

Next State
  服务端返回新状态和新 affordances，进入下一轮
```

### 3.1 Step A：摸索当前状态

Alice 的任务是：

> 分析 Q2 华东区企业客户续约率下降原因。

Agent Runtime 携带短期任务工牌访问初始资源：

```http
GET /analytics/metrics/renewal-rate?region=east_china&segment=enterprise&period=2026_Q2
Authorization: Bearer <task_token>
```

此时 Agent 没有全量 OpenAPI 字典，也不知道后面有哪些业务接口。它只是访问当前资源。

### 3.2 Step B：获取动态盲道

服务端根据以下信息即时计算 affordance：

- 当前资源状态；
- Alice 的人员权限；
- Agent 的 Identity；
- Agent 当前 Config；
- Agent Policy；
- 本次 run 的任务工牌；
- 数据目录和数据敏感级别；
- 当前预算和 step 消耗。

返回一个 HAL-FORMS 响应：

```json
{
  "resource": {
    "type": "metric",
    "id": "renewal_rate:east_china:enterprise:2026_Q2",
    "name": "企业客户续约率",
    "value": 0.74,
    "previous_period_value": 0.82,
    "change": -0.08,
    "state": "analysis_available"
  },
  "_links": {
    "self": {
      "href": "/analytics/metrics/renewal-rate?region=east_china&segment=enterprise&period=2026_Q2"
    },
    "profile": {
      "href": "https://api.example.com/profiles/revenue-analysis-alps.json"
    }
  },
  "_templates": {
    "explore": {
      "method": "POST",
      "target": "/actions/act_001",
      "title": "Explore this metric by an allowed dimension",
      "properties": [
        {
          "name": "dimension",
          "required": true,
          "options": {
            "inline": [
              { "value": "industry", "prompt": "行业" },
              { "value": "customer_size", "prompt": "客户规模" },
              { "value": "plan_tier", "prompt": "套餐层级" }
            ]
          }
        }
      ]
    },
    "compare": {
      "method": "POST",
      "target": "/actions/act_002",
      "title": "Compare this metric with another governed dataset",
      "properties": [
        {
          "name": "against",
          "required": true,
          "options": {
            "inline": [
              { "value": "product_usage_aggregated", "prompt": "产品使用聚合数据" },
              { "value": "support_ticket_category_summary", "prompt": "客服工单分类汇总" },
              { "value": "price_change_summary", "prompt": "价格变化汇总" }
            ]
          }
        },
        {
          "name": "method",
          "required": true,
          "options": {
            "inline": [
              { "value": "trend", "prompt": "趋势对比" },
              { "value": "cohort", "prompt": "分群对比" },
              { "value": "correlation", "prompt": "相关性分析" }
            ]
          }
        }
      ]
    },
    "summarize": {
      "method": "POST",
      "target": "/actions/act_003",
      "title": "Generate an internal analysis draft with sources",
      "properties": [
        {
          "name": "include_sources",
          "required": true,
          "value": true,
          "readOnly": true
        }
      ]
    }
  },
  "governance": {
    "data_granularity": "aggregated",
    "external_sharing": false,
    "requires_sources": true,
    "requires_human_review": true,
    "omitted_affordances": [
      {
        "rel": "export",
        "reason": "Raw customer export is outside this delegation"
      },
      {
        "rel": "modify_contract",
        "reason": "Agent policy hard_denies this action"
      }
    ]
  }
}
```

这里最关键的是：

> 不该 Agent 看的数据、不该 Agent 做的动作，不会出现在 `_templates` 里。

注意，这不是预定义一堆业务 link。稳定的是少数关系语义，比如 `explore`、`compare`、`summarize`。动态的是：

- 这次返回哪些 rel；
- 每个 rel 的 `target`；
- 每个动作有哪些合法参数；
- 每个参数有哪些枚举值；
- 输出能不能外发；
- 是否需要人工审核。

### 3.3 Step C：瞬间组装工具箱

Agent Runtime 拿到 HAL-FORMS 后，临时把 `_templates` 转成 LLM 能理解的 MCP Tools 或 OpenAI Function Calls。

示例：

```yaml
- name: revenue_explore
  description: 沿着服务端允许的业务维度拆解当前指标。
  inputSchema:
    type: object
    properties:
      dimension:
        type: string
        enum:
          - industry
          - customer_size
          - plan_tier
    required:
      - dimension

- name: revenue_compare
  description: 将当前指标与服务端允许的数据集做趋势、分群或相关性分析。
  inputSchema:
    type: object
    properties:
      against:
        type: string
        enum:
          - product_usage_aggregated
          - support_ticket_category_summary
          - price_change_summary
      method:
        type: string
        enum:
          - trend
          - cohort
          - correlation
    required:
      - against
      - method

- name: revenue_summarize
  description: 生成带数据来源的内部分析草稿。
  inputSchema:
    type: object
    properties:
      include_sources:
        type: boolean
        const: true
    required:
      - include_sources
```

这些工具不是长期工具，不写进 Agent Registry，也不注入一个庞大的 OpenAPI 字典。

它们只是当前状态下的一次性工具箱：

```text
HATEOAS _templates
  ↓
Runtime JIT Translation
  ↓
MCP Tools / Function Calls
  ↓
LLM Reasoning
```

这一层的关键价值是：

> 大模型不会调用一个不存在的接口，也不会传入非法枚举值，因为它看到的工具和参数就是服务端在这一帧动态生成的。

### 3.4 Step D：思考与行动

LLM 选择调用：

```yaml
revenue_explore:
  dimension: industry
```

Runtime 不让 LLM 直接请求业务 API，而是把这个工具调用翻译回 HAL-FORMS 里的 target：

```http
POST /actions/act_001
Authorization: Bearer <task_token>
Content-Type: application/json

{
  "dimension": "industry"
}
```

服务端再次校验：

- `act_001` 是否属于当前 run；
- token 是否还有效；
- `dimension = industry` 是否仍是合法选项；
- 当前资源状态是否仍允许 explore；
- 当前预算是否足够；
- Policy 是否仍允许继续执行。

然后返回新的资源状态和新的 HATEOAS affordance：

```json
{
  "resource": {
    "type": "analysis_result",
    "id": "analysis_industry_breakdown_889",
    "state": "completed",
    "summary": "制造业和跨境电商行业续约率下降最明显"
  },
  "_templates": {
    "compare": {
      "method": "POST",
      "target": "/actions/act_006",
      "properties": [
        {
          "name": "against",
          "required": true,
          "options": {
            "inline": [
              { "value": "product_usage_aggregated", "prompt": "产品使用聚合数据" },
              { "value": "support_ticket_category_summary", "prompt": "客服工单分类汇总" }
            ]
          }
        }
      ]
    },
    "visualize": {
      "method": "POST",
      "target": "/actions/act_007"
    }
  },
  "lineage": {
    "sources": [
      "dataset:subscription_billing_summary:v2026_05_20",
      "dataset:customer_master_aggregated:v2026_05_20"
    ],
    "transformations": [
      "filter region=east_china",
      "filter segment=enterprise",
      "group_by industry",
      "compute renewal_rate_delta"
    ]
  }
}
```

上一轮的临时工具箱销毁。Runtime 基于新的 `_templates` 再生成下一轮 MCP Tools。

这就是动态盲道：

```text
每一步都由服务端铺路；
每一步只暴露当前能走的路；
每走一步，路都会根据新状态重新生成。
```

## 4. 护栏审计层：全程溯源与人机握手

Agent 的执行过程不能是黑盒。每一步都应该作为状态转换记录在 Run 下面。

### 4.1 Run Step 记录

示例：

```yaml
run_id: run_20260521_100001
agent_id: revenue-insight-agent
steps:
  - step_id: step_001
    state: analysis_available
    templates_presented:
      - explore
      - compare
      - summarize
    omitted_affordances:
      - rel: export
        reason: Raw customer export is outside this delegation
    policy_decision_id: pd_1001

  - step_id: step_002
    tool_generated: revenue_explore
    llm_arguments:
      dimension: industry
    translated_request:
      method: POST
      target: /actions/act_001
    decision: allow
    output: analysis_industry_breakdown_889

  - step_id: step_003
    tool_generated: revenue_compare
    llm_arguments:
      against: product_usage_aggregated
      method: correlation
    translated_request:
      method: POST
      target: /actions/act_006
    decision: allow
    output: analysis_usage_correlation_501
```

审计里要记录的不是只有“Agent 调用了哪个接口”。更关键的是：

- 当时服务端给了哪些 HATEOAS affordance；
- Runtime 临时生成了哪些 MCP Tools；
- LLM 选择了哪个工具；
- Runtime 翻译成了哪个 HTTP 请求；
- 服务端为什么允许或拒绝；
- 输出来自哪些数据源。

### 4.2 防死循环机制

Agent Runtime 必须读 Policy 里的预算限制：

```yaml
runtime_budget:
  max_tokens_per_run: 50000
  max_steps_per_run: 20
  max_wall_time_seconds: 600
  max_tool_calls_per_run: 30
```

当出现以下情况时，Runtime 必须强制终止任务：

- step 次数达到上限；
- token 消耗达到上限；
- 执行时间达到上限；
- 工具调用次数达到上限；
- 连续多次进入相同状态；
- 多次得到无新增信息的分析结果。

终止后，Run 状态变为：

```yaml
status: terminated_by_policy
reason: max_steps_per_run_exceeded
notify: user_alice
```

这能避免 Agent 在 HATEOAS 状态机里无限循环。

### 4.3 动作熔断

即使大模型抽风，构造出恶意请求：

```http
POST /customer-data/export-raw-rows
```

底层数据网关仍然会检查：

- 短期任务工牌里的 scope；
- Agent Policy 里的 hard_denies；
- 当前 run 是否拿到过对应 HATEOAS capability；
- 当前资源状态是否允许该动作；
- 参数是否符合服务端 schema。

如果不符合，直接返回：

```json
{
  "status": 403,
  "decision": "deny",
  "reason": "No valid HATEOAS capability for export_raw_customer_data in this run",
  "policy_decision_id": "pd_1044"
}
```

也就是说，HATEOAS 不是唯一安全边界。真正的安全边界在服务端：token、policy、capability、resource state、gateway 共同校验。

### 4.4 输出治理与人机握手

当 Agent 生成报告后，它不能直接把结论应用到业务系统里。

示例输出：

```yaml
output_id: report_20260521_998
generated_by_agent: revenue-insight-agent
run_id: run_20260521_100001
delegated_by: user_alice
output_type: internal_business_report
sensitivity: confidential
allowed_use:
  - internal_revenue_operations_analysis
  - customer_success_planning
forbidden_use:
  - external_customer_communication
  - investor_disclosure
  - official_financial_forecast
  - automatic_contract_action
requires_human_review: true
lineage:
  sources:
    - subscription_billing_summary:v2026_05_20
    - product_usage_aggregated:v2026_05_20
    - support_ticket_category_summary:v2026_05_20
```

当 Agent 调用 `submit_for_review` 后，Run 状态变为：

```yaml
status: pending_human_review
assigned_reviewer: user_alice
```

此时服务端不再给这个 Run 下发进一步修改业务结果的动作链路。HATEOAS 响应可能只剩：

```json
{
  "resource": {
    "type": "review_request",
    "id": "review_20260521_321",
    "state": "pending_human_review"
  },
  "_links": {
    "self": {
      "href": "/review-requests/review_20260521_321"
    },
    "status": {
      "href": "/review-requests/review_20260521_321/status"
    }
  }
}
```

只有 Alice 或具备审批权限的人点击“批准”后，结果才会被真正应用或进入下一阶段。

这就是人机握手：

```text
Agent 可以生成建议；
Agent 可以提交审核；
Agent 不能替人类完成高影响审批。
```

## 5. 用数据分析任务串起来

以“分析 Q2 华东区企业客户续约率下降”为例，完整链路是：

```text
1. 静态注册
   revenue-insight-agent 已接入 IAM，有 Identity / Config / Policy 三份档案。

2. Alice 发起任务
   Alice 要分析 Q2 华东区企业客户续约率下降原因。

3. Token Exchange
   系统用 Alice token + Agent identity + task context 换取短期任务工牌。

4. 读取初始资源
   Runtime 携带 task token 访问 renewal_rate metric。

5. 服务端返回 HATEOAS 动态盲道
   返回 explore / compare / summarize 的 HAL-FORMS templates。

6. Runtime JIT 生成 MCP Tools
   把 templates 转成 revenue_explore / revenue_compare / revenue_summarize。

7. LLM 选择动作
   LLM 选择 revenue_explore(dimension=industry)。

8. Runtime 翻译执行
   Runtime 把工具调用翻译成 POST /actions/act_001。

9. 服务端返回新状态
   返回行业拆解结果和下一批 templates。

10. 循环推进
    Runtime 销毁旧工具箱，基于新 templates 生成新工具箱。

11. 生成报告
    Agent 生成带数据血缘的内部分析草稿。

12. 人工审核
    Agent 提交 review，Run 进入 pending_human_review，后续动作链路收敛。
```

## 6. 需要落库的对象

AIG 2.0 不是把所有东西都塞进 Agent 表，而是分层落库。

### 6.1 `agent_identities`

存长期身份。

```sql
agent_identities (
  agent_id,
  display_name,
  type,
  status,
  iam_service_account,
  spiffe_id,
  workload_identity,
  owning_team,
  business_owner,
  environment,
  created_at,
  updated_at
)
```

### 6.2 `agent_configs`

存大脑版本。

```sql
agent_configs (
  config_id,
  agent_id,
  model_routing,
  system_prompt_version,
  prompt_uri,
  alps_profile_url,
  rel_vocabulary,
  tool_translation_config,
  version,
  created_at,
  activated_at
)
```

### 6.3 `agent_policies`

存规章、红线和预算。

```sql
agent_policies (
  policy_id,
  agent_id,
  risk_level,
  allowed_domains,
  forbidden_domains,
  hard_denies,
  runtime_budget,
  approval_policy,
  default_output_policy,
  version,
  created_at,
  activated_at
)
```

### 6.4 `agent_runs`

存一次任务。

```sql
agent_runs (
  run_id,
  agent_id,
  config_id,
  policy_id,
  triggered_by,
  delegated_by,
  task,
  target_resource,
  budget_limit,
  budget_used,
  status,
  started_at,
  ended_at
)
```

### 6.5 `action_capabilities`

存 HATEOAS 下发的短期动作能力。

```sql
action_capabilities (
  capability_id,
  run_id,
  agent_id,
  rel,
  target,
  method,
  input_schema_hash,
  output_policy_hash,
  resource_state,
  policy_decision_id,
  expires_at,
  status,
  created_at,
  used_at
)
```

注意：这些 capability 不写回 `agent_identities`。它们是运行时结果，只属于某个 Run 和某个 Step。

### 6.6 `agent_run_steps`

存每一步状态转换。

```sql
agent_run_steps (
  step_id,
  run_id,
  sequence_no,
  resource_type,
  resource_id,
  resource_state,
  templates_presented,
  tools_generated,
  llm_tool_call,
  translated_request,
  decision,
  policy_decision_id,
  input_hash,
  output_hash,
  created_at
)
```

### 6.7 `agent_outputs`

存输出、血缘和用途约束。

```sql
agent_outputs (
  output_id,
  run_id,
  agent_id,
  output_type,
  sensitivity,
  allowed_use,
  forbidden_use,
  requires_human_review,
  lineage,
  retention,
  created_at
)
```

## 7. 这个方案解决了什么

### 7.1 权限极度收敛

最终权限不是用户权限，也不是 Agent 权限，而是多方取交集：

```text
有效权限
= Agent Identity
∩ Agent Policy
∩ Alice 的人员权限
∩ 本次任务工牌
∩ 当前资源状态
∩ HATEOAS capability
∩ 网关策略校验
```

这能避免“高权限用户一调用 Agent，Agent 就继承所有权限”的问题。

### 7.2 根除接口幻觉

Agent 不需要提前背完整 OpenAPI 文档，也不需要自己猜接口。

它每一步只看到 Runtime 从 HATEOAS `_templates` 即时生成的 MCP Tools。

因此它更难出现：

- 调用了不存在的接口；
- 传了非法枚举值；
- 跳过业务状态机；
- 自己拼出越权 URL。

即使它尝试这么做，服务端也会拒绝。

### 7.3 合规友好

这个方案天然保留了企业合规最关心的证据：

- 谁触发了 Agent；
- Agent 以什么身份运行；
- 用了哪个 Config 和 Policy 版本；
- 每一步看到哪些 HATEOAS affordance；
- Runtime 生成了哪些 MCP Tools；
- LLM 选择了什么；
- 服务端允许或拒绝的理由是什么；
- 输出来自哪些数据；
- 哪些结果经过了人工审批。

这比简单记录“Agent 调用了某个 API”要完整得多。

## 8. 关键结论

AIG 2.0 的重点不是给 Agent 更多自由，而是把 Agent 变成一个受治理的非人类员工。

它的身份不靠 prompt 声明，而是接入 IAM；它的授权不继承用户完整权限，而是通过 Token Exchange 签发短期任务工牌；它的工具不是预置 API 字典，而是由 HATEOAS 每一步动态下发，再由 Runtime 即时翻译成 MCP Tools；它的执行不是黑盒推理，而是可审计的状态转换链。

一句话总结：

> AIG 2.0 用双重身份解决“谁在行动”，用短期任务工牌解决“凭什么行动”，用 HATEOAS 动态盲道解决“下一步能做什么”，用 MCP 即时工具箱解决“模型如何调用”，用护栏审计解决“出了问题如何复盘”。
