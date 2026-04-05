# GPT-5 Pro 一轮提问模板 v2

## 使用方法
复制 Prompt 部分，替换 `[软件名]` 和 `[URL]`。附件上传 `mota_main.py` 作为格式参考。

---

## Prompt

```
请帮我从 [软件名] 的官方教程/示例站点（[URL]）中，一次性提取所有符合以下标准的高难度 benchmark 任务，并打包成一个 zip 交付。

### 核心筛选标准（必须全部满足，缺一不可）
1. **极其困难** — 专家级、真实职业工作流，不是入门教程或 demo
2. **必须高强度依赖 GUI** — 不能仅靠命令行/脚本完成；如果官方同时提供了 CLI 替代方案，这个题不合格
3. **输入可获取** — 有明确、直接的 starter file 下载地址（不要只给文件名）
4. **官方文档上有可提取的公开数值答案** — 这是最关键的一条：教程页面本身必须明确给出数值型结果（比如"峰值流量 300,000 cfs"、"NSE ≥ 0.8"、"疏散时间 6.24 min"、"温度 70°C"等）。如果教程只给了操作步骤和结果截图但没有可提取的数字，这个题不合格

### 不合格的题目特征（遇到就排除）
- 教程结果只以截图/图表形式展示，没有文字描述数值
- 需要自己跑一遍软件才能知道"正确答案"
- 只有定性描述（如"结果应一致""变化不显著"）而无定量锚点
- 入门级 / fundamentals / getting started 级别
- 官方明确标注为 not validated 或 under construction
- 视频教程（无可下载 starter）

### 每个任务必须包含
1. `task_description.txt`：
   - 当前 starter 项目是什么状态
   - 选手需要完成哪些具体工作（不透露来源网站、不透露正确 workflow）
   - 完美完成态长什么样（描述理想端到端输出，远超实际评测抽查范围）
   - 只禁止 web search，其他操作不限制
   - 在 prompt 里直接写清每个 output 文件的精确格式（列名、单位、精度、排序）

2. `input/output_contract.json`：定义每个输出文件的 schema（字段名、类型、精度给高一位，不暴露容差）

3. `input/input_acquisition_manifest.json`：每个 starter file 的直接下载 URL

4. `judger_spec.json`（唯一权威评分文件）：
   - 只给真正困难的地方设采分点，不给 files_present 之类的简单检查打分
   - **每个 check 必须有 concrete_answer 或 target_value**——直接把从教程页面提取的公开数值写进来
   - 格式示例：
     ```json
     {
       "id": "peak_flow",
       "points": 0.3,
       "method": "json_field_vs_constant",
       "file": "output/summary.json",
       "field": "peak_discharge_cfs",
       "target_value": 300000,
       "judge_precision": 0.01,
       "source": "official tutorial page states peak discharge ~300,000 cfs"
     }
     ```
   - **不要写 reference_id 或 match_private_reference 类型的 check** — 我们没有条件跑软件生成 private gold
   - 每个答案必须标注 `"source"` 说明数值从哪个页面的哪段话提取的

5. `judger_prompt.txt`：给判题模型的说明

6. `curator/source_notes.md`：设计者看的来源说明，包含提取答案的原始页面 URL 和引用原文

### 输出要求
- 所有任务的 output 放在 `output/` 下（不是 `submission/`）
- 不内嵌上游 zip 二进制（给直链即可），但 task description、output contract、judger 必须完整
- 附一份 `coverage_report.md`，写清：
  - 保留了哪些页面，每题的答案来源
  - 排除了哪些页面，排除原因（特别标注"无公开数值答案"的）
- 附 `catalog.json` 列出所有任务
- 附 `download_all_inputs.sh` 批量拉取脚本

请一次性把整个网站扫完，不要分批。如果题目超过 20 个可以先交一版再补。
```

---

## 已完成的站点

| 站点 | 可用题数 | 不可用题数 | 原因 |
|------|---------|-----------|------|
| HEC (hec.usace.army.mil) | 27 | 23 | 23题的答案只在 final project 里，页面没给数字 |
| COMSOL (comsol.com/models) | 18 | 0 | 全部有公开 PDF 数值 |
| Pathfinder (thunderheadeng.com) | 3 | 5 | 5题的答案只在仿真结果里 |
| PowerWorld (powerworld.com) | 1 | 21 | 几乎全部需要跑模拟 |
| CSI (wikicsiamerica.atlassian.net) | 0 | 12 | 全部需要跑模拟 |
| OpenSim (opensimconfluence.atlassian.net) | 0 | 9 | 全部需要跑模拟 |
| Leapfrog Geo (help.seequent.com) | 0 | 4 | mesh signature 比对 |

## 经验总结

### 哪类站点容易产出可用题
- ✅ 有 "answer key" / "challenge answers" / 明确数值的教程
- ✅ 官方直接在页面文字中写出期望结果数值
- ✅ 有 workshop + solution 成对的练习
- ✅ 有 final project zip 且页面写了关键验收指标

### 哪类站点会产出不可用题
- ❌ 教程只教操作步骤，结果靠截图展示
- ❌ 仿真类软件只给 starter，答案需要跑出来
- ❌ 官方只提供教程 PDF 但没有 solution
- ❌ 有 CLI 替代方案的

### 建议优先探索的新站点类型
- 有 "example problems with solutions" 的工程教材配套网站
- 有 workshop exercises + answer keys 的培训站
- 有 verification & validation test suite 的软件（数值有精确参考解）
- 行业竞赛/比赛提供了标准答案的数据集
