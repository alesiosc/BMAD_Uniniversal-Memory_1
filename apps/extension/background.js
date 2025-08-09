async function sendDataWithRetry(payload, retries = 3, delay = 1000) {
    for (let i = 0; i < retries; i++) {
        try {
            const response = await fetch("http://127.0.0.1:8000/conversations", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(payload),
            });
            if (response.ok) {
                console.log("Successfully saved conversation:", await response.json());
                return; // Success
            }
            console.error(`Attempt ${i + 1}: HTTP error! status: ${response.status}`);
        } catch (error) {
            console.error(`Attempt ${i + 1}: Network error`, error);
        }
        // Wait before retrying
        if (i < retries - 1) {
            await new Promise(resolve => setTimeout(resolve, delay));
        }
    }
    console.error("Failed to save conversation after multiple retries:", payload);
}

chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.type === "SAVE_CONVERSATION") {
        console.log("Received conversation to save:", request.data);
        sendDataWithRetry(request.data);
        return true; // Indicate async response
    }
});