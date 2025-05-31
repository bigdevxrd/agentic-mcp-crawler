#!/usr/bin/env python3
"""
Unified MCP Server - Multi-Client Architecture
"""

import os
import json
from typing import Dict, Any, Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn

# Import existing MCP functionality
from enhanced_mcp_server import mcp, EnhancedCrawlContext, enhanced_crawl_lifespan


class CrawlRequest(BaseModel):
    url: str
    user_query: str
    context: Optional[str] = None
    client_type: Optional[str] = "api"


class ResponseFormatter:
    """Handles response formatting for different client types"""
    
    @staticmethod
    def format_for_client(data: Dict[str, Any], client_type: str = "api") -> Dict[str, Any]:
        if client_type == "discord":
            return ResponseFormatter._discord_format(data)
        elif client_type == "python":
            return ResponseFormatter._python_format(data)
        elif client_type == "claude":
            return ResponseFormatter._claude_format(data)
        else:
            return ResponseFormatter._api_format(data)
    
    @staticmethod
    def _discord_format(data: Dict[str, Any]) -> Dict[str, Any]:
        """Optimized for Discord embeds"""
        if not data.get("success"):
            return {"embed": {"title": "❌ Failed", "description": data.get("error", "Unknown error")}}
        
        results = data.get("results", {})
        primary = results.get("primary_content", {})
        
        return {
            "embed": {
                "title": f"🎯 {primary.get('title', 'Analysis Complete')}",
                "description": primary.get('summary', 'Successfully analyzed')[:400],
                "color": 0x00ff00
            }
        }
