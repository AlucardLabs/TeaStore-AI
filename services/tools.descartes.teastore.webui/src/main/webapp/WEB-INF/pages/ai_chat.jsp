<%@include file="head.jsp"%><%@include file="header.jsp"%><div class="container" id="main">
	<div class="row">
		<%@include file="categorylist.jsp"%>
		<div class="col-md-9 col-lg-10 col-sm-12">
			<h2 class="minipage-title">AI Chat Assistant</h2>
			<p class="text-muted">Ask questions or search for products using natural language</p>

			<!-- CHAT CONTAINER -->
			<div class="chat-container" id="chatContainer">
				<div class="chat-messages" id="chatMessages">
					<!-- Messages will be added here dynamically -->
				</div>
			</div>

			<!-- CHAT INPUT -->
			<div class="chat-input-group">
				<div class="input-group">
					<input type="text"
					       class="form-control"
					       id="chatInput"
					       placeholder="Type your message..."
					       autocomplete="off">
					<span class="input-group-btn">
						<button class="btn btn-primary" type="button" id="sendButton">
							<span class="glyphicon glyphicon-send"></span> Send
						</button>
					</span>
				</div>
			</div>

			<!-- ERROR ALERT (hidden by default) -->
			<div class="alert alert-danger" id="chatError" style="display: none; margin-top: 15px;">
				<strong>Error:</strong> <span id="chatErrorMessage"></span>
			</div>

		</div>
	</div>
</div>

<!-- Load chat.js -->
<script src="<c:url value="/chat.js"/>"></script>

<%@include file="footer.jsp"%>
