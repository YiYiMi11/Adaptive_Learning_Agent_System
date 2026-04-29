# -*- coding: utf-8 -*-
"""
自适应学习Agent系统 - Flask后端主应用
"""

import os
import sys
import random
from flask import Flask, render_template, request, jsonify, redirect, url_for
from datetime import datetime

# 确保项目根目录在路径中
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database import init_db, get_db, get_setting, set_setting
from agents.diagnostic_agent import DiagnosticAgent
from agents.planning_agent import PlanningAgent
from agents.tutoring_agent import TutoringAgent
from agents.assessment_agent import AssessmentAgent
from data.knowledge_graph import KNOWLEDGE_GRAPH, get_node, get_nodes_by_category
from data.question_bank import QUESTION_BANK, get_questions_by_knowledge

app = Flask(__name__)
app.secret_key = 'adaptive-learning-agent-system'

# 初始化Agent
diagnostic_agent = DiagnosticAgent()
planning_agent = PlanningAgent()
tutoring_agent = TutoringAgent()
assessment_agent = AssessmentAgent()


# ==================== 页面路由 ====================

@app.route('/')
def landing():
    """起始页 - Landing Page"""
    return render_template('landing.html')


@app.route('/agents')
def agents():
    """Agent 介绍页"""
    return render_template('agents.html')


@app.route('/app')
def index():
    """首页 - 学生列表或设置页"""
    students = get_all_students()
    api_key = get_setting("api_key", "")
    return render_template('index.html', students=students, has_api_key=bool(api_key))


@app.route('/student/<int:student_id>')
def student_dashboard(student_id):
    """学生仪表盘"""
    student = get_student(student_id)
    if not student:
        return redirect(url_for('index'))

    # 获取学习进度
    progress = assessment_agent.get_overall_progress(student_id)
    report = assessment_agent.generate_report(student_id)
    review_items = assessment_agent.get_review_schedule(student_id)[:5]
    streak = assessment_agent.get_learning_streak(student_id)

    # 获取学习路径
    current_path = planning_agent.get_current_path(student_id)

    return render_template('dashboard.html',
                           student=student,
                           progress=progress,
                           report=report,
                           review_items=review_items,
                           streak=streak,
                           current_path=current_path)


@app.route('/learn/<int:student_id>')
def learn(student_id):
    """学习页面 - 做题和辅导"""
    student = get_student(student_id)
    if not student:
        return redirect(url_for('index'))

    # 获取推荐题目
    diagnosis = diagnostic_agent.diagnose(student_id)
    next_node = planning_agent.get_next_node(student_id, diagnosis)

    if next_node:
        questions = get_questions_by_knowledge(next_node["id"])
        if questions:
            question = random.choice(questions)
        else:
            question = random.choice(QUESTION_BANK)
            next_node = get_node(question["knowledge_id"])
    else:
        question = random.choice(QUESTION_BANK)
        next_node = get_node(question["knowledge_id"])

    knowledge_name = next_node["name"] if next_node else "综合练习"

    return render_template('learn.html',
                           student=student,
                           question=question,
                           knowledge_name=knowledge_name,
                           knowledge_id=next_node["id"] if next_node else "")


@app.route('/report/<int:student_id>')
def report(student_id):
    """学习报告页面"""
    student = get_student(student_id)
    if not student:
        return redirect(url_for('index'))

    report = assessment_agent.generate_report(student_id)
    diagnosis = diagnostic_agent.diagnose(student_id)
    review_schedule = assessment_agent.get_review_schedule(student_id)

    return render_template('report.html',
                           student=student,
                           report=report,
                           diagnosis=diagnosis,
                           review_schedule=review_schedule)


@app.route('/settings')
def settings():
    """设置页面"""
    api_key = get_setting("api_key", "")
    api_base = get_setting("api_base", "https://api.openai.com/v1")
    model = get_setting("model", "gpt-4o-mini")
    return render_template('settings.html',
                           api_key=api_key,
                           api_base=api_base,
                           model=model)


