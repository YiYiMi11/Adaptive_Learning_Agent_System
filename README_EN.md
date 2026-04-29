# Adaptive Learning Agent System

<p align="center">
  <strong>An Adaptive Intelligent English Learning System Based on Multi-Agent Collaboration</strong>
</p>

<p align="center">
  Four specialized Agents work together to provide personalized learning diagnosis, path planning, AI tutoring, and learning assessment for every student
</p>

<p align="center">
  <a href="./README.md">中文文档</a> | English
</p>

---

## Table of Contents

- [System Architecture](#system-architecture)
- [Key Features](#key-features)
- [Tech Stack](#tech-stack)
- [Quick Start](#quick-start)
- [Project Structure](#project-structure)
- [Agent Modules in Detail](#agent-modules-in-detail)
  - [Diagnostic Agent](#diagnostic-agent)
  - [Planning Agent](#planning-agent)
  - [Tutoring Agent](#tutoring-agent)
  - [Assessment Agent](#assessment-agent)
- [Knowledge Graph](#knowledge-graph)
- [Question Bank](#question-bank)
- [Frontend Features](#frontend-features)
- [API Reference](#api-reference)
- [Database Design](#database-design)
- [Core Algorithms](#core-algorithms)
- [License](#license)

---

## System Architecture

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│  Diagnostic  │───>│  Planning   │───>│  Tutoring   │───>│ Assessment  │
│    Agent     │    │    Agent    │    │    Agent    │    │    Agent    │
│  (Diagnosis) │    │  (Planning) │    │  (Tutoring) │    │ (Assessment)│
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

The system adopts a **multi-agent collaboration architecture** where four specialized Agents each handle their own responsibilities, forming a complete adaptive learning loop:

1. **Diagnostic Agent** analyzes student answer data and identifies weak knowledge points
2. **Planning Agent** generates personalized learning paths based on diagnostic results
3. **Tutoring Agent** provides Socratic-style heuristic teaching through AI dialogue
4. **Assessment Agent** continuously tracks learning progress and generates assessment reports with review schedules

## Key Features

- **Bayesian Knowledge Tracing (BKT)**: Real-time modeling of student mastery probability for each knowledge point, precisely identifying weak areas
- **Knowledge Graph Driven**: 34 knowledge points and 40+ dependency edges form a directed acyclic graph (DAG), ensuring scientifically sound learning paths
- **Socratic AI Tutoring**: Never gives direct answers; guides students to think independently through multi-turn dialogue
- **Spaced Repetition Review**: SM-2 algorithm variant intelligently schedules review plans by urgency level
- **Chain-of-Thought Error Analysis**: Four-step reasoning chain traces error root causes from observation to diagnosis
- **Answer Timer**: Accurately records time spent on each question with timer protection on page switches
- **Apple-Inspired Design**: Modern UI with smooth entrance animations and interactive experience

## Tech Stack

| Layer | Technology | Description |
|-------|------------|-------------|
| Backend | Python 3.7+ / Flask | Lightweight web framework |
| Database | SQLite (WAL mode) | Zero configuration, concurrent read support |
| Frontend | HTML + CSS + Vanilla JavaScript | No framework dependencies, lightweight |
| Template Engine | Jinja2 | Flask built-in template engine |
| AI | OpenAI-compatible API | Default gpt-4o-mini, supports custom endpoints |
| Icons | Font Awesome 6.5.1 | CDN loaded |

## Quick Start

### Prerequisites

- Python 3.7 or higher
- pip

### Installation & Running

**Clone the repository**

```bash
git clone https://github.com/your-username/adaptive-learning-agent-system.git
cd adaptive-learning-agent-system/adaptive_learning
```

**Install dependencies**

```bash
pip install -r requirements.txt
```

Dependencies:
- `flask>=2.3.0` — Web framework
- `requests>=2.28.0` — HTTP requests (AI API calls)

**Start the system**

```bash
# Linux / macOS
python3 app.py

# Windows
python app.py

# Or use startup scripts
# Linux / macOS
bash start.sh

# Windows
start.bat
```

Visit **http://localhost:8080** after startup.

### AI Tutoring Configuration

The AI tutoring feature requires an OpenAI-compatible API Key. After starting the system:

1. Go to the settings page (`/settings`)
2. Fill in the following configuration:
   - **API Key**: Your OpenAI API key
   - **API Base URL**: API endpoint address (default `https://api.openai.com/v1`)
   - **Model Name**: Model to use (default `gpt-4o-mini`)
3. Click "Test Connection" to verify the configuration
4. Save settings

Supports any OpenAI-compatible interface, including:
- OpenAI official API
- Azure OpenAI
- Locally deployed compatible models (e.g., Ollama, vLLM)
- Third-party proxy services

## Project Structure

```
adaptive_learning/
├── agents/                        # Four Agent modules
│   ├── diagnostic_agent.py        #   Diagnostic Agent - BKT + Chain-of-Thought
│   ├── planning_agent.py          #   Planning Agent - Topological Sort + Multi-Objective Optimization
│   ├── tutoring_agent.py          #   Tutoring Agent - Socratic Teaching + LLM
│   └── assessment_agent.py        #   Assessment Agent - SM-2 Spaced Repetition
├── data/                          # Data layer
│   ├── knowledge_graph.py         #   Knowledge graph (34 nodes, 39 dependency edges)
│   └── question_bank.py           #   Question bank (56 questions)
├── static/                        # Static assets
│   ├── css/
│   │   ├── style.css              #   Main styles (Apple-Inspired design system)
│   │   └── agents.css             #   Agent introduction page styles
│   └── js/
│       ├── main.js                #   Main logic (quizzes, tutoring, path management)
│       └── agents.js              #   Agent introduction page interactions
├── templates/                     # Jinja2 templates
│   ├── base.html                  #   Base template
│   ├── landing.html               #   Product landing page
│   ├── agents.html                #   Agent details page
│   ├── index.html                 #   Student management page
│   ├── dashboard.html             #   Student dashboard
│   ├── learn.html                 #   Learning / quiz page
│   ├── report.html                #   Learning report page
│   └── settings.html              #   System settings page
├── app.py                         # Flask main application (entry point, routes + API)
├── database.py                    # SQLite database models
├── requirements.txt               # Python dependencies
├── start.sh                       # Linux/macOS startup script
└── start.bat                      # Windows startup script
```

## Agent Modules in Detail

### Diagnostic Agent

**File**: `agents/diagnostic_agent.py`

The Diagnostic Agent is the system's "diagnostic engine." It analyzes student answer data, combines with the knowledge graph for multi-dimensional capability modeling, and precisely identifies weak areas.

**Core Capabilities**:

- **Bayesian Knowledge Tracing (BKT)**: Maintains a mastery probability value for each knowledge point, updated via BKT formulas after each answer
- **Chain-of-Thought Error Analysis**: Traces error root causes through a four-step reasoning chain

**Chain-of-Thought Reasoning Flow**:

| Step | Type | Description |
|------|------|-------------|
| Step 1 | Observation | Counts total attempts, errors, and accuracy rate for the knowledge point |
| Step 2 | Pattern Analysis | When attempts >= 3, compares first-half vs second-half accuracy to detect improvement trends |
| Step 3 | Prerequisite Check | Checks mastery of prerequisite knowledge points; marks base knowledge points as having no prerequisites |
| Step 4 | Root Cause | Diagnoses by mastery probability: < 0.3 = "conceptual misunderstanding", < 0.6 = "insufficient application ability", 0 attempts = "not yet started" |

**Diagnostic Output**:

- Weak knowledge points list (top 10, sorted by priority: attempted-but-wrong first > lower level first > lower mastery first)
- Strong knowledge points list (top 5 with mastery probability >= 0.8)
- Mastery probability map for all knowledge points
- Four-step reasoning chain analysis for each weak point
- Categorized improvement recommendations

### Planning Agent

**File**: `agents/planning_agent.py`

The Planning Agent dynamically generates personalized learning paths based on diagnostic results.

**Path Generation Process**:

1. **Select Learning Nodes**: Picks weak knowledge points from diagnostic results, automatically adds prerequisites with mastery < 0.7
2. **Topological Sort**: Uses DFS algorithm to topologically sort all nodes to learn, ensuring prerequisites come first
3. **Multi-Objective Optimization**: Splits nodes into two phases, interleaving grammar/vocabulary/reading within each phase
   - Phase 1: Foundation building (Level <= 2)
   - Phase 2: Capability enhancement (Level >= 3)
4. **Generate Daily Plan**: Schedules 3 knowledge points per day, ~15 minutes per point
5. **Set Milestones**: Places milestone markers every certain number of completed knowledge points

**Output**:

- Optimized learning path node list
- Daily learning plan (with focus areas and estimated duration)
- Milestone list
- Estimated completion days

### Tutoring Agent

**File**: `agents/tutoring_agent.py`

The Tutoring Agent is the system's "AI teacher," using Socratic heuristic teaching methods to guide students through multi-turn dialogue.

**Teaching Principles**:

1. Never give direct answers — guide students to think through questioning
2. Progressive approach — from simple to complex, step by step
3. Encouragement first — affirm student effort, build confidence
4. Analogical explanation — use real-life examples to explain abstract concepts
5. Error analysis — help students understand *why* they were wrong, not just tell them the correct answer

**Teaching Strategies**:

- When student answers incorrectly: Ask "Why did you choose this?" first, then guide analysis
- When student is confused: Use analogies or examples to illustrate
- When student answers correctly: Follow up with "Can you explain why?" to deepen understanding
- When student shows progress: Provide positive feedback and appropriately increase difficulty

**Technical Implementation**:

- Calls OpenAI-compatible Chat Completions API
- System prompt injected with current knowledge point name, description, question, answer, and explanation
- Context management: retains system prompt + last 3 conversation turns (max 7 messages) to prevent context overflow
- Standalone knowledge point explanation feature, concise within 100 words
- API parameters: `temperature=0.7` (tutoring dialogue) / `0.5` (concept explanation), `max_tokens=500`, 30s timeout
- Comprehensive error handling: distinguishes 401 (invalid key), 429 (rate limited), 404 (model not found) status codes

### Assessment Agent

**File**: `agents/assessment_agent.py`

The Assessment Agent continuously tracks learning effectiveness, generates comprehensive assessment reports, and creates scientific review schedules.

**Assessment Dimensions**:

- Overall mastery progress (touched knowledge points / total knowledge points)
- Category mastery rates (grammar, vocabulary, reading modules separately)
- Answer accuracy rate
- Learning streak (consecutive days)
- Comprehensive evaluation grade

**Grading Criteria**:

| Mastery Rate | Grade |
|-------------|-------|
| >= 0.8 | Excellent |
| >= 0.6 | Good |
| >= 0.4 | Average |
| >= 0.2 | Needs Improvement |
| < 0.2 | Getting Started |

**Spaced Repetition Review Schedule**:

| Mastery Probability | Urgency | Review Interval |
|--------------------|---------|-----------------|
| < 0.5 | critical | 1 day |
| >= 0.5 | high | max(1, attempts // 2) days |
| >= 0.7 | medium | min(max(attempts, 2), 14) days |
| >= 0.9 | low | min(attempts * 2, 30) days |

## Knowledge Graph

The system includes a built-in English knowledge graph covering three major modules: grammar, vocabulary, and reading, with **34 knowledge point nodes** and **39 dependency edges** forming a directed acyclic graph (DAG).

### Knowledge Point Distribution

| Module | Count | Level Distribution | ID Range |
|--------|-------|--------------------|----------|
| Grammar | 16 | L1: 5, L2: 3, L3: 3, L4: 3, L5: 2 | G01 - G16 |
| Vocabulary | 9 | L1: 2, L2: 3, L3: 2, L4: 1, L5: 1 | V01 - V09 |
| Reading | 9 | L1: 2, L2: 2, L3: 3, L4: 1, L5: 1 | R01 - R09 |

### Dependency Types

- **Intra-module dependencies**: Sequential relationships within the same module (e.g., Simple Present -> Simple Past -> Present Perfect)
- **Cross-module dependencies**: Knowledge connections across modules (e.g., Simple Present -> Basic Reading Comprehension, Relative Clauses -> Complex Sentence Analysis)

### Grammar Module Knowledge Points (Sample)

| ID | Knowledge Point | Level |
|----|----------------|-------|
| G01 | Letters & Pronunciation | 1 |
| G05 | Be Verbs | 1 |
| G06 | Simple Present Tense | 2 |
| G08 | Simple Past Tense | 2 |
| G10 | Present Perfect Tense | 3 |
| G13 | Relative Clauses | 4 |
| G15 | Subjunctive Mood | 5 |
| G16 | Non-finite Verbs | 5 |

## Question Bank

The system includes **56 built-in questions** covering all 34 knowledge points.

### Question Types

| Type | Count | Description |
|------|-------|-------------|
| Multiple Choice (choice) | 48 | Four-option questions with detailed explanations |
| Fill in the Blank (fill_blank) | 4 | Fill-in-the-blank with hints |
| Reading Comprehension (reading) | 6 | Includes passage, questions, and options |

### Question Distribution

| Module | Questions | Coverage |
|--------|-----------|----------|
| Grammar (G01-G16) | ~34 | Level 1-5 |
| Vocabulary (V01-V09) | ~14 | Level 1-4 |
| Reading (R01-R09) | ~8 | Level 1-3 |

Each question contains fields: `id`, `knowledge_id`, `type`, `question`, `options` (array), `answer`, `explanation`.

## Frontend Features

### Quiz System

- **Answer Timer**: Real-time display of elapsed time in `MM:SS` format
- **Timer Protection**: When the page is hidden for more than 5 minutes, a confirmation dialog asks whether to continue or reset the timer
- **Instant Feedback**: Immediately shows correct/incorrect status (green/red highlight) after submission, with detailed explanation
- **Mastery Update**: Real-time update of knowledge point mastery probability and progress bar after each answer

### AI Tutoring Chat

- **Multi-turn Dialogue**: Supports continuous conversation with the AI tutor
- **Loading Animation**: Displays loading animation while waiting for AI response
- **Knowledge Point Explanation**: Click on a knowledge point to get a concise AI explanation (within 100 words)
- **Auto-scroll**: Automatically scrolls to the bottom on new messages

### Learning Path

- **Visual Path**: Displays current learning path and daily plan
- **Path Regeneration**: One-click learning path regeneration (with confirmation dialog)

### UI/UX

- **Apple-Inspired Design System**: Modern color scheme and component styles
- **Entrance Animations**: IntersectionObserver-based animations triggered when elements enter the viewport
- **Toast Notifications**: Auto-dismiss after 3 seconds, supports info/error/success types
- **Progress Bar Color Coding**: >= 80% green, >= 60% orange, < 60% red
- **Responsive Design**: Adapts to different screen sizes

## API Reference

### Page Routes

| Route | Template | Description |
|-------|----------|-------------|
| `/` | landing.html | Product landing page |
| `/agents` | agents.html | Agent details introduction page |
| `/app` | index.html | Student list management |
| `/student/<id>` | dashboard.html | Student dashboard |
| `/learn/<id>` | learn.html | Learning / quiz page |
| `/report/<id>` | report.html | Learning report page |
| `/settings` | settings.html | System settings page |

### REST API

| Method | Route | Description | Request Body/Params |
|--------|-------|-------------|---------------------|
| POST | `/api/students` | Create student | `{name, level, target}` |
| DELETE | `/api/students/<id>` | Delete student | - |
| POST | `/api/answer` | Submit answer (with timer) | `{student_id, question_id, knowledge_id, answer, time_spent}` |
| POST | `/api/tutor/start` | Start AI tutoring | `{student_id, knowledge_id, question_id}` |
| POST | `/api/tutor/continue` | Continue tutoring dialogue | `{session_id, message}` |
| POST | `/api/tutor/explain` | Explain knowledge point | `{student_id, knowledge_id}` |
| GET | `/api/diagnose/<id>` | Run full diagnosis | - |
| POST | `/api/plan/<id>` | Generate learning path | - |
| POST | `/api/plan/auto/<id>` | Auto-generate path (only if none exists) | - |
| GET | `/api/progress/<id>` | Get learning progress | - |
| GET | `/api/report/<id>` | Get learning report | - |
| POST | `/api/settings` | Save settings | `{api_key, api_base, model}` |
| POST | `/api/test_api` | Test API connection | `{api_key, api_base, model}` |

## Database Design

Uses SQLite lightweight database with WAL mode and foreign key constraints. 6 tables total:

### students

| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER PK | Student ID |
| name | TEXT NOT NULL | Student name |
| level | TEXT | Student level (default: beginner) |
| target | TEXT | Learning goal |
| created_at | TIMESTAMP | Creation time |
| updated_at | TIMESTAMP | Update time |

### knowledge_mastery

| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER PK | Primary key |
| student_id | INTEGER FK | Associated student |
| knowledge_id | TEXT | Knowledge point ID |
| mastery_prob | REAL | Mastery probability (BKT, 0.0-1.0) |
| attempt_count | INTEGER | Number of attempts |
| correct_count | INTEGER | Number of correct answers |
| last_practiced | TIMESTAMP | Last practice time |
| next_review | TIMESTAMP | Next review time |

### answer_records

| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER PK | Primary key |
| student_id | INTEGER FK | Associated student |
| question_id | TEXT | Question ID |
| knowledge_id | TEXT | Knowledge point ID |
| student_answer | TEXT | Student's answer |
| is_correct | INTEGER | Whether correct (0/1) |
| time_spent | REAL | Time spent (seconds) |
| created_at | TIMESTAMP | Answer time |

### learning_paths

| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER PK | Primary key |
| student_id | INTEGER FK | Associated student |
| path_data | TEXT | Path data (JSON) |
| is_active | INTEGER | Whether active (0/1) |
| created_at | TIMESTAMP | Creation time |

### tutoring_sessions

| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER PK | Primary key |
| student_id | INTEGER FK | Associated student |
| knowledge_id | TEXT | Knowledge point ID |
| messages | TEXT | Conversation messages (JSON) |
| created_at | TIMESTAMP | Creation time |

### settings

| Column | Type | Description |
|--------|------|-------------|
| key | TEXT PK | Setting key |
| value | TEXT | Setting value |
| updated_at | TIMESTAMP | Update time |

## Core Algorithms

### Bayesian Knowledge Tracing (BKT)

The Diagnostic Agent uses the BKT algorithm to perform real-time modeling of student mastery probability for each knowledge point.

**Parameters**:

| Parameter | Value | Meaning |
|-----------|-------|---------|
| p_learn | 0.1 | Probability of transitioning from "not mastered" to "mastered" after each practice |
| p_guess | 0.25 | Probability of guessing correctly when not mastered |
| p_slip | 0.1 | Probability of answering incorrectly when mastered |

**Update Formulas**:

```
When correct: p_known = old_prob * (1 - p_slip) / (old_prob * (1 - p_slip) + (1 - old_prob) * p_guess)
When incorrect: p_known = old_prob * p_slip / (old_prob * p_slip + (1 - old_prob) * (1 - p_guess))
Learning transfer: new_prob = p_known + (1 - p_known) * p_learn
```

Probability values are clamped to the `[0.0, 1.0]` range. First attempts are set directly to 1.0 (correct) or 0.0 (incorrect).

### SM-2 Spaced Repetition

The Assessment Agent schedules review plans based on an SM-2 algorithm variant. It dynamically calculates review intervals and urgency levels based on mastery probability and practice count, ensuring students review before the forgetting threshold.

## License

MIT
