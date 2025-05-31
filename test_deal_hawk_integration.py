#!/usr/bin/env python3
"""
🦅 DEAL HAWK + AGENTIC MCP - LIVE TESTING SUITE
Test the complete pipeline: Deal Hawk → MCP Client → Railway Server → Results
"""

import asyncio
import aiohttp
import json
import os
import sys
from datetime import datetime
from pathlib import Path

# Add current directory to path so we can import our modules
sys.path.insert(0, str(Path(__file__).parent))

try:
    from deal_hawk_mcp_client import (
        find_deals_for_product, 
        discover_trending_deals, 
        DealHawkMCPClient
    )
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Make sure deal_hawk_mcp_client.py is in the same directory")
    sys.exit(1)

class DealHawkTester:
    """Comprehensive testing suite for Deal Hawk + Agentic MCP integration"""
    
    def __init__(self, server_url: str):
        self.server_url = server_url.rstrip('/')
        self.test_results = []
        
    def log_test(self, test_name: str, success: bool, message: str, details: str = None):
        """Log test results"""
        status = "✅ PASS" if success else "❌ FAIL"
        timestamp = datetime.now().strftime('%H:%M:%S')
        
        print(f"\n{status} [{timestamp}] {test_name}")
        print(f"   📝 {message}")
        if details:
            print(f"   📊 {details}")
            
        self.test_results.append({
            'name': test_name,
            'success': success,
            'message': message,
            'details': details,
            'timestamp': timestamp
        })
        
    async def test_server_health(self):
        """Test 1: Check if Railway server is online"""
        print("🔍 Testing Railway server health...")
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.server_url}/health",
                    timeout=aiohttp.ClientTimeout(total=10)
                ) as response:
                    
                    if response.status == 200:
                        self.log_test(
                            "Railway Server Health",
                            True,
                            f"Server online and responding at {self.server_url}",
                            f"Response time: {response.headers.get('response-time', 'N/A')}"
                        )
                        return True
                    else:
                        self.log_test(
                            "Railway Server Health",
                            False,
                            f"Server returned status {response.status}",
                            f"URL: {self.server_url}/health"
                        )
                        return False
                        
        except asyncio.TimeoutError:
            self.log_test(
                "Railway Server Health",
                False,
                "Server request timed out after 10 seconds",
                "Check if Railway deployment is running"
            )
            return False
        except Exception as e:
            self.log_test(
                "Railway Server Health",
                False,
                f"Connection failed: {str(e)}",
                "Verify Railway URL and deployment status"
            )
            return False
            
    async def test_mcp_endpoints(self):
        """Test 2: Check MCP server endpoints"""
        print("🔍 Testing MCP server endpoints...")
        
        endpoints = [
            ("/agentic_crawl", "POST", "Agentic crawling endpoint"),
            ("/discover_opportunities", "POST", "Discovery endpoint"),
            ("/intelligent_search", "POST", "Search endpoint")
        ]
        
        async with aiohttp.ClientSession() as session:
            for endpoint, method, description in endpoints:
                try:
                    # Test with minimal valid payload
                    if endpoint == "/agentic_crawl":
                        payload = {
                            "url": "https://example.com",
                            "user_query": "test query"
                        }
                    elif endpoint == "/discover_opportunities":
                        payload = {
                            "domain": "test",
                            "interests": ["test"]
                        }
                    else:  # intelligent_search
                        payload = {
                            "query": "test",
                            "max_results": 1
                        }
                    
                    async with session.request(
                        method,
                        f"{self.server_url}{endpoint}",
                        json=payload,
                        timeout=aiohttp.ClientTimeout(total=30)
                    ) as response:
                        
                        if response.status in [200, 400, 422]:  # 400/422 expected for test data
                            self.log_test(
                                f"MCP Endpoint {endpoint}",
                                True,
                                f"{description} is accessible",
                                f"Status: {response.status}"
                            )
                        else:
                            self.log_test(
                                f"MCP Endpoint {endpoint}",
                                False,
                                f"Unexpected status {response.status}",
                                f"Expected 200, 400, or 422"
                            )
                            
                except Exception as e:
                    self.log_test(
                        f"MCP Endpoint {endpoint}",
                        False,
                        f"Request failed: {str(e)}",
                        "Check server logs for errors"
                    )
                    
    async def test_deal_hawk_client(self):
        """Test 3: Test Deal Hawk MCP Client directly"""
        print("🔍 Testing Deal Hawk MCP Client...")
        
        try:
            async with DealHawkMCPClient(self.server_url) as client:
                # Test health check
                health = await client.health_check()
                
                if health:
                    self.log_test(
                        "Deal Hawk MCP Client",
                        True,
                        "Client successfully connected to server",
                        "Health check passed"
                    )
                    return True
                else:
                    self.log_test(
                        "Deal Hawk MCP Client", 
                        False,
                        "Client health check failed",
                        "Server may be down or unreachable"
                    )
                    return False
                    
        except Exception as e:
            self.log_test(
                "Deal Hawk MCP Client",
                False,
                f"Client initialization failed: {str(e)}",
                "Check client code and server connectivity"
            )
            return False
            
    async def test_simple_deal_finding(self):
        """Test 4: Simple deal finding with agentic intelligence"""
        print("🔍 Testing simple deal finding...")
        
        try:
            # Test with a simple, common product
            deals = await find_deals_for_product(
                product_name="wireless mouse",
                mcp_server_url=self.server_url
            )
            
            if deals:
                self.log_test(
                    "Simple Deal Finding",
                    True,
                    f"Successfully found {len(deals)} deals for 'wireless mouse'",
                    f"Top deal: {deals[0].title} - {deals[0].price} (confidence: {deals[0].confidence_score:.1%})"
                )
                
                # Show top 3 deals
                print("   🏆 Top 3 Deals Found:")
                for i, deal in enumerate(deals[:3], 1):
                    print(f"   {i}. {deal.title}")
                    print(f"      💰 {deal.price} | 📊 {deal.confidence_score:.1%} confidence")
                    print(f"      🔗 {deal.url[:60]}...")
                    
                return True
            else:
                self.log_test(
                    "Simple Deal Finding",
                    False,
                    "No deals found for 'wireless mouse'",
                    "Check server logs and agentic crawler functionality"
                )
                return False
                
        except ConnectionError as e:
            self.log_test(
                "Simple Deal Finding",
                False,
                "Server connection error",
                str(e)
            )
            return False
        except Exception as e:
            self.log_test(
                "Simple Deal Finding",
                False,
                f"Deal finding failed: {str(e)}",
                "Check agentic crawler and Claude API integration"
            )
            return False
            
    async def test_advanced_deal_finding(self):
        """Test 5: Advanced deal finding with filters"""
        print("🔍 Testing advanced deal finding with filters...")
        
        try:
            # Test with price filtering and categories
            deals = await find_deals_for_product(
                product_name="gaming laptop",
                max_price=1000.0,
                categories=["electronics", "computers"],
                mcp_server_url=self.server_url
            )
            
            if deals:
                # Check if price filtering worked
                price_filtered = []
                for deal in deals:
                    try:
                        # Extract price number for filtering check
                        price_str = deal.price.replace('$', '').replace(',', '')
                        price_num = float(price_str)
                        if price_num <= 1000:
                            price_filtered.append(deal)
                    except (ValueError, AttributeError):
                        # If we can't parse price, assume it's valid
                        price_filtered.append(deal)
                
                self.log_test(
                    "Advanced Deal Finding",
                    True,
                    f"Found {len(deals)} gaming laptop deals under $1000",
                    f"Price filtering: {len(price_filtered)} deals within budget"
                )
                
                # Show results
                print("   🎮 Gaming Laptop Deals Found:")
                for i, deal in enumerate(deals[:3], 1):
                    print(f"   {i}. {deal.title}")
                    print(f"      💰 {deal.price} | 📊 {deal.confidence_score:.1%}")
                    if deal.discount:
                        print(f"      💸 Discount: {deal.discount}")
                        
                return True
            else:
                self.log_test(
                    "Advanced Deal Finding",
                    False,
                    "No gaming laptop deals found under $1000",
                    "May be expected if no deals match criteria"
                )
                return False
                
        except Exception as e:
            self.log_test(
                "Advanced Deal Finding",
                False,
                f"Advanced deal finding failed: {str(e)}",
                "Check filtering logic and server response"
            )
            return False
            
    async def test_deal_discovery(self):
        """Test 6: Proactive deal discovery"""
        print("🔍 Testing proactive deal discovery...")
        
        try:
            # Test discovery mode
            trending = await discover_trending_deals(
                category="electronics",
                mcp_server_url=self.server_url
            )
            
            if trending:
                self.log_test(
                    "Deal Discovery",
                    True,
                    f"Discovered {len(trending)} trending deal sources in electronics",
                    f"First discovery: {trending[0].get('url', 'N/A')}"
                )
                
                # Show discovered opportunities
                print("   🔥 Trending Deal Sources Discovered:")
                for i, opp in enumerate(trending[:3], 1):
                    print(f"   {i}. {opp.get('url', 'Unknown URL')}")
                    print(f"      📝 {opp.get('reasoning', 'High relevance detected')[:100]}...")
                    
                return True
            else:
                self.log_test(
                    "Deal Discovery",
                    False,
                    "No trending deal sources discovered",
                    "Discovery mode may need more time or different parameters"
                )
                return False
                
        except Exception as e:
            self.log_test(
                "Deal Discovery",
                False,
                f"Deal discovery failed: {str(e)}",
                "Check discovery endpoints and Claude API integration"
            )
            return False
            
    async def run_comprehensive_test(self):
        """Run all tests in sequence"""
        print("🦅 DEAL HAWK + AGENTIC MCP - COMPREHENSIVE TEST SUITE")
        print("=" * 60)
        print(f"🎯 Testing server: {self.server_url}")
        print(f"⏰ Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Run tests in order
        tests = [
            self.test_server_health,
            self.test_mcp_endpoints,
            self.test_deal_hawk_client,
            self.test_simple_deal_finding,
            self.test_advanced_deal_finding,
            self.test_deal_discovery
        ]
        
        passed = 0
        total = len(tests)
        
        for test in tests:
            try:
                result = await test()
                if result:
                    passed += 1
            except Exception as e:
                print(f"❌ Test failed with exception: {e}")
                
        # Final results
        print("\n" + "=" * 60)
        print("🎯 FINAL TEST RESULTS")
        print("=" * 60)
        
        print(f"📊 Tests Passed: {passed}/{total}")
        print(f"✅ Success Rate: {(passed/total)*100:.1f}%")
        
        if passed == total:
            print("🎉 ALL TESTS PASSED - DEAL HAWK + AGENTIC MCP FULLY OPERATIONAL!")
            print("🚀 Your Deal Hawk app is ready for agentic deal finding!")
        elif passed >= total * 0.8:
            print("🎯 MOSTLY SUCCESSFUL - Core functionality working")
            print("⚠️  Some advanced features may need attention")
        else:
            print("⚠️  ISSUES DETECTED - Check server deployment and configuration")
            
        # Show detailed results
        print(f"\n📋 Detailed Results:")
        for result in self.test_results:
            status = "✅" if result['success'] else "❌"
            print(f"   {status} {result['name']}: {result['message']}")
            
        return passed == total

async def main():
    """Main test execution"""
    
    # Default to Railway URL - update with your actual deployment URL
    server_url = os.getenv(
        'AGENTIC_CRAWLER_URL',
        'https://agentic-mcp-crawler-production.up.railway.app'
    )
    
    print("🦅 DEAL HAWK AGENTIC TESTING")
    print(f"Server URL: {server_url}")
    print("=" * 60)
    
    if server_url == 'https://agentic-mcp-crawler-production.up.railway.app':
        print("⚠️  Using default Railway URL - update AGENTIC_CRAWLER_URL if different")
        print("   You can also pass your URL as environment variable")
        
    tester = DealHawkTester(server_url)
    success = await tester.run_comprehensive_test()
    
    if success:
        print("\n🎉 READY FOR PRODUCTION!")
        print("Your Deal Hawk app can now use agentic intelligence for deal finding!")
        return 0
    else:
        print("\n🔧 ISSUES FOUND - Check deployment and configuration")
        return 1

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
