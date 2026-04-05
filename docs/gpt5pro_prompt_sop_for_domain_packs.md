# 使用 GPT-5 Pro 产出领域 benchmark 数据包的 Prompt SOP

## 目标
这份 SOP 不是讲人工如何整理会话，而是讲：

> **为了让 GPT-5 Pro 帮我们生成某个领域的 benchmark pack，应该怎么给 prompt。**

目标产物应尽量接近：
- `pathfinder_gui_benchmark_pack_v2_strict.zip`
- 或同类的“领域下包含若干 task，每个 task 有 input/output/reference”的严格数据包

---

## 一、你要让 GPT-5 Pro 做的事，不是泛泛 brainstorm
错误方式：
- “推荐一些适合做 benchmark 的领域”
- “想几个 GUI task”
- “给我一些高质量任务”

这样只会得到松散建议，不会得到可执行 pack。

正确方式：
- 明确要求 GPT-5 Pro **直接输出最终 pack 设计**
- 明确要求它按：
  - `domain`
  - `task`
  - `input`
  - `output`
  - `reference`
  来组织
- 明确要求它给出：
  - 最终保留任务
  - 严格提交格式
  - 评测锚点
  - gold/reference 策略
  - 对应 zip 的目录结构

---

## 二、总原则：一开始就要求“最终答案格式”
每次给 GPT-5 Pro 的 prompt，都要把它锁定在：

1. **不要只列候选，要给最终入选结果**
2. **不要只讲思路，要给可落地目录结构**
3. **不要只讲任务描述，要给 input/output/reference**
4. **不要只讲 judge 思路，要给 machine-verifiable artifacts**
5. **不要混淆公开输入与私有参考答案**
6. **不要把 Python/CLI 可轻易替代的任务算作 GUI benchmark 主体**

---

## 三、推荐的 Prompt 结构

### Prompt 模板 1：领域首轮收敛（从候选到最终入选）
适用于：
- 你已经知道一个领域
- 但还没让 GPT-5 Pro 收敛成最终 task pack

#### 模板
```text
你现在不是在做泛泛 brainstorm，而是在为一个 GUI-heavy benchmark 设计“最终可落地的数据包”。

请围绕下面这个领域，直接给出最终入选任务，而不是宽泛候选清单：

领域：<DOMAIN>

目标：为这个领域设计一个严格 benchmark pack，风格类似 pathfinder_gui_benchmark_pack_v2_strict.zip。

请严格遵守以下要求：
1. 任务必须是高难、强 GUI 依赖、真实工作流。
2. 排除那些可以被 Python/CLI 很快替代的任务。
3. 每个任务都必须有较客观的 machine-verifiable judging anchors。
4. 每个任务必须明确拆成：
   - input
   - output
   - reference
5. output 必须优先依赖结构化导出物（CSV / SQLite / workbook / GeoTIFF / HDF / 原生工程文件），而不是截图。
6. 如果官方没有 final answer，请明确说明需要冻结 private gold bundle。
7. 不要给过多备选；请直接给最终建议保留的 3-8 个任务。

输出格式请严格写成：

# Domain
- domain_id:
- domain_name:
- why_this_domain:

# Final Tasks
对于每个 task，给出：
- task_id
- task_name
- software
- why_keep
- why_not_easily-scriptable
- judging_anchors
- package structure:
  - input/
  - output/
  - reference/

# Cross-task Standard
- 统一 submission 最小 schema
- 统一 scorer contract
- 哪些锚点来自官方
- 哪些需要人工冻结 gold

# Final Recommendation
- 最终保留哪些任务
- 丢弃哪些看似相关但不应纳入 benchmark 的任务，以及原因
```

---

### Prompt 模板 2：把任务包逼成严格 zip 结构
适用于：
- GPT-5 Pro 已经给了一批 task
- 但你现在需要它进一步输出“像 strict.zip 一样”的目录结构

