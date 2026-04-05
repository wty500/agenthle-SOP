# 使用 GPT-5 Pro 获取领域 benchmark 数据的完整 SOP（偏人工整理/回收视角）

## 0. 目标重述
目标不是只做 Earth Science，而是建立一套**可扩展到任意领域**的方法，从 ChatGPT / GPT-5 Pro 的历史对话与产物中，系统提取：
- 每个领域（domain）的**最终答案**
- 每个领域下若干 task 的标准化结构：
  - `input/`
  - `output/`
  - `reference/`
- 以及一套后续可复用的生产流程（SOP），用于继续扩展更多领域。

这里的“最终答案”指的不是对话过程中的中间 brainstorm，而是 GPT-5 Pro 在某一轮收敛后给出的：
- 最终 task 列表
- 每个 task 的输入包、提交包、参考包
- 关键评测锚点
- 必要时的统一 schema / scorer 约定

---

## 1. 核心定义

### 1.1 Domain
一个相对独立的软件/工作流领域，例如：
- Earth Science / Water Resources Modeling
- CAD / 3D Modeling
- GIS / Remote Sensing
- Video Editing
- EDA / PCB
- Bioinformatics GUI workflows
- Finance / Spreadsheet modeling
- Enterprise office workflows

### 1.2 Task
领域内一个可独立评测的 benchmark 单元。
每个 task 理应最终落成：

```text
<task_id>/
  input/
  output/
  reference/
```

其中：
- `input/`：给 agent 的公开起始材料
- `output/`：agent 必须提交的结果格式
- `reference/`：评测端持有的 gold/reference/scorer

### 1.3 Final Answer
某个领域的“最终答案”至少要包含：
1. 领域名
2. task 清单
3. 每个 task 的 `input/output/reference` 结构
4. 关键 judging anchors
5. 需要时的统一输出 schema
6. 需要时的 scorer contract

如果只是在对话里讨论候选、优缺点、草案，而没有稳定落成上述 6 项，则不能算 final answer。

---

## 2. 总流程概览

```text
会话发现
  -> 领域归类
  -> 分支去重与主线识别
  -> 提取 GPT-5 Pro 最终答案
  -> 标准化为 domain pack
  -> 校验是否达到 final-answer 标准
  -> 写入领域索引
  -> 沉淀成可复用 SOP
```

---

## 3. Step-by-step SOP

## Step 1：发现候选会话
来源包括：
- ChatGPT 历史主会话
- ChatGPT 分支会话
- 导出的 zip / workbook / project files
- 中途生成的 markdown 笔记

对每个候选会话先记录最小元数据：
- session_id
- title
- 是否主会话/分支
- 是否可正常打开
- 是否明确提到某一 domain
- 是否出现 task/package/schema/scorer 等关键词
- 是否由 GPT-5 Pro 作答

### 产物
- `session_inventory.csv` 或 `session_inventory.md`

建议字段：
- `session_id`
- `title`
- `model`
- `accessible`
- `suspected_domain`
- `contains_final_answer`
- `notes`

---

## Step 2：完整回看对话，不要提前按单一领域收缩
这是这次教训里最重要的一条。

执行规则：
- 不要因为一个已读分支主要是 Earth Science，就默认整批会话都只属于 Earth Science。
- 必须把同主题下的主线、分支、续聊、打包讨论都重新扫一遍。
- 只有在完成“全量回看”后，才能决定：
  - 是一个领域下多个 task
  - 还是多个领域各自一组 task
  - 或者两者混合

### 判定问题
对每个会话都问：
1. 它在讨论的是候选筛选，还是已收敛的 final packaging？
2. 它有没有提出新领域，而不是只是同一领域的新 task？
3. 它给的是草案，还是最终结构化答案？
4. 它是否引用了类似 `xxx_benchmark_pack_v2_strict.zip` 这种打包范式？

---

## Step 3：做“分支去重 + 主线收敛”
很多 ChatGPT 分支会重复同一批内容，因此需要去重。

