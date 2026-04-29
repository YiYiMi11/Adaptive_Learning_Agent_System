// ========== 工具函数 ==========

function showToast(message, type = 'info') {
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    toast.textContent = message;
    document.body.appendChild(toast);
    setTimeout(() => toast.remove(), 3000);
}

function $(selector) {
    return document.querySelector(selector);
}

function $$(selector) {
    return document.querySelectorAll(selector);
}

// ========== 学生管理 ==========

function showCreateModal() {
    const modal = document.getElementById('createModal');
    modal.style.display = 'flex';
    $('#studentName').focus();
}

function hideCreateModal() {
    document.getElementById('createModal').style.display = 'none';
}

async function createStudent() {
    const name = $('#studentName').value.trim();
    if (!name) {
        showToast('请输入学生姓名', 'error');
        return;
    }

    const level = $('#studentLevel').value;
    const target = $('#studentTarget').value.trim();

    try {
        const res = await fetch('/api/students', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ name, level, target })
        });
        const data = await res.json();
        if (data.error) {
            showToast(data.error, 'error');
            return;
        }
        showToast(`学生 ${name} 创建成功！`, 'success');
        location.reload();
    } catch (e) {
        showToast('创建失败', 'error');
    }
}

async function deleteStudent(id, name) {
    if (!confirm(`确定要删除学生 "${name}" 吗？所有学习数据将被清除。`)) return;

    try {
        await fetch(`/api/students/${id}`, { method: 'DELETE' });
        showToast('删除成功', 'success');
        location.reload();
    } catch (e) {
        showToast('删除失败', 'error');
    }
}

// ========== 答题系统 ==========

let currentQuestion = null;
let selectedAnswer = null;
let isAnswered = false;
let currentSessionId = null;

// ========== 答题计时器 ==========
let questionStartTime = null;
let timerInterval = null;

function startTimer() {
    questionStartTime = Date.now();
    const timerEl = document.getElementById('questionTimer');
    if (!timerEl) return;
    timerEl.style.display = 'inline-flex';
    timerInterval = setInterval(() => {
        const elapsed = Math.floor((Date.now() - questionStartTime) / 1000);
        const minutes = Math.floor(elapsed / 60).toString().padStart(2, '0');
        const seconds = (elapsed % 60).toString().padStart(2, '0');
        timerEl.textContent = `⏱ ${minutes}:${seconds}`;
    }, 1000);
}

function stopTimer() {
    if (timerInterval) {
        clearInterval(timerInterval);
        timerInterval = null;
    }
    if (questionStartTime) {
        return Math.round((Date.now() - questionStartTime) / 1000);
    }
    return 0;
}

function resetTimer() {
    stopTimer();
    questionStartTime = null;
    const timerEl = document.getElementById('questionTimer');
    if (timerEl) {
        timerEl.textContent = '⏱ 00:00';
    }
}

function selectOption(btn, answer) {
    if (isAnswered) return;
    $$('.option-btn').forEach(b => b.classList.remove('selected'));
    btn.classList.add('selected');
    selectedAnswer = answer;
    $('#submitBtn').disabled = false;
}

async function submitAnswer() {
    if (!selectedAnswer || isAnswered) return;

    const studentId = $('#studentId').value;
    const questionId = currentQuestion.id;

    isAnswered = true;
    const timeSpent = stopTimer();
    $('#submitBtn').disabled = true;

    // 显示正确/错误
    $$('.option-btn').forEach(btn => {
        const answer = btn.dataset.answer;
        if (answer === currentQuestion.answer) {
            btn.classList.add('correct');
        }
        if (btn.classList.contains('selected') && answer !== currentQuestion.answer) {
            btn.classList.add('wrong');
        }
        btn.style.pointerEvents = 'none';
    });

    try {
        const res = await fetch('/api/answer', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                student_id: studentId,
                question_id: questionId,
                answer: selectedAnswer,
                time_spent: timeSpent
            })
        });
        const data = await res.json();

        // 显示解析
        const explanationDiv = document.getElementById('explanation');
        const isCorrect = data.is_correct;

        explanationDiv.className = `explanation-box ${isCorrect ? '' : 'error'}`;
        explanationDiv.innerHTML = `
            <div class="title"><i class="fa-solid ${isCorrect ? 'fa-circle-check' : 'fa-circle-xmark'}"></i> ${isCorrect ? '回答正确' : '回答错误'}</div>
            <div>${data.explanation}</div>
            <div class="explanation-meta">
                ${timeSpent > 0 ? `<span>⏱ 用时：${timeSpent}秒</span>` : ''}
                ${data.diagnosis ? `<span>掌握度：${(data.diagnosis.new_mastery_prob * 100).toFixed(0)}%</span>` : ''}
            </div>
        `;
        explanationDiv.style.display = 'block';

        // 显示辅导按钮
        $('#tutorSection').style.display = 'block';
        $('#tutorBtn').disabled = false;

        // 更新统计
        updateQuickStats(studentId);
        updateProgressBar(studentId);

    } catch (e) {
        showToast('提交失败', 'error');
    }
}

