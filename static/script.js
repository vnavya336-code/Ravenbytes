const form = document.getElementById("chatForm");

const input = document.getElementById("question");

const messages = document.getElementById("messages");


function addBubble(text, who) {

  const div = document.createElement("div");

  div.className = "bubble " + who;

  div.textContent = text;

  messages.appendChild(div);

  messages.scrollTop = messages.scrollHeight;
}


async function sendQuestion(question) {

  if (!question.trim()) return;

  addBubble(question, "user");

  input.value = "";

  try {

    const response = await fetch("/ask", {

      method: "POST",

      headers: {
        "Content-Type": "application/json"
      },

      body: JSON.stringify({question})

    });

    const data = await response.json();

    addBubble(
      data.answer || "Sorry, I couldn't prepare an answer.",
      "bot"
    );

  } catch (error) {

    addBubble(
      "Connection problem. Please try again.",
      "bot"
    );

  }

}


if (form) {

  form.addEventListener("submit", (event) => {

    event.preventDefault();

    sendQuestion(input.value);

  });

}


function quickAsk(question) {

  sendQuestion(question);

}