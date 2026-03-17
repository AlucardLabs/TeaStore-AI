/**
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
package tools.descartes.teastore.webui.servlet;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.net.HttpURLConnection;
import java.net.URL;
import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import javax.naming.InitialContext;
import javax.naming.NamingException;

import jakarta.servlet.ServletException;
import jakarta.servlet.annotation.WebServlet;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.node.ObjectNode;

import tools.descartes.teastore.entities.Category;
import tools.descartes.teastore.entities.ImageSizePreset;
import tools.descartes.teastore.entities.Product;
import tools.descartes.teastore.registryclient.Service;
import tools.descartes.teastore.registryclient.loadbalancers.LoadBalancerTimeoutException;
import tools.descartes.teastore.registryclient.rest.LoadBalancedCRUDOperations;
import tools.descartes.teastore.registryclient.rest.LoadBalancedImageOperations;
import tools.descartes.teastore.registryclient.rest.LoadBalancedStoreOperations;

/**
 * Servlet implementation for AI Chat Interface using Intelligent Gateway (Track 2).
 * Provides a conversational interface with intent detection and natural language processing.
 *
 * @author TeaStore AI Integration Team
 */
@WebServlet("/aichat")
public class AIChatServlet extends AbstractUIServlet {
	private static final long serialVersionUID = 1L;

	private static final String INTELLIGENT_GATEWAY_URL_ENV = "intelligentGatewayURL";
	private static final String DEFAULT_INTELLIGENT_GATEWAY_URL = "http://localhost:8000/api/v1/intelligent";

	private String intelligentGatewayURL;
	private ObjectMapper objectMapper;

	/**
	 * Constructor - initializes Intelligent Gateway URL from web.xml.
	 */
	public AIChatServlet() {
		super();
		this.objectMapper = new ObjectMapper();

		// Read Intelligent Gateway URL from web.xml env-entry
		try {
			InitialContext ctx = new InitialContext();
			intelligentGatewayURL = (String) ctx.lookup("java:comp/env/" + INTELLIGENT_GATEWAY_URL_ENV);
		} catch (NamingException e) {
			// Fallback to default if not configured
			intelligentGatewayURL = DEFAULT_INTELLIGENT_GATEWAY_URL;
			System.err.println("Intelligent Gateway URL not configured in web.xml, using default: "
					+ intelligentGatewayURL);
		}
	}

	/**
	 * {@inheritDoc}
	 * Displays the AI chat interface.
	 */
	@Override
	protected void handleGETRequest(HttpServletRequest request, HttpServletResponse response)
			throws ServletException, IOException, LoadBalancerTimeoutException {

		checkforCookie(request, response);

		// Set common attributes for JSP
		request.setAttribute("storeIcon",
				LoadBalancedImageOperations.getWebImage("icon", ImageSizePreset.ICON.getSize()));
		request.setAttribute("CategoryList", LoadBalancedCRUDOperations
				.getEntities(Service.PERSISTENCE, "categories", Category.class, -1, -1));
		request.setAttribute("title", "TeaStore AI Chat Assistant");
		request.setAttribute("login",
				LoadBalancedStoreOperations.isLoggedIn(getSessionBlob(request)));

		// Forward to JSP
		request.getRequestDispatcher("WEB-INF/pages/ai_chat.jsp").forward(request, response);
	}

	/**
	 * {@inheritDoc}
	 * Processes chat messages via AJAX or redirects form submissions.
	 */
	@Override
	protected void handlePOSTRequest(HttpServletRequest request, HttpServletResponse response)
			throws ServletException, IOException, LoadBalancerTimeoutException {

		// Check if this is an AJAX request (expecting JSON response)
		String acceptHeader = request.getHeader("Accept");
		if (acceptHeader != null && acceptHeader.contains("application/json")) {
			handleAjaxChatMessage(request, response);
		} else {
			// Regular form submission - redirect to GET
			redirect("/aichat", response);
		}
	}

	/**
	 * Handles AJAX chat messages and returns JSON response.
	 *
	 * @param request HTTP request containing the user message
	 * @param response HTTP response to send JSON result
	 * @throws IOException if response writing fails
	 */
	private void handleAjaxChatMessage(HttpServletRequest request, HttpServletResponse response)
			throws IOException {

		// Set response type to JSON
		response.setContentType("application/json");
		response.setCharacterEncoding("UTF-8");

		// Parse request to get user message
		String message = request.getParameter("message");

		if (message == null || message.trim().isEmpty()) {
			// Return error for empty message
			ObjectNode errorResponse = objectMapper.createObjectNode();
			errorResponse.put("success", false);
			errorResponse.put("error", "Message cannot be empty");
			response.getWriter().write(objectMapper.writeValueAsString(errorResponse));
			return;
		}

		try {
			// Call Intelligent Gateway (Track 2)
			IntelligentResponse aiResponse = callIntelligentGateway(message.trim());

			// Build JSON response
			ObjectNode jsonResponse = objectMapper.createObjectNode();
			jsonResponse.put("success", true);
			jsonResponse.put("intent", aiResponse.intent);
			jsonResponse.put("message", aiResponse.message);

			// Add products if intent is SEARCH
			if ("SEARCH".equals(aiResponse.intent) && aiResponse.products != null
					&& !aiResponse.products.isEmpty()) {

				// Limit to maximum 4 products for chat display
				List<Product> productsToShow = aiResponse.products.size() > 4
						? aiResponse.products.subList(0, 4)
						: aiResponse.products;

				// Update message to show correct count
				if (aiResponse.message != null && aiResponse.message.contains(String.valueOf(aiResponse.products.size()))) {
					aiResponse.message = aiResponse.message.replace(
							String.valueOf(aiResponse.products.size()),
							String.valueOf(productsToShow.size()));
				}

				// Load product images
				Map<Long, String> productImages =
						LoadBalancedImageOperations.getProductPreviewImages(productsToShow);

				// Convert product images map to have String keys for JSON compatibility
				Map<String, String> productImagesForJson = new HashMap<>();
				for (Map.Entry<Long, String> entry : productImages.entrySet()) {
					productImagesForJson.put(String.valueOf(entry.getKey()), entry.getValue());
				}

				// Convert products to JSON array
				jsonResponse.set("products", objectMapper.valueToTree(productsToShow));
				jsonResponse.set("productImages", objectMapper.valueToTree(productImagesForJson));
			}

			response.getWriter().write(objectMapper.writeValueAsString(jsonResponse));

		} catch (Exception e) {
			// Return error response
			ObjectNode errorResponse = objectMapper.createObjectNode();
			errorResponse.put("success", false);
			errorResponse.put("error", "AI service unavailable. Please try again later.");
			System.err.println("Error calling Intelligent Gateway: " + e.getMessage());
			e.printStackTrace();
			response.getWriter().write(objectMapper.writeValueAsString(errorResponse));
		}
	}