// ========== 学习路径管理 ==========

async function regeneratePath(studentId) {
    if (!confirm('重新规划将基于你最新的学习数据生成新路径，当前进度不会丢失。确定继续？')) return;

    const btn = document.getElementById('regenPathBtn');
    if (btn) {
        btn.disabled = true;
        btn.innerHTML = '<div class="spinner" style="width:12px;height:12px;border-width:2px;"></div> 生成中...';
    }

    try {
        const res = await fetch(`/api/plan/${studentId}`, { method: 'POST' });
        const data = await res.json();

        if (data.path || data.success) {
            showToast('学习路径已更新 ✨', 'success');
            setTimeout(() => location.reload(), 500);
        } else {
            showToast(data.message || '路径生成失败', 'error');
        }
    } catch (e) {
        showToast('请求失败，请重试', 'error');
    }

    if (btn) {
        btn.disabled = false;
        btn.innerHTML = '<i class="fa-solid fa-arrows-rotate"></i> 重新规划';
    }
}

// ========== AI辅导 ==========

async function startTutoring() {
    const studentId = $('#studentId').value;
    const questionId = currentQuestion.id;

    $('#tutorBtn').disabled = true;
    $('#tutorMessages').innerHTML = '<div class="loading"><div class="spinner"></div> AI老师正在思考...</div>';
    $('#tutorSection').style.display = 'block';

    try {
        const res = await fetch('/api/tutor/start', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                student_id: studentId,
                question_id: questionId,
                student_answer: selectedAnswer
            })
        });
        const data = await res.json();

        if (data.error) {
            $('#tutorMessages').innerHTML = `<div class="chat-message assistant">
                <div class="chat-avatar"><i class="fa-solid fa-robot"></i></div>
                <div class="chat-bubble">${data.error}</div>
            </div>`;
            return;
        }

        currentSessionId = data.session_id;
        $('#tutorMessages').innerHTML = `
            <div class="chat-message assistant">
                <div class="chat-avatar"><i class="fa-solid fa-robot"></i></div>
                <div class="chat-bubble">${data.response}</div>
            </div>
        `;
    } catch (e) {
        $('#tutorMessages').innerHTML = `<div class="chat-message assistant">
            <div class="chat-avatar"><i class="fa-solid fa-robot"></i></div>
            <div class="chat-bubble">辅导服务暂时不可用，请稍后再试。</div>
        </div>`;
    }
}

async function sendTutorMessage() {
    const input = $('#tutorInput');
    const message = input.value.trim();
    if (!message || !currentSessionId) return;

    const studentId = $('#studentId').value;

    // 显示用户消息
    $('#tutorMessages').innerHTML += `
        <div class="chat-message user">
            <div class="chat-avatar"><i class="fa-solid fa-user"></i></div>
            <div class="chat-bubble">${escapeHtml(message)}</div>
        </div>
    `;
    input.value = '';

    // 滚动到底部
    const container = $('#tutorMessages');
    container.scrollTop = container.scrollHeight;

    // 显示加载
    const loadingId = 'loading-' + Date.now();
    container.innerHTML += `
        <div class="chat-message assistant" id="${loadingId}">
            <div class="chat-avatar"><i class="fa-solid fa-robot"></i></div>
            <div class="chat-bubble"><div class="loading"><div class="spinner"></div> 思考中...</div></div>
        </div>
    `;
    container.scrollTop = container.scrollHeight;

    try {
        const res = await fetch('/api/tutor/continue', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                student_id: studentId,
                session_id: currentSessionId,
                message: message
            })
        });
        const data = await res.json();

        // 移除加载
        document.getElementById(loadingId)?.remove();

        container.innerHTML += `
            <div class="chat-message assistant">
                <div class="chat-avatar"><i class="fa-solid fa-robot"></i></div>
                <div class="chat-bubble">${escapeHtml(data.response || '抱歉，无法回复。')}</div>
            </div>
        `;
    } catch (e) {
        document.getElementById(loadingId)?.remove();
        container.innerHTML += `
            <div class="chat-message assistant">
                <div class="chat-avatar"><i class="fa-solid fa-robot"></i></div>
                <div class="chat-bubble">抱歉，出现了错误，请重试。</div>
            </div>
        `;
    }

    container.scrollTop = container.scrollHeight;
}

