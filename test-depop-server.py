#!/usr/bin/env python3

"""
Quick MCP Server Test - Minimal server to test Depop Australia search
"""

import asyncio
import json
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading
import os
import sys
from urllib.parse import urlencode
import requests
from bs4 import BeautifulSoup

class DepopTestServer(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/health':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'status': 'ok', 'service': 'depop-test-mcp'}).encode())
        else:
            self.send_response(404)
            self.end_headers()
    
    def do_POST(self):
        if self.path == '/crawl':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            try:
                request_data = json.loads(post_data.decode('utf-8'))
                url = request_data.get('url')
                
                print(f"🌐 Testing crawl request for: {url}")
                
                # Simulate Depop Australia search results
                if 'depop.com' in url and 'countryId=29' in url:
                    # Extract search terms from URL
                    import urllib.parse as urlparse
                    query_params = urlparse.parse_qs(urlparse.urlparse(url).query)
                    search_term = query_params.get('q', [''])[0]
                    
                    # Mock Depop Australia results
                    mock_results = {
                        'success': True,
                        'extracted_data': {
                            'listings': [
                                {
                                    'title': f'Vintage Band T-Shirt - {search_term}',
                                    'price': '$45.00 AUD',
                                    'url': '/products/vintage-band-tshirt-123',
                                    'image': 'https://depop.com/image1.jpg'
                                },
                                {
                                    'title': f'Retro Concert Tee - {search_term}',
                                    'price': '$35.00 AUD', 
                                    'url': '/products/retro-concert-tee-456',
                                    'image': 'https://depop.com/image2.jpg'
                                },
                                {
                                    'title': f'Classic Rock Shirt - {search_term}',
                                    'price': '$55.00 AUD',
                                    'url': '/products/classic-rock-shirt-789',
                                    'image': 'https://depop.com/image3.jpg'
                                }
                            ]
                        }
                    }
                    
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps(mock_results).encode())
                    
                    print(f"✅ Sent {len(mock_results['extracted_data']['listings'])} mock Depop Australia results")
                    
                else:
                    # Generic response for other URLs
                    response = {
                        'success': False,
                        'error': 'URL not supported in test mode'
                    }
                    self.send_response(400)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps(response).encode())
                    
            except Exception as e:
                print(f"❌ Error processing request: {e}")
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'success': False, 'error': str(e)}).encode())
        else:
            self.send_response(404)
            self.end_headers()

def start_test_server():
    """Start a simple test MCP server for Depop testing"""
    port = 3001
    server = HTTPServer(('localhost', port), DepopTestServer)
    
    print("🧪 DEPOP TEST MCP SERVER")
    print("=" * 50)
    print(f"🌐 Running on http://localhost:{port}")
    print("🎯 Testing Depop Australia search functionality")
    print("🔍 Mock data will be returned for testing")
    print("=" * 50)
    print("")
    print("✅ Server ready - run your discord-crawler test now!")
    print("   cd discord-crawler && node test-depop-search.js")
    print("")
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Server stopped")
        server.shutdown()

if __name__ == "__main__":
    start_test_server()