	/**
	 * Calls the Intelligent Gateway API (Track 2) to process natural language requests.
	 *
	 * @param message The user's natural language message
	 * @return IntelligentResponse containing intent, AI message, and optional products
	 * @throws IOException if the API call fails
	 */
	private IntelligentResponse callIntelligentGateway(String message) throws IOException {
		IntelligentResponse result = new IntelligentResponse();

		// Create request JSON
		ObjectNode requestJson = objectMapper.createObjectNode();
		requestJson.put("request", message);

		String requestBody = objectMapper.writeValueAsString(requestJson);

		// Make HTTP POST request
		URL url = new URL(intelligentGatewayURL);
		HttpURLConnection conn = (HttpURLConnection) url.openConnection();

		try {
			conn.setRequestMethod("POST");
			conn.setRequestProperty("Content-Type", "application/json");
			conn.setDoOutput(true);
			conn.setConnectTimeout(5000); // 5 seconds
			conn.setReadTimeout(15000); // 15 seconds

			// Send request
			try (OutputStream os = conn.getOutputStream()) {
				byte[] input = requestBody.getBytes(StandardCharsets.UTF_8);
				os.write(input, 0, input.length);
			}

			// Read response
			int responseCode = conn.getResponseCode();
			if (responseCode == HttpURLConnection.HTTP_OK) {
				StringBuilder responseBody = new StringBuilder();
				try (BufferedReader br = new BufferedReader(
						new InputStreamReader(conn.getInputStream(), StandardCharsets.UTF_8))) {
					String line;
					while ((line = br.readLine()) != null) {
						responseBody.append(line);
					}
				}

				// Parse JSON response
				result = parseIntelligentResponse(responseBody.toString());

			} else {
				throw new IOException("Intelligent Gateway returned HTTP " + responseCode);
			}

		} finally {
			conn.disconnect();
		}

		return result;
	}

	/**
	 * Parses the Intelligent Gateway JSON response.
	 *
	 * @param jsonResponse JSON response from Intelligent Gateway
	 * @return IntelligentResponse object
	 * @throws IOException if JSON parsing fails
	 */
	private IntelligentResponse parseIntelligentResponse(String jsonResponse) throws IOException {
		IntelligentResponse result = new IntelligentResponse();

		JsonNode root = objectMapper.readTree(jsonResponse);

		// Extract intent
		if (root.has("intent")) {
			result.intent = root.get("intent").asText();
		}

		// Extract AI message/response (could be in different fields)
		if (root.has("response")) {
			result.message = root.get("response").asText();
		} else if (root.has("message")) {
			result.message = root.get("message").asText();
		}

		// Extract products if SEARCH intent
		if ("SEARCH".equals(result.intent)) {
			JsonNode results = root.get("results");
			if (results != null && results.isArray()) {
				result.products = new ArrayList<>();
				for (JsonNode resultNode : results) {
					// Each result contains {product: {...}, score: ...}
					JsonNode productNode = resultNode.get("product");

					if (productNode != null) {
						Product product = new Product();

						if (productNode.has("id")) {
							product.setId(productNode.get("id").asLong());
						}
						if (productNode.has("category_id")) {
							product.setCategoryId(productNode.get("category_id").asLong());
						}
						if (productNode.has("name")) {
							product.setName(productNode.get("name").asText());
						}
						if (productNode.has("description")) {
							product.setDescription(productNode.get("description").asText());
						}
						if (productNode.has("price_cents")) {
							product.setListPriceInCents(productNode.get("price_cents").asLong());
						}

						result.products.add(product);
					}
				}

				// Set a default message if not provided
				if (result.message == null || result.message.isEmpty()) {
					result.message = "Here are " + result.products.size() + " products I found:";
				}
			}
		}

		// Fallback message if none provided
		if (result.message == null || result.message.isEmpty()) {
			result.message = "I'm not sure how to help with that. Can you try rephrasing?";
		}

		return result;
	}

	/**
	 * Internal class to hold Intelligent Gateway response data.
	 */
	private static class IntelligentResponse {
		String intent;
		String message;
		List<Product> products;
	}
}
