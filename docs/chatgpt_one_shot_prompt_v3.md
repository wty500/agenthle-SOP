# GPT-5 Pro 一轮提问模板 v3

## 使用方法
复制 Prompt 部分，替换 `[行业/领域名]`。附件上传 `mota_main.py` 作为格式参考。

---

## Prompt

```
请帮我在 [行业/领域名] 领域中，找到所有适合做 AI Agent Benchmark 的高难度 GUI 软件任务。自行寻找该领域中有市占率的专业 GUI 软件的官方教程站、培训材料、竞赛、行业 benchmark 等来源，一次性提取所有符合标准的任务，打包成一个 zip 交付。

### 核心筛选标准（必须全部满足）
1. **极其困难** — 专家级、真实职业工作流，不是入门教程或 demo
2. **必须高强度依赖 GUI** — 不能仅靠命令行/脚本完成；如果官方同时提供了 CLI 替代方案，不合格
3. **输入可获取** — 有明确的 starter file 下载方式（直接 URL 或随软件安装提供）
4. **有客观评分依据** — 至少满足以下之一：
   - 教程/文档上有可提取的公开数值答案
   - 有官方 final project / solution 可作为参考截图
   - 有 verification & validation test suite 提供精确参考解
   - 有竞赛/行业 benchmark 提供标准答案
   - 有可截图比对的明确预期结果（judge 有 vision 能力，可以判断结果截图是否与参考一致）

### 每个任务必须包含

#### 1. `task_prompt.md`（给选手的完整 prompt，最重要的文件）
必须写清楚：
- **任务目标**：你要用什么软件做什么事情
- **当前输入状态**：starter 文件是什么、在哪获取
- **具体工作内容**：需要完成哪些步骤（不透露来源网站和正确 workflow 的具体操作细节）
- **交付文件清单**：选手必须提交哪些文件到 `output/`，每个文件的精确格式要求（列名、单位、精度、排序等）
- **满分标准**：完美完成态长什么样——描述一个远超评测抽查范围的理想端到端输出
- **限制**：只禁止 web search，其他操作（脚本、命令行辅助等）不限制

#### 2. `judger_spec.json`（唯一权威评分文件）
- 只给真正困难的地方设采分点，不给 files_present 之类的简单检查打分
- **每个 check 必须有明确的评判标准**，支持以下类型：
  - `target_value`：数值比对（从教程/文档提取的公开数值）
  - `reference_image`：截图比对（从教程页面/PDF 提取的参考结果图，judge 用 vision 判断是否一致）
  - `threshold`：阈值检查（如 NSE ≥ 0.8）
  - `exact_match`：精确匹配（如布尔值、枚举值）
- **不要写 reference_id 或 match_private_reference** — 我们没有条件跑软件生成 private gold
- 每个答案标注 `"source"` 说明从哪提取的

格式示例：
```json
{
  "id": "peak_flow",
  "points": 0.3,
  "method": "json_field_vs_constant",
  "file": "output/summary.json",
  "field": "peak_discharge_cfs",
  "target_value": 300000,
  "judge_precision": 0.01,
  "source": "tutorial page: 'peak discharge is approximately 300,000 cfs'"
}
```

截图比对示例：
```json
{
  "id": "result_plot_match",
  "points": 0.25,
  "method": "vision_compare_to_reference",
  "file": "output/result_plot.png",
  "reference_image": "reference/expected_result_plot.png",
  "criteria": "The submitted plot should show the same curve shape, axis ranges, and key features as the reference",
  "source": "tutorial PDF Figure 4.3"
}
```

#### 3. `judger_prompt.txt`（给判题模型的说明）

#### 4. `reference/`（参考材料，可选）
- 从教程页面/PDF 提取的参考截图
- 公开的 solution 文件
- 官方 final project 的关键导出

#### 5. `input/`（输入文件信息，可选）
- `input_acquisition_manifest.json`：starter file 的下载 URL
- `output_contract.json`：输出 schema（如果在 task_prompt.md 里已经写清楚了，这个可以省略）

#### 6. `curator/source_notes.md`（来源说明）

### 输出要求
- 每个任务一个目录
- 所有选手交付文件放 `output/` 下
- 附 `coverage_report.md`：保留/排除了哪些来源及原因
- 附 `catalog.json`：所有任务列表
- 附 `download_all_inputs.sh`：批量拉取脚本

请一次性扫完该领域所有主流软件的教程站，不要分批。如果题目超过 20 个可以先交一版再补。
```

---

## 推荐的行业/领域列表

可以直接替换 `[行业/领域名]` 使用：

### 已探索过的领域（有产出）
- ✅ 水文/水动力建模 (HEC-RAS/HMS/QSWAT) — 27 可用
- ✅ 多物理场仿真 (COMSOL) — 18 可用
- ✅ 消防/疏散模拟 (Pathfinder) — 3 可用

### 待探索的领域
- 电路设计与仿真 (LTspice / KiCad / Altium)
- 化工流程模拟 (Aspen Plus / DWSIM / CHEMCAD)
- 建筑能耗模拟 (EnergyPlus / DesignBuilder / eQUEST)
- 地理信息系统 (QGIS / ArcGIS)
- 声学分析 (COMSOL Acoustics / Odeon)
- 机器人仿真 (ROS + Gazebo / CoppeliaSim)
- 光学设计 (Zemax OpticStudio / Ansys Lumerical)
- 天文数据处理 (CASA / CIAO)
- 实验心理学 (PsychoPy Builder)
- 精准农业 (QGIS + PAT)
- 核工程 (SNAP / SCALE)
- 船舶/海洋工程 (Maxsurf / MOSES)
- 采矿规划 (Surpac / Micromine / Datamine)
- 石油工程 (Petrel / Eclipse / CMG)

## 经验总结

### 高产出站点特征
- ✅ 有 answer key / challenge answers / 公开数值
- ✅ 页面文字中直接写出期望结果数值
- ✅ 有 workshop + solution 成对练习
- ✅ 有 V&V test suite（数值有精确参考解）
- ✅ 有可截图比对的清晰参考结果图

### 低产出站点特征
- ❌ 教程只教步骤，结果靠截图展示且无参考图可提取
- ❌ 仿真软件只给 starter，答案需要跑出来
- ❌ 有 CLI 替代方案
