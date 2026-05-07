const chatBox = document.getElementById("chat-box");

// Tab Switching
function switchTab(tab) {
    document.getElementById("panel-upload").classList.toggle("hidden", tab !== "upload");
    document.getElementById("panel-chat").classList.toggle("hidden", tab !== "chat");
    document.getElementById("tab-upload").classList.toggle("active", tab === "upload");
    document.getElementById("tab-chat").classList.toggle("active", tab === "chat");
}

// Send Message
async function sendMessage() {
    const inputField = document.getElementById("user-input");
    const question = inputField.value.trim();
    if (!question) return;

    addUserMessage(question);
    inputField.value = "";

    const loadingDiv = document.createElement("div");
    loadingDiv.className = "msg bot-row";
    loadingDiv.innerHTML = `
        <div class="avatar">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2">
                <circle cx="12" cy="8" r="4"/>
                <path d="M4 20c0-4 3.6-7 8-7s8 3 8 7"/>
            </svg>
        </div>
        <div class="bubble bot-bubble loading-bubble">Analyzing company documents...</div>
    `;
    chatBox.appendChild(loadingDiv);
    scrollToBottom();

    try {
        const response = await fetch("http://127.0.0.1:8000/api/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ question })
        });
        const data = await response.json();
        loadingDiv.remove();
        addBotMessage(data.answer, data.sources);
    } catch (error) {
        loadingDiv.remove();
        addBotMessage("Error connecting to backend.", []);
        console.error(error);
    }
}

// Upload File
async function uploadFile() {
    const fileInput = document.getElementById("pdf-file");
    const file = fileInput.files[0];
    const statusEl = document.getElementById("upload-status");

    if (!file) {
        statusEl.style.color = "#ef4444";
        statusEl.textContent = "Please select a PDF file.";
        return;
    }

    statusEl.style.color = "#94a3b8";
    statusEl.textContent = "Uploading...";

    const formData = new FormData();
    formData.append("file", file);

    try {
        const response = await fetch("http://127.0.0.1:8000/api/upload", {
            method: "POST",
            body: formData
        });
        const data = await response.json();
        statusEl.style.color = "#22c55e";
        statusEl.textContent = data.message || "Upload successful!";
    } catch (error) {
        console.error(error);
        statusEl.style.color = "#ef4444";
        statusEl.textContent = "Upload failed. Please try again.";
    }
}

// Add User Message
function addUserMessage(message) {
    const div = document.createElement("div");
    div.className = "msg user-row";
    div.innerHTML = `<div class="bubble user-bubble">${escapeHtml(message)}</div>`;
    chatBox.appendChild(div);
    scrollToBottom();
}

// Add Bot Message
function addBotMessage(message, sources) {
    const div = document.createElement("div");
    div.className = "msg bot-row";

    let sourcesHTML = "";
    if (sources && sources.length > 0) {
        sourcesHTML = `
            <div class="sources">
                <strong>Sources:</strong><br>
                ${sources.join("<br>")}
            </div>
        `;
    }

    div.innerHTML = `
        <div class="avatar">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2">
                <circle cx="12" cy="8" r="4"/>
                <path d="M4 20c0-4 3.6-7 8-7s8 3 8 7"/>
            </svg>
        </div>
        <div class="bubble bot-bubble">
            <div>${message}</div>
            ${sourcesHTML}
        </div>
    `;
    chatBox.appendChild(div);
    scrollToBottom();
}

// Suggestions
function sendSuggestion(question) {
    document.getElementById("user-input").value = question;
    sendMessage();
}

// Scroll
function scrollToBottom() {
    chatBox.scrollTop = chatBox.scrollHeight;
}

// Escape HTML
function escapeHtml(text) {
    const d = document.createElement("div");
    d.appendChild(document.createTextNode(text));
    return d.innerHTML;
}

// Enter Key
document.getElementById("user-input").addEventListener("keypress", function(e) {
    if (e.key === "Enter") sendMessage();
});