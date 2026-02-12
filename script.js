const chatBody = document.getElementById("chat-body");

function addMessage(text, sender) {
  const msg = document.createElement("div");
  msg.classList.add("message", sender);
  msg.textContent = text;
  chatBody.appendChild(msg);
  chatBody.scrollTop = chatBody.scrollHeight;
}

function sendMessage() {
  const input = document.getElementById("user-input");
  const userText = input.value.trim();
  if (!userText) return;
  addMessage(userText, "user");
  input.value = "";

  // Beginner-friendly financial dictionary
  const financeTerms = {
    "stock": "A stock is a share of ownership in a company. If you own a stock, you own a piece of that company.",
    "bond": "A bond is like a loan you give to a company or government. They promise to pay you back with interest.",
    "mutual fund": "A mutual fund pools money from many people to invest in stocks and bonds. It’s managed by professionals.",
    "inflation": "Inflation means prices of goods and services go up over time, reducing the value of money.",
    "budget": "A budget is a plan for how you will spend and save your money.",
    "sip": "SIP (Systematic Investment Plan) is a way to invest small amounts regularly in mutual funds, helping you build wealth over time.",
    "share market": "The share market is where people buy and sell shares (stocks) of companies. It’s also called the stock market."
  };

  let response = "I'm not sure about that term yet, but I can help explain basic finance concepts.";
  for (let term in financeTerms) {
    if (userText.toLowerCase().includes(term)) {
      response = financeTerms[term];
      break;
    }
  }

  setTimeout(() => addMessage(response, "bot"), 600);
}

// Default greeting when page loads
window.onload = () => {
  addMessage("Hi! I’m your financial chatbot. Ask me about terms like SIP, stock, bond, inflation, or share market, and I’ll explain them simply.", "bot");
};
