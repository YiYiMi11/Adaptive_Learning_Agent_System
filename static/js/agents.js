/* ========================================
   Agents Introduction Page — JavaScript
   ======================================== */

// ========== Navbar Scroll Effect ==========
const agentsNav = document.getElementById('agentsNav');
if (agentsNav) {
    window.addEventListener('scroll', () => {
        agentsNav.classList.toggle('scrolled', window.scrollY > 20);
    });
}

// ========== Scroll Animations (IntersectionObserver) ==========
(function() {
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.animationPlayState = 'running';
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.1 });

    document.querySelectorAll('.page-enter').forEach(el => {
        if (el.closest('.agents-hero')) {
            el.style.animationPlayState = 'running';
        } else {
            el.style.animationPlayState = 'paused';
            observer.observe(el);
        }
    });
})();

// ========== Collaboration Graph Interaction ==========
(function() {
    const nodes = document.querySelectorAll('.collab-node');
    const lines = document.querySelectorAll('.collab-line');

    function highlightConnections(agentName) {
        lines.forEach(line => {
            const from = line.dataset.from;
            const to = line.dataset.to;
            if (from === agentName || to === agentName) {
                line.classList.add('highlighted');
            } else {
                line.classList.remove('highlighted');
            }
        });
    }

    function clearHighlights() {
        lines.forEach(line => line.classList.remove('highlighted'));
        nodes.forEach(node => node.classList.remove('active'));
    }

    nodes.forEach(node => {
        node.addEventListener('mouseenter', () => {
            clearHighlights();
            const agent = node.dataset.agent;
            node.classList.add('active');
            highlightConnections(agent);
        });

        node.addEventListener('mouseleave', () => {
            clearHighlights();
        });

        // Mobile tap support
        node.addEventListener('click', (e) => {
            e.stopPropagation();
            const agent = node.dataset.agent;
            const isActive = node.classList.contains('active');

            clearHighlights();

            if (!isActive) {
                node.classList.add('active');
                highlightConnections(agent);
            }
        });
    });

    document.addEventListener('click', () => {
        clearHighlights();
    });
})();

// ========== Flow Step Toggle ==========
function toggleStep(containerId, stepNum) {
    const container = document.getElementById(containerId);
    if (!container) return;

    const steps = container.querySelectorAll('.flow-step');
    steps.forEach(step => {
        const num = parseInt(step.dataset.step);
        if (num === stepNum) {
            step.classList.toggle('active');
        } else {
            step.classList.remove('active');
        }
    });
}

// ========== Path Animation ==========
function runPathAnimation() {
    const nodes = document.querySelectorAll('.path-node');
    const connectors = document.querySelectorAll('.path-connector');
    const btn = document.getElementById('pathAnimBtn');

    // Reset
    nodes.forEach(n => n.classList.remove('visible'));
    connectors.forEach(c => c.classList.remove('visible'));

    btn.disabled = true;
    btn.innerHTML = '<div class="spinner" style="width:12px;height:12px;border-width:2px;"></div> 生成中...';

    // Animate sequentially
    let delay = 0;
    const items = [...document.querySelectorAll('.path-demo-graph > *')];

    items.forEach((item, index) => {
        delay = index * 300;
        setTimeout(() => {
            item.classList.add('visible');
        }, delay);
    });

    // Re-enable button
    setTimeout(() => {
        btn.disabled = false;
        btn.innerHTML = '<i class="fa-solid fa-rotate-right"></i> 重新播放';
    }, delay + 500);
}

// ========== Chat Animation ==========
const chatMessages = [
    {
        role: 'assistant',
        text: '你好！这道题考察的是一般现在时第三人称单数的用法。你选择了 "He go to school every day"，我们来看看这个答案。'
    },
    {
        role: 'user',
        text: '我觉得应该选这个，go就是去的意思啊。'
    },
    {
        role: 'assistant',
        text: '你的理解方向是对的！"go"确实是"去"的意思。不过我们来想一下：主语是 "He"，这是第三人称单数。在一般现在时中，当主语是第三人称单数时，动词需要有什么变化呢？'
    },
    {
        role: 'user',
        text: '哦...是不是要加 s？'
    },
    {
        role: 'assistant',
        text: '非常棒！你理解对了！第三人称单数（he/she/it）做主语时，动词要加 -s 或 -es。所以正确的答案是 "He goes to school every day"。记住这个规律：he/she/it 后面动词要变形！'
    }
];

let chatAnimating = false;

function runChatAnimation() {
    if (chatAnimating) return;
    chatAnimating = true;

    const container = document.getElementById('chatDemoMessages');
    const btn = document.getElementById('chatAnimBtn');

    // Clear previous messages
    container.innerHTML = '';
    btn.disabled = true;
    btn.innerHTML = '<div class="spinner" style="width:12px;height:12px;border-width:2px;"></div> 对话中...';

    let index = 0;

    function addNextMessage() {
        if (index >= chatMessages.length) {
            btn.disabled = false;
            btn.innerHTML = '<i class="fa-solid fa-rotate-right"></i> 重新播放';
            chatAnimating = false;
            return;
        }

        const msg = chatMessages[index];
        const msgEl = document.createElement('div');
        msgEl.className = `chat-demo-msg ${msg.role}`;

        const avatarIcon = msg.role === 'assistant' ? 'fa-robot' : 'fa-user';

        msgEl.innerHTML = `
            <div class="chat-demo-avatar"><i class="fa-solid ${avatarIcon}"></i></div>
            <div class="chat-demo-bubble">${msg.text}</div>
        `;

        container.appendChild(msgEl);

        // Trigger animation
        requestAnimationFrame(() => {
            msgEl.classList.add('visible');
        });

        // Scroll to bottom
        container.scrollTop = container.scrollHeight;

        index++;
        setTimeout(addNextMessage, 1200);
    }

    setTimeout(addNextMessage, 400);
}

// ========== Timeline Interaction ==========
function showTimelineInfo(node) {
    const info = node.dataset.info;
    const infoEl = document.getElementById('timelineInfo');

    if (!info) return;

    // Remove active from all nodes
    document.querySelectorAll('.timeline-node').forEach(n => n.classList.remove('active'));
    node.classList.add('active');

    infoEl.innerHTML = info;
    infoEl.classList.add('has-data');
}

// ========== Hash Navigation ==========
(function() {
    function scrollToHash() {
        const hash = window.location.hash;
        if (hash) {
            const target = document.querySelector(hash);
            if (target) {
                setTimeout(() => {
                    target.scrollIntoView({ behavior: 'smooth', block: 'start' });
                }, 100);
            }
        }
    }

    // Handle initial hash
    if (window.location.hash) {
        scrollToHash();
    }

    // Handle hash changes
    window.addEventListener('hashchange', scrollToHash);
})();
