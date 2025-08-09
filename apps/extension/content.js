console.log("Universal Memory content script loaded.");

const siteConfig = {
  chatGpt: {
    targetNodeSelector: 'main',
    messageSelector: '.text-base',
  }
};

function sendConversationData(text) {
    if (!text || text.trim().length < 10) return;
    const payload = {
        source: window.location.hostname,
        timestamp: Math.floor(Date.now() / 1000),
        content: [{ speaker: 'unknown', text: text }]
    };
    chrome.runtime.sendMessage({ type: "SAVE_CONVERSATION", data: payload });
}

function processNewMessages(mutationsList) {
    for (const mutation of mutationsList) {
        if (mutation.type === 'childList' && mutation.addedNodes.length > 0) {
            mutation.addedNodes.forEach(node => {
                if (node.nodeType === Node.ELEMENT_NODE) {
                    const messageElement = node.querySelector(siteConfig.chatGpt.messageSelector);
                    if (messageElement) {
                        sendConversationData(messageElement.innerText);
                    }
                }
            });
        }
    }
}

const observer = new MutationObserver(processNewMessages);

const interval = setInterval(() => {
    const targetNode = document.querySelector(siteConfig.chatGpt.targetNodeSelector);
    if (targetNode) {
        clearInterval(interval);
        observer.observe(targetNode, { childList: true, subtree: true });
        console.log("Observer is now watching the chat.");
    }
}, 1000);