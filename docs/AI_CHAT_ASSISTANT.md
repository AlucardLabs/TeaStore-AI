# AI Chat Assistant - Technical Documentation

## Overview

The AI Chat Assistant is a conversational interface integrated into TeaStore WebUI that provides natural language interaction with the product catalog. It uses LLM-powered intent detection to understand user queries and orchestrate appropriate responses.

## Architecture

```
┌──────────────────────────────────────────────────────┐
│             User Browser                              │
│  ┌────────────┐         ┌────────────────────────┐  │
│  │ ai_chat.jsp│◄────────┤ chat.js (Vanilla JS)   │  │
│  │            │         │ - Fetch API            │  │
│  │            │         │ - AJAX messaging       │  │
│  └────────────┘         └────────────────────────┘  │
└────────────────────┬─────────────────────────────────┘
                     │ POST /aichat
                     │ { message: "..." }
                     ↓
         ┌───────────────────────────┐
         │  AIChatServlet (Java)     │
         │  - Servlet @WebServlet    │
         │  - Jackson JSON parsing   │
         │  - HttpURLConnection      │
         └───────────────────────────┘
                     │ POST /api/v1/intelligent
                     │ { request: "..." }
                     ↓
         ┌───────────────────────────┐
         │  AI Gateway (Python)      │
         │  Track 2: Intelligent     │
         └───────────────────────────┘
                     │
                     ↓
         ┌───────────────────────────┐
         │  Ollama (LLM)             │
         │  - Intent detection       │
         │  - llama3.2 model         │
         └───────────────────────────┘
                     │ Intent: SEARCH
                     ↓
         ┌───────────────────────────┐
         │  AI Orchestrator          │
         │  - LangChain/LangGraph    │
         │  - Workflow orchestration │
         └───────────────────────────┘
                     │
                     ↓
         ┌───────────────────────────┐
         │  Search Service           │
         │  - Vector embeddings      │
         │  - Semantic search        │
         └───────────────────────────┘
                     │
                     ↓
         ┌───────────────────────────┐
         │  Qdrant Vector DB         │
         │  - Product vectors        │
         │  - Similarity search      │
         └───────────────────────────┘
```

## Components

### 1. Frontend (`chat.js`)

**Technology:** Vanilla JavaScript with Fetch API

**Key Features:**
- AJAX communication with servlet
- Real-time message rendering
- Product card display with images
- Loading indicators (animated dots)
- Error handling and retry logic
- XSS prevention with HTML escaping
- 15-second request timeout

**Message Flow:**
```javascript
1. User types message and hits Enter or clicks Send
2. Display user message bubble (right-aligned, blue)
3. Show loading indicator (animated dots)
4. POST to /aichat via Fetch API
5. Parse JSON response
6. Hide loading indicator
7. Display AI message bubble (left-aligned, gray)
8. If products: render product cards with images
```

**Product Card Format:**
- Thumbnail image
- Product name (bold)
- Price (formatted as $XX.XX)
- Description
- "Add to Cart" button (functional form submission)

### 2. Backend Servlet (`AIChatServlet.java`)

**Technology:** Jakarta EE Servlet, Jackson JSON

**Key Classes:**
- `AIChatServlet` - Main servlet handling GET/POST requests
- `IntelligentResponse` - Internal DTO for Gateway responses

**Endpoints:**

**GET /aichat**
- Displays chat interface
- Sets up JSP with categories, login state, icons
- Forwards to `ai_chat.jsp`

**POST /aichat**
- Detects AJAX via `Accept: application/json` header
- Parses `message` parameter
- Calls Intelligent Gateway
- Returns JSON response:
  ```json
  {
    "success": true,
    "intent": "SEARCH",
    "message": "Here are 4 products I found:",
    "products": [...],
    "productImages": { "1": "data:image/webp;base64,..." }
  }
  ```

**Configuration:**
```java
// Read from web.xml env-entry
InitialContext ctx = new InitialContext();
intelligentGatewayURL = (String) ctx.lookup("java:comp/env/intelligentGatewayURL");
// Default: http://localhost:8000/api/v1/intelligent
```

