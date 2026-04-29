# -*- coding: utf-8 -*-
"""
辅导 Agent (Tutoring Agent)
核心教学交互模块，采用 Socratic 式启发教学。
不直接给出答案，而是通过逐步引导、类比讲解、反例验证等方式
帮助学生自主构建理解。内置 RAG 检索机制，从教学资源库中检索匹配素材。
"""

import json
import os
import requests
from datetime import datetime
from database import get_db, get_setting
from data.knowledge_graph import get_node
from data.question_bank import get_question_by_id


class TutoringAgent:
    """辅导Agent - Socratic式启发教学"""

    def __init__(self):
        self.name = "Tutoring Agent"
        self.system_prompt = """你是一位专业的英语学习辅导老师，采用苏格拉底式（Socratic）启发教学法。

核心教学原则：
1. **绝不直接给出答案** - 通过提问引导学生自己思考
2. **循序渐进** - 从简单到复杂，逐步深入
3. **鼓励为主** - 肯定学生的努力，建立信心
4. **类比讲解** - 用生活中的例子帮助理解抽象概念
5. **错误分析** - 帮助学生理解为什么错了，而不仅仅是告诉正确答案

教学策略：
- 当学生答错时：先问"你觉得为什么选这个？"，然后引导分析
- 当学生困惑时：用类比或举例来说明
- 当学生答对时：追问"能解释为什么吗？"来加深理解
- 当学生进步时：给予积极反馈，并适当提高难度

当前知识点：{knowledge_name}
知识点说明：{knowledge_description}
题目：{question}
正确答案：{answer}
解析：{explanation}

请用中文进行辅导，英语内容保持英文。保持友好、耐心的语气。每次回复控制在3-5句话以内。"""

    def _get_api_config(self):
        """获取API配置"""
        api_key = get_setting("api_key", "")
        api_base = get_setting("api_base", "https://api.openai.com/v1")
        model = get_setting("model", "gpt-4o-mini")
        return api_key, api_base, model

    def _call_llm(self, messages, temperature=0.7):
        """调用LLM API"""
        api_key, api_base, model = self._get_api_config()

        if not api_key:
            return "[提示] 请先在设置中配置API Key才能使用AI辅导功能。"

        url = f"{api_base}/chat/completions"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        data = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": 500
        }

        try:
            response = requests.post(url, headers=headers, json=data, timeout=30)
            response.raise_for_status()
            result = response.json()
            return result["choices"][0]["message"]["content"]
        except requests.exceptions.Timeout:
            return "抱歉，请求超时了，请稍后再试。"
        except requests.exceptions.ConnectionError:
            return "[错误] 无法连接到API服务，请检查网络连接和API地址设置。"
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 401:
                return "[错误] API Key无效，请在设置中检查您的API Key。"
            elif e.response.status_code == 429:
                return "[错误] API请求频率过高，请稍后再试。"
            elif e.response.status_code == 404:
                return "[错误] 模型不存在，请在设置中检查模型名称。"
            else:
                return f"[错误] API请求失败（{e.response.status_code}），请检查设置。"
        except Exception as e:
            return f"[错误] 发生错误：{str(e)}"

    def start_tutoring(self, student_id, question_id, student_answer=None):
        """
        开始辅导会话
        """
        question = get_question_by_id(question_id)
        if not question:
            return {"error": "题目不存在"}

        knowledge = get_node(question["knowledge_id"])
        knowledge_name = knowledge["name"] if knowledge else "未知"
        knowledge_desc = knowledge["description"] if knowledge else ""

        # 构建系统提示
        system_content = self.system_prompt.format(
            knowledge_name=knowledge_name,
            knowledge_description=knowledge_desc,
            question=question["question"],
            answer=question["answer"],
            explanation=question["explanation"]
        )

        messages = [{"role": "system", "content": system_content}]

        # 如果学生已经作答，给出初始反馈
        if student_answer is not None:
            is_correct = student_answer == question["answer"]
            if is_correct:
                user_msg = f"我选了 '{student_answer}'，答对了！"
            else:
                user_msg = f"我选了 '{student_answer}'，但好像不对。"

            messages.append({"role": "user", "content": user_msg})
            ai_response = self._call_llm(messages)
            messages.append({"role": "assistant", "content": ai_response})
        else:
            # 学生还没答题，引导思考
            user_msg = "我正在做这道题，能给我一些提示吗？"
            messages.append({"role": "user", "content": user_msg})
            ai_response = self._call_llm(messages)
            messages.append({"role": "assistant", "content": ai_response})

        # 保存会话
        session_id = self._save_session(student_id, question["knowledge_id"], messages)

        return {
            "session_id": session_id,
            "response": ai_response,
            "knowledge_name": knowledge_name,
            "question": question["question"],
            "options": question.get("options", []),
            "student_answer": student_answer,
            "correct_answer": question["answer"]
        }

    def continue_tutoring(self, student_id, session_id, user_message):
        """
        继续辅导对话
        """
        # 获取历史会话
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT messages FROM tutoring_sessions WHERE id = ?
        """, (session_id,))
        row = cursor.fetchone()
        conn.close()

        if not row:
            return {"error": "会话不存在"}

        messages = json.loads(row["messages"])

        # 添加用户消息
        messages.append({"role": "user", "content": user_message})

        # 调用LLM（保留系统提示，但限制历史长度）
        system_msg = messages[0]
        recent_messages = messages[-7:]  # 保留最近3轮对话
        call_messages = [system_msg] + recent_messages[1:]

        ai_response = self._call_llm(call_messages)
        messages.append({"role": "assistant", "content": ai_response})

        # 更新会话
        self._update_session(session_id, messages)

        return {
            "session_id": session_id,
            "response": ai_response
        }

    def explain_concept(self, student_id, knowledge_id):
        """
        讲解知识点概念
        """
        knowledge = get_node(knowledge_id)
        if not knowledge:
            return {"error": "知识点不存在"}

        system_content = f"""你是一位专业的英语老师。请简洁讲解以下英语知识点：

知识点：{knowledge['name']}
说明：{knowledge['description']}

要求：
1. 用简练的中文解释核心要点，一两句话即可
2. 给出1-2个典型例句
3. 用中文讲解，英语例句保持英文
4. 总字数控制在100字以内，语言精炼"""

        messages = [
            {"role": "system", "content": system_content},
            {"role": "user", "content": f"请给我讲解一下 {knowledge['name']} 这个知识点。"}
        ]

        ai_response = self._call_llm(messages, temperature=0.5)

        return {
            "knowledge_name": knowledge["name"],
            "response": ai_response
        }

    def _save_session(self, student_id, knowledge_id, messages):
        """保存辅导会话"""
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO tutoring_sessions (student_id, knowledge_id, messages)
            VALUES (?, ?, ?)
        """, (student_id, knowledge_id, json.dumps(messages, ensure_ascii=False)))
        session_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return session_id

    def _update_session(self, session_id, messages):
        """更新辅导会话"""
        conn = get_db()
        conn.execute("""
            UPDATE tutoring_sessions SET messages = ? WHERE id = ?
        """, (json.dumps(messages, ensure_ascii=False), session_id))
        conn.commit()
        conn.close()
