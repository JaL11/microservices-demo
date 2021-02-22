const USER = 0
const BOT = 1

var inputField = document.getElementById("message-input-field");

inputField.addEventListener("keyup", (e) => {
    if (e.key == "Enter") {
        sendMessage();
    }
});

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

function postMessage(message) {
    var fd = new FormData();
    fd.append("user_message", message);
      
    var postRequest = new XMLHttpRequest();
    postRequest.open("POST", "/chat/sendMessage", true);

    postRequest.addEventListener(' error', function(event) { addMessageToChatbox(BOT, "Sorry, I couldn't answer that. Please try again.") });

    postRequest.onreadystatechange = function () {
        if(postRequest.readyState === XMLHttpRequest.DONE) {
          addMessageToChatbox(BOT, postRequest.responseText);
        }
      };

    postRequest.send(fd);
}

function sendMessage() {
    var input = inputField.value;
    inputField.value = "";
    addMessageToChatbox(USER, input);
    postMessage(input);
}