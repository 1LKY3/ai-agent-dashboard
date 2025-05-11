document.addEventListener('DOMContentLoaded', () => {
    // DOM Elements
    const chatMessages = document.getElementById('chat-messages');
    const userInput = document.getElementById('user-input');
    const sendButton = document.getElementById('send-button');
    const viewDataButton = document.getElementById('view-data');
    const clearChatButton = document.getElementById('clear-chat');
    const databaseOutput = document.getElementById('database-output');

    // API Endpoints
    const API_BASE_URL = 'http://localhost:8000';
    const CHAT_ENDPOINT = `${API_BASE_URL}/chat`;
    const DB_QUERY_ENDPOINT = `${API_BASE_URL}/db/query`;

    // Add a message to the chat
    function addMessage(sender, message) {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message', `${sender}-message`);
        messageDiv.textContent = message;
        chatMessages.appendChild(messageDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    // Send message to AI
    async function sendMessage() {
        const message = userInput.value.trim();
        if (!message) return;

        // Add user message to chat
        addMessage('user', message);
        userInput.value = '';

        try {
            const response = await fetch(CHAT_ENDPOINT, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message })
            });

            if (!response.ok) {
                throw new Error('Network response was not ok');
            }

            const data = await response.json();
            addMessage('ai', data.response);
        } catch (error) {
            console.error('Error:', error);
            addMessage('ai', 'Sorry, there was an error processing your request.');
        }
    }

    // Fetch all data from database
    async function fetchAllData() {
        try {
            const response = await fetch(DB_QUERY_ENDPOINT, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    query: 'SELECT * FROM messages',
                    params: []
                })
            });

            if (!response.ok) {
                throw new Error('Failed to fetch data');
            }


            const data = await response.json();
            databaseOutput.textContent = JSON.stringify(data, null, 2);
        } catch (error) {
            console.error('Error:', error);
            databaseOutput.textContent = 'Error fetching data from database';
        }
    }

    // Clear chat
    function clearChat() {
        chatMessages.innerHTML = '';
        databaseOutput.textContent = '';
    }

    // Event Listeners
    sendButton.addEventListener('click', sendMessage);
    userInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') sendMessage();
    });

    viewDataButton.addEventListener('click', fetchAllData);
    clearChatButton.addEventListener('click', clearChat);
});
