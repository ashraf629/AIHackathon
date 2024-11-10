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
    messageDiv.textContent = message;
    chatWindow.appendChild(messageDiv);
    chatWindow.scrollTop = chatWindow.scrollHeight;
}

function startVoiceRecognition() {
    alert('Voice recognition is not implemented in this demo.');
    // Implement voice recognition using Web Speech API or other services
}

// Task management functionality
function addNewTask() {
    const newTaskInput = document.getElementById('new-task');
    const newTask = newTaskInput.value.trim();
    if (newTask !== '') {
        console.log('Adding new task:', newTask); // Debugging statement
        // Submit the form via fetch API
        fetch('/add_task', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            body: new URLSearchParams({
                'new_task': newTask
            })
        }).then(response => {
            if (response.ok) {
                // Refresh the tasks page
                window.location.href = '/tasks';
            } else {
                console.error('Failed to add task');
            }
        }).catch(error => {
            console.error('Error:', error);
        });
    }
    return false; // Prevent form submission
}

function completeTask(task) {
    alert(`Complete task: ${task}`);
    // Implement the logic to mark the task as complete
}

function deleteTask(task) {
    console.log('Deleting task:', task); // Debugging statement
    // Submit the form via fetch API
    fetch('/delete_task', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: new URLSearchParams({
            'task': task
        })
    }).then(response => {
        if (response.ok) {
            // Refresh the tasks page
            window.location.href = '/tasks';
        } else {
            console.error('Failed to delete task');
        }
    }).catch(error => {
        console.error('Error:', error);
    });
}