**HTTP Client:**
- Uses `HttpURLConnection` (no external dependencies)
- Connect timeout: 5 seconds
- Read timeout: 15 seconds
- JSON serialization: Jackson `ObjectMapper`

**Error Handling:**
- Empty message validation
- HTTP status code checking
- JSON parsing error handling
- Timeout handling
- Generic error responses to prevent information leakage

### 3. Intelligent Gateway API

**Endpoint:** `POST /api/v1/intelligent`

**Request:**
```json
{
  "request": "Show me organic green teas"
}
```

**Response (SEARCH Intent):**
```json
{
  "intent": "SEARCH",
  "response": "Here are 4 products I found:",
  "results": [
    {
      "product": {
        "id": 5,
        "category_id": 1,
        "name": "Organic Sencha",
        "description": "Premium organic Japanese green tea",
        "price_cents": 1895
      },
      "score": 0.892
    }
  ]
}
```

**Response (GENERAL Intent):**
```json
{
  "intent": "GENERAL",
  "response": "I'm here to help you find tea products. Would you like me to search for something specific?"
}
```

**Intents Supported:**
- `SEARCH` - Product search queries → triggers semantic search
- `GENERAL` - General conversation → AI-generated response
- Additional intents can be added via LLM prompt engineering

### 4. UI/UX Design

**Chat Container:**
- Fixed height with scrolling
- Auto-scroll to bottom on new messages
- Border and rounded corners
- White background

**Message Bubbles:**
- User: Right-aligned, blue background (`#007bff`), white text
- AI: Left-aligned, gray background (`#e9ecef`), dark text
- Max-width: 70% of container
- Padding: 10px 15px
- Border-radius: 15px

**Loading Indicator:**
- Three animated dots
- CSS keyframe animation
- Gray background matching AI messages
- Bouncing effect (0.6s duration)

**Product Grid:**
- Bootstrap grid layout (col-sm-6)
- Responsive: 2 columns on medium+, 1 column on small screens
- Thumbnail format matching product listing pages
- Functional "Add to Cart" forms with product ID

**Error Display:**
- Bootstrap alert-danger
- Hidden by default
- Shows below chat input
- Auto-hides on new message

## Configuration

### web.xml Entry

```xml
<env-entry>
  <env-entry-name>intelligentGatewayURL</env-entry-name>
  <env-entry-type>java.lang.String</env-entry-type>
  <env-entry-value>http://host.docker.internal:8000/api/v1/intelligent</env-entry-value>
</env-entry>
```

### Docker Networking

**Mac/Windows:**
```yaml
environment:
  - intelligentGatewayURL=http://host.docker.internal:8000/api/v1/intelligent
```

**Linux:**
```yaml
extra_hosts:
  - "host.docker.internal:172.17.0.1"
environment:
  - intelligentGatewayURL=http://host.docker.internal:8000/api/v1/intelligent
```

Or use host IP directly:
```yaml
environment:
  - intelligentGatewayURL=http://192.168.1.100:8000/api/v1/intelligent
```

## Usage Examples

### Simple Product Search

**User Input:**
```
Show me green teas
```

**AI Response:**
```
Here are 4 green tea products I found:
[Product Card: Organic Sencha - $18.95]
[Product Card: Dragon Well - $24.95]
[Product Card: Matcha Powder - $29.95]
[Product Card: Jasmine Green Tea - $16.95]
```

### Natural Language Query

**User Input:**
```
I need something relaxing for bedtime
```

**AI Response:**
```
I found some great relaxing teas perfect for bedtime:
[Product Card: Chamomile Tea - $12.95]
[Product Card: Lavender Dream - $14.95]
[Product Card: Bedtime Blend - $13.95]
[Product Card: Valerian Root Tea - $15.95]
```

### Price-Filtered Search

**User Input:**
```
Find me cheap herbal teas under $15
```

**AI Response:**
```
Here are 4 affordable herbal teas under $15:
[Product Card: Peppermint Tea - $11.95]
[Product Card: Chamomile Tea - $12.95]
[Product Card: Ginger Turmeric - $13.95]
[Product Card: Hibiscus Tea - $10.95]
```

