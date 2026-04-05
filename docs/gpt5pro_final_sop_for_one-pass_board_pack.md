# GPT-5 Pro 最终 SOP：一次产出可交付的 benchmark task files

## 目标
这份 SOP 的目标不是让 GPT-5 Pro 输出一大堆泛泛文档，而是让它尽量一次性产出**每个 task 真正需要的最小交付物**。

你最新明确的最小需求是：

每个 task 只需要：
1. `input` 文件
2. 任务详细要求、输出格式和完美答案应该长什么样（参考现有 prompt 风格）
3. `judger` 评分标准（必须客观、详细到能无脑执行）
4. `reference` 文件（如有）

同时还要满足：
- 找任务的标准必须写进 SOP
- 任务必须极其困难
- 必须依赖 GUI
- 必须是行业里 human expert 真实会做的困难工作流
- 在这个前提下尽量收集全面
- 如果 GPT-5 Pro 不能直接下载 zip/input 文件，则人工手动下载并补齐 input 本体

---

## 一、任务筛选标准（必须先写给 GPT-5 Pro）
在让 GPT-5 Pro 出 task 之前，必须先把筛题标准锁死。

### 硬约束
任务必须同时满足：
1. **极其困难**
   - 不是 beginner tutorial
   - 不是单一按钮演示
   - 不是简单 feature demo
2. **必须依赖复杂 GUI**
   - 核心难点发生在专业 GUI 软件内部
   - 不能主要靠 Python/CLI/脚本轻易替代
3. **是真实职业工作流**
   - 是行业内 human expert 真正会做的复杂工作
   - 不是课堂小游戏、竞赛玩具或纯教学例子
4. **可客观评测**
   - 必须能写出结构化、无脑执行的 judging rules
   - 不能主要依赖截图感受或自由文本总结
5. **输入可获得**
   - 最好有明确直接下载地址
   - 如果 GPT-5 Pro 只能给 URL 而无法下载，则必须把 direct URL 写清楚，后续人工补下载

### 优先保留
- 官方教程/官方 sample project/官方 example workflow
- 官方给了 starter files、sample case、初始工程、教程模型
- 可以导出结构化结果：CSV / JSON / SQLite / workbook / native project / raster / vector / HDF
- 页面本身就提供明确的最终目标、结果值、对比对象或验证逻辑

### 优先剔除
- 只是视频 walkthrough，没有 starter files
- 只是 feature demo，没有真实复杂工作流
- 主要靠脚本或命令行可完成
- 缺少直接输入来源，且无法稳定镜像
- judge 很难客观化
- 结果开放度太高，无法无脑判断对错

---

## 二、每个 task 的最小交付结构
以后不要让 GPT-5 Pro 再发散；每个 task 一律只产出下面这 4 类东西：

```text
<task_id>/
  input/
  task_prompt.txt
  judger_spec.json
  reference/
```

其中：

### 1. input/
放给模型/agent 的输入材料。
应尽量包含：
- starter project / initial files / sample case / tutorial assets
- 若 GPT-5 Pro 无法直接下载，则至少放：
  - `input_manifest.json`
  - 其中明确每个文件的 direct download URL
  - 文件名
  - 来源页面
  - 下载说明

### 2. task_prompt.txt
这是最关键的文件。
它必须把三件事一次写清：
- 任务详细要求
- 输出格式
- 完美答案应该长什么样

也就是说，不再拆成很多散文件；这份 prompt 本身就要足够完整，能直接发给模型做题。

### 3. judger_spec.json
必须是**客观、详细到能无脑执行**的评分标准。
要求：
- 不允许模糊打分
- 不允许主要依赖截图
- 不允许只写“文件存在”这种简单项作为主要分数
- 必须把每个 check 写成结构化规则

### 4. reference/
若需要参考答案、私有 gold 或公开答案文件，就放这里。
可包含：
- `answer_key_public.json`
- `reference_exports/`
- `private_gold_contract.json`
- `reference_manifest.json`

如果该题不需要单独 reference 文件，也要在 `reference/README.md` 里明确写“why no extra reference files are needed”。

---

