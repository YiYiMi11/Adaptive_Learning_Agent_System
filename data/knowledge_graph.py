# -*- coding: utf-8 -*-
"""
英语学习知识图谱 - 包含知识点节点和依赖关系
覆盖：语法、词汇、阅读三大模块
"""

KNOWLEDGE_GRAPH = {
    "nodes": [
        # ========== 语法模块 ==========
        {"id": "G01", "name": "字母与发音", "category": "grammar", "level": 1, "description": "26个字母的认读与基本发音规则"},
        {"id": "G02", "name": "名词单复数", "category": "grammar", "level": 1, "description": "可数名词与不可数名词，规则与不规则变化"},
        {"id": "G03", "name": "冠词用法", "category": "grammar", "level": 1, "description": "a/an/the的用法与区别"},
        {"id": "G04", "name": "代词基础", "category": "grammar", "level": 1, "description": "人称代词、物主代词、指示代词"},
        {"id": "G05", "name": "be动词", "category": "grammar", "level": 1, "description": "am/is/are的用法"},
        {"id": "G06", "name": "一般现在时", "category": "grammar", "level": 2, "description": "第三人称单数、频率副词、基本句型"},
        {"id": "G07", "name": "现在进行时", "category": "grammar", "level": 2, "description": "be+doing结构、动词ing变化规则"},
        {"id": "G08", "name": "一般过去时", "category": "grammar", "level": 2, "description": "规则与不规则动词过去式、时间标志词"},
        {"id": "G09", "name": "一般将来时", "category": "grammar", "level": 3, "description": "will/shall/be going to的用法"},
        {"id": "G10", "name": "现在完成时", "category": "grammar", "level": 3, "description": "have/has+过去分词、since/for的用法"},
        {"id": "G11", "name": "情态动词", "category": "grammar", "level": 3, "description": "can/could/may/might/must/should"},
        {"id": "G12", "name": "被动语态", "category": "grammar", "level": 4, "description": "各时态的被动语态转换"},
        {"id": "G13", "name": "定语从句", "category": "grammar", "level": 4, "description": "关系代词who/which/that/whose"},
        {"id": "G14", "name": "状语从句", "category": "grammar", "level": 4, "description": "时间/条件/原因/结果状语从句"},
        {"id": "G15", "name": "虚拟语气", "category": "grammar", "level": 5, "description": "if条件句、wish从句"},
        {"id": "G16", "name": "非谓语动词", "category": "grammar", "level": 5, "description": "不定式、动名词、分词的用法"},

        # ========== 词汇模块 ==========
        {"id": "V01", "name": "基础日常词汇", "category": "vocabulary", "level": 1, "description": "数字、颜色、家庭成员、食物等"},
        {"id": "V02", "name": "学校与教育词汇", "category": "vocabulary", "level": 1, "description": "学科、文具、校园设施"},
        {"id": "V03", "name": "动词短语", "category": "vocabulary", "level": 2, "description": "常用动词短语如look after, give up"},
        {"id": "V04", "name": "形容词与副词", "category": "vocabulary", "level": 2, "description": "常见形容词副词及比较级最高级"},
        {"id": "V05", "name": "同义词与反义词", "category": "vocabulary", "level": 2, "description": "常见同义词反义词辨析"},
        {"id": "V06", "name": "词根词缀", "category": "vocabulary", "level": 3, "description": "常见前缀后缀如un-, re-, -tion, -ment"},
        {"id": "V07", "name": "学术词汇", "category": "vocabulary", "level": 3, "description": "学术写作常用词汇"},
        {"id": "V08", "name": "习语与搭配", "category": "vocabulary", "level": 4, "description": "常用习语和固定搭配"},
        {"id": "V09", "name": "高级词汇拓展", "category": "vocabulary", "level": 5, "description": "高阶词汇和表达方式"},

        # ========== 阅读模块 ==========
        {"id": "R01", "name": "基础阅读理解", "category": "reading", "level": 1, "description": "短文阅读、主旨大意理解"},
        {"id": "R02", "name": "细节信息提取", "category": "reading", "level": 1, "description": "从文中查找具体信息"},
        {"id": "R03", "name": "词义猜测", "category": "reading", "level": 2, "description": "根据上下文猜测生词含义"},
        {"id": "R04", "name": "推理判断", "category": "reading", "level": 2, "description": "根据文章信息进行推断"},
        {"id": "R05", "name": "长难句分析", "category": "reading", "level": 3, "description": "复杂句子的结构分析"},
        {"id": "R06", "name": "文章结构分析", "category": "reading", "level": 3, "description": "段落关系、论证结构"},
        {"id": "R07", "name": "阅读速度提升", "category": "reading", "level": 3, "description": "略读、扫读技巧"},
        {"id": "R08", "name": "批判性阅读", "category": "reading", "level": 4, "description": "评价作者观点、识别偏见"},
        {"id": "R09", "name": "学术文献阅读", "category": "reading", "level": 5, "description": "学术论文的阅读策略"},
    ],
    "edges": [
        # 语法依赖关系
        {"from": "G01", "to": "G02"}, {"from": "G01", "to": "G03"},
        {"from": "G01", "to": "G04"}, {"from": "G01", "to": "G05"},
        {"from": "G05", "to": "G06"}, {"from": "G05", "to": "G07"},
        {"from": "G06", "to": "G08"}, {"from": "G06", "to": "G09"},
        {"from": "G08", "to": "G10"}, {"from": "G06", "to": "G11"},
        {"from": "G08", "to": "G12"}, {"from": "G04", "to": "G13"},
        {"from": "G09", "to": "G14"}, {"from": "G10", "to": "G15"},
        {"from": "G11", "to": "G16"}, {"from": "G13", "to": "G16"},

        # 词汇依赖关系
        {"from": "V01", "to": "V02"}, {"from": "V01", "to": "V03"},
        {"from": "V01", "to": "V04"}, {"from": "V04", "to": "V05"},
        {"from": "V05", "to": "V06"}, {"from": "V06", "to": "V07"},
        {"from": "V07", "to": "V08"}, {"from": "V08", "to": "V09"},

        # 阅读依赖关系
        {"from": "V01", "to": "R01"}, {"from": "R01", "to": "R02"},
        {"from": "R02", "to": "R03"}, {"from": "V05", "to": "R03"},
        {"from": "R03", "to": "R04"}, {"from": "G13", "to": "R05"},
        {"from": "R04", "to": "R06"}, {"from": "R06", "to": "R07"},
        {"from": "R07", "to": "R08"}, {"from": "V07", "to": "R09"},
        {"from": "R08", "to": "R09"},

        # 跨模块依赖
        {"from": "G06", "to": "R01"}, {"from": "G08", "to": "R03"},
        {"from": "V03", "to": "R04"}, {"from": "G14", "to": "R06"},
    ]
}


