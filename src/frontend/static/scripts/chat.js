const USER = 0
const BOT = 1

function addMessageToChatbox(author, message) {
    if (message == "") return;
    var messageNode = document.createElement("div");
    if (author == USER) {
        messageNode.className = "message-bubble message-bubble-user";
    } else if (author == BOT) {
        messageNode.className = "message-bubble message-bubble-bot";
    }
    messageNode.innerHTML = message;

    var messageBoxElement = document.querySelector(".message-box");
    messageBoxElement.appendChild(messageNode);
    messageBoxElement.scrollTop = messageBoxElement.scrollHeight; // scroll to the new message in the chatbox
}

function sendMessage() {
    var inputField = document.getElementById("message-input-field");
    var input = inputField.value;
    inputField.value = "";

    addMessageToChatbox(USER, input);
}