# ==================== API路由 ====================

@app.route('/api/students', methods=['POST'])
def create_student():
    """创建学生"""
    data = request.json
    name = data.get('name', '').strip()
    if not name:
        return jsonify({"error": "请输入学生姓名"}), 400

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO students (name, level, target) VALUES (?, ?, ?)
    """, (name, data.get('level', 'beginner'), data.get('target', '')))
    student_id = cursor.lastrowid
    conn.commit()
    conn.close()

    return jsonify({"id": student_id, "name": name, "message": "创建成功"})


@app.route('/api/students/<int:student_id>', methods=['DELETE'])
def delete_student(student_id):
    """删除学生"""
    conn = get_db()
    conn.execute("DELETE FROM answer_records WHERE student_id=?", (student_id,))
    conn.execute("DELETE FROM knowledge_mastery WHERE student_id=?", (student_id,))
    conn.execute("DELETE FROM learning_paths WHERE student_id=?", (student_id,))
    conn.execute("DELETE FROM tutoring_sessions WHERE student_id=?", (student_id,))
    conn.execute("DELETE FROM students WHERE id=?", (student_id,))
    conn.commit()
    conn.close()
    return jsonify({"message": "删除成功"})


@app.route('/api/answer', methods=['POST'])
def submit_answer():
    """提交答案"""
    data = request.json
    time_spent = data.get('time_spent', 0)
    student_id = data.get('student_id')
    question_id = data.get('question_id')
    student_answer = data.get('answer')

    if not all([student_id, question_id, student_answer]):
        return jsonify({"error": "参数不完整"}), 400

    # 获取题目信息
    from data.question_bank import get_question_by_id
    question = get_question_by_id(question_id)
    if not question:
        return jsonify({"error": "题目不存在"}), 404

    is_correct = student_answer == question["answer"]

    # 保存答题记录
    conn = get_db()
    conn.execute("""
        INSERT INTO answer_records (student_id, question_id, knowledge_id, student_answer, is_correct, time_spent)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (student_id, question_id, question["knowledge_id"], student_answer, is_correct, time_spent))
    conn.commit()
    conn.close()

    # 诊断Agent即时分析
    diagnosis_update = diagnostic_agent.quick_diagnose(student_id, question_id, is_correct)

    return jsonify({
        "is_correct": is_correct,
        "correct_answer": question["answer"],
        "explanation": question["explanation"],
        "diagnosis": diagnosis_update
    })


@app.route('/api/tutor/start', methods=['POST'])
def start_tutoring():
    """开始辅导"""
    data = request.json
    result = tutoring_agent.start_tutoring(
        data.get('student_id'),
        data.get('question_id'),
        data.get('student_answer')
    )
    return jsonify(result)


@app.route('/api/tutor/continue', methods=['POST'])
def continue_tutoring():
    """继续辅导"""
    data = request.json
    result = tutoring_agent.continue_tutoring(
        data.get('student_id'),
        data.get('session_id'),
        data.get('message')
    )
    return jsonify(result)


@app.route('/api/tutor/explain', methods=['POST'])
def explain_concept():
    """讲解知识点"""
    data = request.json
    result = tutoring_agent.explain_concept(
        data.get('student_id'),
        data.get('knowledge_id')
    )
    return jsonify(result)


@app.route('/api/diagnose/<int:student_id>')
def diagnose(student_id):
    """运行诊断"""
    result = diagnostic_agent.diagnose(student_id)
    return jsonify(result)


@app.route('/api/plan/<int:student_id>', methods=['POST'])
def generate_plan(student_id):
    """生成学习路径"""
    diagnosis = diagnostic_agent.diagnose(student_id)
    result = planning_agent.generate_path(student_id, diagnosis)
    return jsonify(result)


