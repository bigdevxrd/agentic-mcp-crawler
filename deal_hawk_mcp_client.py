"""
🦅 DEAL HAWK - MCP CLIENT INTEGRATION
Connects Deal Hawk app to the deployed Agentic MCP Crawler for intelligent deal finding
"""

import asyncio
import aiohttp
import json
import os
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from datetime import datetime
import logging

@dataclass
class DealSearchResult:
    """Structured deal search result"""
    title: str
    price: Optional[str]
    original_price: Optional[str]
    discount: Optional[str]
    url: str
    description: str
    source: str
    confidence_score: float
    discovered_at: datetime

class DealHawkMCPClient:
    """
    Deal Hawk MCP Client - Connects to deployed Agentic MCP Crawler
    Enables intelligent deal finding with strategic crawling
    """
    
    def __init__(self, mcp_server_url: str):
        self.mcp_server_url = mcp_server_url.rstrip('/')
        self.session: Optional[aiohttp.ClientSession] = None
        self.logger = logging.getLogger(__name__)
        
    async def __aenter__(self):
        """Async context manager entry"""
        self.session = aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=60),
            headers={'User-Agent': 'DealHawk-MCP-Client/1.0'}
        )
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        if self.session:
            await self.session.close()
            
    async def health_check(self) -> bool:
        """Check if the MCP server is online"""
        try:
            async with self.session.get(f"{self.mcp_server_url}/health") as response:
                return response.status == 200
        except Exception as e:
            self.logger.error(f"Health check failed: {e}")
            return False
            
    async def find_deals_intelligent(
        self, 
        query: str, 
        target_sites: Optional[List[str]] = None,
        price_range: Optional[tuple] = None,
        categories: Optional[List[str]] = None
    ) -> List[DealSearchResult]:
        """
        Use agentic intelligence to find deals based on natural language query
        
        Args:
            query: Natural language description of what deals to find
            target_sites: Optional list of specific sites to search
            price_range: Optional (min_price, max_price) tuple
            categories: Optional categories to focus on
            
        Returns:
            List of structured deal results
        """
        
        # Build context for intelligent crawling
        context = {
            "intent": "deal_finding",
            "urgency": "medium",
            "focus": "pricing_and_discounts"
        }
        
        if price_range:
            context["price_range"] = {"min": price_range[0], "max": price_range[1]}
        if categories:
            context["categories"] = categories
            
        deals = []
        
        # If specific sites provided, crawl them intelligently
        if target_sites:
            for site in target_sites:
                site_deals = await self._crawl_site_for_deals(site, query, context)
                deals.extend(site_deals)
        else:
            # Use discovery mode to find deal sites
            deal_sites = await self._discover_deal_sites(query, context)
            
            # Crawl discovered sites
            for site_info in deal_sites[:5]:  # Limit to top 5 discoveries
                site_deals = await self._crawl_site_for_deals(
                    site_info.get('url'), query, context
                )
                deals.extend(site_deals)
                
        return sorted(deals, key=lambda x: x.confidence_score, reverse=True)
        
    async def _crawl_site_for_deals(
        self, 
        site_url: str, 
        query: str, 
        context: Dict
    ) -> List[DealSearchResult]:
        """Crawl a specific site for deals using agentic intelligence"""
        
        try:
            # Enhanced query for deal finding
            enhanced_query = f"""
            Find deals and discounts for: {query}
            
            Focus on:
            - Product names and descriptions
            - Current prices and original prices  
            - Discount percentages or savings amounts
            - Deal expiration dates
            - Product availability
            - Special offers or promotions
            
            Look for pricing patterns, sale indicators, and discount terminology.
            """
            
            payload = {
                "url": site_url,
                "user_query": enhanced_query,
                "context": context
            }
            
            async with self.session.post(
                f"{self.mcp_server_url}/agentic_crawl",
                json=payload
            ) as response:
                
                if response.status == 200:
                    result = await response.json()
                    return self._parse_deals_from_crawl_result(result, site_url)
                else:
                    self.logger.warning(f"Crawl failed for {site_url}: {response.status}")
                    return []
                    
        except Exception as e:
            self.logger.error(f"Error crawling {site_url}: {e}")
            return []
            
    async def _discover_deal_sites(self, query: str, context: Dict) -> List[Dict]:
        """Use discovery mode to find relevant deal sites"""
        
        try:
            # Determine domain based on query
            domain = self._extract_domain_from_query(query)
            
            interests = [
                "deals and discounts",
                "price comparison", 
                "sales and promotions",
                "coupon codes",
                "clearance items",
                query  # Include the original query
            ]
            
            payload = {
                "domain": domain,
                "interests": interests
            }
            
            async with self.session.post(
                f"{self.mcp_server_url}/discover_opportunities", 
                json=payload
            ) as response:
                
                if response.status == 200:
                    result = await response.json()
                    if result.get("success"):
                        return result.get("opportunities", [])
                        
        except Exception as e:
            self.logger.error(f"Discovery failed: {e}")
            
        return []
        
    def _extract_domain_from_query(self, query: str) -> str:
        """Extract domain/category from query for better discovery"""
        
        # Simple keyword matching - could be enhanced with NLP
        domain_keywords = {
            "electronics": ["phone", "laptop", "computer", "tv", "camera", "headphones"],
            "fashion": ["clothing", "shoes", "dress", "shirt", "jacket", "accessories"],
            "home": ["furniture", "decor", "kitchen", "appliances", "bedding"],
            "books": ["book", "novel", "ebook", "textbook", "magazine"],
            "sports": ["fitness", "sports", "gym", "outdoor", "exercise"],
            "beauty": ["makeup", "skincare", "cosmetics", "beauty", "perfume"],
            "toys": ["toy", "game", "kids", "children", "baby"],
            "food": ["food", "grocery", "snacks", "cooking", "restaurant"]
        }
        
        query_lower = query.lower()
        for domain, keywords in domain_keywords.items():
            if any(keyword in query_lower for keyword in keywords):
                return domain
                
        return "general"
        
    def _parse_deals_from_crawl_result(
        self, 
        crawl_result: Dict, 
        source_url: str
    ) -> List[DealSearchResult]:
        """Parse crawl results into structured deal objects"""
        
        deals = []
        
        if not crawl_result.get("success"):
            return deals
            
        results = crawl_result.get("results", {})
        primary_content = results.get("primary_content", {})
        opportunities = results.get("discovered_opportunities", [])
        
        # Parse primary content for deals
        content = primary_content.get("content", "")
        if content:
            parsed_deals = self._extract_deals_from_content(content, source_url)
            deals.extend(parsed_deals)
            
        # Parse discovered opportunities  
        for opp in opportunities:
            opp_deals = self._extract_deals_from_content(
                opp.get("content", ""), 
                opp.get("url", source_url)
            )
            deals.extend(opp_deals)
            
        return deals
        
    def _extract_deals_from_content(self, content: str, source_url: str) -> List[DealSearchResult]:
        """Extract deal information from text content"""
        
        deals = []
        
        # This is a simplified parser - in production you'd want more sophisticated
        # extraction using the structured data from the agentic crawler
        
        try:
            # Try to parse as JSON if it's structured
            if content.strip().startswith('{'):
                data = json.loads(content)
                if isinstance(data, dict):
                    deals.append(self._create_deal_from_structured_data(data, source_url))
                elif isinstance(data, list):
                    for item in data:
                        deals.append(self._create_deal_from_structured_data(item, source_url))
            else:
                # Parse unstructured text for deal patterns
                deal = self._create_deal_from_text(content, source_url)
                if deal:
                    deals.append(deal)
                    
        except json.JSONDecodeError:
            # Fallback to text parsing
            deal = self._create_deal_from_text(content, source_url)
            if deal:
                deals.append(deal)
                
        return deals
        
    def _create_deal_from_structured_data(self, data: Dict, source_url: str) -> DealSearchResult:
        """Create deal object from structured data"""
        
        return DealSearchResult(
            title=data.get("title", data.get("name", "Deal Found")),
            price=data.get("price", data.get("current_price")),
            original_price=data.get("original_price", data.get("was_price")),
            discount=data.get("discount", data.get("savings")),
            url=data.get("url", source_url),
            description=data.get("description", "")[:200],
            source=source_url,
            confidence_score=0.8,  # High confidence for structured data
            discovered_at=datetime.now()
        )
        
    def _create_deal_from_text(self, text: str, source_url: str) -> Optional[DealSearchResult]:
        """Create deal object from unstructured text"""
        
        # Simple regex patterns for price detection
        import re
        
        price_patterns = [
            r'\$(\d+\.?\d*)',
            r'(\d+\.?\d*)\s*dollars?',
            r'£(\d+\.?\d*)',
            r'€(\d+\.?\d*)'
        ]
        
        discount_patterns = [
            r'(\d+)%\s*off',
            r'save\s*\$(\d+\.?\d*)',
            r'(\d+\.?\d*)\s*off'
        ]
        
        prices = []
        for pattern in price_patterns:
            matches = re.findall(pattern, text.lower())
            prices.extend([float(match) for match in matches if match])
            
        discounts = []
        for pattern in discount_patterns:
            matches = re.findall(pattern, text.lower())
            discounts.extend(matches)
            
        if prices:
            return DealSearchResult(
                title="Deal Found",
                price=f"${min(prices):.2f}" if prices else None,
                original_price=f"${max(prices):.2f}" if len(prices) > 1 else None,
                discount=discounts[0] if discounts else None,
                url=source_url,
                description=text[:200],
                source=source_url,
                confidence_score=0.6,  # Medium confidence for text parsing
                discovered_at=datetime.now()
            )
            
        return None
        
    async def search_previous_deals(self, query: str, limit: int = 10) -> List[Dict]:
        """Search through previously found deals"""
        
        try:
            payload = {
                "query": f"deals {query}",
                "max_results": limit
            }
            
            async with self.session.post(
                f"{self.mcp_server_url}/intelligent_search",
                json=payload
            ) as response:
                
                if response.status == 200:
                    result = await response.json()
                    if result.get("success"):
                        return result.get("results", [])
                        
        except Exception as e:
            self.logger.error(f"Search failed: {e}")
            
        return []