def get_node(node_id):
    """根据ID获取知识点节点"""
    for node in KNOWLEDGE_GRAPH["nodes"]:
        if node["id"] == node_id:
            return node
    return None


def get_prerequisites(node_id):
    """获取某知识点的所有前置依赖"""
    prerequisites = []
    for edge in KNOWLEDGE_GRAPH["edges"]:
        if edge["to"] == node_id:
            prerequisites.append(edge["from"])
    return prerequisites


def get_dependents(node_id):
    """获取依赖某知识点的所有后续节点"""
    dependents = []
    for edge in KNOWLEDGE_GRAPH["edges"]:
        if edge["from"] == node_id:
            dependents.append(edge["to"])
    return dependents


def get_nodes_by_category(category):
    """按类别获取知识点"""
    return [n for n in KNOWLEDGE_GRAPH["nodes"] if n["category"] == category]


def get_nodes_by_level(level):
    """按级别获取知识点"""
    return [n for n in KNOWLEDGE_GRAPH["nodes"] if n["level"] == level]


def get_learning_order():
    """获取推荐学习顺序（拓扑排序）"""
    visited = set()
    order = []

    def dfs(node_id):
        if node_id in visited:
            return
        visited.add(node_id)
        for prereq in get_prerequisites(node_id):
            dfs(prereq)
        order.append(node_id)

    for node in KNOWLEDGE_GRAPH["nodes"]:
        dfs(node["id"])

    return order