## 三、task_prompt.txt 必须长什么样
GPT-5 Pro 最容易偷懒的地方，就是 task prompt 只写个任务介绍，不写交付细节。
所以必须强制它按下面结构写。

### task_prompt.txt 强制结构
```text
# Task
- task_id:
- task_name:
- software:
- source:

# Objective
清楚描述当前输入是什么、要做什么、最终完成态是什么。

# Why this is hard and GUI-heavy
说明为什么这个任务必须依赖复杂 GUI，为什么不是脚本题。

# Input files
列出 input/ 下有哪些文件，每个文件的用途是什么。
如果 input 文件没有直接内嵌，必须写 direct download URL。

# Required outputs
明确要求所有输出放在哪里、叫什么、格式是什么。

# Output format requirements
逐文件写清：
- 文件名
- 文件类型
- schema / 列名 / key
- 单位
- 排序要求
- 精度要求
- 允许/不允许的额外字段

# What a perfect answer looks like
这部分必须写“完美答案应该长什么样”，包括：
- 模型/工程状态应满足什么条件
- 哪些关键结果值、关键关系、关键结构必须出现
- 哪些 structured exports 应与参考答案一致或近似一致
- 哪些错误是致命错误

# Submission checklist
给模型一个最终提交前 checklist。
```

### 这里特别强调
你最新指出的点非常对：

> 任务 prompt 里不止要说做什么，还要说 output 的具体格式，以及“完美答案应该长什么样”。

这一步非常关键，因为 judge 再严格，如果 prompt 没把交付长相说清楚，模型也容易交偏。

---

## 四、judger_spec.json 必须长什么样
judger 必须做到：
- 客观
- 细
- 无脑执行

### judger_spec.json 基本结构
```json
{
  "task_id": "...",
  "pass_rule": "...",
  "invalid_if_missing": ["..."],
  "checks": [
    {
      "name": "...",
      "type": "...",
      "points": 20,
      "target_source": "public_answer|reference_file|private_gold",
      "target": "...",
      "tolerance": "...",
      "compare_fields": ["..."],
      "failure_message": "..."
    }
  ]
}
```

### judger 的硬规则
1. **不能主要靠截图**
2. **不能主要靠自然语言 summary**
3. **不能把 files_present 当主要采分点**
4. 缺关键文件应该直接 `invalid_submission`
5. 主要采分点必须来自：
   - native project state
   - structured exports
   - explicit metrics
   - reference matching

### judger 应优先比较什么
- JSON key/value
- CSV row/column/value
- workbook cells
- SQLite queries
- GeoTIFF / raster statistics
- vector geometry / attribute tables
- native project metadata / key parameters

### 如果需要 private gold
那也必须写清楚：
- reference_id
- 对应文件格式
- 比较字段
- 容差
- judge 怎么接

不能出现“judger 规则写了，但没有人知道正确答案在哪”。

---

## 五、reference/ 应该怎么设计
如果一个任务需要参考答案或金标，优先按下面思路整理：

### 公开锚点
如果页面或官方教程已经公开给出答案/结果值/关键关系，就放：
- `reference/answer_key_public.json`

### 可公开 reference exports
如果可以公开放结构化参考结果，就放：
- `reference/reference_exports/...`

### 私有 gold
如果不能公开完整答案，但 judge 又必须依赖 gold，则放：
- `reference/private_gold_contract.json`
- `reference/reference_manifest.json`

这两个文件至少要说明：
- 缺哪些 gold
- gold 应该长什么样
- judge 怎么用它们

---

## 六、关于 input 下载的特殊规则
你刚才指出一个很实际的问题：

> GPT-5 Pro 好像没有下载 zip 文件的能力，所以 input 文件如果给的是地址的话你要手动下载。

所以 SOP 必须明确写：

### 输入获取规则
1. GPT-5 Pro 必须尽量给出**直接下载地址**，而不是模糊页面链接。
2. 如果它无法直接把 zip 本体纳入交付，就必须在 `input/input_manifest.json` 中写清：
   - 文件名
   - direct download URL
   - 来源页面
   - 校验方法（如果能给）
