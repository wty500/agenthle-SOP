# AgentHLE 任务获取 SOP（草案）

## 目标
从公开教程/官方样例中，系统构建一批**高难、强 GUI 依赖、可客观评测**的 benchmark 任务，并将其标准化为统一的数据包、输出包与评分接口。

---

## 一、筛题原则

### 1. 必须满足的硬约束
- 任务不能被 Python / 命令行快速替代。
- 任务必须高强度依赖 GUI 软件或交互式桌面操作。
- 必须存在较客观的验收锚点：
  - 官方数值指标
  - 官方 final project / final zip / workbook
  - 或可冻结的一次性 gold bundle

### 2. 优先保留的任务特征
- 官方教程完整、公开数据稳定可获取
- 软件生态成熟，工程文件可导出
- 结果可通过 CSV / SQLite / HDF / GeoTIFF / 工程文件进行机检
- 即使只用弱 VLM，也能依赖结构化导出物而非截图给出客观判断

### 3. 优先剔除的任务特征
- 本质上可被 Rasterio / xarray / GDAL / WhiteboxTools / CDO / SNAP CLI 等脚本链快速完成
- 官方教程自带 Python/CLI 预处理且该预处理构成任务主体
- 结果开放性太高、路径太多、缺少硬数值锚点，导致 judge 容易主观

---

## 二、任务获取流程

### Step 1：候选任务收集
从官方教程、官方 example project、官方 training manual 收集候选。

每个候选先记录：
- task_id（临时）
- 软件
- 官方来源 URL
- 官方输入包名
- 是否有官方 final zip / workbook
- 是否有明确数值锚点
- 是否有明显 Python / CLI 替代路径

### Step 2：GUI 依赖性审查
对每个候选问 4 个问题：
1. 是否必须在 GUI 中交互建模/编辑/校准？
2. 是否只是“GUI 可做，但 CLI 也能秒做”？
3. 官方教程是否把 Python/CLI 作为主工作流？
4. 如果删去预处理脚本后，剩余核心任务是否仍足够困难？

结论分三类：
- **保留**：强 GUI 依赖，可进入 benchmark
- **保留但裁剪**：需跳过官方的脚本预处理步骤，只保留 GUI 主体
- **剔除**：CLI / Python 可快速替代

### Step 3：评分客观性审查
检查是否存在以下至少一种：
- 官方数值阈值（如 NSE / PBIAS / 峰值流量 / 水位）
- 官方 final project / final workbook / final zip
- 可由熟练工程师跑一次、冻结成 gold bundle 的唯一结果

如果只有截图或视觉判断，没有结构化导出锚点，则不进入首发任务。

### Step 4：标准化为任务包
在包装前，先做一轮 **公开 prompt 防泄题审查**：
- 公开给选手/agent 的任务说明里，禁止出现 `follow tutorial`、`official guide`、`refer to ...`、`according to ...`、教程标题、课程标题、网页标题、`Phase 1–5` / `Part 3` / `Lesson 4` 等可直接定位答案页的表述。
- 公开 prompt 必须写成**显式、闭环、可执行的具体要求列表**，直接给出对象、参数、结构、公式、输出物、截图/导出物要求。
- 官方来源 URL、教程标题、原始截图、gold values 抽取说明，只能保留在私有 `reference/`、`audit` 或内部 SOP 材料中。
- 若一个任务离开教程引用后无法形成闭环要求，则该任务暂不进入可发包集合。

每个任务统一包装为：

```text
<task_id>/
  public/
  submission/
  private/
```

- `public/`：给 agent 的公开输入
- `submission/`：agent 必交输出约定
- `private/`：评测端金标、ROI、scorer，不给 agent

---

## 三、统一数据包规范

### 1. public/
包含：
- 官方原始输入包（尽量保留官方 zip 原名）
- `task.md`：自然语言任务说明
- `export_requirements.md`：要求 agent 必须额外导出的机检文件
- helper/：ROI、参考点、profile line、模板等辅助文件
- templates/：manifest / stats / summary / workbook 模板