### 去重原则
若多个会话满足以下特征，可视作同一主线的不同展开：
- task 名称高度重合
- package skeleton 高度重合
- judging anchors 高度重合
- 只是更换表达方式或增加补充说明

### 主线选择原则
优先把下列会话视为“主内容源”：
- 信息最完整
- 结构最接近最终 pack
- 明确给出 task input/output/reference
- 明确给出关键锚点和评分方法

### 产物
- `session_dedup_map.md`

格式建议：
```markdown
Domain candidate: Earth Science
- canonical session: 69bc1ec8-...
- duplicates:
  - 69b2bcb4-...
- inaccessible but possibly relevant:
  - 69bc1fa6-...
```

---

## Step 4：识别 GPT-5 Pro 的“最终答案”
这是整个流程的核心。

### final answer 判定标准
一个领域只有在满足以下大部分条件时，才算已拿到最终答案：
- 给出稳定的 domain name
- 给出 task 列表
- 每个 task 有明确 `input/output/reference`
- 给出关键判断锚点
- 说明哪些是公开官方材料，哪些需要私有冻结 gold bundle
- 不是纯 brainstorming，而是接近可落地的 pack spec

### 不能算最终答案的情况
- 只有候选任务列表，没有 task 包结构
- 只有评价“这个领域不错”，没有提交格式
- 只有截图型验收，没有 machine-verifiable outputs
- 同一问题还在不同分支里来回推翻，没有收敛版本

### 提取方法
对每个领域汇总为：

```markdown
## Domain: <name>
### Final answer source session(s)
- ...

### Final tasks
1. ...
2. ...

### Per-task package
- task_id:
  - input:
  - output:
  - reference:

### Cross-task conventions
- manifest
- metrics
- artifacts
- scorer contract
```

---

## Step 5：把 final answer 标准化成 domain pack
每个领域单独沉淀成一个领域规范文件。

### 推荐文件
```text
domains/
  <domain_id>/
    domain_overview.md
    tasks/
      <task_id>.md
    pack_schema.json
    scorer_contract.md
    provenance.md
```

### 其中必须包含
#### A. domain_overview.md
- 领域定义
- 最终 task 列表
- 与其它领域的边界
- 来源会话清单

#### B. tasks/<task_id>.md
- 软件栈
- input/output/reference
- judging anchors
- special constraints

#### C. provenance.md
记录来源，避免以后分不清：
- 哪些内容来自 GPT-5 Pro 会话
- 哪些内容来自官方教程/官网 docs
- 哪些内容是后续人工补充冻结的 gold bundle

---

## Step 6：统一跨领域的最小 submission schema
不同领域可有自己的 task-specific artifacts，但跨领域至少要有最小统一层。

### 推荐统一文件
每个 task 的 `output/` 至少要求：
- `manifest.json`
- `metrics.json`
- `artifacts.json`
- `run_log.txt`

### manifest.json
```json
{
  "domain_id": "earth_science",
  "task_id": "ras_merced_2d_refinement",
  "software": "HEC-RAS",
  "software_version": "",
  "submission_version": "1.0",
  "exported_at": "ISO-8601"
}
```

### metrics.json
记录机器可比的核心数值，避免 judge 临场猜。

### artifacts.json
列出原生工程包、导出文件、workbook、数据库、栅格等路径。

注意：
- task-specific summary 允许保留
- 但必须能映射到统一 `metrics.json`

---

## Step 7：区分三类“答案来源”
后续扩展领域时，必须把来源分开写清楚。

### A. GPT-5 Pro final answer
指 GPT-5 Pro 在对话里给出的最终任务结构与判断标准。

### B. Official public anchors
指官方教程、官方 final workbook、官方示例工程、官方答案中的公开锚点。

### C. Frozen private gold bundle
对于官方没有 final package 的任务，需要你们人工跑一次得到 gold，然后冻结为私有 reference。

