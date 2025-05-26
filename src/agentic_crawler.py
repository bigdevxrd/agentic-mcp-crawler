"""
Agentic Web Crawler - Intelligent MCP Enhancement
Transforms basic crawling into strategic, learning-based web intelligence.
"""

import asyncio
import json
import time
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from urllib.parse import urlparse, urljoin
import re
from pathlib import Path

from anthropic import AsyncAnthropic
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig
from supabase import Client

@dataclass
class CrawlStrategy:
    """Represents an intelligent crawling strategy"""
    name: str
    description: str
    target_patterns: List[str]
    depth_limit: int
    follow_links: bool
    extract_patterns: List[str]
    success_metrics: Dict[str, Any]
    adaptation_rules: List[str]

@dataclass
class CrawlContext:
    """Context for intelligent crawling decisions"""
    user_intent: str
    domain_knowledge: Dict[str, Any]
    previous_attempts: List[Dict[str, Any]]
    success_patterns: List[str]
    failure_patterns: List[str]
    time_constraints: Optional[int] = None

class AgenticCrawler:
    """
    Intelligent, self-adapting web crawler that thinks strategically
    about how to find and extract the most relevant information.
    """
    
    def __init__(self, anthropic_client: AsyncAnthropic, supabase_client: Client):
        self.claude = anthropic_client
        self.supabase = supabase_client
        self.strategies = self._load_base_strategies()
        self.learned_patterns = self._load_learned_patterns()
        self.success_history = []
        
    def _load_base_strategies(self) -> Dict[str, CrawlStrategy]:
        """Load base crawling strategies"""
        return {
            "deep_research": CrawlStrategy(
                name="Deep Research",
                description="Thorough multi-page analysis for comprehensive understanding",
                target_patterns=["article", "blog", "research", "study", "analysis"],
                depth_limit=3,
                follow_links=True,
                extract_patterns=["main content", "citations", "references", "related links"],
                success_metrics={"content_depth": 0.8, "relevance_score": 0.7},
                adaptation_rules=["increase_depth_if_shallow", "follow_citations"]
            ),
            "quick_scan": CrawlStrategy(
                name="Quick Scanner",
                description="Fast overview crawl for key information extraction",
                target_patterns=["summary", "overview", "key points", "highlights"],
                depth_limit=1,
                follow_links=False,
                extract_patterns=["headings", "bullet points", "key metrics"],
                success_metrics={"speed": 0.9, "coverage": 0.6},
                adaptation_rules=["prioritize_structured_data"]
            ),
            "discovery_mode": CrawlStrategy(
                name="Discovery Explorer",
                description="Proactive discovery of related opportunities and content",
                target_patterns=["sitemap", "directory", "index", "catalog"],
                depth_limit=2,
                follow_links=True,
                extract_patterns=["navigation", "categories", "related topics"],
                success_metrics={"discovery_rate": 0.8, "novelty": 0.7},
                adaptation_rules=["expand_to_related_domains", "follow_category_links"]
            )
        }
    
    def _load_learned_patterns(self) -> Dict[str, Any]:
        """Load previously learned patterns from Supabase"""
        try:
            result = self.supabase.table('learned_patterns').select('*').execute()
            patterns = {}
            for row in result.data:
                patterns[row['pattern_type']] = row['pattern_data']
            return patterns
        except Exception as e:
            print(f"Could not load learned patterns: {e}")
            return {}
    
    async def analyze_intent(self, user_query: str, context: Optional[Dict] = None) -> CrawlContext:
        """
        Use Claude to understand user intent and create optimal crawl context
        """
        system_prompt = """
        You are an expert web crawling strategist. Analyze the user's query and determine:
        1. Primary intent (research, monitoring, discovery, extraction)
        2. Content type preferences (news, technical, academic, commercial)
        3. Depth requirements (surface-level vs deep analysis)
        4. Urgency level (real-time vs comprehensive)
        5. Success criteria for the crawl
        
        Return JSON with your analysis.
        """
        
        user_prompt = f"""
        User Query: "{user_query}"
        Additional Context: {json.dumps(context or {}, indent=2)}
        
        Previous successful patterns from our database:
        {json.dumps(self.learned_patterns, indent=2)}
        
        Provide strategic analysis for optimal crawling approach.
        """
        
        try:
            response = await self.claude.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=1000,
                system=system_prompt,
                messages=[{"role": "user", "content": user_prompt}]
            )
            
            analysis = json.loads(response.content[0].text)
            
            return CrawlContext(
                user_intent=analysis.get("primary_intent", "research"),
                domain_knowledge=analysis.get("domain_insights", {}),
                previous_attempts=[],  # Will be populated from history
                success_patterns=analysis.get("recommended_patterns", []),
                failure_patterns=analysis.get("avoid_patterns", [])
            )
            
        except Exception as e:
            print(f"Intent analysis failed: {e}")
            # Fallback to basic context
            return CrawlContext(
                user_intent="research",
                domain_knowledge={},
                previous_attempts=[],
                success_patterns=[],
                failure_patterns=[]
            )
    
    async def select_strategy(self, context: CrawlContext, target_url: str) -> CrawlStrategy:
        """
        Intelligently select the best crawling strategy based on context and URL analysis
        """
        # Analyze URL characteristics
        parsed_url = urlparse(target_url)
        domain_indicators = {
            "news_site": any(indicator in parsed_url.netloc for indicator in 
                           ["news", "cnn", "bbc", "reuters", "bloomberg"]),
            "academic": any(indicator in parsed_url.netloc for indicator in 
                          [".edu", "arxiv", "scholar", "research"]),
            "ecommerce": any(indicator in parsed_url.netloc for indicator in 
                           ["shop", "store", "amazon", "ebay"]),
            "social": any(indicator in parsed_url.netloc for indicator in 
                        ["twitter", "linkedin", "facebook", "reddit"])
        }
        
        # Use Claude to make strategic decision
        strategy_prompt = f"""
        Select the optimal crawling strategy based on:
        
        User Intent: {context.user_intent}
        Target URL: {target_url}
        Domain Type: {domain_indicators}
        Success Patterns: {context.success_patterns}
        
        Available Strategies:
        {json.dumps({name: asdict(strategy) for name, strategy in self.strategies.items()}, indent=2)}
        
        Return the strategy name and any recommended modifications.
        """
        
        try:
            response = await self.claude.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=500,
                messages=[{"role": "user", "content": strategy_prompt}]
            )
            
            decision = json.loads(response.content[0].text)
            strategy_name = decision.get("selected_strategy", "deep_research")
            modifications = decision.get("modifications", {})
            
            # Apply modifications to selected strategy
            selected_strategy = self.strategies[strategy_name]
            if modifications:
                selected_strategy = self._modify_strategy(selected_strategy, modifications)
                
            return selected_strategy
            
        except Exception as e:
            print(f"Strategy selection failed: {e}")
            return self.strategies["deep_research"]  # Safe fallback
    
    def _modify_strategy(self, strategy: CrawlStrategy, modifications: Dict) -> CrawlStrategy:
        """Apply real-time modifications to a strategy"""
        modified = CrawlStrategy(**asdict(strategy))
        
        if "depth_limit" in modifications:
            modified.depth_limit = modifications["depth_limit"]
        if "additional_patterns" in modifications:
            modified.extract_patterns.extend(modifications["additional_patterns"])
        if "follow_links" in modifications:
            modified.follow_links = modifications["follow_links"]
            
        return modified
    
    async def adaptive_crawl(self, url: str, user_query: str, context: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Execute an intelligent, adaptive crawl that learns and adjusts in real-time
        """
        start_time = time.time()
        
        # Phase 1: Analyze Intent
        crawl_context = await self.analyze_intent(user_query, context)
        
        # Phase 2: Select Strategy
        strategy = await self.select_strategy(crawl_context, url)
        
        # Phase 3: Execute with Monitoring
        results = await self._execute_with_monitoring(url, strategy, crawl_context)
        
        # Phase 4: Learn from Results
        await self._learn_from_crawl(url, user_query, strategy, results, start_time)
        
        return results
    
    async def _execute_with_monitoring(self, url: str, strategy: CrawlStrategy, 
                                     context: CrawlContext) -> Dict[str, Any]:
        """Execute crawl with real-time monitoring and adaptation"""
        
        crawler_config = BrowserConfig(
            headless=True,
            extra_args=["--no-sandbox", "--disable-dev-shm-usage"]
        )
        
        run_config = CrawlerRunConfig(
            word_count_threshold=10,
            extraction_strategy="LLMExtractionStrategy",
            extraction_schema={
                "name": "intelligent_extraction",
                "schema": {
                    "type": "object",
                    "properties": {
                        "main_content": {"type": "string"},
                        "key_insights": {"type": "array", "items": {"type": "string"}},
                        "relevance_score": {"type": "number"},
                        "discovered_links": {"type": "array", "items": {"type": "string"}},
                        "content_quality": {"type": "string"}
                    }
                }
            }
        )
        
        results = {
            "primary_content": {},
            "discovered_opportunities": [],
            "performance_metrics": {},
            "adaptation_log": []
        }
        
        async with AsyncWebCrawler(config=crawler_config) as crawler:
            # Primary crawl
            primary_result = await crawler.arun(url=url, config=run_config)
            
            if primary_result.success:
                results["primary_content"] = {
                    "url": url,
                    "content": primary_result.extracted_content,
                    "metadata": primary_result.metadata,
                    "timestamp": datetime.now().isoformat()
                }
                
                # Adaptive follow-up based on strategy
                if strategy.follow_links and strategy.depth_limit > 1:
                    follow_up_links = await self._identify_follow_up_links(
                        primary_result, context, strategy
                    )
                    
                    for link_url in follow_up_links[:3]:  # Limit for performance
                        try:
                            follow_result = await crawler.arun(url=link_url, config=run_config)
                            if follow_result.success:
                                results["discovered_opportunities"].append({
                                    "url": link_url,
                                    "content": follow_result.extracted_content,
                                    "relation_to_primary": "discovered_link"
                                })
                        except Exception as e:
                            results["adaptation_log"].append(f"Failed to crawl {link_url}: {e}")
            
        return results
    
    async def _identify_follow_up_links(self, primary_result, context: CrawlContext, 
                                      strategy: CrawlStrategy) -> List[str]:
        """Use Claude to identify the most promising follow-up links"""
        
        links_prompt = f"""
        Based on the primary crawl results and user context, identify the 3 most valuable
        follow-up links to crawl for additional insights.
        
        Primary Content Summary: {str(primary_result.extracted_content)[:1000]}...
        User Intent: {context.user_intent}
        Strategy Focus: {strategy.description}
        
        Available Links: {primary_result.links[:20] if hasattr(primary_result, 'links') else []}
        
        Return JSON array of the top 3 URLs with reasoning.
        """
        
        try:
            response = await self.claude.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=400,
                messages=[{"role": "user", "content": links_prompt}]
            )
            
            link_analysis = json.loads(response.content[0].text)
            return [item["url"] for item in link_analysis.get("recommended_links", [])]
            
        except Exception as e:
            print(f"Link analysis failed: {e}")
            return []
    
    async def _learn_from_crawl(self, url: str, user_query: str, strategy: CrawlStrategy,
                              results: Dict[str, Any], start_time: float) -> None:
        """Learn from crawl results to improve future performance"""
        
        crawl_duration = time.time() - start_time
        success_metrics = {
            "duration": crawl_duration,
            "content_extracted": len(str(results.get("primary_content", {}))),
            "opportunities_found": len(results.get("discovered_opportunities", [])),
            "strategy_used": strategy.name
        }
        
        # Store learning data
        learning_record = {
            "timestamp": datetime.now().isoformat(),
            "url_pattern": urlparse(url).netloc,
            "user_intent": user_query,
            "strategy_effectiveness": success_metrics,
            "adaptation_notes": results.get("adaptation_log", [])
        }
        
        # Update learned patterns
        try:
            self.supabase.table('crawl_learning').insert(learning_record).execute()
        except Exception as e:
            print(f"Could not store learning data: {e}")
        
        # Update success history for real-time adaptation
        self.success_history.append(learning_record)
        if len(self.success_history) > 100:  # Keep last 100 records
            self.success_history = self.success_history[-100:]
    
    async def proactive_discovery(self, domain: str, interests: List[str]) -> List[Dict[str, Any]]:
        """
        Proactively discover new opportunities in a domain based on learned patterns
        """
        discovery_prompt = f"""
        Based on the domain "{domain}" and user interests {interests}, 
        suggest 5 high-value URLs that would likely contain relevant information.
        
        Consider:
        - Common URL patterns for this domain type
        - Likely content structures
        - Related subtopics worth exploring
        
        Our successful patterns from previous crawls:
        {json.dumps(self.learned_patterns, indent=2)}
        
        Return JSON array of suggested URLs with reasoning.
        """
        
        try:
            response = await self.claude.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=800,
                messages=[{"role": "user", "content": discovery_prompt}]
            )
            
            suggestions = json.loads(response.content[0].text)
            return suggestions.get("suggested_urls", [])
            
        except Exception as e:
            print(f"Proactive discovery failed: {e}")
            return []

# Utility functions for integration with existing MCP server
async def create_agentic_crawler(anthropic_api_key: str, supabase_client: Client) -> AgenticCrawler:
    """Factory function to create agentic crawler instance"""
    anthropic_client = AsyncAnthropic(api_key=anthropic_api_key)
    return AgenticCrawler(anthropic_client, supabase_client)
