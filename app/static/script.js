function randomNumber(min, max) {
    return Math.floor(Math.random() * max) + min;
}

/**
 * A relatively simple object to store the messages that have happened
 * 
 * @param {string} sender This is the name that will be displayed at the top of the message.
 * @param {string} message This is the message that has been sent.
 */
class Message {
    constructor(sender, message) {
        this.sender = sender;
        this.message = message;
    }
}

/**
 * This is the client side version of the chat bot. It stores a local copy of all messages sent & recieved
 * Which are used to create the chat trail.
 */
class HolidayChatBot {
    username;
    constructor() {
        this.beforeFirstMessage = true;
        this.messages = [
            new Message("Bot", "Welcome to the holiday chat bot!\nBefore we begin, what should I call you?")
        ];
    }

    /**
     * Sends a http `Post` request to the Flask application
     * 
     * This request triggers the server side bot to set user preferences
     * and respond with either the next question or the recommended holidays.
     * @param {string} message
     */
    async sendMessageToBot(message) {
        if (this.beforeFirstMessage) {
            this.beforeFirstMessage = false;
            this.username = message;
        }

        this.messages.push(new Message(this.username, message));
        const method = "POST";
        const headers = {
            "Content-Type": "application/json"
        };
        const body = JSON.stringify({
            "msg": message
        });

        let res = await fetch("/recieve-message", {
            method: method,
            headers: headers,
            body: body
        })
            .then(res => res.json());

        this.updateScreen();
        setTimeout(() => {
            this.messages.push(new Message("Bot", res.msg));
            this.updateScreen();
        }, randomNumber(500, 1500));
    }

    /**
     * Called upon sending / receiving a message.
     * 
     * Replaces the existing Messages in the message list element
     * with the messages stored on the bot.
     */
    updateScreen() {
        let messageList = document.querySelector("#message-list");
        let messages = [];

        for (let message of this.messages) {
            let listItem = document.createElement("li");
            let h4Elem = document.createElement("h4");
            let pElem = document.createElement("p");

            h4Elem.innerText = message.sender;
            pElem.innerText = message.message;
            listItem.appendChild(h4Elem);
            listItem.appendChild(pElem);

            listItem.classList.add("message");

            messages.push(listItem);
        }

        messageList.replaceChildren(...messages);
        let chatBox = document.querySelector("#chat-box");
        chatBox.scrollTop = chatBox.scrollHeight;
    }
}

let bot = new HolidayChatBot();
/**
 * This function will shake the input and change the placeholder message.
 * This is a more user friendly way of letting them know the input is wrong than an alert.
 */
function shakeInput() {
    // Getting the required elements
    let container = document.querySelector("#message-box-container");
    let messageInput = document.querySelector("#message-input");
    let sendMessageButton = document.querySelector("#submit-button");

    let placeholderMessage = messageInput.placeholder;

    container.classList.add("shake");
    messageInput.classList.add("red", "red-border");
    sendMessageButton.classList.add("red", "red-border");

    messageInput.placeholder = "Invalid Input.";

    setTimeout(() => {
        container.classList.remove("shake");
        messageInput.classList.remove("red", "red-border");
        sendMessageButton.classList.remove("red", "red-border");

        messageInput.placeholder = placeholderMessage;
    }, 1000); // 1 Second
}

/**
 * This function is called when either 'Enter' is pressed
 * or the "Send Messages" button is clicked.
 * 
 * Calls the method on the `bot` instance to send a message to the server.
 */
async function handleMessageSubmit() {
    let messageInput = document.querySelector("#message-input");
    let message = messageInput.value;

    // Invalid Input (undefined, empty, etc)
    if (!message) {
        shakeInput();
        return;
    }

    await bot.sendMessageToBot(message);

    messageInput.value = "";
}

/**
 * Sends a request to reset the preferences and questions on the server side bot.
 */
async function resetBot() {
    fetch("/reset", { method: "POST" });
}

/**
 * Setting up the window.
 * 
 * Focuses the message input box for UX
 * Adds an event handler for the "Enter" key.
 * 
 * Updates the screen.
 */
window.onload = async () => {
    document.querySelector("#message-input").focus();
    document.addEventListener("keypress", async ev => {
        if (ev.code === "Enter") {
            await handleMessageSubmit();
        }
    });

    bot.updateScreen();
}