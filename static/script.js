// ==========================================================================
// Simple JavaScript for College FAQ Chatbot (Student Project)
// ==========================================================================

document.addEventListener("DOMContentLoaded", function () {
  const chatForm = document.getElementById("chat-form");
  const userInput = document.getElementById("user-input");
  const chatBox = document.getElementById("chat-box");
  const suggestionButtons = document.querySelectorAll(".suggestion-btn");

  // Function to append a message to the chat window
  function appendMessage(sender, text) {
    const messageDiv = document.createElement("div");
    messageDiv.classList.add("message");

    if (sender === "user") {
      messageDiv.classList.add("user-message");
    } else {
      messageDiv.classList.add("bot-message");
    }

    const bubbleDiv = document.createElement("div");
    bubbleDiv.classList.add("bubble");
    bubbleDiv.textContent = text;

    messageDiv.appendChild(bubbleDiv);
    chatBox.appendChild(messageDiv);

    // Automatically scroll to the bottom of the chat box
    chatBox.scrollTop = chatBox.scrollHeight;
  }

  // Function to send user question to the Flask backend
  function sendMessage(messageText) {
    const trimmedMessage = messageText.trim();
    if (!trimmedMessage) {
      return;
    }

    // 1. Display user message
    appendMessage("user", trimmedMessage);
    userInput.value = "";

    // 2. Send POST request to Flask endpoint /get_response
    fetch("/get_response", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ message: trimmedMessage })
    })
      .then(function (response) {
        if (!response.ok) {
          throw new Error("Server error: " + response.status);
        }
        return response.json();
      })
      .then(function (data) {
        // 3. Display chatbot response
        appendMessage("bot", data.answer);
      })
      .catch(function (error) {
        console.error("Error:", error);
        appendMessage("bot", "Sorry, something went wrong while connecting to the server. Please check if Flask is running.");
      });
  }

  // Handle form submit (when user presses Enter or clicks Send)
  chatForm.addEventListener("submit", function (e) {
    e.preventDefault();
    sendMessage(userInput.value);
  });

  // Handle clicking on sample suggestion buttons
  suggestionButtons.forEach(function (button) {
    button.addEventListener("click", function () {
      sendMessage(button.textContent);
    });
  });
});
