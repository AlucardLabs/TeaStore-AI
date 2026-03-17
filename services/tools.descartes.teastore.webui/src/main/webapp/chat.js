/**
 * AI Chat Interface - Client-side JavaScript (Vanilla JS with Fetch API)
 * Handles communication with AIChatServlet and dynamic message rendering
 */

// Initialize chat when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
    // Add welcome message on page load
    addWelcomeMessage();

    // Get DOM elements
    const sendButton = document.getElementById('sendButton');
    const chatInput = document.getElementById('chatInput');

    // Send message on button click
    sendButton.addEventListener('click', sendMessage);

    // Send message on Enter key
    chatInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            e.preventDefault();
            sendMessage();
        }
    });
});

/**
 * Add welcome message when chat loads
 */
function addWelcomeMessage() {
    addMessage('ai', 'Hi I am your AI Assistant, how can I help you?');
}

/**
 * Send user message to server via Fetch API
 */
async function sendMessage() {
    const input = document.getElementById('chatInput');
    const message = input.value.trim();

    if (message === '') {
        return; // Don't send empty messages
    }

    // Display user message
    addMessage('user', message);

    // Clear input field
    input.value = '';

    // Disable send button during request
    const sendButton = document.getElementById('sendButton');
    sendButton.disabled = true;

    // Show loading indicator
    showLoading();

    // Hide any previous errors
    document.getElementById('chatError').style.display = 'none';

    try {
        // Create form data
        const formData = new URLSearchParams();
        formData.append('message', message);

        // Make fetch request with timeout
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), 15000); // 15 second timeout

        const response = await fetch('aichat', {
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            body: formData,
            signal: controller.signal
        });

        clearTimeout(timeoutId);

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        hideLoading();
        handleResponse(data);

    } catch (error) {
        hideLoading();

        let errorMsg = 'Failed to communicate with AI service.';
        if (error.name === 'AbortError') {
            errorMsg = 'Request timed out. The AI service may be processing your request.';
        }

        showError(errorMsg);
        addMessage('ai', 'Sorry, I encountered an error. Please try again.');
        console.error('Chat error:', error);

    } finally {
        sendButton.disabled = false;
    }
}

/**
 * Handle successful response
 */
function handleResponse(data) {
    if (!data.success) {
        showError(data.error || 'Unknown error occurred');
        addMessage('ai', 'Sorry, I encountered an error processing your request.');
        return;
    }

    // Add AI response message
    if (data.message) {
        addMessage('ai', data.message);
    }

    // Add product cards if present
    if (data.products && data.products.length > 0) {
        addProducts(data.products, data.productImages);
    }
}

/**
 * Add a text message to the chat
 */
function addMessage(sender, text) {
    const messagesContainer = document.getElementById('chatMessages');
    const messageClass = sender === 'user' ? 'chat-message user' : 'chat-message ai';

    const messageDiv = document.createElement('div');
    messageDiv.className = messageClass;
    messageDiv.innerHTML = `<div class="message-bubble">${escapeHtml(text)}</div>`;

    messagesContainer.appendChild(messageDiv);
    scrollToBottom();
}

/**
 * Add product cards to the chat
 */
function addProducts(products, productImages) {
    const messagesContainer = document.getElementById('chatMessages');

    const messageDiv = document.createElement('div');
    messageDiv.className = 'chat-message ai';

    let productsHtml = '<div class="chat-products-grid row">';

    products.forEach(product => {
        // Access image using String key (product.id converted to string)
        const imageUrl = productImages && productImages[String(product.id)] ? productImages[String(product.id)] : '';
        const priceFormatted = (product.listPriceInCents / 100).toFixed(2);
        const description = product.description || '';

        productsHtml += `
            <div class="col-sm-6">
                <div class="thumbnail">
                    <form action="cartAction" method="POST">
                        <table>
                            <tr>
                                <td class="productthumb">
                                    <input type="hidden" name="productid" value="${product.id}">
                                    <a href="product?id=${product.id}">
                                        <img src="${escapeHtml(imageUrl)}" alt="${escapeHtml(product.name)}">
                                    </a>
                                </td>
                                <td class="divider"></td>
                                <td class="description">
                                    <b>${escapeHtml(product.name)}</b><br>
                                    <span>Price: $${priceFormatted}</span><br>
                                    <span>${escapeHtml(description)}</span>
                                </td>
                            </tr>
                        </table>
                        <input name="addToCart" class="btn" value="Add to Cart" type="submit">
                    </form>
                </div>
            </div>`;
    });

    productsHtml += '</div>';
    messageDiv.innerHTML = productsHtml;

    messagesContainer.appendChild(messageDiv);
    scrollToBottom();
}

/**
 * Show loading indicator
 */
function showLoading() {
    const messagesContainer = document.getElementById('chatMessages');

    const loadingDiv = document.createElement('div');
    loadingDiv.className = 'chat-message ai';
    loadingDiv.id = 'loadingIndicator';
    loadingDiv.innerHTML = `
        <div class="message-bubble chat-loading">
            <span></span><span></span><span></span>
        </div>`;

    messagesContainer.appendChild(loadingDiv);
    scrollToBottom();
}

/**
 * Hide loading indicator
 */
function hideLoading() {
    const loadingIndicator = document.getElementById('loadingIndicator');
    if (loadingIndicator) {
        loadingIndicator.remove();
    }
}

/**
 * Show error alert
 */
function showError(message) {
    document.getElementById('chatErrorMessage').textContent = message;
    document.getElementById('chatError').style.display = 'block';
}

/**
 * Scroll chat to bottom
 */
function scrollToBottom() {
    const container = document.getElementById('chatContainer');
    container.scrollTop = container.scrollHeight;
}

/**
 * Escape HTML to prevent XSS
 */
function escapeHtml(text) {
    if (!text) return '';
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}
