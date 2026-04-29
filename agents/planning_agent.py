# -*- coding: utf-8 -*-
"""
规划 Agent (Planning Agent)
基于诊断结果，动态生成个性化学习路径。
综合考虑知识依赖关系、学生当前水平、学习目标等因素，
采用多目标优化算法，在"补基础"和"提能力"之间找到最优平衡点。
"""

import json
from datetime import datetime, timedelta
from database import get_db
from data.knowledge_graph import (
    get_node, get_prerequisites, get_dependents,
    get_learning_order, get_nodes_by_category, KNOWLEDGE_GRAPH
)


class PlanningAgent:
    """规划Agent - 生成个性化学习路径"""

    def __init__(self):
        self.name = "Planning Agent"

    def generate_path(self, student_id, diagnosis_result):
        """
        基于诊断结果生成学习路径
        返回：{
            "path": [...],           # 学习路径节点列表
            "daily_plan": [...],     # 每日学习计划
            "milestones": [...],     # 里程碑
            "estimated_days": N      # 预计完成天数
        }
        """
        weak_nodes = diagnosis_result.get("weak_nodes", [])
        mastery_map = diagnosis_result.get("mastery_map", {})

        # 1. 筛选需要学习的知识点
        nodes_to_learn = self._select_nodes_to_learn(weak_nodes, mastery_map)

        # 2. 按依赖关系排序（拓扑排序）
        sorted_nodes = self._topological_sort(nodes_to_learn)

        # 3. 多目标优化：平衡补基础和提能力
        optimized_path = self._optimize_path(sorted_nodes, mastery_map, weak_nodes)

        # 4. 生成每日学习计划
        daily_plan = self._generate_daily_plan(optimized_path)

        # 5. 设置里程碑
        milestones = self._set_milestones(optimized_path)

        # 6. 保存路径到数据库
        self._save_path(student_id, optimized_path)

        return {
            "path": optimized_path,
            "daily_plan": daily_plan,
            "milestones": milestones,
            "estimated_days": len(daily_plan),
            "total_nodes": len(optimized_path)
        }

    def _select_nodes_to_learn(self, weak_nodes, mastery_map):
        """筛选需要学习的知识点"""
        nodes = []
        for node in weak_nodes:
            kid = node["id"]
            # 确保前置知识也在学习列表中
            prereqs = get_prerequisites(kid)
            for p in prereqs:
                p_mastery = mastery_map.get(p, {}).get("prob", 0.0)
                if p_mastery < 0.7 and p not in [n["id"] for n in nodes]:
                    p_node = get_node(p)
                    if p_node:
                        nodes.append({
                            "id": p["id"] if isinstance(p, dict) else p,
                            "name": p_node["name"],
                            "category": p_node["category"],
                            "level": p_node["level"],
                            "priority": "high",
                            "reason": "前置知识需要巩固"
                        })

            if kid not in [n["id"] for n in nodes]:
                priority = "high" if node.get("mastery_prob", 0) < 0.3 else "medium"
                nodes.append({
                    "id": kid,
                    "name": node["name"],
                    "category": node["category"],
                    "level": node["level"],
                    "priority": priority,
                    "reason": "薄弱知识点"
                })

        return nodes

    def _topological_sort(self, nodes):
        """拓扑排序：确保先学前置知识"""
        node_ids = [n["id"] for n in nodes]
        visited = set()
        result = []
        node_map = {n["id"]: n for n in nodes}

        def dfs(nid):
            if nid in visited or nid not in node_ids:
                return
            visited.add(nid)
            for prereq in get_prerequisites(nid):
                if prereq in node_ids:
                    dfs(prereq)
            if nid in node_map:
                result.append(node_map[nid])

        for nid in node_ids:
            dfs(nid)

        return result

    def _optimize_path(self, sorted_nodes, mastery_map, weak_nodes):
        """
        多目标优化学习路径
        目标：1. 补基础（低级别优先） 2. 提能力（高频错误优先） 3. 保持动力（穿插不同类别）
        """
        if not sorted_nodes:
            return []

        # 按优先级和级别分组
        foundation = [n for n in sorted_nodes if n["level"] <= 2]
        improvement = [n for n in sorted_nodes if n["level"] >= 3]

        # 优化策略：先补基础，再提能力，穿插不同类别保持新鲜感
        optimized = []

        # 阶段1：补基础（按类别穿插）
        grammar_f = [n for n in foundation if n["category"] == "grammar"]
        vocab_f = [n for n in foundation if n["category"] == "vocabulary"]
        reading_f = [n for n in foundation if n["category"] == "reading"]

        # 交替插入不同类别
        max_len = max(len(grammar_f), len(vocab_f), len(reading_f))
        for i in range(max_len):
            if i < len(grammar_f):
                optimized.append(grammar_f[i])
            if i < len(vocab_f):
                optimized.append(vocab_f[i])
            if i < len(reading_f):
                optimized.append(reading_f[i])

        # 阶段2：提能力
        grammar_i = [n for n in improvement if n["category"] == "grammar"]
        vocab_i = [n for n in improvement if n["category"] == "vocabulary"]
        reading_i = [n for n in improvement if n["category"] == "reading"]

        max_len = max(len(grammar_i), len(vocab_i), len(reading_i))
        for i in range(max_len):
            if i < len(grammar_i):
                optimized.append(grammar_i[i])
            if i < len(vocab_i):
                optimized.append(vocab_i[i])
            if i < len(reading_i):
                optimized.append(reading_i[i])

        # 去重（保持依赖顺序）
        seen = set()
        final = []
        for n in optimized:
            if n["id"] not in seen:
                seen.add(n["id"])
                final.append(n)

        return final

    def _generate_daily_plan(self, path):
        """生成每日学习计划，每天3-4个知识点"""
        daily_plan = []
        nodes_per_day = 3

        for i in range(0, len(path), nodes_per_day):
            day_nodes = path[i:i + nodes_per_day]
            day_num = i // nodes_per_day + 1
            daily_plan.append({
                "day": day_num,
                "nodes": day_nodes,
                "focus": self._get_day_focus(day_nodes),
                "estimated_minutes": len(day_nodes) * 15
            })

        return daily_plan

    def _get_day_focus(self, nodes):
        """获取当天学习重点"""
        categories = {}
        for n in nodes:
            cat = n["category"]
            categories[cat] = categories.get(cat, 0) + 1

        category_names = {"grammar": "语法", "vocabulary": "词汇", "reading": "阅读"}
        main_cat = max(categories, key=categories.get)
        return f"{category_names.get(main_cat, main_cat)}为主（{len(nodes)}个知识点）"

    def _set_milestones(self, path):
        """设置学习里程碑"""
        milestones = []
        total = len(path)

        if total == 0:
            return milestones

        # 每5个知识点设置一个里程碑
        milestone_interval = max(5, total // 4)

        for i in range(0, total, milestone_interval):
            node = path[min(i, total - 1)]
            milestones.append({
                "index": i + 1,
                "node_name": node["name"],
                "message": f"完成 {i + 1}/{total} 个知识点！当前进度：{node['name']}",
                "reward": "complete" if (i + 1) >= total else "done"
            })

        # 最终里程碑
        if milestones and milestones[-1]["index"] < total:
            milestones.append({
                "index": total,
                "node_name": path[-1]["name"],
                "message": f"已完成全部 {total} 个知识点的学习路径！",
                "reward": "finished"
            })

        return milestones

    def _save_path(self, student_id, path):
        """保存学习路径到数据库"""
        conn = get_db()
        # 将当前活跃路径设为非活跃
        conn.execute("""
            UPDATE learning_paths SET is_active = 0 WHERE student_id = ?
        """, (student_id,))

        # 保存新路径
        path_data = json.dumps([{
            "id": n["id"],
            "name": n["name"],
            "category": n["category"],
            "level": n["level"],
            "priority": n.get("priority", "medium")
        } for n in path], ensure_ascii=False)

        conn.execute("""
            INSERT INTO learning_paths (student_id, path_data, is_active)
            VALUES (?, ?, 1)
        """, (student_id, path_data))
        conn.commit()
        conn.close()

    def get_current_path(self, student_id):
        """获取学生当前活跃的学习路径"""
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT path_data FROM learning_paths
            WHERE student_id = ? AND is_active = 1
            ORDER BY created_at DESC LIMIT 1
        """, (student_id,))
        row = cursor.fetchone()
        conn.close()

        if row:
            return json.loads(row["path_data"])
        return None

    def get_next_node(self, student_id, diagnosis_result):
        """获取下一个应该学习的知识点"""
        path = self.get_current_path(student_id)

        if not path:
            # 没有路径，根据诊断结果推荐
            weak = diagnosis_result.get("weak_nodes", [])
            if weak:
                return weak[0]
            return None

        # 找到路径中第一个未掌握的知识点
        mastery_map = diagnosis_result.get("mastery_map", {})
        for node in path:
            kid = node["id"]
            prob = mastery_map.get(kid, {}).get("prob", 0.0)
            if prob < 0.8:
                return node

        # 全部掌握，推荐进阶
        return None
