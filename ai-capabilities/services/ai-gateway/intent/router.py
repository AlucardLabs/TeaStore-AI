"""Intent Router - LLM-based request analysis for Track 2 Intelligent API."""

import os
from typing import Dict, Optional
from langchain_community.chat_models import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
import structlog

logger = structlog.get_logger(__name__)

# Get Ollama URL from environment
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://ollama:11434")


class IntentRouter:
    """LLM-based intent analyzer and request router."""

    def __init__(self, model_name: str = "llama3.2"):
        """Initialize the intent router.

        Args:
            model_name: Ollama model to use (default: llama3.2)
        """
        self.model_name = model_name
        self.llm = ChatOllama(
            model=model_name,
            base_url=OLLAMA_URL,
            temperature=0.1  # Low temperature for consistent intent detection
        )

        # Intent detection prompt
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an intent analyzer for a tea store AI system.
Analyze the user request and extract:
1. Intent: one of [SEARCH, QUESTION, RECOMMENDATION, COMPARISON, CHAT]
2. Parameters: filters, constraints, preferences extracted from the request
3. Workflow: which workflow to execute

Intent types:
- SEARCH: User wants to find/search for products (e.g., "find green tea", "show me teas under $20")
- QUESTION: User asks about brewing, health benefits, tea types (e.g., "how to brew oolong?")
- RECOMMENDATION: User wants product suggestions (e.g., "recommend something like Earl Grey")
- COMPARISON: User wants to compare products (e.g., "difference between sencha and matcha")
- CHAT: General conversation or unclear intent

For SEARCH intent, extract:
- query: search query string
- filters: category, min_price_cents, max_price_cents, origin
- limit: number of results (default 10)

Return ONLY valid JSON, no other text."""),
            ("user", "{request}")
        ])

        # Output parser for JSON
        self.json_parser = JsonOutputParser()

    async def analyze_request(self, user_request: str) -> Dict:
        """Analyze user request and detect intent.

        Args:
            user_request: Natural language user request

        Returns:
            Dictionary with intent, parameters, and workflow
        """
        try:
            logger.info("Analyzing intent", request=user_request)

            # Create chain
            chain = self.prompt | self.llm | self.json_parser

            # Execute analysis
            result = await chain.ainvoke({"request": user_request})

            logger.info(
                "Intent analyzed",
                intent=result.get("intent"),
                workflow=result.get("workflow")
            )

            return result

        except Exception as e:
            logger.error("Intent analysis failed", error=str(e))
            # Fallback to basic SEARCH intent
            return {
                "intent": "SEARCH",
                "parameters": {
                    "query": user_request,
                    "limit": 10
                },
                "workflow": "search_workflow",
                "error": str(e)
            }

    def get_workflow_endpoint(self, intent: str) -> str:
        """Map intent to orchestrator workflow endpoint.

        Args:
            intent: Detected intent

        Returns:
            Workflow endpoint path
        """
        intent_mapping = {
            "SEARCH": "/workflows/search",
            "QUESTION": "/workflows/search",  # For now, use search for questions
            "RECOMMENDATION": "/workflows/search",  # Use search with similarity
            "COMPARISON": "/workflows/search",  # Use search for comparison
            "CHAT": "/workflows/search"  # Fallback to search
        }

        return intent_mapping.get(intent, "/workflows/search")


# Example usage and expected outputs:

# Input: "Show me organic green teas under $20 from Japan"
# Output: {
#   "intent": "SEARCH",
#   "parameters": {
#     "query": "organic green tea",
#     "filters": {
#       "category": "Green Tea",
#       "max_price_cents": 2000,
#       "origin": "Japan"
#     },
#     "limit": 10
#   },
#   "workflow": "search_workflow"
# }

# Input: "How do I brew oolong tea?"
# Output: {
#   "intent": "QUESTION",
#   "topic": "brewing",
#   "tea_type": "oolong",
#   "workflow": "product_qa_workflow"
# }

# Input: "Find teas similar to Earl Grey"
# Output: {
#   "intent": "RECOMMENDATION",
#   "reference_product": "Earl Grey",
#   "workflow": "similarity_workflow"
# }