# Deal Hawk Integration Helper Functions

async def find_deals_for_product(
    product_name: str,
    max_price: Optional[float] = None,
    categories: Optional[List[str]] = None,
    mcp_server_url: str = None
) -> List[DealSearchResult]:
    """
    Main function for Deal Hawk app to find deals for a specific product
    
    Args:
        product_name: Name or description of product to find deals for
        max_price: Maximum price filter
        categories: Product categories to focus on
        mcp_server_url: URL of deployed agentic MCP server
        
    Returns:
        List of deal results sorted by confidence score
    """
    
    # Default to environment variable or Railway URL
    if not mcp_server_url:
        mcp_server_url = os.getenv(
            'AGENTIC_CRAWLER_URL', 
            'https://agentic-mcp-crawler-production.up.railway.app'
        )
    
    async with DealHawkMCPClient(mcp_server_url) as client:
        # Check if server is online
        if not await client.health_check():
            raise ConnectionError("Agentic MCP server is not available")
            
        # Build price range if max_price provided
        price_range = (0, max_price) if max_price else None
        
        # Find deals using agentic intelligence
        deals = await client.find_deals_intelligent(
            query=product_name,
            price_range=price_range,
            categories=categories
        )
        
        return deals

async def discover_trending_deals(
    category: str = "general",
    mcp_server_url: str = None
) -> List[Dict]:
    """
    Discover trending deals in a category using agentic discovery
    
    Args:
        category: Category to discover deals in
        mcp_server_url: URL of deployed agentic MCP server
        
    Returns:
        List of discovered deal opportunities
    """
    
    if not mcp_server_url:
        mcp_server_url = os.getenv(
            'AGENTIC_CRAWLER_URL',
            'https://agentic-mcp-crawler-production.up.railway.app'
        )
    
    async with DealHawkMCPClient(mcp_server_url) as client:
        if not await client.health_check():
            raise ConnectionError("Agentic MCP server is not available")
            
        return await client._discover_deal_sites(
            f"trending deals {category}",
            {"intent": "discovery", "focus": "trending_deals"}
        )

# Example usage for Deal Hawk app integration
async def example_deal_hawk_usage():
    """Example of how to integrate into Deal Hawk app"""
    
    print("🦅 Deal Hawk - Agentic Deal Finding Demo")
    
    # Find deals for a specific product
    deals = await find_deals_for_product(
        product_name="gaming laptop under $1000",
        max_price=1000.0,
        categories=["electronics", "computers"]
    )
    
    print(f"\n✅ Found {len(deals)} deals:")
    for i, deal in enumerate(deals[:3], 1):
        print(f"\n{i}. {deal.title}")
        print(f"   💰 Price: {deal.price}")
        if deal.original_price:
            print(f"   🏷️  Original: {deal.original_price}")
        if deal.discount:
            print(f"   💸 Discount: {deal.discount}")
        print(f"   🔗 URL: {deal.url}")
        print(f"   📊 Confidence: {deal.confidence_score:.1%}")
        
    # Discover trending deals
    trending = await discover_trending_deals("electronics")
    print(f"\n🔥 Discovered {len(trending)} trending deal sources")
    
if __name__ == "__main__":
    asyncio.run(example_deal_hawk_usage())
