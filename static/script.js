// script.js

// Function to format message text
function formatMessage(message) {
    // Replace **text** with <strong>text</strong>
    message = message.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
    // Replace \n with <br>
    message = message.replace(/\n/g, '<br>');
    return message;
}

// Navigation functions
function goToPage(page) {
    window.location.href = page;
}

// Placeholder functions for navigation buttons
function startChat() {
    goToPage('/chatbot');
}

function addTask() {
    goToPage('/tasks');
}

// Chatbot functionality
async function sendMessage() {
    const inputField = document.getElementById('user-input');
    const message = inputField.value.trim();
    if (message !== '') {
        // Display user's message
        addMessage('user', message);
        // Clear input field
        inputField.value = '';

        try {
            // Send message to the backend
            const response = await fetch('/api/chatbot/message', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ message: message })
            });

            if (!response.ok) {
                throw new Error(`Server error: ${response.statusText}`);
            }

            const responseData = await response.json();
            const botMessage = responseData.answer;  // Extract the answer from the response

            // Display bot's message
            addMessage('bot', botMessage);
        } catch (error) {
            console.error('Error:', error);
            addMessage('bot', 'Sorry, something went wrong. Please try again later.');
        }
    }
}

function addMessage(sender, message) {
    const chatWindow = document.getElementById('chat-window');
    const messageDiv = document.createElement('div');
    messageDiv.classList.add('message', sender);
    messageDiv.innerHTML = formatMessage(message);  // Use innerHTML to render HTML tags
    chatWindow.appendChild(messageDiv);
    chatWindow.scrollTop = chatWindow.scrollHeight;
}

function startVoiceRecognition() {
    alert('Voice recognition is not implemented in this demo.');
    // Implement voice recognition using Web Speech API or other services
}

// Task management functionality
function addNewTask() {
    alert('Add new task functionality is not implemented in this demo.');
    // Implement the logic to add a new task
}