@app.route('/api/plan/auto/<int:student_id>', methods=['POST'])
def auto_generate_plan(student_id):
    """自动生成学习路径（仅在无活跃路径时生成）"""
    try:
        # 检查是否已有活跃路径
        existing_path = planning_agent.get_current_path(student_id)
        if existing_path:
            return jsonify({
                "status": "existing",
                "path": existing_path,
                "message": "已有活跃学习路径"
            })

        # 无路径，执行诊断 + 规划
        diagnosis = diagnostic_agent.diagnose(student_id)
        result = planning_agent.generate_path(student_id, diagnosis)

        if result.get("success") or result.get("path"):
            path = result.get("path", [])
            return jsonify({
                "status": "generated",
                "path": path,
                "message": "已生成个性化学习路径"
            })
        else:
            return jsonify({
                "status": "error",
                "message": result.get("message", "路径生成失败")
            })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"路径生成出错：{str(e)}"
        })


@app.route('/api/progress/<int:student_id>')
def get_progress(student_id):
    """获取学生答题进度（轻量级）"""
    progress = assessment_agent.get_overall_progress(student_id)
    return jsonify(progress)


@app.route('/api/report/<int:student_id>')
def get_report(student_id):
    """获取学习报告"""
    result = assessment_agent.generate_report(student_id)
    return jsonify(result)


@app.route('/api/settings', methods=['POST'])
def save_settings():
    """保存设置"""
    data = request.json
    api_key = data.get('api_key', '').strip()
    api_base = data.get('api_base', '').strip()
    model = data.get('model', '').strip()

    if api_key:
        set_setting('api_key', api_key)
    if api_base:
        set_setting('api_base', api_base)
    if model:
        set_setting('model', model)

    # 验证API Key
    if api_key:
        test_result = test_api_connection(api_key, api_base, model)
        return jsonify({
            "message": "设置已保存",
            "test_result": test_result
        })
    else:
        return jsonify({"message": "设置已保存（未配置API Key，AI辅导功能不可用）"})


@app.route('/api/test_api', methods=['POST'])
def test_api():
    """测试API连接"""
    data = request.json
    result = test_api_connection(
        data.get('api_key', ''),
        data.get('api_base', ''),
        data.get('model', '')
    )
    return jsonify(result)


# ==================== 辅助函数 ====================

def get_all_students():
    """获取所有学生"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT s.*, 
               COUNT(ar.id) as total_questions,
               SUM(CASE WHEN ar.is_correct = 1 THEN 1 ELSE 0 END) as correct_questions
        FROM students s
        LEFT JOIN answer_records ar ON s.id = ar.student_id
        GROUP BY s.id
        ORDER BY s.updated_at DESC
    """)
    students = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return students


def get_student(student_id):
    """获取学生信息"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students WHERE id=?", (student_id,))
    student = cursor.fetchone()
    conn.close()
    return dict(student) if student else None


def test_api_connection(api_key, api_base, model):
    """测试API连接"""
    import requests
    try:
        url = f"{api_base}/chat/completions"
        headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
        data = {
            "model": model,
            "messages": [{"role": "user", "content": "Hi"}],
            "max_tokens": 5
        }
        response = requests.post(url, headers=headers, json=data, timeout=10)
        if response.status_code == 200:
            return {"success": True, "message": "API连接成功"}
        elif response.status_code == 401:
            return {"success": False, "message": "API Key无效"}
        elif response.status_code == 404:
            return {"success": False, "message": "模型不存在，请检查模型名称"}
        else:
            return {"success": False, "message": f"API返回错误：{response.status_code}"}
    except requests.exceptions.ConnectionError:
        return {"success": False, "message": "无法连接到API服务器，请检查地址"}
    except Exception as e:
        return {"success": False, "message": f"连接失败：{str(e)}"}


# ==================== 启动 ====================

if __name__ == '__main__':
    init_db()
    print("=" * 50)
    print("  Adaptive Learning Agent System")
    print("  http://localhost:8080")
    print("=" * 50)
    app.run(debug=False, host='0.0.0.0', port=8080)
