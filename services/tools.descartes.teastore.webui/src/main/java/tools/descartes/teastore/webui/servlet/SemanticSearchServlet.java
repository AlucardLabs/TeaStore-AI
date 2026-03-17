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
import java.util.List;

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
 * Servlet implementation for Semantic Search using AI Gateway (Track 1).
 *
 * @author TeaStore AI Integration Team
 */
@WebServlet("/semanticsearch")
public class SemanticSearchServlet extends AbstractUIServlet {
	private static final long serialVersionUID = 1L;

	private static final int DEFAULT_SEARCH_LIMIT = 20;
	private static final String AI_GATEWAY_URL_ENV = "aiGatewayURL";
	private static final String DEFAULT_AI_GATEWAY_URL = "http://localhost:8000/api/v1/search";

	private String aiGatewayURL;
	private ObjectMapper objectMapper;

	/**
	 * Constructor - initializes AI Gateway URL from web.xml.
	 */
	public SemanticSearchServlet() {
		super();
		this.objectMapper = new ObjectMapper();

		// Read AI Gateway URL from web.xml env-entry
		try {
			InitialContext ctx = new InitialContext();
			aiGatewayURL = (String) ctx.lookup("java:comp/env/" + AI_GATEWAY_URL_ENV);
		} catch (NamingException e) {
			// Fallback to default if not configured
			aiGatewayURL = DEFAULT_AI_GATEWAY_URL;
			System.err.println("AI Gateway URL not configured in web.xml, using default: " + aiGatewayURL);
		}
	}

	/**
	 * {@inheritDoc}
	 * Displays the semantic search form.
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
		request.setAttribute("title", "TeaStore Semantic Search");
		request.setAttribute("login",
				LoadBalancedStoreOperations.isLoggedIn(getSessionBlob(request)));

		// Forward to JSP
		request.getRequestDispatcher("WEB-INF/pages/semantic_search.jsp").forward(request, response);
	}

	/**
	 * {@inheritDoc}
	 * Processes the semantic search request.
	 */
	@Override
	protected void handlePOSTRequest(HttpServletRequest request, HttpServletResponse response)
			throws ServletException, IOException, LoadBalancerTimeoutException {

		String query = request.getParameter("query");

		if (query == null || query.trim().isEmpty()) {
			// No query provided, redirect to GET
			redirect("/semanticsearch", response);
			return;
		}

		try {
			// Call AI Gateway Track 1
			List<Product> searchResults = callAIGateway(query.trim());

			// Load product images from Image Service (reusing TeaStore infrastructure)
			request.setAttribute("productImages",
					LoadBalancedImageOperations.getProductPreviewImages(searchResults));

			// Set results in request
			request.setAttribute("searchResults", searchResults);
			request.setAttribute("query", query);

			// Log for verification
			System.out.println("=== Semantic Search Results ===");
			System.out.println("Query: " + query);
			System.out.println("Results count: " + searchResults.size());
			for (Product p : searchResults) {
				System.out.println("  - Product ID: " + p.getId() + ", Name: " + p.getName()
					+ ", Price: " + p.getListPriceInCents() + " cents");
			}

		} catch (Exception e) {
			// Error calling AI Gateway
			request.setAttribute("error", "AI Search service unavailable. Please try again later.");
			request.setAttribute("query", query);
			System.err.println("Error calling AI Gateway: " + e.getMessage());
			e.printStackTrace();
		}

		// Set common attributes
		checkforCookie(request, response);
		request.setAttribute("storeIcon",
				LoadBalancedImageOperations.getWebImage("icon", ImageSizePreset.ICON.getSize()));
		request.setAttribute("CategoryList", LoadBalancedCRUDOperations
				.getEntities(Service.PERSISTENCE, "categories", Category.class, -1, -1));
		request.setAttribute("title", "TeaStore Semantic Search");
		request.setAttribute("login",
				LoadBalancedStoreOperations.isLoggedIn(getSessionBlob(request)));

		// Forward to JSP with results
		request.getRequestDispatcher("WEB-INF/pages/semantic_search.jsp").forward(request, response);
	}

	/**
	 * Calls the AI Gateway Track 1 API to perform semantic search.
	 *
	 * @param query The search query
	 * @return List of products matching the query
	 * @throws IOException if the API call fails
	 */
	private List<Product> callAIGateway(String query) throws IOException {
		List<Product> products = new ArrayList<>();

		// Create request JSON
		ObjectNode requestJson = objectMapper.createObjectNode();
		requestJson.put("query", query);
		requestJson.put("limit", DEFAULT_SEARCH_LIMIT);

		String requestBody = objectMapper.writeValueAsString(requestJson);

		// Make HTTP POST request
		URL url = new URL(aiGatewayURL);
		HttpURLConnection conn = (HttpURLConnection) url.openConnection();

		try {
			conn.setRequestMethod("POST");
			conn.setRequestProperty("Content-Type", "application/json");
			conn.setDoOutput(true);
			conn.setConnectTimeout(5000); // 5 seconds
			conn.setReadTimeout(10000); // 10 seconds

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
				products = parseAIGatewayResponse(responseBody.toString());

			} else {
				throw new IOException("AI Gateway returned HTTP " + responseCode);
			}

		} finally {
			conn.disconnect();
		}

		return products;
	}

	/**
	 * Parses the AI Gateway JSON response and converts to Product entities.
	 *
	 * @param jsonResponse JSON response from AI Gateway
	 * @return List of Product entities
	 * @throws IOException if JSON parsing fails
	 */
	private List<Product> parseAIGatewayResponse(String jsonResponse) throws IOException {
		List<Product> products = new ArrayList<>();

		JsonNode root = objectMapper.readTree(jsonResponse);
		JsonNode results = root.get("results");

		if (results != null && results.isArray()) {
			for (JsonNode resultNode : results) {
				// AI Gateway returns {product: {...}, score: ...}
				// Extract the product sub-object
				JsonNode productNode = resultNode.get("product");

				if (productNode != null) {
					Product product = new Product();

					// Map AI response fields to TeaStore Product entity
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

					products.add(product);

					// Log for compatibility verification
					System.out.println("Mapped Product: ID=" + product.getId()
						+ ", CategoryID=" + product.getCategoryId()
						+ ", Name=" + product.getName()
						+ ", Price=" + product.getListPriceInCents());
				}
			}
		}

		return products;
	}
}