### General Conversation

**User Input:**
```
How are you today?
```

**AI Response:**
```
I'm doing well, thank you! I'm here to help you find the perfect tea.
Would you like me to recommend something based on your preferences?
```

## Development Guide

### Adding New Intents

1. **Update LLM Prompt** (AI Gateway):
```python
# In AI Gateway prompt engineering
INTENTS = ["SEARCH", "GENERAL", "PRICE_INQUIRY", "CATEGORY_BROWSE"]
```

2. **Handle in AIChatServlet**:
```java
if ("PRICE_INQUIRY".equals(result.intent)) {
    // Handle price inquiry logic
    jsonResponse.put("intent", "PRICE_INQUIRY");
    jsonResponse.put("message", result.message);
}
```

3. **Update Frontend** (chat.js):
```javascript
if (data.intent === 'PRICE_INQUIRY') {
    // Custom rendering for price inquiries
    addPriceCard(data.price_info);
}
```

### Customizing Product Display Limit

Current limit: 4 products max in chat

To change:
```java
// In AIChatServlet.java:162
List<Product> productsToShow = aiResponse.products.size() > 4
    ? aiResponse.products.subList(0, 4)  // Change this limit
    : aiResponse.products;
```

### Adding Loading States

```javascript
// In chat.js
function showTypingIndicator() {
    const loadingDiv = document.createElement('div');
    loadingDiv.className = 'chat-message ai typing-indicator';
    loadingDiv.innerHTML = '<div class="message-bubble">AI is typing...</div>';
    messagesContainer.appendChild(loadingDiv);
}
```

### Error Recovery

**Timeout Handling:**
```javascript
// In chat.js:68
const timeoutId = setTimeout(() => controller.abort(), 15000); // Adjust timeout
```

**Retry Logic:**
```java
// In AIChatServlet
int maxRetries = 3;
for (int i = 0; i < maxRetries; i++) {
    try {
        result = callIntelligentGateway(message);
        break;
    } catch (IOException e) {
        if (i == maxRetries - 1) throw e;
    }
}
```

## Testing

### Manual Testing

1. **Start Services:**
```bash
scripts/start-full-stack.sh
```

2. **Access Chat:**
```
http://localhost:8080/tools.descartes.teastore.webui/aichat
```

3. **Test Scenarios:**
- Product search queries
- Natural language conversation
- Price filtering
- Category browsing
- Edge cases (empty input, special characters)

### API Testing

```bash
# Test Intelligent Gateway directly
curl -X POST http://localhost:8000/api/v1/intelligent \
  -H "Content-Type: application/json" \
  -d '{"request": "Show me organic green teas"}'

# Expected response
{
  "intent": "SEARCH",
  "response": "Here are 4 products I found:",
  "results": [...]
}
```

### Browser Console Testing

```javascript
// Test message sending
fetch('/tools.descartes.teastore.webui/aichat', {
    method: 'POST',
    headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/x-www-form-urlencoded'
    },
    body: 'message=Show me green teas'
})
.then(r => r.json())
.then(console.log);
```

## Performance Considerations

### Response Times

- **Network Latency**: WebUI → Gateway: ~10ms
- **LLM Inference**: Ollama intent detection: ~500-2000ms
- **Semantic Search**: Vector search: ~50-200ms
- **Total**: Average 1-3 seconds

### Optimization Tips

1. **Cache Common Intents:**
```java
private final Map<String, String> intentCache = new ConcurrentHashMap<>();
```

2. **Product Image Preloading:**
```javascript
// Preload common product images
productImages.forEach(img => {
    const image = new Image();
    image.src = img;
});
```

3. **Reduce LLM Token Count:**
- Limit chat history context
- Use shorter system prompts
- Enable streaming responses

### Scalability

**Current Limitations:**
- Single-threaded Ollama (1 request at a time)
- No conversation history persistence
- In-memory session management

**Improvements:**
- Deploy multiple Ollama instances with load balancing
- Add Redis for conversation state
- Implement request queuing for high traffic

## Security

### Input Validation

