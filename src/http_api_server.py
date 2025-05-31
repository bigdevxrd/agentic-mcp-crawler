"""
HTTP API Server for Crawl4AI - Railway Ready
Provides REST endpoints for discord-crawler integration
"""
from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import os
import asyncio
from urllib.parse import urlparse, parse_qs
import sys
sys.path.append(os.path.dirname(__file__))

# Import existing crawler modules
try:
    from marketplace_config import MARKETPLACE_CONFIGS
    from agentic_crawler import create_agentic_crawler
    from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig
except ImportError:
    print("Warning: Some modules not found, running in basic mode")
    MARKETPLACE_CONFIGS = {}

class CrawlAPIHandler(BaseHTTPRequestHandler):
    crawler = None
    
    @classmethod
    async def init_crawler(cls):
        if not cls.crawler:
            browser_config = BrowserConfig(headless=True, verbose=False)
            cls.crawler = AsyncWebCrawler(config=browser_config)
            await cls.crawler.__aenter__()
    
    def do_GET(self):
        if self.path == '/health':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {
                'status': 'healthy',
                'service': 'crawl4ai-http-api',
                'version': '1.0',
                'crawler_ready': self.crawler is not None
            }
            self.wfile.write(json.dumps(response).encode())
            
    def do_POST(self):
        if self.path.startswith('/tools/crawl_single_page'):
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            try:
                params = json.loads(post_data)
                url = params.get('url', '')
                
                # Run async crawl
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                result = loop.run_until_complete(self._crawl_page(url, params))
                
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(result).encode())
                
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                error_response = {
                    'success': False,
                    'error': str(e)
                }
                self.wfile.write(json.dumps(error_response).encode())
                
    async def _crawl_page(self, url, params):
        """Crawl a page using Crawl4AI"""
        try:
            await self.init_crawler()
            
            config = CrawlerRunConfig(
                wait_for=params.get('wait_for', 'networkidle'),
                timeout=params.get('timeout', 30000),
                remove_overlay_elements=True
            )
            
            result = await self.crawler.crawl(url, config=config)
            
            if result.success:
                # Basic parsing - you can enhance this
                return {
                    'success': True,
                    'items': [],  # Add parsing logic here
                    'raw_content': result.cleaned_html[:1000] if params.get('include_raw') else None
                }
            else:
                return {
                    'success': False,
                    'error': result.error_message
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
            
def main():
    # Get port from environment or default
    port = int(os.getenv('PORT', 8080))
    host = os.getenv('HOST', '0.0.0.0')
    
    # Create server
    server = HTTPServer((host, port), CrawlAPIHandler)
    
    print(f"🚀 Crawl4AI HTTP API Server")
    print(f"🌐 Running on http://{host}:{port}")
    print(f"✅ Health check: http://{host}:{port}/health")
    print(f"📡 Ready for Railway deployment!")
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Server stopped")
        server.shutdown()

if __name__ == "__main__":
    main()