如果这三类来源混在一起，后面会很难追溯“哪些是 GPT 的建议，哪些是官方事实，哪些是你们自己的 benchmark engineering”。

---

## Step 8：构建“领域索引表”
为了扩展到更多领域，必须有一个总索引，而不是散落在聊天记录里。

### 推荐字段
- `domain_id`
- `domain_name`
- `status`：candidate / in_review / final
- `final_answer_session`
- `task_count`
- `has_pack_schema`
- `has_scorer_contract`
- `has_private_gold_strategy`
- `notes`

### 示例
```markdown
| domain_id | domain_name | status | final_answer_session | task_count | notes |
|---|---|---:|---|---:|---|
| earth_science | Earth Science / Water Resources Modeling | in_review | 69bc1ec8 | 5 | 已有 task 包结构，但跨领域 schema 仍需统一 |
```

---

## Step 9：扩展到更多领域时的复用流程
每加入一个新领域，都重复以下模板：
1. 找到相关 GPT-5 Pro 会话主线与分支
2. 去重并确定 canonical session
3. 提取 final tasks
4. 为每个 task 规范 `input/output/reference`
5. 标注公开锚点 vs 私有 gold
6. 补充统一 schema 映射
7. 进入领域索引表

这样做的重点不是“让 GPT 再想一遍”，而是把 GPT-5 Pro 已经产出的最终答案变成**工程上可复用的数据资产**。

---

## 4. 当前已知结论与边界

### 4.1 当前已知可靠结论
目前工作区里**已被稳定提取**的 GPT-5 Pro final-answer 只覆盖到一个明确领域：
- `Earth Science / Water Resources Modeling`

其已知 final tasks 为：
1. `ras_merced_2d_refinement`
2. `ras_sayers_dam_breach_sensitivity`
3. `hms_schafer_advanced_final`
4. `hms_sayers_pmf_existing_model`
5. `qswat_robit_anchor`

### 4.2 当前还不能下定论的地方
- 目前没有证据表明“整批会话只包含 Earth Science”。
- 也没有证据表明其它领域的 GPT-5 Pro final answers 已经被完整提取到本地笔记中。
- 至少有一个分支会话当前因为 advanced features/model limit 无法正常展开正文，因此存在信息缺口。

### 4.3 因此当前正确表述应为
- 不是“领域只有 Earth Science”；
- 而是“当前本地已稳定提取出的 final answer，明确落在 Earth Science 这一域；其它领域是否存在、其 final answer 是否已被完整读到，仍需继续完整回看原始对话。”

---

## 5. 对你当前需求的直接落地版本
你要的事情可以拆成两个并行目标：

### 目标 A：回收已有 GPT-5 Pro final answers
- 完整回看相关对话
- 按领域提取最终答案
- 每个领域输出为 `domain_overview + task specs + provenance`

### 目标 B：建立以后可复用的获取 SOP
- 固化会话发现、去重、final-answer 判定、标准化打包、统一 schema、provenance 记录
- 用于继续扩到更多领域

---

## 6. 立即执行建议
下一轮实际执行时，建议严格按下面顺序走：

1. 重新完整回看与该主题相关的全部 GPT-5 Pro 会话
2. 对每个会话标注：领域候选 / 是否 final answer / 是否可访问
3. 先产出 `domain index`
4. 再对每个已确认领域产出 `domain_overview.md`
5. 最后再写跨领域统一 `pack_schema.json` 和 `scorer_contract.md`

如果跳过第 1-3 步，直接写领域 spec，很容易再次把“某个分支的子域内容”误写成“全部领域答案”。

---

## 7. 最重要的原则
**不要把“已经读到的 final answer”误当成“全部 final answers”。**

当前最稳妥的方法不是继续猜领域范围，而是：
- 以会话为单位完整回看
- 以领域为单位归档 final answers
- 以 task 为单位沉淀 input/output/reference
- 以 schema 为单位统一 judge 接口

这样后面无论扩到 5 个领域还是 50 个领域，流程都不需要重写。