#### 模板
```text
把你刚才给出的领域 benchmark 方案，进一步收敛成一个“严格数据包设计”。

要求：
1. 顶层是一个 domain pack。
2. domain pack 下包含若干 task。
3. 每个 task 都必须严格包含：
   - input/
   - output/
   - reference/
4. 请直接给出接近 zip 解压后的目录树。
5. 对每个文件说明它为什么存在、由谁提供（官方/agent/评测端）。
6. 明确哪些文件是 agent 可见的，哪些是 private。
7. 明确 output 中 agent 必交的文件名，不允许模糊描述。
8. 如果某个任务需要 workbook / native project / exported tables / rasters / shapefiles，请全部列出。
9. 不要只说“等等”“例如”；请尽量枚举完整。

请输出：
- domain pack 顶层目录树
- 每个 task 的完整目录树
- 每个目录/文件的用途说明
- 哪些文件用于评分
- 哪些文件仅用于复核
```

---

### Prompt 模板 3：逼 GPT-5 Pro 给“最终答案”，不要中间推理
适用于：
- 你发现它一直在讨论候选，而不愿收敛

#### 模板
```text
不要继续给候选和开放讨论了。

我现在要的是“最终答案版本”，不是 brainstorming。
请你假设今天就要把这个 benchmark pack 交给工程团队落地，因此必须直接给出：

1. 最终保留的 domain/tasks
2. 每个 task 的 input/output/reference
3. 必交输出文件名
4. 关键 judging anchors
5. 官方公开锚点 vs 私有 gold bundle 的边界
6. 统一 submission schema
7. 统一 scorer I/O 契约

要求：
- 如果有不确定项，用 `TODO:` 显式标注
- 但不要因此回退成泛泛建议
- 尽量给出当前最严格、最可执行的 final spec
```

---

### Prompt 模板 4：要求 GPT-5 Pro 输出 machine-verifiable judge 设计
适用于：
- 你已经有 task 了
- 但 judge 还不够严格

#### 模板
```text
基于你刚才给出的任务包设计，请进一步只做一件事：
为这些任务设计“machine-verifiable 的评分输入和 judge 接口”。

要求：
1. 不要以截图作为主判据。
2. 优先使用 CSV / JSON / SQLite / workbook cells / GeoTIFF / HDF / native project exports。
3. 对每个 task 给出：
   - primary metrics
   - secondary metrics
   - integrity checks
   - task-specific constraints
4. 给出统一的：
   - manifest.json
   - metrics.json
   - artifacts.json
   - scorer output JSON schema
5. 明确 tolerance 的写法。
6. 明确哪些字段必须由 agent 显式提交，而不是让 judge 自己从自然语言里猜。

输出请用工程规范文档风格，不要泛泛描述。
```

---

### Prompt 模板 5：要求 GPT-5 Pro 做跨领域扩展
适用于：
- 你已经有一个成功领域
- 想扩到更多领域，同时保持同一标准

#### 模板
```text
我们已经有一个严格 benchmark pack 的成功案例（风格类似 pathfinder_gui_benchmark_pack_v2_strict.zip）。

现在请你不要重复 Earth Science，而是扩展到更多领域。
要求你直接给出“多个领域的最终答案”，每个领域都按同一标准组织：

- domain
- final tasks
- 每个 task 的 input/output/reference
- 关键 judging anchors
- 统一 submission schema 映射
- 是否需要 private gold bundle

要求：
1. 不要只列领域名，要给出每个领域下最终保留任务。
2. 不要重复已经做过的 Earth Science，除非是作为格式示例。
3. 每个领域优先给 2-5 个真正高价值任务。
4. 排除容易脚本化、难以客观评分、过于开放式的任务。
5. 最终以“可交给工程团队实现”的格式输出。

输出结构：
# Domain 1
# Domain 2
# Domain 3
...
```

---

## 四、推荐的多轮对话策略
单轮 prompt 往往不够，建议用“三段式”。

### Round 1：让它做最终任务收敛
目标：
- 先从一个领域拿到 final tasks
- 不允许只给候选

