# -*- coding: utf-8 -*-
"""
诊断 Agent (Diagnostic Agent)
分析学生答题数据、错题模式，结合知识图谱进行多维度能力建模，
精准定位学生在知识体系中的薄弱节点。使用长链推理追溯错误根因。
"""

import json
from datetime import datetime
from database import get_db
from data.knowledge_graph import (
    get_node, get_prerequisites, get_dependents,
    KNOWLEDGE_GRAPH
)


class DiagnosticAgent:
    """诊断Agent - 分析学生能力，定位薄弱环节"""

    def __init__(self):
        self.name = "Diagnostic Agent"

    def diagnose(self, student_id):
        """
        对学生进行全面诊断
        返回：{
            "weak_nodes": [...],        # 薄弱知识点
            "strong_nodes": [...],      # 掌握良好的知识点
            "mastery_map": {...},       # 所有知识点的掌握概率
            "error_analysis": {...},    # 错误分析
            "recommendations": [...]    # 改进建议
        }
        """
        conn = get_db()
        cursor = conn.cursor()

        # 1. 获取学生所有答题记录
        cursor.execute("""
            SELECT knowledge_id, question_id, is_correct, created_at
            FROM answer_records
            WHERE student_id = ?
            ORDER BY created_at
        """, (student_id,))
        records = [dict(row) for row in cursor.fetchall()]

        # 2. 获取当前掌握情况
        cursor.execute("""
            SELECT knowledge_id, mastery_prob, attempt_count, correct_count
            FROM knowledge_mastery
            WHERE student_id = ?
        """, (student_id,))
        mastery_rows = [dict(row) for row in cursor.fetchall()]

        conn.close()

        # 3. 构建掌握概率图
        mastery_map = {}
        for row in mastery_rows:
            mastery_map[row["knowledge_id"]] = {
                "prob": row["mastery_prob"],
                "attempts": row["attempt_count"],
                "correct": row["correct_count"]
            }

        # 4. 长链推理分析 - 追溯错误根因
        weak_nodes = []
        strong_nodes = []
        error_analysis = {}

        for node in KNOWLEDGE_GRAPH["nodes"]:
            kid = node["id"]
            if kid in mastery_map:
                prob = mastery_map[kid]["prob"]
                if prob < 0.6:
                    weak_nodes.append({
                        "id": kid,
                        "name": node["name"],
                        "mastery_prob": prob,
                        "category": node["category"],
                        "level": node["level"],
                        "attempts": mastery_map[kid]["attempts"],
                        "correct": mastery_map[kid]["correct"]
                    })
                elif prob >= 0.8:
                    strong_nodes.append({
                        "id": kid,
                        "name": node["name"],
                        "mastery_prob": prob,
                        "category": node["category"],
                        "level": node["level"]
                    })
            else:
                # 未接触的知识点，标记为需要学习
                weak_nodes.append({
                    "id": kid,
                    "name": node["name"],
                    "mastery_prob": 0.0,
                    "category": node["category"],
                    "level": node["level"],
                    "attempts": 0,
                    "correct": 0,
                    "status": "not_started"
                })

        # 5. 错误根因分析（Chain-of-Thought推理）
        for weak in weak_nodes:
            if weak.get("status") == "not_started":
                continue

            kid = weak["id"]
            # 获取该知识点的答题记录
            node_records = [r for r in records if r["knowledge_id"] == kid]
            total = len(node_records)
            wrong = sum(1 for r in node_records if not r["is_correct"])

            # 推理链：分析错误原因
            reasoning_chain = self._analyze_error_reasoning(kid, weak, node_records)
            error_analysis[kid] = reasoning_chain

        # 6. 按优先级排序薄弱节点
        weak_nodes.sort(key=lambda x: (
            -x["attempts"] if x.get("attempts", 0) > 0 else 0,  # 做过但错的优先
            x["level"],  # 低级别优先
            x["mastery_prob"]  # 掌握度低的优先
        ))

        # 7. 生成改进建议
        recommendations = self._generate_recommendations(weak_nodes, mastery_map)

        return {
            "weak_nodes": weak_nodes[:10],  # 返回前10个最需要改进的
            "strong_nodes": strong_nodes[:5],
            "mastery_map": mastery_map,
            "error_analysis": error_analysis,
            "recommendations": recommendations,
            "total_questions": len(records),
            "correct_rate": sum(1 for r in records if r["is_correct"]) / max(len(records), 1)
        }

    def _analyze_error_reasoning(self, knowledge_id, weak_info, records):
        """
        长链推理：分析错误根因
        推理链：观察现象 → 分析模式 → 追溯原因 → 定位根因
        """
        chain = []

        # Step 1: 观察现象
        total = len(records)
        wrong = sum(1 for r in records if not r["is_correct"])
        chain.append({
            "step": 1,
            "type": "observation",
            "content": f"知识点 [{weak_info['name']}] 共作答 {total} 次，错误 {wrong} 次，正确率 {weak_info['mastery_prob']*100:.0f}%"
        })

        # Step 2: 分析模式
        if total >= 3:
            # 检查是否有进步趋势
            first_half = records[:total//2]
            second_half = records[total//2:]
            first_rate = sum(1 for r in first_half if r["is_correct"]) / max(len(first_half), 1)
            second_rate = sum(1 for r in second_half if r["is_correct"]) / max(len(second_half), 1)

            if second_rate > first_rate:
                chain.append({
                    "step": 2,
                    "type": "pattern",
                    "content": f"有进步趋势：前半段正确率 {first_rate*100:.0f}%，后半段 {second_rate*100:.0f}%，说明正在逐步理解"
                })
            else:
                chain.append({
                    "step": 2,
                    "type": "pattern",
                    "content": f"无明显进步：前半段正确率 {first_rate*100:.0f}%，后半段 {second_rate*100:.0f}%，可能存在根本性理解偏差"
                })

        # Step 3: 追溯前置知识
        prerequisites = get_prerequisites(knowledge_id)
        if prerequisites:
            chain.append({
                "step": 3,
                "type": "prerequisite_check",
                "content": f"检查前置知识点：{', '.join([get_node(p)['name'] for p in prerequisites if get_node(p)])}"
            })
        else:
            chain.append({
                "step": 3,
                "type": "prerequisite_check",
                "content": "该知识点为基础知识点，无前置依赖"
            })

        # Step 4: 定位根因
        if weak_info["mastery_prob"] < 0.3 and total > 0:
            root_cause = "概念理解偏差"
            suggestion = "建议从基础概念重新学习，配合辅导Agent进行Socratic式引导"
        elif weak_info["mastery_prob"] < 0.6 and total > 0:
            root_cause = "应用能力不足"
            suggestion = "概念基本理解，但需要更多练习来巩固应用"
        elif total == 0:
            root_cause = "尚未开始学习"
            suggestion = "建议从该知识点的基础内容开始学习"
        else:
            root_cause = "需要持续练习"
            suggestion = "继续练习以巩固掌握"

        chain.append({
            "step": 4,
            "type": "root_cause",
            "content": f"根因诊断：{root_cause}。{suggestion}"
        })

        return chain

    def _generate_recommendations(self, weak_nodes, mastery_map):
        """生成改进建议"""
        recommendations = []

        # 按类别统计薄弱情况
        category_stats = {}
        for node in weak_nodes:
            cat = node["category"]
            if cat not in category_stats:
                category_stats[cat] = {"count": 0, "names": []}
            category_stats[cat]["count"] += 1
            category_stats[cat]["names"].append(node["name"])

        category_names = {"grammar": "语法", "vocabulary": "词汇", "reading": "阅读"}

        for cat, stats in category_stats.items():
            recommendations.append({
                "category": cat,
                "category_name": category_names.get(cat, cat),
                "priority": "high" if stats["count"] >= 3 else "medium",
                "message": f"{category_names.get(cat, cat)}模块有 {stats['count']} 个薄弱知识点：{', '.join(stats['names'][:3])}{'...' if len(stats['names']) > 3 else ''}",
                "suggestion": f"建议优先加强{category_names.get(cat, cat)}训练"
            })

        # 检查前置知识缺失
        for node in weak_nodes[:5]:
            kid = node["id"]
            prereqs = get_prerequisites(kid)
            for p in prereqs:
                if p in mastery_map and mastery_map[p]["prob"] < 0.6:
                    prereq_name = get_node(p)["name"]
                    recommendations.append({
                        "category": "prerequisite",
                        "priority": "high",
                        "message": f"[{node['name']}] 的前置知识点 [{prereq_name}] 掌握不足（{mastery_map[p]['prob']*100:.0f}%）",
                        "suggestion": f"建议先巩固 [{prereq_name}] 再学习 [{node['name']}]"
                    })

        return recommendations

    def quick_diagnose(self, student_id, question_id, is_correct):
        """
        快速诊断 - 单题作答后的即时分析
        用于实时更新掌握概率
        """
        conn = get_db()
        cursor = conn.cursor()

        # 获取题目对应的知识点
        from data.question_bank import get_question_by_id
        question = get_question_by_id(question_id)
        if not question:
            conn.close()
            return None

        knowledge_id = question["knowledge_id"]

        # 获取当前掌握情况
        cursor.execute("""
            SELECT mastery_prob, attempt_count, correct_count
            FROM knowledge_mastery
            WHERE student_id = ? AND knowledge_id = ?
        """, (student_id, knowledge_id))
        row = cursor.fetchone()

        if row:
            # 贝叶斯知识追踪更新
            old_prob = row["mastery_prob"]
            attempts = row["attempt_count"] + 1
            correct = row["correct_count"] + (1 if is_correct else 0)

            # BKT参数
            p_learn = 0.1   # 学习概率
            p_guess = 0.25  # 猜对概率
            p_slip = 0.1    # 失误概率

            if is_correct:
                # 答对：更新掌握概率
                p_known = old_prob * (1 - p_slip) / (
                    old_prob * (1 - p_slip) + (1 - old_prob) * p_guess
                )
            else:
                # 答错：更新掌握概率
                p_known = old_prob * p_slip / (
                    old_prob * p_slip + (1 - old_prob) * (1 - p_guess)
                )

            # 学习转移：即使答对也可能学到新知识
            new_prob = p_known + (1 - p_known) * p_learn
            new_prob = min(max(new_prob, 0.0), 1.0)

            cursor.execute("""
                UPDATE knowledge_mastery
                SET mastery_prob = ?, attempt_count = ?, correct_count = ?,
                    last_practiced = CURRENT_TIMESTAMP
                WHERE student_id = ? AND knowledge_id = ?
            """, (new_prob, attempts, correct, student_id, knowledge_id))
        else:
            # 首次作答
            new_prob = 1.0 if is_correct else 0.0
            cursor.execute("""
                INSERT INTO knowledge_mastery (student_id, knowledge_id, mastery_prob, attempt_count, correct_count, last_practiced)
                VALUES (?, ?, ?, 1, ?, CURRENT_TIMESTAMP)
            """, (student_id, knowledge_id, new_prob, 1 if is_correct else 0))

        conn.commit()
        conn.close()

        return {
            "knowledge_id": knowledge_id,
            "knowledge_name": get_node(knowledge_id)["name"] if get_node(knowledge_id) else knowledge_id,
            "new_mastery_prob": new_prob if 'new_prob' in dir() else 0.0,
            "is_correct": is_correct
        }