3. 后续由人工/系统手动下载这些 input 文件并放入 `input/`。
4. 如果某个任务拿不到 direct input URL，且资产又不稳定，则该任务应优先 reject，而不是硬保留。

---

## 七、最重要的 prompt 策略
不要再让 GPT-5 Pro 自己决定交付粒度。
直接要求它：

### 你要它做的事
- 先完整扫描一个站点/板块
- 再按严格标准筛题
- 最后只输出每个保留 task 的这四类交付物：
  - `input/`
  - `task_prompt.txt`
  - `judger_spec.json`
  - `reference/`

### 不要它做的事
- 不要泛泛给建议
- 不要只给候选任务列表
- 不要只说“这个网站不错”
- 不要只写 judge 思路，不给答案来源
- 不要给一堆不执行的模板名

---

## 八、给 GPT-5 Pro 的最终 prompt（精简版）
下面这版可以直接喂。

```text
请你围绕 <BOARD_NAME> 这个网站/教程库，做一次完整、高标准、尽量无遗漏的 benchmark task 扫描与打包设计。

筛题标准必须严格满足：
1. 任务必须极其困难；
2. 必须依赖复杂专业 GUI 软件；
3. 必须是行业里 human expert 真实会做的困难工作流；
4. 不能主要靠 Python/CLI/脚本轻易替代；
5. 必须能够设计出客观、无脑执行的 judge；
6. 输入必须可获取，最好给出直接下载地址；
7. 在满足上述条件的前提下，尽量收集全面，不要漏掉高质量任务；
8. beginner tutorial、纯 feature demo、视频 walkthrough、缺乏客观 judge 的任务应 reject。

对每个最终保留的 task，你只需要输出下面四类交付物：

<task_id>/
  input/
  task_prompt.txt
  judger_spec.json
  reference/

具体要求如下：

1. input/
- 尽量包含 starter project / initial files / sample case / tutorial assets。
- 如果你无法直接下载 zip/input 文件，必须写一个 input_manifest.json，里面给出：
  - 文件名
  - direct download URL
  - 来源页面
  - 简短说明

2. task_prompt.txt
必须一次写清：
- 当前输入是什么状态
- 要完成哪些具体工作
- 输出格式是什么
- 每个输出文件的文件名、格式、列名/key、单位、排序、精度
- 完美答案应该长什么样
- 为什么这个任务是 GUI-heavy 且困难

3. judger_spec.json
必须客观、详细到能无脑执行：
- 明确 pass_rule
- 明确 invalid_if_missing
- 每个 check 都要写：
  - check name
  - points
  - compare type
  - target source（public_answer / reference_file / private_gold）
  - target value 或 reference_id
  - tolerance
  - compare fields
- 不允许主要依赖截图
- 不允许只给 files_present 之类简单分

4. reference/
如果需要参考答案、公开锚点或 private gold contract，请放在这里。
至少要说明：
- 哪些是公开答案
- 哪些需要 private gold
- judge 如何接这些 reference

另外，请在输出最前面先给：
- 扫描了哪些页面/教程家族
- 保留了哪些 task
- reject 了哪些 task 以及原因

不要泛泛描述。请用“工程团队可以直接照着实现”的格式输出。
如果有不确定项，用 TODO: 标注，但不要退回成候选清单。
```

---

## 九、实操建议
真正执行时，建议分两步：

### 第一步：让 GPT-5 Pro 只做“扫描 + 保留/拒绝 + task 草单”
先避免它一次输出过长。

### 第二步：再让它只针对保留 task 输出四类交付物
即：
- `input/`
- `task_prompt.txt`
- `judger_spec.json`
- `reference/`

这样更稳，也更容易检查有没有漏 judge 或漏答案对象。

---

## 十、当前最核心的教训
这次最大的经验不是“文件越多越好”，而是：

> **每个 task 真正需要的只是少数几个关键文件，但这几个文件必须写得非常硬。**

特别是：
- `task_prompt.txt` 必须把“输出格式 + 完美答案长相”写清
- `judger_spec.json` 必须把“如何无脑执行”写清
- `reference/` 必须把“答案到底在哪里”写清
- `input/` 如果 GPT 无法下载，就必须给 direct URL 让后处理来补
