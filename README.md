# Adaptive Learning Agent System

<p align="center">
  <strong>基于多 Agent 协作架构的自适应英语智能学习系统</strong>
</p>

<p align="center">
  通过四个专业化 Agent 协同工作，为每位学生提供个性化的学习诊断、路径规划、AI 辅导和学习评估
</p>

---

## 目录

- [系统架构](#系统架构)
- [核心特性](#核心特性)
- [技术栈](#技术栈)
- [快速开始](#快速开始)
- [项目结构](#项目结构)
- [Agent 模块详解](#agent-模块详解)
  - [Diagnostic Agent (诊断)](#diagnostic-agent-诊断)
  - [Planning Agent (规划)](#planning-agent-规划)
  - [Tutoring Agent (辅导)](#tutoring-agent-辅导)
  - [Assessment Agent (评估)](#assessment-agent-评估)
- [知识图谱](#知识图谱)
- [题库系统](#题库系统)
- [前端功能](#前端功能)
- [API 接口](#api-接口)
- [数据库设计](#数据库设计)
- [核心算法](#核心算法)
- [License](#license)

---

## 系统架构

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│  Diagnostic  │───>│  Planning   │───>│  Tutoring   │───>│ Assessment  │
│    Agent     │    │    Agent    │    │    Agent    │    │    Agent    │
│  (诊断分析)  │    │  (路径规划) │    │  (AI辅导)   │    │  (学习评估) │
└──────┬──────┘    └──────┬──────┘    └──────┬──────┘    └──────┬──────┘
       │                  │                  │                  │
       └──────────────────┴──────────────────┴──────────────────┘
                                   │
                          ┌────────┴────────┐
                          │  Knowledge Graph │
                          │  (34 nodes)      │
                          │  Question Bank   │
                          │  (56 items)      │
                          └─────────────────┘
```

系统采用 **多 Agent 协作架构**，四个专业化 Agent 各司其职，形成完整的自适应学习闭环：

1. **Diagnostic Agent** 分析学生答题数据，定位薄弱知识点
2. **Planning Agent** 基于诊断结果，生成个性化学习路径
3. **Tutoring Agent** 通过 AI 对话进行苏格拉底式启发教学
4. **Assessment Agent** 持续跟踪学习效果，生成评估报告和复习计划

## 核心特性

- **贝叶斯知识追踪 (BKT)**: 实时建模学生对每个知识点的掌握概率，精准定位薄弱环节
- **知识图谱驱动**: 34 个知识点、40+ 条依赖关系构成有向无环图，确保学习路径科学合理
- **苏格拉底式 AI 辅导**: 不直接给答案，通过多轮对话引导学生主动思考，培养独立解题能力
- **间隔重复复习**: 基于 SM-2 算法变体，按紧急度智能调度复习计划
- **长链推理错误分析**: 四步推理链追溯错误根因，从现象到本质
- **答题计时**: 精确记录每道题的作答时长，支持页面切换后的计时保护
- **Apple-Inspired 设计**: 现代化 UI，流畅的入场动画和交互体验

## 技术栈

| 层级 | 技术 | 说明 |
|------|------|------|
| 后端 | Python 3.7+ / Flask | 轻量级 Web 框架 |
| 数据库 | SQLite (WAL 模式) | 零配置，支持并发读 |
| 前端 | HTML + CSS + Vanilla JavaScript | 无框架依赖，轻量高效 |
| 模板引擎 | Jinja2 | Flask 内置模板引擎 |
| AI | OpenAI 兼容 API | 默认 gpt-4o-mini，支持自定义端点 |
| 图标 | Font Awesome 6.5.1 | CDN 加载 |

## 快速开始

### 环境要求

- Python 3.7 或更高版本
- pip

### 安装与运行

**克隆项目**

```bash
git clone https://github.com/your-username/adaptive-learning-agent-system.git
cd adaptive-learning-agent-system/adaptive_learning
```

**安装依赖**

```bash
pip install -r requirements.txt
```

依赖清单：
- `flask>=2.3.0` — Web 框架
- `requests>=2.28.0` — HTTP 请求（AI API 调用）

**启动系统**

```bash
# Linux / macOS
python3 app.py

# Windows
python app.py

# 或使用启动脚本
# Linux / macOS
bash start.sh

# Windows
start.bat
```

启动后访问 **http://localhost:8080**

### AI 辅导功能配置

AI 辅导功能需要 OpenAI 兼容的 API Key。启动系统后：

1. 访问设置页面 (`/settings`)
2. 填写以下配置项：
   - **API Key**: 你的 OpenAI API 密钥
   - **API Base URL**: API 端点地址（默认 `https://api.openai.com/v1`）
   - **模型名称**: 使用的模型（默认 `gpt-4o-mini`）
3. 点击"测试连接"验证配置是否正确
4. 保存设置

支持任何 OpenAI 兼容接口，包括：
- OpenAI 官方 API
- Azure OpenAI
- 本地部署的兼容模型（如 Ollama、vLLM 等）
- 第三方代理服务

## 项目结构

```
adaptive_learning/
├── agents/                        # 四大 Agent 模块
│   ├── diagnostic_agent.py        #   诊断 Agent - BKT 知识追踪 + 长链推理
│   ├── planning_agent.py          #   规划 Agent - 拓扑排序 + 多目标优化
│   ├── tutoring_agent.py          #   辅导 Agent - 苏格拉底式教学 + LLM
│   └── assessment_agent.py        #   评估 Agent - SM-2 间隔重复
├── data/                          # 数据层
│   ├── knowledge_graph.py         #   知识图谱 (34 节点, 39 依赖边)
│   └── question_bank.py           #   题库 (56 道题)
├── static/                        # 静态资源
│   ├── css/
│   │   ├── style.css              #   主样式 (Apple-Inspired 设计系统)
│   │   └── agents.css             #   Agent 介绍页专用样式
│   └── js/
│       ├── main.js                #   主逻辑 (答题、辅导、路径管理)
│       └── agents.js              #   Agent 介绍页交互
├── templates/                     # Jinja2 模板
│   ├── base.html                  #   基础模板
│   ├── landing.html               #   产品介绍页
│   ├── agents.html                #   Agent 详情介绍页
│   ├── index.html                 #   学生管理页
│   ├── dashboard.html             #   学生仪表盘
│   ├── learn.html                 #   学习答题页
│   ├── report.html                #   学习报告页
│   └── settings.html              #   系统设置页
├── app.py                         # Flask 主应用 (入口, 路由 + API)
├── database.py                    # SQLite 数据库模型
├── requirements.txt               # Python 依赖
├── start.sh                       # Linux/macOS 启动脚本
└── start.bat                      # Windows 启动脚本
```

## Agent 模块详解

### Diagnostic Agent (诊断)

**文件**: `agents/diagnostic_agent.py`

诊断 Agent 是系统的"诊断引擎"，负责分析学生的答题数据，结合知识图谱进行多维度能力建模，精准定位薄弱环节。

**核心能力**:

- **贝叶斯知识追踪 (BKT)**: 对每个知识点维护一个掌握概率值，每次作答后根据 BKT 公式更新
- **长链推理错误分析**: 通过四步推理链追溯错误根因

**长链推理流程**:

| 步骤 | 类型 | 说明 |
|------|------|------|
| Step 1 | 观察现象 | 统计该知识点的总作答次数、错误次数、正确率 |
| Step 2 | 分析模式 | 当作答 >= 3 次时，对比前半段与后半段正确率，判断是否有进步趋势 |
| Step 3 | 追溯前置知识 | 检查前置知识点的掌握情况，为基础知识点标注无前置依赖 |
| Step 4 | 定位根因 | 根据掌握概率分级：< 0.3 为"概念理解偏差"，< 0.6 为"应用能力不足"，0 次作答为"尚未开始学习" |

**诊断输出**:

- 薄弱知识点列表（前 10 个，按优先级排序：做过但错的优先 > 低级别优先 > 掌握度低优先）
- 强项知识点列表（掌握概率 >= 0.8 的前 5 个）
- 全部知识点的掌握概率图
- 每个薄弱知识点的四步推理链分析
- 分类改进建议

### Planning Agent (规划)

**文件**: `agents/planning_agent.py`

规划 Agent 基于诊断结果，动态生成个性化学习路径。

**路径生成流程**:

1. **筛选学习节点**: 从诊断结果中选取薄弱知识点，自动补充前置知识（掌握概率 < 0.7 的前置节点）
2. **拓扑排序**: 使用 DFS 算法对所有待学习节点进行拓扑排序，确保前置知识排在前面
3. **多目标优化**: 将节点分为两个阶段，每个阶段内按语法/词汇/阅读三类交替穿插
   - 阶段一：补基础（Level <= 2）
   - 阶段二：提能力（Level >= 3）
4. **生成每日计划**: 每天安排 3 个知识点，每个知识点预计 15 分钟
5. **设置里程碑**: 每完成一定数量的知识点设置里程碑节点

**输出**:

- 优化后的学习路径节点列表
- 每日学习计划（含学习重点和预计时长）
- 里程碑列表
- 预计完成天数

### Tutoring Agent (辅导)

**文件**: `agents/tutoring_agent.py`

辅导 Agent 是系统的"AI 教师"，采用苏格拉底式启发教学法，通过多轮对话引导学生主动思考。

**教学原则**:

1. 绝不直接给出答案 — 通过提问引导学生自己思考
2. 循序渐进 — 从简单到复杂，逐步深入
3. 鼓励为主 — 肯定学生的努力，建立信心
4. 类比讲解 — 用生活中的例子帮助理解抽象概念
5. 错误分析 — 帮助学生理解为什么错了，而不仅仅是告诉正确答案

**教学策略**:

- 学生答错时：先问"你觉得为什么选这个？"，然后引导分析
- 学生困惑时：用类比或举例来说明
- 学生答对时：追问"能解释为什么吗？"来加深理解
- 学生进步时：给予积极反馈，并适当提高难度

**技术实现**:

- 调用 OpenAI 兼容的 Chat Completions API
- 系统提示词中注入当前知识点名称、描述、题目、答案和解析
- 上下文管理：保留系统提示 + 最近 3 轮对话（最多 7 条消息），防止上下文过长
- 独立的知识点讲解功能，100 字以内简洁讲解
- API 参数：`temperature=0.7`（辅导对话）/ `0.5`（概念讲解），`max_tokens=500`，超时 30 秒
- 完善的错误处理：区分 401（Key 无效）、429（频率过高）、404（模型不存在）等状态码

### Assessment Agent (评估)

**文件**: `agents/assessment_agent.py`

评估 Agent 持续跟踪学习效果，生成综合评估报告和科学的复习计划。

**评估维度**:

- 整体掌握进度（已接触知识点数 / 总知识点数）
- 分类掌握率（语法、词汇、阅读三大模块分别统计）
- 答题正确率
- 学习连续天数
- 综合评价等级

**评级标准**:

| 掌握率 | 等级 |
|--------|------|
| >= 0.8 | 优秀 |
| >= 0.6 | 良好 |
| >= 0.4 | 中等 |
| >= 0.2 | 需加强 |
| < 0.2 | 起步阶段 |

**间隔重复复习调度**:

| 掌握概率 | 紧急程度 | 复习间隔 |
|----------|----------|----------|
| < 0.5 | critical | 1 天 |
| >= 0.5 | high | max(1, attempts // 2) 天 |
| >= 0.7 | medium | min(max(attempts, 2), 14) 天 |
| >= 0.9 | low | min(attempts * 2, 30) 天 |

## 知识图谱

系统内置涵盖语法、词汇、阅读三大模块的英语知识图谱，共 **34 个知识点节点** 和 **39 条依赖关系边**，构成有向无环图 (DAG)。

### 知识点分布

| 模块 | 数量 | Level 分布 | 编号范围 |
|------|------|------------|----------|
| 语法 (Grammar) | 16 个 | L1: 5, L2: 3, L3: 3, L4: 3, L5: 2 | G01 - G16 |
| 词汇 (Vocabulary) | 9 个 | L1: 2, L2: 3, L3: 2, L4: 1, L5: 1 | V01 - V09 |
| 阅读 (Reading) | 9 个 | L1: 2, L2: 2, L3: 3, L4: 1, L5: 1 | R01 - R09 |

### 依赖关系类型

- **模块内依赖**: 同一模块内知识点之间的前后关系（如：一般现在时 -> 一般过去时 -> 现在完成时）
- **跨模块依赖**: 不同模块间的知识关联（如：一般现在时 -> 基础阅读理解，定语从句 -> 长难句分析）

### 语法模块知识点示例

| 编号 | 知识点 | Level |
|------|--------|-------|
| G01 | 字母与发音 | 1 |
| G05 | be 动词 | 1 |
| G06 | 一般现在时 | 2 |
| G08 | 一般过去时 | 2 |
| G10 | 现在完成时 | 3 |
| G13 | 定语从句 | 4 |
| G15 | 虚拟语气 | 5 |
| G16 | 非谓语动词 | 5 |

## 题库系统

系统内置 **56 道题目**，覆盖所有 34 个知识点。

### 题目类型

| 类型 | 数量 | 说明 |
|------|------|------|
| 选择题 (choice) | 48 题 | 四选一，含选项和详细解析 |
| 填空题 (fill_blank) | 4 题 | 带有提示的填空题 |
| 阅读理解 (reading) | 6 题 | 含短文、问题和选项 |

### 题目分布

| 知识模块 | 题目数 | 覆盖范围 |
|----------|--------|----------|
| 语法 (G01-G16) | ~34 题 | Level 1-5 |
| 词汇 (V01-V09) | ~14 题 | Level 1-4 |
| 阅读 (R01-R09) | ~8 题 | Level 1-3 |

每道题包含字段：`id`、`knowledge_id`、`type`、`question`、`options`（数组）、`answer`、`explanation`。

## 前端功能

### 答题系统

- **答题计时器**: 实时显示 `MM:SS` 格式的作答时长
- **计时保护**: 页面隐藏超过 5 分钟后恢复时，弹出确认框询问是否继续计时或重置
- **即时反馈**: 提交答案后立即显示正确/错误状态（绿色/红色高亮），展示详细解析
- **掌握度更新**: 每次作答后实时更新知识点掌握概率和进度条

### AI 辅导聊天

- **多轮对话**: 支持与 AI 辅导老师进行连续对话
- **Loading 动画**: 等待 AI 响应时显示加载动画
- **知识点讲解**: 点击知识点可弹出 AI 简洁讲解（100 字以内）
- **自动滚动**: 新消息自动滚动到对话底部

### 学习路径

- **可视化路径**: 展示当前学习路径和每日计划
- **路径重规划**: 支持一键重新生成学习路径（带确认弹窗）

### UI/UX

- **Apple-Inspired 设计系统**: 现代化的配色方案和组件样式
- **入场动画**: 基于 IntersectionObserver，元素进入视口时触发动画
- **Toast 通知**: 3 秒自动消失，支持 info/error/success 类型
- **进度条颜色编码**: >= 80% 绿色, >= 60% 橙色, < 60% 红色
- **响应式设计**: 适配不同屏幕尺寸

## API 接口

### 页面路由

| 路由 | 页面 | 说明 |
|------|------|------|
| `/` | landing.html | 产品介绍页 |
| `/agents` | agents.html | 四 Agent 详情介绍页 |
| `/app` | index.html | 学生列表管理 |
| `/student/<id>` | dashboard.html | 学生仪表盘 |
| `/learn/<id>` | learn.html | 学习答题页面 |
| `/report/<id>` | report.html | 学习报告页面 |
| `/settings` | settings.html | 系统设置页 |

### REST API

| 方法 | 路由 | 说明 | 请求体/参数 |
|------|------|------|-------------|
| POST | `/api/students` | 创建学生 | `{name, level, target}` |
| DELETE | `/api/students/<id>` | 删除学生 | - |
| POST | `/api/answer` | 提交答案（含计时） | `{student_id, question_id, knowledge_id, answer, time_spent}` |
| POST | `/api/tutor/start` | 开始 AI 辅导 | `{student_id, knowledge_id, question_id}` |
| POST | `/api/tutor/continue` | 继续辅导对话 | `{session_id, message}` |
| POST | `/api/tutor/explain` | 讲解知识点 | `{student_id, knowledge_id}` |
| GET | `/api/diagnose/<id>` | 运行完整诊断 | - |
| POST | `/api/plan/<id>` | 生成学习路径 | - |
| POST | `/api/plan/auto/<id>` | 自动生成路径（仅无路径时） | - |
| GET | `/api/progress/<id>` | 获取学习进度 | - |
| GET | `/api/report/<id>` | 获取学习报告 | - |
| POST | `/api/settings` | 保存设置 | `{api_key, api_base, model}` |
| POST | `/api/test_api` | 测试 API 连接 | `{api_key, api_base, model}` |

## 数据库设计

使用 SQLite 轻量级数据库，启用 WAL 模式和外键约束。共 6 张表：

### students (学生表)

| 列名 | 类型 | 说明 |
|------|------|------|
| id | INTEGER PK | 学生 ID |
| name | TEXT NOT NULL | 学生姓名 |
| level | TEXT | 学生级别 (默认 beginner) |
| target | TEXT | 学习目标 |
| created_at | TIMESTAMP | 创建时间 |
| updated_at | TIMESTAMP | 更新时间 |

### knowledge_mastery (知识点掌握情况表)

| 列名 | 类型 | 说明 |
|------|------|------|
| id | INTEGER PK | 主键 |
| student_id | INTEGER FK | 关联学生 |
| knowledge_id | TEXT | 知识点 ID |
| mastery_prob | REAL | 掌握概率 (BKT, 0.0-1.0) |
| attempt_count | INTEGER | 尝试次数 |
| correct_count | INTEGER | 正确次数 |
| last_practiced | TIMESTAMP | 最后练习时间 |
| next_review | TIMESTAMP | 下次复习时间 |

### answer_records (答题记录表)

| 列名 | 类型 | 说明 |
|------|------|------|
| id | INTEGER PK | 主键 |
| student_id | INTEGER FK | 关联学生 |
| question_id | TEXT | 题目 ID |
| knowledge_id | TEXT | 知识点 ID |
| student_answer | TEXT | 学生答案 |
| is_correct | INTEGER | 是否正确 (0/1) |
| time_spent | REAL | 用时 (秒) |
| created_at | TIMESTAMP | 答题时间 |

### learning_paths (学习路径表)

| 列名 | 类型 | 说明 |
|------|------|------|
| id | INTEGER PK | 主键 |
| student_id | INTEGER FK | 关联学生 |
| path_data | TEXT | 路径数据 (JSON) |
| is_active | INTEGER | 是否活跃 (0/1) |
| created_at | TIMESTAMP | 创建时间 |

### tutoring_sessions (辅导会话表)

| 列名 | 类型 | 说明 |
|------|------|------|
| id | INTEGER PK | 主键 |
| student_id | INTEGER FK | 关联学生 |
| knowledge_id | TEXT | 知识点 ID |
| messages | TEXT | 对话消息 (JSON) |
| created_at | TIMESTAMP | 创建时间 |

### settings (系统设置表)

| 列名 | 类型 | 说明 |
|------|------|------|
| key | TEXT PK | 设置键名 |
| value | TEXT | 设置值 |
| updated_at | TIMESTAMP | 更新时间 |

## 核心算法

### 贝叶斯知识追踪 (BKT)

诊断 Agent 使用 BKT 算法对学生每个知识点的掌握概率进行实时建模。

**参数**:

| 参数 | 值 | 含义 |
|------|-----|------|
| p_learn | 0.1 | 每次练习后从"未掌握"到"掌握"的转移概率 |
| p_guess | 0.25 | 未掌握状态下猜对的概率 |
| p_slip | 0.1 | 已掌握状态下答错的概率 |

**更新公式**:

```
答对时: p_known = old_prob * (1 - p_slip) / (old_prob * (1 - p_slip) + (1 - old_prob) * p_guess)
答错时: p_known = old_prob * p_slip / (old_prob * p_slip + (1 - old_prob) * (1 - p_guess))
学习转移: new_prob = p_known + (1 - p_known) * p_learn
```

概率值被钳制在 `[0.0, 1.0]` 范围内。首次作答直接设为 1.0（答对）或 0.0（答错）。

### SM-2 间隔重复

评估 Agent 基于 SM-2 算法变体调度复习计划。根据知识点的掌握概率和练习次数，动态计算复习间隔和紧急程度，确保学生在遗忘临界点前进行复习。

## License

MIT
