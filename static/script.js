// Get elements
const sendBtn = document.getElementById('send-btn');
const userInputField = document.getElementById('user-input');
const chatBox = document.getElementById('chat-box');
const thinkingText = document.getElementById('thinking-text');

// Send button click
sendBtn.addEventListener('click', sendMessage);

// Enter key support
userInputField.addEventListener('keypress', function (e) {
    if (e.key === 'Enter') {
        sendMessage();
    }
});

function sendMessage() {
    const userInput = userInputField.value.trim();
    if (userInput === "") return;

    addMessageToChatBox('user', userInput);
    userInputField.value = '';

    // Disable button while waiting
    sendBtn.disabled = true;
    thinkingText.style.display = 'block';

    fetch('/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: userInput })
    })
    .then(response => response.json())
    .then(data => {
        thinkingText.style.display = 'none';
        sendBtn.disabled = false;

        if (data.reply) {
            typeMessage('bot', data.reply);
        } else {
            addMessageToChatBox('bot', '⚠️ No response received.');
        }
    })
    .catch(error => {
        console.error("Error:", error);
        thinkingText.style.display = 'none';
        sendBtn.disabled = false;
        addMessageToChatBox('bot', '❌ Sorry, something went wrong. Please try again.');
    });
}

// Safely add message (no innerHTML)
function addMessageToChatBox(sender, message) {
    const messageElement = document.createElement('div');
    messageElement.classList.add('message', sender);
    messageElement.textContent = message;
    chatBox.appendChild(messageElement);
    chatBox.scrollTop = chatBox.scrollHeight;
}

// Typing animation
function typeMessage(sender, message) {
    const messageElement = document.createElement('div');
    messageElement.classList.add('message', sender);
    chatBox.appendChild(messageElement);

    let index = 0;
    const typingSpeed = 15;
    let isTyping = true;

    // Stop button
    const stopButton = document.createElement('button');
    stopButton.textContent = 'Stop';
    stopButton.classList.add('stop-button');
    stopButton.onclick = function () {
        isTyping = false;
        stopButton.remove();
    };

    chatBox.appendChild(stopButton);

    function type() {
        if (index < message.length && isTyping) {
            messageElement.textContent += message.charAt(index);
            index++;
            chatBox.scrollTop = chatBox.scrollHeight;
            setTimeout(type, typingSpeed);
        } else {
            stopButton.remove();
        }
    }

    type();
}
