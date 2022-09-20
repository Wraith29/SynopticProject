class Message {
    constructor(sender, message) {
        this.sender = sender;
        this.message = message;
    }
}

class HolidayChatBot {
    constructor() {
        this.messages = [new Message("Bot", "Welcome to the holiday chat bot!")];
    }

    async sendMessageToBot(message) {
        this.messages.push(new Message("User", message));
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
            this.messages.push(new Message("Bot", res.res));
            this.updateScreen();
        }, 1000);
    }
    
    // This method will update the list of messages on screen
    // It does this by reading all of the messages in the object
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
    }
}

let bot = new HolidayChatBot();

bot.updateScreen();

async function handleMessageSubmit() {
    let messageInput = document.querySelector("#message-input");
    let message = messageInput.value;

    // Invalid Input (undefined, empty, etc)
    if (!message) {
        alert("That is an invalid input, please try again!"); // TODO: Fix this maybe?
        return;
    }

    await bot.sendMessageToBot(message);

    messageInput.value = "";
}

async function resetBot() {
    fetch("/reset", {method: "POST"});
}