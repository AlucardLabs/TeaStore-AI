<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core"%><%@ taglib uri="http://java.sun.com/jsp/jstl/functions" prefix="fn"%><%@ taglib uri="http://java.sun.com/jsp/jstl/fmt" prefix="fmt"%>
<div class="col-sm-3 col-md-3 col-lg-2 sidebar">
	<!-- Semantic Search Button -->
	<div style="margin-bottom: 20px;">
		<a href="<c:url value="/semanticsearch" />" class="btn btn-primary btn-block">
			<span class="glyphicon glyphicon-search"></span> Semantic Search
		</a>
		<a href="<c:url value="/aichat" />" class="btn btn-success btn-block" style="margin-top: 10px;">
			<span class="glyphicon glyphicon-comment"></span> AI Chat Assistant
		</a>
	</div>

	<h3>Categories</h3>
	<ul class="nav-sidebar">
		<c:forEach items="${CategoryList}" var="category">
			<li class="category-item" role="presentation"><a
				href="<c:url value="/category?category=${category.id}&page=1" />"
				class="menulink" id="link_${category.name}">${category.name}<br>
					<span>${category.description}</span></a></li>
		</c:forEach>
	</ul>
</div>