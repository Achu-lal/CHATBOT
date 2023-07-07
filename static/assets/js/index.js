const startGame = () => {
  const playBtn = document.querySelector(".icon");
  const match = document.querySelector(".chatbot");
  const close = document.querySelector(".close-btn");

  playBtn.addEventListener("click", () => {
    playBtn.classList.add("fadeOut");
    match.classList.add("fadeIn");
  });

  close.addEventListener("click", () => {
    match.classList.remove("fadeIn");
    playBtn.classList.remove("fadeOut");
  });
};

startGame();

const inputField = document.querySelector('.chat-footer input[type="text"]');
const sendButton = document.querySelector('.chat-footer .send-btn');
const messagesContainer = document.querySelector('.chat-body .messages');

function appendMessage(content, sender) {
  const messageDiv = document.createElement('div');
  messageDiv.classList.add('message', sender);
  messageDiv.innerHTML = `<p>${content}</p>`;
  messagesContainer.appendChild(messageDiv);
}

function handleUserInput() {
  const userMessage = inputField.value;
  appendMessage(userMessage, 'sent');
  inputField.value = '';
 
  fetch('/process-user-input', {
    method: 'POST',
    body: JSON.stringify({ message: userMessage }),
    headers: { 'Content-Type': 'application/json' }
  })
    .then(response => response.json())
    .then(data => appendMessage(data.message, 'received'))
    .catch(error => console.error('Error:', error));
}

sendButton.addEventListener('click', handleUserInput);
inputField.addEventListener('keypress', (event) => {
  if (event.key === 'Enter') {
    handleUserInput();
  }
});