```java
// In AIChatServlet
if (message == null || message.trim().isEmpty()) {
    return errorResponse("Message cannot be empty");
}

// Limit message length
if (message.length() > 500) {
    return errorResponse("Message too long");
}
```

### XSS Prevention

```javascript
// In chat.js:240
function escapeHtml(text) {
    if (!text) return '';
    const div = document.createElement('div');
    div.textContent = text;  // Uses textContent, not innerHTML
    return div.innerHTML;
}
```

### Rate Limiting

```java
// Add rate limiting per session
private final Map<String, RateLimiter> rateLimiters = new ConcurrentHashMap<>();

@Override
protected void handlePOSTRequest(...) {
    String sessionId = getSessionBlob(request).getUID();
    RateLimiter limiter = rateLimiters.computeIfAbsent(
        sessionId, k -> RateLimiter.create(10) // 10 req/sec
    );

    if (!limiter.tryAcquire()) {
        response.setStatus(429); // Too Many Requests
        return;
    }
    // ... rest of handler
}
```

## Troubleshooting

### Chat Not Loading

**Symptom:** Blank page or JSP errors

**Solutions:**
1. Check WebUI logs: `scripts/logs.sh webui`
2. Verify categories are loaded: `curl http://localhost:8080/tools.descartes.teastore.webui/rest/categories`
3. Check servlet mapping in web.xml

### Gateway Unreachable

**Symptom:** "AI service unavailable" errors

**Solutions:**
1. Verify Gateway is running: `curl http://localhost:8000/health`
2. Check Docker networking: `docker exec webui ping host.docker.internal`
3. Try direct IP instead of `host.docker.internal`
4. Check firewall rules

### Products Not Displaying

**Symptom:** Chat works but no product cards

**Solutions:**
1. Verify products are indexed: `curl http://localhost:8002/index/status`
2. Check JSON structure in browser console
3. Verify image service: `curl http://localhost:8080/tools.descartes.teastore.webui/rest/image/5`
4. Check for JavaScript errors in console

### Slow Responses

**Symptom:** >5 second response times

**Solutions:**
1. Check Ollama model loaded: `curl http://localhost:11434/api/tags`
2. Monitor CPU/GPU usage during inference
3. Reduce Qdrant search limit in AI Orchestrator
4. Enable Ollama GPU acceleration if available

## Future Enhancements

### Conversation History

```java
// Store conversation in session
class ChatHistory {
    List<Message> messages = new ArrayList<>();

    void addUserMessage(String text) {
        messages.add(new Message("user", text, Instant.now()));
    }

    void addAIMessage(String text) {
        messages.add(new Message("ai", text, Instant.now()));
    }
}

// In servlet
ChatHistory history = (ChatHistory) request.getSession()
    .getAttribute("chatHistory");
```

### Streaming Responses

```javascript
// Use Server-Sent Events for real-time streaming
const eventSource = new EventSource('/aichat/stream');
eventSource.onmessage = (event) => {
    const chunk = JSON.parse(event.data);
    appendToLastMessage(chunk.text);
};
```

### Multi-language Support

```java
// Detect user language from headers
String userLang = request.getHeader("Accept-Language");
requestJson.put("language", userLang);
```

### Voice Input

```javascript
// Add speech recognition
const recognition = new webkitSpeechRecognition();
recognition.onresult = (event) => {
    const transcript = event.results[0][0].transcript;
    chatInput.value = transcript;
    sendMessage();
};
```

## References

- **Servlet Code:** `services/tools.descartes.teastore.webui/src/main/java/tools/descartes/teastore/webui/servlet/AIChatServlet.java`
- **Frontend Code:** `services/tools.descartes.teastore.webui/src/main/webapp/chat.js`
- **JSP Template:** `services/tools.descartes.teastore.webui/src/main/webapp/WEB-INF/pages/ai_chat.jsp`
- **CSS Styles:** `services/tools.descartes.teastore.webui/src/main/webapp/teastore.css` (lines 326-419)
- **Configuration:** `services/tools.descartes.teastore.webui/src/main/webapp/WEB-INF/web.xml` (lines 40-43)
- **AI Gateway Docs:** `ai-capabilities/README.md`