**public prompt 写作硬规则：**
- 不得直接暴露官方教程、来源网页、章节/phase 名称、标准答案出处。
- 不得把“follow xxx”当作任务要求本身。
- 必须把真正需要完成的 GUI 操作、关键参数、目标结构、验证输出写完整。
- 目标是：即使选手完全不知道原教程，也能仅凭任务说明理解边界；但又不能从 prompt 直接反查到 gold source。

### 2. submission/
必须同时包含两类东西：

#### A. 原生工程包
例如：
- HEC-RAS：`project.zip`
- HEC-HMS：`hms_project.zip`
- HEC-SSP：`ssp_project.zip`
- QSWAT：`.qgz` / `.sqlite`

#### B. 机检导出包
例如：
- CSV
- SQLite
- HDF/HDF5
- GeoTIFF
- shapefile zip
- JSON summary
- workbook

**原则：评分优先使用导出物，原生工程包用于可打开性和复核，不以截图为主。**

### 3. private/
包含：
- 官方 final zip / workbook（如果官方给了）
- 或人工冻结的一次性 gold bundle
- scorer 脚本
- 私有 ROI / profile / reference files
- gold_metrics.json
- 来源 URL、来源截图、gold 抽取说明、audit 材料

---

## 四、统一输出 schema 设计（关键补强）

你指出的问题是对的：目前已有 SOP 里**缺少统一标准输出和评分标准**，这会导致 judge 乱判。

所以需要补上跨任务统一 schema。

### 1. 顶层统一文件
每个任务 submission 根目录都必须至少包含：
- `manifest.json`
- `metrics.json`
- `artifacts.json`
- `run_log.txt`

### 2. manifest.json（统一身份信息）
建议字段：

```json
{
  "task_id": "ras_merced_2d_refinement",
  "software": "HEC-RAS",
  "software_version": "",
  "submission_version": "1.0",
  "final_plan_name": "",
  "agent_notes": "",
  "exported_at": "ISO-8601"
}
```

### 3. metrics.json（统一评分输入）
要求把所有可比数值显式写出，避免 scorer 自己从自然语言里猜。

```json
{
  "primary_metrics": {
    "peak_stage_ft": null,
    "peak_inflow_cfs": null,
    "peak_outflow_cfs": null,
    "nse": null,
    "pbias": null,
    "rsr": null,
    "rmse": null,
    "iou": null
  },
  "secondary_metrics": {
    "freeboard_ft": null,
    "volume_error_pct": null,
    "arrival_time_minutes": null,
    "annual_maxima_count": null
  }
}
```

### 4. artifacts.json（统一工件索引）

```json
{
  "project_bundle": "submission/project.zip",
  "exports": [
    "submission/exports/reference_point_timeseries_refined.csv",
    "submission/exports/maxdepth_refined.tif"
  ],
  "workbooks": [
    "submission/workbooks/Final_Project_Results.xlsx"
  ]
}
```

### 5. task-specific summary files
保留任务专用 summary，例如：
- `run_summary.json`
- `stats.json`
- `pmf_summary.json`
- `challenge_answers.json`

但这些文件必须映射到统一的 `metrics.json`，避免 judge 为每题单独写大量 ad hoc 解析逻辑。

---

## 五、统一评分框架

### 评分原则
总分建议统一拆成四层：

1. **结构完整性（10-15 分）**
   - 文件齐全
   - 工程可打开
   - 必交导出物存在

2. **核心数值指标（40-60 分）**
   - 与官方锚点或 gold bundle 比较
   - 使用明确容差

3. **曲线/栅格/空间一致性（20-30 分）**
   - RMSE / DTW / IoU / zonal max / area diff

4. **任务特定约束（10-20 分）**
   - 例如 parking lot 必须 dry
   - overtopped 必须 false
   - DWE 到达时间需早于 SWE

### 统一评分接口
每个 scorer 输出：

