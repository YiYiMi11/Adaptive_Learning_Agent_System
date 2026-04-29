# -*- coding: utf-8 -*-
"""
英语学习题库 - 包含各知识点的练习题
"""

QUESTION_BANK = [
    # ========== 语法 Level 1 ==========
    {
        "id": "Q001", "knowledge_id": "G02", "type": "choice",
        "question": "There are three ___ on the table.",
        "options": ["box", "boxs", "boxes", "boxies"],
        "answer": "boxes",
        "explanation": "以x, s, ch, sh结尾的名词变复数加-es。box → boxes"
    },
    {
        "id": "Q002", "knowledge_id": "G02", "type": "choice",
        "question": "I can see some ___ in the park.",
        "options": ["child", "childs", "children", "childrens"],
        "answer": "children",
        "explanation": "child是不规则名词，复数形式为children。"
    },
    {
        "id": "Q003", "knowledge_id": "G03", "type": "choice",
        "question": "___ apple a day keeps the doctor away.",
        "options": ["A", "An", "The", "/"],
        "answer": "An",
        "explanation": "apple以元音音素开头，用an。这是一句谚语。"
    },
    {
        "id": "Q004", "knowledge_id": "G04", "type": "choice",
        "question": "___ are playing basketball after school.",
        "options": ["Us", "We", "Our", "Ours"],
        "answer": "We",
        "explanation": "作主语需要用主格人称代词we（大写We）。"
    },
    {
        "id": "Q005", "knowledge_id": "G05", "type": "choice",
        "question": "She ___ a teacher at our school.",
        "options": ["am", "is", "are", "be"],
        "answer": "is",
        "explanation": "She是第三人称单数，be动词用is。"
    },
    {
        "id": "Q006", "knowledge_id": "G05", "type": "choice",
        "question": "They ___ from China.",
        "options": ["am", "is", "are", "be"],
        "answer": "are",
        "explanation": "They是复数主语，be动词用are。"
    },

    # ========== 语法 Level 2 ==========
    {
        "id": "Q007", "knowledge_id": "G06", "type": "choice",
        "question": "He ___ to school every day.",
        "options": ["go", "goes", "going", "gone"],
        "answer": "goes",
        "explanation": "一般现在时，主语He是第三人称单数，动词加-s/-es。go → goes"
    },
    {
        "id": "Q008", "knowledge_id": "G06", "type": "choice",
        "question": "She usually ___ breakfast at 7 o'clock.",
        "options": ["have", "has", "having", "had"],
        "answer": "has",
        "explanation": "usually表示经常性动作，用一般现在时。She是第三人称单数，have → has。"
    },
    {
        "id": "Q009", "knowledge_id": "G07", "type": "choice",
        "question": "Look! The children ___ in the playground.",
        "options": ["play", "plays", "are playing", "played"],
        "answer": "are playing",
        "explanation": "Look!提示正在发生的动作，用现在进行时be+doing。children是复数，用are playing。"
    },
    {
        "id": "Q010", "knowledge_id": "G07", "type": "choice",
        "question": "Be quiet! The baby ___ .",
        "options": ["sleeps", "slept", "is sleeping", "sleep"],
        "answer": "is sleeping",
        "explanation": "Be quiet!提示此刻正在进行的动作，用现在进行时。baby是单数，用is sleeping。"
    },
    {
        "id": "Q011", "knowledge_id": "G08", "type": "choice",
        "question": "I ___ a movie yesterday evening.",
        "options": ["watch", "watches", "watched", "am watching"],
        "answer": "watched",
        "explanation": "yesterday evening是过去时间标志词，用一般过去时。watch → watched。"
    },
    {
        "id": "Q012", "knowledge_id": "G08", "type": "choice",
        "question": "She ___ to Beijing last summer.",
        "options": ["go", "goes", "went", "going"],
        "answer": "went",
        "explanation": "last summer是过去时间，用一般过去时。go是不规则动词，过去式为went。"
    },

    # ========== 语法 Level 3 ==========
    {
        "id": "Q013", "knowledge_id": "G09", "type": "choice",
        "question": "We ___ a meeting tomorrow afternoon.",
        "options": ["have", "had", "will have", "having"],
        "answer": "will have",
        "explanation": "tomorrow afternoon是将来时间，用一般将来时will+动词原形。"
    },
    {
        "id": "Q014", "knowledge_id": "G09", "type": "choice",
        "question": "They are going ___ a picnic this weekend.",
        "options": ["have", "to have", "having", "had"],
        "answer": "to have",
        "explanation": "be going to + 动词原形表示计划或打算做某事。"
    },
    {
        "id": "Q015", "knowledge_id": "G10", "type": "choice",
        "question": "I ___ already ___ my homework.",
        "options": ["have...finished", "has...finished", "had...finish", "am...finishing"],
        "answer": "have...finished",
        "explanation": "already常与现在完成时连用。I用have，finish的过去分词是finished。"
    },
    {
        "id": "Q016", "knowledge_id": "G10", "type": "choice",
        "question": "She ___ in this city since 2010.",
        "options": ["lives", "lived", "has lived", "is living"],
        "answer": "has lived",
        "explanation": "since 2010表示从过去持续到现在，用现在完成时。She用has。"
    },
    {
        "id": "Q017", "knowledge_id": "G11", "type": "choice",
        "question": "You ___ finish your homework before going out.",
        "options": ["can", "should", "must", "will"],
        "answer": "must",
        "explanation": "must表示必须，语气最强，强调义务和必要性。"
    },
    {
        "id": "Q018", "knowledge_id": "G11", "type": "choice",
        "question": "___ I use your dictionary?",
        "options": ["Must", "Should", "May", "Will"],
        "answer": "May",
        "explanation": "May I...? 用于请求许可，语气礼貌。"
    },

    # ========== 语法 Level 4 ==========
    {
        "id": "Q019", "knowledge_id": "G12", "type": "choice",
        "question": "The cake ___ by my mother yesterday.",
        "options": ["made", "was made", "is made", "makes"],
        "answer": "was made",
        "explanation": "蛋糕是被妈妈做的，用被动语态。yesterday表示过去时，所以用was made。"
    },
    {
        "id": "Q020", "knowledge_id": "G12", "type": "choice",
        "question": "English ___ all over the world.",
        "options": ["speaks", "spoke", "is spoken", "speaking"],
        "answer": "is spoken",
        "explanation": "英语被全世界使用，用一般现在时的被动语态is + 过去分词。"
    },
    {
        "id": "Q021", "knowledge_id": "G13", "type": "choice",
        "question": "The man ___ is standing there is my father.",
        "options": ["who", "which", "what", "where"],
        "answer": "who",
        "explanation": "先行词是人（man），用who引导定语从句。"
    },
    {
        "id": "Q022", "knowledge_id": "G13", "type": "choice",
        "question": "This is the book ___ I bought yesterday.",
        "options": ["who", "which", "what", "where"],
        "answer": "which",
        "explanation": "先行词是物（book），用which或that引导定语从句。"
    },
    {
        "id": "Q023", "knowledge_id": "G14", "type": "choice",
        "question": "I will go to the party ___ I finish my work.",
        "options": ["if", "because", "although", "so"],
        "answer": "if",
        "explanation": "if引导条件状语从句，表示'如果'。主将从现：主句将来时，从句现在时。"
    },
    {
        "id": "Q024", "knowledge_id": "G14", "type": "choice",
        "question": "___ it was raining, he still went out.",
        "options": ["Because", "If", "Although", "So"],
        "answer": "Although",
        "explanation": "Although引导让步状语从句，表示'尽管/虽然'。"
    },

    # ========== 语法 Level 5 ==========
    {
        "id": "Q025", "knowledge_id": "G15", "type": "choice",
        "question": "If I ___ you, I would study harder.",
        "options": ["am", "was", "were", "be"],
        "answer": "were",
        "explanation": "与现在事实相反的虚拟条件句，if从句用过去时，be动词统一用were。"
    },
    {
        "id": "Q026", "knowledge_id": "G15", "type": "choice",
        "question": "I wish I ___ a bird.",
        "options": ["am", "was", "were", "be"],
        "answer": "were",
        "explanation": "wish后面的从句用虚拟语气，表示与现在事实相反的愿望，be动词用were。"
    },
    {
        "id": "Q027", "knowledge_id": "G16", "type": "choice",
        "question": "I enjoy ___ music in my free time.",
        "options": ["listen to", "listening to", "listened to", "to listen to"],
        "answer": "listening to",
        "explanation": "enjoy后面接动名词（doing）作宾语。enjoy doing sth."
    },
    {
        "id": "Q028", "knowledge_id": "G16", "type": "choice",
        "question": "She decided ___ abroad for further study.",
        "options": ["go", "going", "to go", "went"],
        "answer": "to go",
        "explanation": "decide后面接不定式（to do）作宾语。decide to do sth."
    },

    # ========== 词汇 Level 1 ==========
    {
        "id": "Q029", "knowledge_id": "V01", "type": "choice",
        "question": "How do you say '苹果' in English?",
        "options": ["banana", "apple", "orange", "grape"],
        "answer": "apple",
        "explanation": "apple是苹果的英文。"
    },
    {
        "id": "Q030", "knowledge_id": "V01", "type": "choice",
        "question": "What color is the sky on a clear day?",
        "options": ["red", "green", "blue", "yellow"],
        "answer": "blue",
        "explanation": "晴天时天空是蓝色的。blue = 蓝色"
    },
    {
        "id": "Q031", "knowledge_id": "V01", "type": "choice",
        "question": "My mother's mother is my ___.",
        "options": ["aunt", "sister", "grandmother", "cousin"],
        "answer": "grandmother",
        "explanation": "mother's mother = grandmother（外婆/奶奶）"
    },
    {
        "id": "Q032", "knowledge_id": "V02", "type": "choice",
        "question": "We study ___ in the classroom.",
        "options": ["math", "maths", "Both A and B", "Neither A nor B"],
        "answer": "Both A and B",
        "explanation": "math（美式）和maths（英式）都是数学的意思，都可以使用。"
    },

    # ========== 词汇 Level 2 ==========
    {
        "id": "Q033", "knowledge_id": "V03", "type": "choice",
        "question": "Please ___ your hand before answering the question.",
        "options": ["look up", "put up", "give up", "take up"],
        "answer": "put up",
        "explanation": "put up one's hand = 举手。look up查阅，give up放弃，take up开始从事。"
    },
    {
        "id": "Q034", "knowledge_id": "V03", "type": "choice",
        "question": "Don't ___! You can do it!",
        "options": ["give up", "look after", "put on", "turn off"],
        "answer": "give up",
        "explanation": "give up = 放弃。根据语境'你能做到'，应选'不要放弃'。"
    },
    {
        "id": "Q035", "knowledge_id": "V04", "type": "choice",
        "question": "She sings ___ than her sister.",
        "options": ["good", "better", "best", "well"],
        "answer": "better",
        "explanation": "than提示用比较级。good/well的比较级是better。"
    },
    {
        "id": "Q036", "knowledge_id": "V04", "type": "choice",
        "question": "He runs very ___.",
        "options": ["fast", "faster", "fastest", "more fast"],
        "answer": "fast",
        "explanation": "very后面接形容词或副词的原级。fast既是形容词也是副词，不需要加-ly。"
    },
    {
        "id": "Q037", "knowledge_id": "V05", "type": "choice",
        "question": "The opposite of 'beautiful' is ___.",
        "options": ["pretty", "ugly", "handsome", "nice"],
        "answer": "ugly",
        "explanation": "beautiful（美丽的）的反义词是ugly（丑陋的）。"
    },

    # ========== 词汇 Level 3 ==========
    {
        "id": "Q038", "knowledge_id": "V06", "type": "choice",
        "question": "The prefix 'un-' in 'unhappy' means ___.",
        "options": ["very", "not", "again", "before"],
        "answer": "not",
        "explanation": "前缀un-表示'不，非'。unhappy = 不快乐的。"
    },
    {
        "id": "Q039", "knowledge_id": "V06", "type": "choice",
        "question": "The suffix '-tion' in 'education' is used to form a ___.",
        "options": ["verb", "noun", "adjective", "adverb"],
        "answer": "noun",
        "explanation": "后缀-tion/-sion用于将动词变为名词。educate → education。"
    },
    {
        "id": "Q040", "knowledge_id": "V07", "type": "choice",
        "question": "Which word means 'to examine or investigate'?",
        "options": ["explore", "exploit", "explode", "export"],
        "answer": "explore",
        "explanation": "explore = 探索/调查。exploit利用，explode爆炸，export出口。"
    },

    # ========== 词汇 Level 4 ==========
    {
        "id": "Q041", "knowledge_id": "V08", "type": "choice",
        "question": "To 'break the ice' means to ___.",
        "options": ["destroy ice", "start a conversation", "cause trouble", "feel cold"],
        "answer": "start a conversation",
        "explanation": "'break the ice'是习语，意思是打破沉默、开始交谈。"
    },
    {
        "id": "Q042", "knowledge_id": "V08", "type": "choice",
        "question": "If something happens 'once in a blue moon', it happens ___.",
        "options": ["every day", "very rarely", "every month", "at night"],
        "answer": "very rarely",
        "explanation": "'once in a blue moon'是习语，意思是极少发生。"
    },

    # ========== 阅读 Level 1-2 ==========
    {
        "id": "Q043", "knowledge_id": "R01", "type": "reading",
        "question": "Read the passage and answer:\n\n'Tom gets up at 6:30 every morning. He has breakfast at 7:00 and goes to school at 7:30. His favorite class is English because he likes speaking with foreign teachers.'\n\nWhat is Tom's favorite class?",
        "options": ["Math", "English", "Science", "Chinese"],
        "answer": "English",
        "explanation": "文中明确提到'His favorite class is English'。"
    },
    {
        "id": "Q044", "knowledge_id": "R02", "type": "reading",
        "question": "Read the passage and answer:\n\n'Last weekend, Mary visited her grandmother. They cooked dinner together and watched a movie. Mary stayed there for two days before going home on Sunday.'\n\nHow long did Mary stay at her grandmother's house?",
        "options": ["One day", "Two days", "Three days", "One week"],
        "answer": "Two days",
        "explanation": "文中提到'Mary stayed there for two days'。"
    },
    {
        "id": "Q045", "knowledge_id": "R03", "type": "reading",
        "question": "Read the passage and answer:\n\n'The weather was inclement, so we decided to stay indoors and play board games instead of going to the park.'\n\nWhat does 'inclement' most likely mean?",
        "options": ["sunny and warm", "bad or severe", "pleasant", "windy but nice"],
        "answer": "bad or severe",
        "explanation": "根据上下文，因为天气不好所以决定留在室内，inclement意为恶劣的。"
    },
    {
        "id": "Q046", "knowledge_id": "R04", "type": "reading",
        "question": "Read the passage and answer:\n\n'Lisa didn't say anything during the meeting, but she looked worried. When the boss announced the new project deadline, she sighed deeply.'\n\nWhat can we infer about Lisa?",
        "options": [
            "She is happy about the project",
            "She is concerned about the deadline",
            "She doesn't care about the meeting",
            "She wants to lead the project"
        ],
        "answer": "She is concerned about the deadline",
        "explanation": "Lisa沉默不语、表情担忧、听到截止日期后深叹一口气，可以推断她对截止日期感到忧虑。"
    },

    # ========== 阅读 Level 3 ==========
    {
        "id": "Q047", "knowledge_id": "R05", "type": "reading",
        "question": "Identify the main clause in this sentence:\n'Although the exam was difficult, the students who had studied hard managed to pass.'",
        "options": [
            "Although the exam was difficult",
            "the students managed to pass",
            "who had studied hard",
            "the exam was difficult"
        ],
        "answer": "the students managed to pass",
        "explanation": "主句是'the students managed to pass'。'Although...'是让步状语从句，'who had studied hard'是定语从句。"
    },
    {
        "id": "Q048", "knowledge_id": "R06", "type": "reading",
        "question": "What is the text structure of the following passage?\n\n'First, gather all the ingredients. Next, mix the flour and eggs. Then, add sugar and milk. Finally, bake the mixture for 30 minutes.'",
        "options": ["Cause and effect", "Problem and solution", "Sequence/Process", "Compare and contrast"],
        "answer": "Sequence/Process",
        "explanation": "文段使用First, Next, Then, Finally等顺序词，描述的是一个步骤流程，属于顺序/过程结构。"
    },

    # ========== 更多综合题 ==========
    {
        "id": "Q049", "knowledge_id": "G06", "type": "fill_blank",
        "question": "She ___ (not like) drinking milk.",
        "options": ["don't like", "doesn't like", "didn't like", "isn't like"],
        "answer": "doesn't like",
        "explanation": "一般现在时，She是第三人称单数，否定用doesn't + 动词原形。"
    },
    {
        "id": "Q050", "knowledge_id": "G07", "type": "fill_blank",
        "question": "___ they ___ (play) football now?",
        "options": ["Do...play", "Are...playing", "Did...play", "Will...play"],
        "answer": "Are...playing",
        "explanation": "now提示现在进行时，疑问句将be动词提前：Are they playing?"
    },
    {
        "id": "Q051", "knowledge_id": "G08", "type": "fill_blank",
        "question": "___ you ___ (see) the movie last night?",
        "options": ["Do...see", "Did...see", "Are...seeing", "Have...seen"],
        "answer": "Did...see",
        "explanation": "last night是过去时间，用一般过去时疑问句：Did you see?"
    },
    {
        "id": "Q052", "knowledge_id": "G10", "type": "fill_blank",
        "question": "I ___ never ___ (be) to Japan.",
        "options": ["have...been", "has...been", "had...been", "am...being"],
        "answer": "have...been",
        "explanation": "never常与现在完成时连用，表示'从未'。I用have，been是be的过去分词。"
    },
    {
        "id": "Q053", "knowledge_id": "V03", "type": "choice",
        "question": "Can you help me ___ this new word?",
        "options": ["look at", "look up", "look after", "look for"],
        "answer": "look up",
        "explanation": "look up = 查阅（字典/资料）。look up a word = 查单词。"
    },
    {
        "id": "Q054", "knowledge_id": "V04", "type": "choice",
        "question": "This is the ___ movie I have ever seen.",
        "options": ["more interesting", "most interesting", "interesting", "most interested"],
        "answer": "most interesting",
        "explanation": "I have ever seen提示用最高级。interesting的最高级是most interesting。"
    },
    {
        "id": "Q055", "knowledge_id": "G13", "type": "choice",
        "question": "The girl ___ father is a doctor studies very hard.",
        "options": ["who", "whom", "whose", "which"],
        "answer": "whose",
        "explanation": "先行词girl与father之间是所属关系，用whose引导定语从句。"
    },
    {
        "id": "Q056", "knowledge_id": "G12", "type": "choice",
        "question": "A new hospital ___ in our town next year.",
        "options": ["builds", "will build", "will be built", "is building"],
        "answer": "will be built",
        "explanation": "医院是被建造的，用被动语态。next year表示将来时，用will be built。"
    },
]


def get_questions_by_knowledge(knowledge_id):
    """根据知识点ID获取所有题目"""
    return [q for q in QUESTION_BANK if q["knowledge_id"] == knowledge_id]


def get_question_by_id(question_id):
    """根据题目ID获取题目"""
    for q in QUESTION_BANK:
        if q["id"] == question_id:
            return q
    return None


def get_questions_by_category(category):
    """根据类别获取题目"""
    from data.knowledge_graph import get_nodes_by_category
    node_ids = [n["id"] for n in get_nodes_by_category(category)]
    return [q for q in QUESTION_BANK if q["knowledge_id"] in node_ids]


def get_questions_by_level(level):
    """根据级别获取题目"""
    from data.knowledge_graph import get_nodes_by_level
    node_ids = [n["id"] for n in get_nodes_by_level(level)]
    return [q for q in QUESTION_BANK if q["knowledge_id"] in node_ids]