用模板：
- 模板 1

### Round 2：让它输出严格 pack 结构
目标：
- 把 task 真正压成 `input/output/reference`
- 接近 strict zip

用模板：
- 模板 2
- 模板 3

### Round 3：让它输出评分与 schema
目标：
- 把 judge 和 submission contract 固化

用模板：
- 模板 4

### Round 4：跨领域复制
目标：
- 用已经稳定的格式扩展到更多领域

用模板：
- 模板 5

---

## 五、你在 prompt 里必须反复强调的约束
下面这些约束建议在多轮里反复重复，不然 GPT-5 Pro 很容易退回宽泛建议模式。

### 约束 A：不要只给候选
关键词：
- “直接给最终保留任务”
- “不要输出宽泛候选池”
- “假设今天就要交付给工程团队”

### 约束 B：必须给目录结构
关键词：
- “给接近 zip 解压后的目录树”
- “每个 task 都要有 input/output/reference”
- “必交文件名必须明确”

### 约束 C：必须 machine-verifiable
关键词：
- “不要以截图作为主判据”
- “优先结构化导出物”
- “judge 以可解析文件为主”

### 约束 D：必须区分 public vs private
关键词：
- “哪些给 agent，哪些只给评测端”
- “官方公开锚点 vs 私有冻结 gold bundle”

### 约束 E：排除伪 GUI 任务
关键词：
- “排除可被 Python/CLI 快速替代的任务”
- “GUI 是任务主体，而不是外壳”

---

## 六、一个最实用的主 Prompt（推荐直接复用）
如果你只想给 GPT-5 Pro 一段高密度 prompt，建议直接用这个：

```text
你现在不是在做 brainstorming，而是在为一个 GUI-heavy benchmark 直接输出“最终可落地的数据包设计”。

请围绕以下目标工作：
- 风格参考：pathfinder_gui_benchmark_pack_v2_strict.zip
- 目标：产出一个 domain pack，里面包含若干高质量 task
- 每个 task 必须严格包含：input / output / reference
- output 必须是 machine-verifiable 的，不要以截图作为主判据
- 排除那些可被 Python/CLI 快速替代的任务
- 不要只给候选，请直接给最终保留方案

请按以下结构输出：

# Domain
- domain_id
- domain_name
- why_this_domain

# Final Tasks
对每个 task 给出：
- task_id
- task_name
- software
- why_keep
- why_not_easily_scriptable
- judging_anchors
- input/
- output/
- reference/

# Strict Pack Layout
请给出接近 zip 解压后的目录树，明确每个 task 的完整文件结构。

# Submission Standard
请定义跨任务统一的最小提交规范，至少包括：
- manifest.json
- metrics.json
- artifacts.json
- run_log.txt

# Judge Contract
请定义统一 scorer 输出 JSON 结构、关键 checks、tolerance 写法。

# Provenance
请明确哪些锚点来自官方公开材料，哪些需要人工冻结 private gold bundle。

要求：
- 不要泛泛建议
- 不要只列候选
- 直接给可交付的 final spec
- 如有不确定项，用 TODO: 标出
```

---

## 七、当前最重要的经验教训
这次最大的坑不是“GPT-5 Pro 不够强”，而是：

> **如果 prompt 没把它锁死在 final spec 上，它就很容易停留在候选、讨论、分析层，而不是输出真正能打包的数据结构。**

所以后续任何一轮，只要你发现它开始：
- 扩写背景
- 列很多候选
- 谈优缺点但不收敛
- 不给目录树
- 不给必交文件名

就应该立刻用模板 2 / 模板 3 把它拉回“最终答案模式”。

---

## 八、落地建议
后续实际执行时，建议每个领域固定走这 4 轮：
1. `final tasks`
2. `strict pack layout`
3. `submission + judge contract`
4. `cross-domain normalization`

这样最容易把 GPT-5 Pro 的输出沉淀成真正的 benchmark 数据资产。
