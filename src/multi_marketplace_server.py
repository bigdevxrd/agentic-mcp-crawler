#!/usr/bin/env python3
"""
Enhanced Multi-Marketplace MCP Server
Intelligently crawls multiple Australian marketplaces with adaptive strategies
"""

import asyncio
import json
import os
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse as urlparse
from marketplace_config import MARKETPLACE_CONFIGS
from intelligent_crawler import IntelligentCrawler

class MultiMarketplaceMCPServer(BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self.crawler = IntelligentCrawler()
        super().__init__(*args, **kwargs)
    
    def log_message(self, format, *args):
        return  # Suppress default logging
        
    def do_GET(self):
        if self.path == '/health':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            response = {
                'status': 'ok',
                'service': 'multi-marketplace-mcp',
                'supported_marketplaces': list(MARKETPLACE_CONFIGS.keys()),
                'capabilities': [
                    'intelligent_crawling',
                    'anti_bot_protection',
                    'marketplace_adaptation',
                    'structured_extraction'
                ]
            }
            self.wfile.write(json.dumps(response).encode())
            print(f"✅ Health check - {len(MARKETPLACE_CONFIGS)} marketplaces supported")
            
        elif self.path == '/marketplaces':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            marketplaces = {}
            for marketplace_id, config in MARKETPLACE_CONFIGS.items():
                marketplaces[marketplace_id] = {
                    'name': config['name'],
                    'base_url': config['base_url'],
                    'supported': True,
                    'features': config.get('features', [])
                }
            
            self.wfile.write(json.dumps(marketplaces).encode())
            
        else:
            self.send_response(404)
            self.end_headers()
    
    def do_POST(self):
        if self.path == '/crawl':
            try:
                content_length = int(self.headers.get('Content-Length', 0))
                if content_length > 0:
                    post_data = self.rfile.read(content_length)
                    request_data = json.loads(post_data.decode('utf-8'))
                else:
                    request_data = {}
                
                url = request_data.get('url', '')
                marketplace_id = self.detect_marketplace(url)
                
                print(f"🌐 Crawling {marketplace_id} - {url}")
                
                if marketplace_id in MARKETPLACE_CONFIGS:
                    result = self.crawler.intelligent_crawl(url, marketplace_id, request_data)
                    
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.end_headers()
                    self.wfile.write(json.dumps(result).encode())
                    
                    print(f"✅ Crawled {marketplace_id} - {len(result.get('extracted_data', {}).get('listings', []))} items")
                    
                else:
                    error_response = {
                        'success': False, 
                        'error': f'Marketplace not supported: {marketplace_id}',
                        'supported_marketplaces': list(MARKETPLACE_CONFIGS.keys())
                    }
                    self.send_response(400)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps(error_response).encode())
                    print(f"⚠️  Unsupported marketplace: {marketplace_id}")
                    
            except Exception as e:
                print(f"❌ Error: {e}")
                error_response = {'success': False, 'error': str(e)}
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(error_response).encode())
        else:
            self.send_response(404)
            self.end_headers()
    
    def detect_marketplace(self, url):
        """Intelligently detect marketplace from URL"""
        url_lower = url.lower()
        
        if 'depop.com' in url_lower:
            return 'depop_au'
        elif 'ebay.com.au' in url_lower:
            return 'ebay_au'
        elif 'gumtree.com.au' in url_lower:
            return 'gumtree_au'
        elif 'facebook.com/marketplace' in url_lower:
            return 'facebook_marketplace'
        else:
            return 'unknown'

def main():
    port = int(os.getenv('PORT', 8080))  # Use Railway's PORT
    host = os.getenv('HOST', '0.0.0.0')  # Bind to all interfaces for Railway
    server = HTTPServer((host, port), MultiMarketplaceMCPServer)
    
    print("🛒 MULTI-MARKETPLACE MCP SERVER")
    print("=" * 50)
    print(f"🌐 Running on http://{host}:{port}")
    print(f"🎯 Supporting {len(MARKETPLACE_CONFIGS)} Australian marketplaces:")
    for marketplace_id, config in MARKETPLACE_CONFIGS.items():
        print(f"   ✅ {config['name']} ({marketplace_id})")
    print("=" * 50)
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Server stopped")
        server.shutdown()

if __name__ == "__main__":
    main()
