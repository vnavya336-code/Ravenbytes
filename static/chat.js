
const chatForm = document.getElementById("chatForm");
const userInput = document.getElementById("userInput");
const messages = document.getElementById("messages");
const sendButton = document.getElementById("sendButton");

function addMessage(text, sender) {

    const message = document.createElement("div");
    message.className = `message ${sender}`;

    const avatar = document.createElement("div");
    avatar.className = "avatar";
    avatar.textContent = sender === "bot" ? "🤖" : "👤";

    const bubble = document.createElement("div");
    bubble.className = "bubble";
    bubble.textContent = text;

    message.appendChild(avatar);
    message.appendChild(bubble);

    messages.appendChild(message);

    messages.scrollTop = messages.scrollHeight;

    return message;
}


async function sendMessage(question) {

    if (!question.trim()) return;

    addMessage(question, "user");

    userInput.value = "";
    sendButton.disabled = true;

    const loadingMessage = addMessage(
        "Thinking... 🤔",
        "bot"
    );

    try {

        const response = await fetch("/ask", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                message: question
            })

        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.reply || "Something went wrong.");
        }

        loadingMessage.querySelector(".bubble").textContent =
            data.reply || "Sorry, I couldn't generate an answer.";

    } catch (error) {

        loadingMessage.querySelector(".bubble").textContent =
            "Sorry! I couldn't connect to the AI assistant. Please try again.";

        console.error(error);

    } finally {

        sendButton.disabled = false;
        userInput.focus();

        messages.scrollTop = messages.scrollHeight;
    }
}


chatForm.addEventListener("submit", function(event) {

    event.preventDefault();

    const question = userInput.value.trim();

    sendMessage(question);

});


function sendSuggestion(question) {

    sendMessage(question);

}
