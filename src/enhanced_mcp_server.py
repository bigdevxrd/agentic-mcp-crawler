"""
Enhanced Agentic MCP Server - Intelligent Web Crawling with Strategic Thinking
Integrates Claude-powered decision making with your existing crawl infrastructure.
"""

from mcp.server.fastmcp import FastMCP, Context
from contextlib import asynccontextmanager
from collections.abc import AsyncIterator
from dataclasses import dataclass
from typing import List, Dict, Any, Optional
from urllib.parse import urlparse, urldefrag
from dotenv import load_dotenv
from supabase import Client
from pathlib import Path
import os
import json
import asyncio

from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig
from agentic_crawler import AgenticCrawler, create_agentic_crawler
from utils import get_supabase_client, add_documents_to_supabase, search_documents

# Load environment variables
project_root = Path(__file__).resolve().parent.parent
dotenv_path = project_root / '.env'
load_dotenv(dotenv_path, override=True)

@dataclass
class EnhancedCrawlContext:
    """Enhanced context with agentic capabilities"""
    crawler: AsyncWebCrawler
    supabase_client: Client
    agentic_crawler: AgenticCrawler

@asynccontextmanager
async def enhanced_crawl_lifespan(server: FastMCP) -> AsyncIterator[EnhancedCrawlContext]:
    """Manages enhanced crawler lifecycle with agentic capabilities"""
    
    # Initialize standard crawler
    browser_config = BrowserConfig(headless=True, verbose=False)
    crawler = AsyncWebCrawler(config=browser_config)
    await crawler.__aenter__()
    
    # Initialize Supabase
    supabase_client = get_supabase_client()
    
    # Initialize agentic crawler
    anthropic_api_key = os.getenv('ANTHROPIC_API_KEY')
    if not anthropic_api_key or anthropic_api_key == 'YOUR_ANTHROPIC_API_KEY_HERE':
        raise ValueError("ANTHROPIC_API_KEY required for agentic features")
    
    agentic_crawler = await create_agentic_crawler(anthropic_api_key, supabase_client)
    # Only print status when not in stdio mode to avoid breaking JSON protocol
    if os.getenv('TRANSPORT', '').lower() != 'stdio':
        print("✅ Agentic intelligence enabled")
    
    try:
        yield EnhancedCrawlContext(
            crawler=crawler,
            supabase_client=supabase_client,
            agentic_crawler=agentic_crawler
        )
    finally:
        await crawler.__aexit__(None, None, None)

# Create the enhanced MCP server
mcp = FastMCP("Enhanced-Crawl4AI-MCP", lifespan=enhanced_crawl_lifespan)

@mcp.tool()
async def agentic_crawl(
    ctx: Context,
    url: str,
    user_query: str,
    context: Optional[str] = None
) -> Dict[str, Any]:
    """
    🧠 Intelligent crawling that thinks strategically about how to find what you need.
    
    Args:
        url: Target URL to crawl
        user_query: Describe what you're looking for (e.g., "Find pricing information", "Research competitor strategies")
        context: Additional context to guide the crawling strategy
    
    Returns:
        Comprehensive results with strategic insights and discovered opportunities
    """
    try:
        context_dict = json.loads(context) if context else {}
        
        # Access the lifespan context properly
        crawler_context = ctx.extra
        results = await crawler_context.agentic_crawler.adaptive_crawl(
            url=url,
            user_query=user_query,
            context=context_dict
        )
        
        # Store results in Supabase for learning
        if results.get("primary_content"):
            content_data = results["primary_content"]
            documents = [{
                "content": str(content_data.get("content", "")),
                "metadata": {
                    "url": url,
                    "user_query": user_query,
                    "crawl_type": "agentic",
                    "timestamp": content_data.get("timestamp"),
                    "strategy_used": results.get("strategy_used"),
                    **content_data.get("metadata", {})
                },
                "source": f"agentic_crawl_{url}"
            }]
            
            await add_documents_to_supabase(ctx.extra.supabase_client, documents)
        
        return {
            "success": True,
            "results": results,
            "insights": {
                "strategy_effectiveness": results.get("performance_metrics", {}),
                "opportunities_discovered": len(results.get("discovered_opportunities", [])),
                "learning_applied": "Strategies adapted based on previous crawls"
            }
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "fallback_suggestion": "Try using standard_crawl for basic extraction"
        }