async function explainConcept(knowledgeId) {
    const studentId = $('#studentId').value;
    if (!studentId || !knowledgeId) return;

    const box = $('#conceptBox');
    const title = $('#conceptTitle');
    const body = $('#conceptBody');

    // 如果已显示同一知识点，则关闭
    if (box.style.display !== 'none' && box.dataset.knowledgeId === knowledgeId) {
        closeConcept();
        return;
    }

    // 显示加载状态
    title.textContent = '加载中...';
    body.innerHTML = '<div class="spinner" style="width:18px;height:18px;border-width:2px;margin:8px auto;"></div>';
    box.style.display = 'block';
    box.dataset.knowledgeId = knowledgeId;

    try {
        const res = await fetch('/api/tutor/explain', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ student_id: studentId, knowledge_id: knowledgeId })
        });
        const data = await res.json();

        if (data.response) {
            title.textContent = '💡 ' + data.knowledge_name;
            body.innerHTML = data.response.replace(/\n/g, '<br>');
        } else {
            box.style.display = 'none';
            showToast('讲解生成失败', 'error');
        }
    } catch (e) {
        box.style.display = 'none';
        showToast('请求失败', 'error');
    }
}

function closeConcept() {
    const box = $('#conceptBox');
    box.style.display = 'none';
    box.dataset.knowledgeId = '';
}

// ========== 设置 ==========

async function saveSettings() {
    const apiKey = $('#apiKey').value.trim();
    const apiBase = $('#apiBase').value.trim();
    const model = $('#model').value.trim();

    if (!apiKey) {
        showToast('请输入API Key', 'error');
        return;
    }

    $('#saveBtn').disabled = true;
    $('#saveBtn').textContent = '保存中...';

    try {
        const res = await fetch('/api/settings', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ api_key: apiKey, api_base: apiBase, model: model })
        });
        const data = await res.json();

        if (data.test_result) {
            showToast(data.test_result.message, data.test_result.success ? 'success' : 'error');
        } else {
            showToast(data.message, 'success');
        }

        if (data.test_result && data.test_result.success) {
            $('#apiStatus').className = 'api-status connected';
            $('#apiStatus').innerHTML = '<i class="fa-solid fa-circle-check"></i> API已连接';
        }
    } catch (e) {
        showToast('保存失败', 'error');
    }

    $('#saveBtn').disabled = false;
    $('#saveBtn').textContent = '保存设置';
}

async function testConnection() {
    const apiKey = $('#apiKey').value.trim();
    const apiBase = $('#apiBase').value.trim();
    const model = $('#model').value.trim();

    if (!apiKey) {
        showToast('请先输入API Key', 'error');
        return;
    }

    $('#testBtn').disabled = true;
    $('#testBtn').textContent = '测试中...';

    try {
        const res = await fetch('/api/test_api', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ api_key: apiKey, api_base: apiBase, model: model })
        });
        const data = await res.json();
        showToast(data.message, data.success ? 'success' : 'error');

        if (data.success) {
            $('#apiStatus').className = 'api-status connected';
            $('#apiStatus').innerHTML = '<i class="fa-solid fa-circle-check"></i> API已连接';
        } else {
            $('#apiStatus').className = 'api-status disconnected';
            $('#apiStatus').innerHTML = '<i class="fa-solid fa-circle-xmark"></i> API未连接';
        }
    } catch (e) {
        showToast('测试失败', 'error');
    }

    $('#testBtn').disabled = false;
    $('#testBtn').textContent = '测试连接';
}

// ========== 辅助函数 ==========

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

async function updateQuickStats(studentId) {
    try {
        const res = await fetch(`/api/report/${studentId}`);
        const data = await res.json();
        if (data.progress) {
            const accuracy = (data.progress.accuracy * 100).toFixed(1);
            const mastery = (data.progress.overall_mastery * 100).toFixed(1);
            const el = document.getElementById('quickStats');
            if (el) {
                el.innerHTML = `正确率: ${accuracy}% | 掌握度: ${mastery}%`;
            }
        }
    } catch (e) {}
}

// ========== 答题进度条 ==========

