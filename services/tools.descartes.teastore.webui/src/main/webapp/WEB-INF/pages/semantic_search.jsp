<%@include file="head.jsp"%><%@include file="header.jsp"%><div class="container" id="main">
	<div class="row">
		<%@include file="categorylist.jsp"%>
		<div class="col-md-9 col-lg-10 col-sm-12">
			<h2 class="minipage-title">Semantic Search</h2>
			<p class="text-muted">Search for products using natural language and semantic understanding</p>

			<!-- SEARCH FORM -->
			<div class="row" style="margin-bottom: 20px;">
				<div class="col-sm-12">
					<form method="post" action="semanticsearch">
						<div class="form-group">
							<label for="query">Search Query:</label>
							<input type="text"
							       class="form-control"
							       id="query"
							       name="query"
							       value="${query}"
							       placeholder="e.g., organic green tea, relaxing herbal blend, morning energy tea"
							       required
							       autofocus>
							<small class="form-text text-muted">
								Try: "green tea", "relaxing tea", "morning boost", "herbal blend"
							</small>
						</div>
						<button type="submit" class="btn btn-primary">
							<span class="glyphicon glyphicon-search"></span> Semantic Search
						</button>

						<!-- CLEAR button (only shown if we have a query) -->
						<c:if test="${not empty query}">
							<a href="semanticsearch" class="btn btn-default">
								<span class="glyphicon glyphicon-remove"></span> Clear
							</a>
						</c:if>
					</form>
				</div>
			</div>

			<hr/>

			<!-- ERROR MESSAGE -->
			<c:if test="${not empty error}">
				<div class="alert alert-danger alert-dismissible" role="alert">
					<button type="button" class="close" data-dismiss="alert" aria-label="Close">
						<span aria-hidden="true">&times;</span>
					</button>
					<strong>Error:</strong> ${error}
				</div>
			</c:if>

			<!-- SEARCH RESULTS -->
			<c:if test="${not empty searchResults}">
				<h4>Found ${fn:length(searchResults)} products for "${query}":</h4>
				<div class="row">
					<c:forEach items="${searchResults}" var="product" varStatus="loop">
						<div class="col-sm-6 col-md-4 col-lg-3 placeholder">
							<%@include file="product_item.jsp"%>
						</div>
					</c:forEach>
				</div>
			</c:if>

			<!-- NO RESULTS MESSAGE -->
			<c:if test="${empty searchResults and not empty query and empty error}">
				<div class="alert alert-info" role="alert">
					<strong>No results found</strong> for "${query}".
					<br>Try different keywords or check if the AI service is running.
				</div>
			</c:if>

			<!-- INITIAL INSTRUCTIONS (when no search performed) -->
			<c:if test="${empty query}">
				<div class="panel panel-info">
					<div class="panel-heading">
						<h3 class="panel-title">How to use Semantic Search</h3>
					</div>
					<div class="panel-body">
						<p>Semantic search uses AI to understand the <strong>meaning</strong> of your query, not just exact keyword matches.</p>
						<p><strong>Example queries:</strong></p>
						<ul>
							<li>"organic green tea" - finds organic varieties</li>
							<li>"relaxing herbal blend" - discovers calming teas like chamomile</li>
							<li>"morning energy boost" - suggests caffeinated options</li>
							<li>"tea for digestion" - finds digestive-friendly blends</li>
						</ul>
						<p class="text-muted">
							<em>Note: This feature is powered by AI Gateway Track 1 (vector embeddings).
							Results are from mock data for demonstration purposes.</em>
						</p>
					</div>
				</div>
			</c:if>

		</div>
	</div>
</div>
<%@include file="footer.jsp"%>