@mcp.tool()
async def discover_opportunities(
    ctx: Context,
    domain: str,
    interests: List[str]
) -> Dict[str, Any]:
    """
    🔍 Proactively discover new high-value URLs and content opportunities.
    
    Args:
        domain: Domain or topic area to explore
        interests: List of specific interests or focus areas
    
    Returns:
        Curated list of discovery opportunities with reasoning
    """
    try:
        opportunities = await ctx.extra.agentic_crawler.proactive_discovery(
            domain=domain,
            interests=interests
        )
        
        return {
            "success": True,
            "opportunities": opportunities,
            "recommendation": "Use agentic_crawl on the most promising URLs",
            "next_steps": [
                "Review suggested URLs for relevance",
                "Use agentic_crawl with specific queries for each URL",
                "Let the system learn from successful crawls"
            ]
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

@mcp.tool()
async def intelligent_search(
    ctx: Context,
    query: str,
    max_results: int = 10
) -> Dict[str, Any]:
    """
    🎯 Search previously crawled content with intelligent ranking and insights.
    
    Args:
        query: Search query for finding relevant content
        max_results: Maximum number of results to return
    
    Returns:
        Ranked results with relevance insights and suggested follow-up actions
    """
    try:
        # Search existing content
        search_results = await search_documents(
            ctx.extra.supabase_client,
            query=query,
            limit=max_results
        )
        
        if not search_results:
            return {
                "success": True,
                "results": [],
                "suggestion": "No results found. Consider using discover_opportunities to find relevant content to crawl."
            }
        
        # Enhance results with intelligent insights
        enhanced_results = []
        for result in search_results:
            enhanced_result = {
                **result,
                "intelligent_summary": f"Relevant content from {result.get('metadata', {}).get('url', 'unknown source')}",
                "suggested_actions": [
                    "Review full content for deeper insights",
                    "Use agentic_crawl to find related content",
                    "Explore discovered opportunities"
                ]
            }
            enhanced_results.append(enhanced_result)
        
        return {
            "success": True,
            "results": enhanced_results,
            "insights": {
                "total_found": len(search_results),
                "search_effectiveness": "High" if len(search_results) > 5 else "Medium",
                "recommendation": "Consider broader discovery if results are limited"
            }
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

@mcp.tool()
async def standard_crawl(
    ctx: Context,
    url: str,
    extract_format: str = "markdown"
) -> Dict[str, Any]:
    """
    📄 Standard web crawling for basic content extraction (fallback method).
    
    Args:
        url: URL to crawl
        extract_format: Format for extracted content (markdown, text, structured)
    
    Returns:
        Basic crawl results without agentic intelligence
    """
    try:
        # Configure basic crawl
        config = CrawlerRunConfig(
            word_count_threshold=10,
            extraction_strategy="CosineStrategy" if extract_format == "structured" else "NoExtractionStrategy",
            chunking_strategy="RegexChunking"
        )
        
        # Execute crawl
        result = await ctx.extra.crawler.arun(url=url, config=config)
        
        if result.success:
            # Store in Supabase
            documents = [{
                "content": result.markdown if extract_format == "markdown" else result.cleaned_html,
                "metadata": {
                    "url": url,
                    "crawl_type": "standard",
                    "extract_format": extract_format,
                    **result.metadata
                },
                "source": f"standard_crawl_{url}"
            }]
            
            await add_documents_to_supabase(ctx.extra.supabase_client, documents)
            
            return {
                "success": True,
                "content": result.markdown if extract_format == "markdown" else result.cleaned_html,
                "metadata": result.metadata,
                "recommendation": "Consider using agentic_crawl for more intelligent extraction"
            }
        else:
            return {
                "success": False,
                "error": result.error_message,
                "suggestion": "Try agentic_crawl which may handle difficult sites better"
            }
            
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

if __name__ == "__main__":
    import uvicorn
    
    # Run the enhanced MCP server
    mcp.run()
