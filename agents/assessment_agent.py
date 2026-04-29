# -*- coding: utf-8 -*-
"""
评估 Agent (Assessment Agent)
持续跟踪学习效果，通过间隔重复（Spaced Repetition）算法安排复习节点，
利用贝叶斯知识追踪模型（BKT）动态更新学生对每个知识点的掌握概率，
形成完整的闭环学习反馈。
"""

import json
import math
from datetime import datetime, timedelta
from database import get_db
from data.knowledge_graph import get_node, get_prerequisites, KNOWLEDGE_GRAPH


class AssessmentAgent:
    """评估Agent - 学习效果跟踪与复习调度"""

    def __init__(self):
        self.name = "Assessment Agent"

    def get_overall_progress(self, student_id):
        """
        获取学生整体学习进度
        """
        conn = get_db()
        cursor = conn.cursor()

        # 总知识点数
        total_nodes = len(KNOWLEDGE_GRAPH["nodes"])

        # 已接触的知识点
        cursor.execute("""
            SELECT COUNT(*) as count FROM knowledge_mastery
            WHERE student_id = ? AND attempt_count > 0
        """, (student_id,))
        touched = cursor.fetchone()["count"]

        # 已掌握的知识点（概率 >= 0.8）
        cursor.execute("""
            SELECT COUNT(*) as count FROM knowledge_mastery
            WHERE student_id = ? AND mastery_prob >= 0.8
        """, (student_id,))
        mastered = cursor.fetchone()["count"]

        # 总答题数
        cursor.execute("""
            SELECT COUNT(*) as count FROM answer_records
            WHERE student_id = ?
        """, (student_id,))
        total_questions = cursor.fetchone()["count"]

        # 总正确数
        cursor.execute("""
            SELECT COUNT(*) as count FROM answer_records
            WHERE student_id = ? AND is_correct = 1
        """, (student_id,))
        correct = cursor.fetchone()["count"]

        # 按类别统计
        cursor.execute("""
            SELECT km.knowledge_id, km.mastery_prob, n.category
            FROM knowledge_mastery km
            JOIN (
                SELECT id as knowledge_id, category FROM (
                    SELECT 'G01' as id, 'grammar' as category UNION ALL
                    SELECT 'G02', 'grammar' UNION ALL SELECT 'G03', 'grammar' UNION ALL
                    SELECT 'G04', 'grammar' UNION ALL SELECT 'G05', 'grammar' UNION ALL
                    SELECT 'G06', 'grammar' UNION ALL SELECT 'G07', 'grammar' UNION ALL
                    SELECT 'G08', 'grammar' UNION ALL SELECT 'G09', 'grammar' UNION ALL
                    SELECT 'G10', 'grammar' UNION ALL SELECT 'G11', 'grammar' UNION ALL
                    SELECT 'G12', 'grammar' UNION ALL SELECT 'G13', 'grammar' UNION ALL
                    SELECT 'G14', 'grammar' UNION ALL SELECT 'G15', 'grammar' UNION ALL
                    SELECT 'G16', 'grammar' UNION ALL
                    SELECT 'V01', 'vocabulary' UNION ALL SELECT 'V02', 'vocabulary' UNION ALL
                    SELECT 'V03', 'vocabulary' UNION ALL SELECT 'V04', 'vocabulary' UNION ALL
                    SELECT 'V05', 'vocabulary' UNION ALL SELECT 'V06', 'vocabulary' UNION ALL
                    SELECT 'V07', 'vocabulary' UNION ALL SELECT 'V08', 'vocabulary' UNION ALL
                    SELECT 'V09', 'vocabulary' UNION ALL
                    SELECT 'R01', 'reading' UNION ALL SELECT 'R02', 'reading' UNION ALL
                    SELECT 'R03', 'reading' UNION ALL SELECT 'R04', 'reading' UNION ALL
                    SELECT 'R05', 'reading' UNION ALL SELECT 'R06', 'reading' UNION ALL
                    SELECT 'R07', 'reading' UNION ALL SELECT 'R08', 'reading' UNION ALL
                    SELECT 'R09', 'reading'
                )
            ) n ON km.knowledge_id = n.knowledge_id
            WHERE km.student_id = ?
        """, (student_id,))
        mastery_rows = cursor.fetchall()

        category_progress = {"grammar": [], "vocabulary": [], "reading": []}
        for row in mastery_rows:
            cat = row["category"]
            if cat in category_progress:
                category_progress[cat].append(row["mastery_prob"])

        conn.close()

        # 计算各类别掌握率
        category_stats = {}
        category_names = {"grammar": "语法", "vocabulary": "词汇", "reading": "阅读"}
        category_totals = {"grammar": 16, "vocabulary": 9, "reading": 9}

        for cat, probs in category_progress.items():
            total_cat = category_totals.get(cat, 1)
            mastered_cat = sum(1 for p in probs if p >= 0.8)
            avg_prob = sum(probs) / len(probs) if probs else 0
            category_stats[cat] = {
                "name": category_names.get(cat, cat),
                "mastered": mastered_cat,
                "total": total_cat,
                "mastery_rate": mastered_cat / total_cat,
                "avg_prob": avg_prob
            }

        return {
            "total_nodes": total_nodes,
            "touched_nodes": touched,
            "mastered_nodes": mastered,
            "overall_mastery": mastered / total_nodes if total_nodes > 0 else 0,
            "total_questions": total_questions,
            "correct_questions": correct,
            "accuracy": correct / total_questions if total_questions > 0 else 0,
            "category_stats": category_stats
        }

    def get_review_schedule(self, student_id):
        """
        基于间隔重复算法生成复习计划
        使用SM-2算法的变体
        """
        conn = get_db()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT knowledge_id, mastery_prob, attempt_count, correct_count, last_practiced
            FROM knowledge_mastery
            WHERE student_id = ? AND attempt_count > 0
            ORDER BY mastery_prob ASC
        """, (student_id,))
        rows = cursor.fetchall()
        conn.close()

        review_items = []

        for row in rows:
            kid = row["knowledge_id"]
            prob = row["mastery_prob"]
            attempts = row["attempt_count"]
            correct = row["correct_count"]
            last_practiced = row["last_practiced"]

            node = get_node(kid)
            if not node:
                continue

            # 计算复习间隔（基于掌握概率和练习次数）
            if prob >= 0.9:
                # 高掌握度：长间隔
                interval_days = min(attempts * 2, 30)
                urgency = "low"
            elif prob >= 0.7:
                # 中等掌握度：中等间隔
                interval_days = min(max(attempts, 2), 14)
                urgency = "medium"
            elif prob >= 0.5:
                # 低掌握度：短间隔
                interval_days = max(1, attempts // 2)
                urgency = "high"
            else:
                # 很低掌握度：需要尽快复习
                interval_days = 1
                urgency = "critical"

            # 计算下次复习时间
            if last_practiced:
                last_dt = datetime.strptime(last_practiced, "%Y-%m-%d %H:%M:%S")
                next_review = last_dt + timedelta(days=interval_days)
                is_overdue = datetime.now() > next_review
            else:
                next_review = datetime.now()
                is_overdue = True

            review_items.append({
                "knowledge_id": kid,
                "knowledge_name": node["name"],
                "category": node["category"],
                "level": node["level"],
                "mastery_prob": prob,
                "urgency": urgency,
                "interval_days": interval_days,
                "next_review": next_review.strftime("%Y-%m-%d"),
                "is_overdue": is_overdue
            })

        # 按紧急程度排序
        urgency_order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
        review_items.sort(key=lambda x: (urgency_order.get(x["urgency"], 4), x["mastery_prob"]))

        return review_items

    def get_learning_streak(self, student_id):
        """获取学习连续天数"""
        conn = get_db()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT DISTINCT DATE(created_at) as practice_date
            FROM answer_records
            WHERE student_id = ?
            ORDER BY practice_date DESC
        """, (student_id,))
        rows = cursor.fetchall()
        conn.close()

        if not rows:
            return {"streak": 0, "total_days": 0}

        dates = [row["practice_date"] for row in rows]
        today = datetime.now().strftime("%Y-%m-%d")

        # 计算连续天数
        streak = 0
        check_date = datetime.now()

        for date_str in dates:
            expected = check_date.strftime("%Y-%m-%d")
            if date_str == expected:
                streak += 1
                check_date -= timedelta(days=1)
            elif date_str < expected:
                break

        return {
            "streak": streak,
            "total_days": len(dates),
            "last_practice": dates[0] if dates else None
        }

    def generate_report(self, student_id):
        """
        生成综合学习报告
        """
        progress = self.get_overall_progress(student_id)
        review = self.get_review_schedule(student_id)
        streak = self.get_learning_streak(student_id)

        # 统计需要复习的数量
        overdue_count = sum(1 for r in review if r["is_overdue"])
        critical_count = sum(1 for r in review if r["urgency"] == "critical")

        # 综合评价
        if progress["overall_mastery"] >= 0.8:
            level = "优秀"
            message = "你的英语学习进展非常出色，继续保持！"
        elif progress["overall_mastery"] >= 0.6:
            level = "良好"
            message = "你的学习效果不错，注意复习薄弱知识点。"
        elif progress["overall_mastery"] >= 0.4:
            level = "中等"
            message = "正在稳步进步，建议增加练习量。"
        elif progress["overall_mastery"] >= 0.2:
            level = "需加强"
            message = "还有不少知识点需要巩固，坚持每天学习！"
        else:
            level = "起步阶段"
            message = "学习之旅刚刚开始，加油！"

        return {
            "level": level,
            "message": message,
            "progress": progress,
            "review_schedule": review[:10],
            "streak": streak,
            "overdue_reviews": overdue_count,
            "critical_reviews": critical_count,
            "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