async function updateProgressBar(studentId) {
    try {
        const res = await fetch(`/api/progress/${studentId}`);
        const data = await res.json();

        const answered = data.total_questions || 0;
        const correct = data.correct_questions || 0;
        const accuracy = data.accuracy || 0;
        const mastery = data.overall_mastery || 0;
        const touched = data.touched_nodes || 0;
        const mastered = data.mastered_nodes || 0;
        const total = data.total_nodes || 1;

        // 更新数值
        const answeredEl = document.getElementById('progressAnswered');
        const accuracyEl = document.getElementById('progressAccuracy');
        const masteryEl = document.getElementById('progressMastery');
        const knowledgeEl = document.getElementById('progressKnowledge');
        const fillEl = document.getElementById('progressFill');
        const detailEl = document.getElementById('progressDetail');

        if (answeredEl) answeredEl.textContent = answered;
        if (accuracyEl) accuracyEl.textContent = answered > 0 ? (accuracy * 100).toFixed(1) + '%' : '--';
        if (masteryEl) masteryEl.textContent = (mastery * 100).toFixed(1) + '%';
        if (knowledgeEl) knowledgeEl.textContent = `${mastered}/${total}`;

        // 更新进度条宽度（基于知识点掌握比例）
        if (fillEl) {
            const percent = Math.round(mastery * 100);
            fillEl.style.width = percent + '%';
        }

        // 更新底部详情
        if (detailEl) {
            if (answered === 0) {
                detailEl.textContent = '开始答题后将显示详细进度';
            } else {
                detailEl.textContent = `已接触 ${touched} 个知识点，已掌握 ${mastered} 个，共 ${total} 个知识点`;
            }
        }

        // 根据正确率给数值着色
        if (accuracyEl && answered > 0) {
            if (accuracy >= 0.8) accuracyEl.style.color = '#1B8A3D';
            else if (accuracy >= 0.6) accuracyEl.style.color = '#9A6700';
            else accuracyEl.style.color = '#D70015';
        }

        // 根据掌握度给数值着色
        if (masteryEl) {
            if (mastery >= 0.6) masteryEl.style.color = '#1B8A3D';
            else if (mastery >= 0.3) masteryEl.style.color = '#0071E3';
            else masteryEl.style.color = 'var(--text-primary)';
        }

    } catch (e) {
        const detailEl = document.getElementById('progressDetail');
        if (detailEl) detailEl.textContent = '进度加载失败';
    }
}

function nextQuestion() {
    location.reload();
}

// ========== Tab切换 ==========

function switchTab(tabName) {
    $$('.tab').forEach(t => t.classList.remove('active'));
    $$('.tab-content').forEach(t => t.classList.remove('active'));
    event.target.classList.add('active');
    document.getElementById(`tab-${tabName}`).classList.add('active');
}

// ========== Enter键支持 ==========

document.addEventListener('keydown', function(e) {
    if (e.key === 'Enter') {
        if (document.activeElement.id === 'tutorInput') {
            sendTutorMessage();
        } else if (document.activeElement.id === 'studentName') {
            createStudent();
        }
    }
});

// ========== 模态框点击外部关闭 ==========

document.addEventListener('click', function(e) {
    if (e.target.classList.contains('modal-overlay')) {
        e.target.style.display = 'none';
    }
});

// ========== 页面可见性监听（计时器） ==========
let pageHiddenTime = null;

document.addEventListener('visibilitychange', function() {
    if (document.hidden) {
        pageHiddenTime = Date.now();
    } else if (pageHiddenTime && questionStartTime) {
        const hiddenDuration = (Date.now() - pageHiddenTime) / 1000;
        if (hiddenDuration > 300) {
            if (confirm('你离开了较长时间，是否继续当前计时？\n\n点击"确定"继续计时，点击"取消"将重置计时器。')) {
                // 继续计时
            } else {
                questionStartTime = Date.now();
            }
        }
        pageHiddenTime = null;
    }
});

// ========== 页面入场动画（IntersectionObserver） ==========

(function() {
    // 仅对非 landing 页面生效
    if (document.body.classList.contains('landing-page')) return;

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.animationPlayState = 'running';
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.05, rootMargin: '0px 0px -20px 0px' });

    document.querySelectorAll('.page-enter').forEach(el => {
        // 仅暂停视口外的元素
        const rect = el.getBoundingClientRect();
        if (rect.top > window.innerHeight) {
            el.style.animationPlayState = 'paused';
            observer.observe(el);
        }
    });
})();
