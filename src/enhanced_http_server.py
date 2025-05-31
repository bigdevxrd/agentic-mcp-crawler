#!/usr/bin/env python3
"""
Enhanced HTTP API Server for Railway - Agentic Capabilities
"""

import asyncio
import json
import os
from http.server import HTTPServer, BaseHTTPRequestHandler
import sys
sys.path.append(os.path.dirname(__file__))

from agentic_crawler import create_agentic_crawler
from utils import get_supabase_client, add_documents_to_supabase
from crawl4ai import AsyncWebCrawler, BrowserConfig


class AgenticAPIHandler(BaseHTTPRequestHandler):
    crawler = None
    agentic_crawler = None
    supabase_client = None
    
    @classmethod
    async def init_services(cls):
        """Initialize all services"""
        if not cls.crawler:
            browser_config = BrowserConfig(headless=True, verbose=False)
            cls.crawler = AsyncWebCrawler(config=browser_config)
            await cls.crawler.__aenter__()
            
        if not cls.supabase_client:
            cls.supabase_client = get_supabase_client()
            
        if not cls.agentic_crawler:
            anthropic_key = os.getenv('ANTHROPIC_API_KEY')
            if anthropic_key and anthropic_key != 'YOUR_ANTHROPIC_API_KEY_HERE':
                cls.agentic_crawler = await create_agentic_crawler(anthropic_key, cls.supabase_client)
                print("✅ Agentic intelligence enabled")
    
    def do_GET(self):
        if self.path == '/health':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            response = {
                'status': 'healthy',
                'service': 'agentic-crawl4ai-api',
                'version': '2.0',
                'capabilities': [
                    'agentic_crawl',
                    'intelligent_search', 
                    'discover_opportunities',
                    'standard_crawl'
                ],
                'agentic_enabled': self.agentic_crawler is not None
            }
            self.wfile.write(json.dumps(response).encode())
        else:
            self.send_response(404)
            self.end_headers()
    
    def do_POST(self):
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            params = json.loads(post_data)
            
            # Handle different endpoints
            if self.path == '/tools/agentic_crawl':
                result = asyncio.run(self._agentic_crawl(params))
            elif self.path == '/tools/crawl':
                result = asyncio.run(self._basic_crawl(params))
            else:
                self.send_response(404)
                self.end_headers()
                return
                
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(result).encode())
            
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            error_response = {'success': False, 'error': str(e)}
            self.wfile.write(json.dumps(error_response).encode())
    
    async def _agentic_crawl(self, params):
        """Perform agentic crawling"""
        await self.init_services()
        
        if not self.agentic_crawler:
            return {
                'success': False,
                'error': 'Agentic capabilities not available (missing ANTHROPIC_API_KEY)'
            }
        
        url = params.get('url', '')
        user_query = params.get('user_query', 'Analyze this page')
        context = params.get('context', {})
        
        try:
            results = await self.agentic_crawler.adaptive_crawl(
                url=url,
                user_query=user_query,
                context=context
            )
            
            # Store in Supabase
            if results.get("primary_content"):
                content_data = results["primary_content"]
                documents = [{
                    "content": str(content_data.get("content", "")),
                    "metadata": {
                        "url": url,
                        "user_query": user_query,
                        "crawl_type": "agentic",
                        **content_data.get("metadata", {})
                    },
                    "source": f"agentic_crawl_{url}"
                }]
                await add_documents_to_supabase(self.supabase_client, documents)
            
            # Format for client type
            client_type = params.get('client_type', 'api')
            if client_type == 'discord':
                return self._format_discord_response(results, url)
            else:
                return {
                    'success': True,
                    'url': url,
                    'results': results
                }
                
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    async def _basic_crawl(self, params):
        """Basic crawling for backward compatibility"""
        await self.init_services()
        
        url = params.get('url', '')
        try:
            result = await self.crawler.arun(url=url)
            if result.success:
                return {
                    'success': True,
                    'items': [],  # For marketplace compatibility
                    'content': result.markdown[:1000]
                }
            else:
                return {'success': False, 'error': result.error_message}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def _format_discord_response(self, results, url):
        """Format response for Discord"""
        primary = results.get("primary_content", {})
        return {
            "embed": {
                "title": f"🎯 {primary.get('title', 'Analysis Complete')}",
                "description": primary.get('summary', 'Successfully analyzed')[:400],
                "url": url,
                "color": 0x00ff00
            },
            "opportunities": results.get("opportunities", [])[:3]
        }


def main():
    port = int(os.getenv('PORT', 8051))
    host = os.getenv('HOST', '0.0.0.0')
    
    server = HTTPServer((host, port), AgenticAPIHandler)
    
    print(f"🚀 Enhanced Agentic HTTP API Server")
    print(f"🌐 Running on http://{host}:{port}")
    print(f"✅ Health: http://{host}:{port}/health")
    print(f"🧠 Agentic: /tools/agentic_crawl")
    print(f"📡 Railway ready!")
    
    server.serve_forever()


if __name__ == "__main__":
    main()
