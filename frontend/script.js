const API_BASE     = 'http://localhost:8000';
const loginEl      = document.getElementById('login-container');
const connectBtn   = document.getElementById('connect-drive');
const chatEl       = document.getElementById('chat-container');
const messagesEl   = document.getElementById('messages');
const inputEl      = document.getElementById('input');
const sendBtn      = document.getElementById('send');

// Utility to show/hide elements
function show(el) { el.classList.remove('hidden'); }
function hide(el) { el.classList.add('hidden'); }

// 1) Check login status
async function checkAuth() {
  try {
    const res = await fetch(`${API_BASE}/auth/status`);
    const { connected } = await res.json();
    if (connected) {
      hide(loginEl);
      show(chatEl);
      inputEl.focus();
    } else {
      show(loginEl);
      hide(chatEl);
    }
  } catch (err) {
    console.error('Auth check failed', err);
    show(loginEl);
  }
}

// 2) Kick off MCP-managed auth
connectBtn.addEventListener('click', async () => {
  try {
    const res = await fetch(`${API_BASE}/auth/status`);
    const { connected, error } = await res.json();

    if (connected) {
      hide(loginEl);
      show(chatEl);
    } else if (error) {
      alert("❌ Failed to connect: " + error);
    } else {
      alert("🔗 Authentication has been triggered. Please complete it in the new window.");
    }
  } catch (err) {
    console.error("Auth start failed", err);
    alert("Something went wrong starting auth.");
  }
});

// 3) Chat logic
function appendMessage(who, text) {
  const wrap = document.createElement('div');
  wrap.className = `message ${who} flex ${who === 'user' ? 'justify-end' : 'justify-start'}`;

  const bubble = document.createElement('div');
  bubble.className = `${who === 'user' 
    ? 'bg-blue-600 text-white rounded-xl rounded-br-none' 
    : 'bg-gray-100 text-black rounded-xl rounded-bl-none'} px-4 py-3 shadow-sm max-w-[80%] text-sm`;

  bubble.textContent = text;
  wrap.appendChild(bubble);
  messagesEl.appendChild(wrap);
  messagesEl.scrollTop = messagesEl.scrollHeight;
}

async function sendMessage() {
  const text = inputEl.value.trim();
  if (!text) return;
  appendMessage('user', text);
  inputEl.value = '';
  sendBtn.disabled = true;

  try {
    const res = await fetch(`${API_BASE}/api/chat`, {
      method: 'POST',
      headers: { 'Content-Type':'application/json' },
      body: JSON.stringify({ message: text, contextIds: [] })
    });
    const { reply } = await res.json();
    appendMessage('bot', reply);
  } catch (err) {
    console.error('Chat error:', err);
    appendMessage('bot', 'Error communicating with server.');
  } finally {
    sendBtn.disabled = false;
    inputEl.focus();
  }
}

sendBtn.addEventListener('click', sendMessage);
inputEl.addEventListener('keydown', e => {
  if (e.key === 'Enter' && !e.shiftKey) {
    e.preventDefault();
    sendMessage();
  }
});

// 4) On load, check auth
window.addEventListener('load', checkAuth);