```json
{
  "task_id": "...",
  "score": 87.5,
  "pass": true,
  "subscores": {
    "integrity": 10,
    "primary_metrics": 45,
    "spatial_or_curve_similarity": 22.5,
    "task_constraints": 10
  },
  "checks": [
    {
      "name": "peak_stage_error",
      "observed": 3963.62,
      "target": 3963.5,
      "tolerance": 0.25,
      "passed": true,
      "score": 30
    }
  ]
}
```

### 明确禁止
- 不允许 judge 主要依赖截图做主判定
- 不允许 judge 从自然语言总结里猜 submission 是否正确
- VLM 最多做：
  - 文件存在性 sanity check
  - UI 截图辅助核验
  - 异常结果辅助解释

---

## 六、首发任务推荐组合（当前版本）

### 主任务 4 个
1. `ras_merced_2d_refinement`
2. `ras_sayers_dam_breach_sensitivity`
3. `hms_schafer_advanced_final`
4. `hms_sayers_pmf_existing_model`

### 锚题 1 个
5. `qswat_robit_anchor`

### 选择理由
- HEC-RAS / HEC-HMS：
  - 难度高
  - GUI 依赖强
  - 工程化强
  - 有数值锚点或可冻结 gold bundle
- QSWAT Robit：
  - 未必最难
  - 但 challenge answers 非常适合作为稳定判分锚题

---

## 七、每题应补充的标准输出要求（你指出的缺口）

当前 ChatGPT 历史会话已经写出了 public/submission/private 的大体结构，**但还没真正把“标准输出”统一好**。必须补以下内容：

### 对每个任务补一份 `output_spec.json`
明确：
- 必交文件名
- 文件格式
- 列名/字段名
- 单位
- 坐标系
- 时间格式
- 缺失值约定

例如 `reference_point_timeseries_refined.csv` 应明示：
- columns: `timestamp`, `stage_ft`
- timestamp timezone / format
- 排序要求
- 是否允许额外列

### 对每个 JSON summary 补字段 schema
例如：
- `run_summary.json`
- `stats.json`
- `pmf_summary.json`
- `challenge_answers.json`

都要写 schema，否则 judger 容易硬编码字符串匹配，最后变得脆弱。

### 对 workbook 任务补“读取单元格映射表”
例如：
- 哪些 sheet
- 哪些 cell
- 容差多少
- 单位是什么

否则 judge 会对 Excel 做随意解析，客观性很差。

---

## 八、当前主动建议的下一步

### 立即该做的 4 件事
1. 为这 5 个任务分别补齐 `output_spec.json`
2. 设计统一 `metrics.json` / `artifacts.json` / `manifest.json`
3. 为每题列出官方可直接下载的数据源与 final zip/workbook 源
4. 区分：
   - **公开官方锚点**
   - **私有冻结 gold bundle**
   - **评分所需私有 ROI / reference geometry**

### 然后再做
5. 写 `benchmark_spec.yaml`
6. 为每题写 scorer I/O 契约
7. 统一 pass/fail 和分数计算方式

---

## 九、当前最重要的判断

补充一条新的硬结论：

> **公开 prompt 不能引用教程来定义任务，必须用显式要求定义任务。**

也就是说：
- 官方教程/官方 guide 可以作为**任务获取来源**，但不能作为**选手 prompt 的显式依赖**。
- benchmark 的任务边界必须在公开 prompt 内自洽闭环。
- 内部 reference 可以保留来源证据；公开 prompt 不能泄露解题路径。

你说的核心问题完全成立：

> 当前 SOP 有任务包框架，但没有统一标准输出和评分输入 schema，导致 judge 容易主观、脆弱、不可复现。

所以接下来真正该补的，不是继续泛泛“找任务”，而是把：
- **任务包结构**
- **标准输出 schema**
- **统一评分接口**
- **gold bundle 策略**
- **公开 prompt 防泄题规则**

这五件事彻底定死。
