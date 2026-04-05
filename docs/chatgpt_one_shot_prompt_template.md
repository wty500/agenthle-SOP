# 一轮搞定的 ChatGPT 提问模板

## 使用方法
直接复制下面的 prompt，替换 `[软件名]` 和 `[官方教程站 URL]`。
附件上传 `mota_main.py`（作为格式参考）。

---

## Prompt

```
请帮我从 [软件名] 的官方教程/示例站点（[URL]）中，一次性提取所有符合以下标准的高难度 benchmark 任务，并打包成一个 zip 交付。

### 筛选标准
1. **极其困难** — 专家级、真实职业工作流，不是入门教程
2. **必须高强度依赖 GUI** — 不能仅靠命令行/脚本完成
3. **输入可获取** — 有明确、直接的 starter file 下载地址（不要只给文件名）
4. **judge 客观可执行** — 必须有具体的数值答案或 private gold 对比规则

### 每个任务必须包含
1. `task_description.txt`：
   - 当前 starter 项目是什么状态
   - 选手需要完成哪些具体工作（不透露来源网站、不透露正确 workflow）
   - 完美完成态长什么样（描述理想端到端输出，远超实际评测抽查范围）
   - 只禁止 web search，其他操作不限制
   - 在 prompt 里直接写清每个 output 文件的精确格式（列名、单位、精度、排序）

2. `input/output_contract.json`：定义每个输出文件的 schema（字段名、类型、精度，精度给高一位，不暴露容差）

3. `input/input_acquisition_manifest.json`：每个 starter file 的直接下载 URL

4. `judger_spec.json`（唯一权威评分文件）：
   - 只给真正困难的地方设采分点，不给 files_present 之类的简单检查打分
   - 每个 check 明确写出：读哪个文件、比什么字段、目标值多少、精度多少、占几分
   - 对有公开答案的题直接写 target_value；对需要 private gold 的题写清 reference_id 和 private_gold_requirements

5. `judger_prompt.txt`：给判题模型的说明

6. `curator/source_notes.md`：设计者看的来源说明

### 输出要求
- 所有任务的 output 放在 `output/` 下（不是 `submission/`）
- 不内嵌上游 zip 二进制（给直链即可），但 task description、output contract、judger 必须完整
- 附一份 `coverage_report.md`，写清保留和排除了哪些页面及原因
- 附 `catalog.json` 列出所有任务
- 附 `download_all_inputs.sh` 批量拉取脚本

请一次性把整个网站扫完，不要分批。如果题目超过 20 个可以先交一版再补。
```

---

## 需要扫的站点清单

### 已完成（有权威 zip）
- ✅ Earth Science (hec.usace.army.mil) — 50 题
- ✅ PowerWorld (powerworld.com) — 22 题
- ✅ COMSOL (comsol.com/models) — 18 题
- ✅ CSI (wikicsiamerica.atlassian.net) — 12 题
- ✅ Pathfinder (thunderheadeng.com) — 6 题
- ✅ Leapfrog Geo (help.seequent.com) — 4 题

### 已完成（本轮新扫）
- ✅ OpenSim — opensimconfluence.atlassian.net — 5 题（会话 69c2bfee）
- ✅ Agisoft Metashape — agisoft.com — 4 题（会话 69c2c57d）
- ✅ SNAP — step.esa.int — 4 题（会话 69c2c8d1）；已排除 CLI 可替代流程
