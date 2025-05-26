#!/usr/bin/env python3
"""
🧠 AGENTIC MCP CRAWLER - SYSTEM HEALTH CHECK
Production-ready health check and system validation
"""

import os
import sys
from pathlib import Path
from datetime import datetime

def health_check():
    """Quick production health check"""
    print("🧠 AGENTIC MCP CRAWLER - HEALTH CHECK")
    print("=" * 50)
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Check critical files
    critical_files = [
        "src/enhanced_mcp_server.py",
        "src/agentic_crawler.py", 
        "src/utils.py",
        ".env",
        "requirements.txt"
    ]
    
    print(f"\n📁 Critical Files:")
    for file in critical_files:
        exists = Path(file).exists()
        print(f"  {'✅' if exists else '❌'} {file}")
        
    # Check environment
    print(f"\n🔧 Environment:")
    env_vars = ["SUPABASE_URL", "SUPABASE_SERVICE_KEY", "ANTHROPIC_API_KEY"]
    
    if Path(".env").exists():
        from dotenv import load_dotenv
        load_dotenv()
        
        for var in env_vars:
            value = os.getenv(var)
            if var == "ANTHROPIC_API_KEY":
                status = "✅" if value and value != "YOUR_ANTHROPIC_API_KEY_HERE" else "⚠️"
            else:
                status = "✅" if value else "❌"
            print(f"  {status} {var}: {'Configured' if value else 'Missing'}")
    else:
        print("  ❌ .env file not found")
        
    # Overall status
    print(f"\n🎯 System Status:")
    if all(Path(f).exists() for f in critical_files):
        if os.getenv("SUPABASE_URL") and os.getenv("SUPABASE_SERVICE_KEY"):
            print("  🟢 READY FOR DEPLOYMENT")
            print("  ℹ️  Add ANTHROPIC_API_KEY for full agentic features")
        else:
            print("  🔴 NEEDS CONFIGURATION")
            print("  ℹ️  Configure Supabase credentials in .env")
    else:
        print("  🔴 MISSING CRITICAL FILES")
        
    print(f"\n🚀 To start: python src/enhanced_mcp_server.py")

if __name__ == "__main__":
    try:
        health_check()
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        sys.exit(1)
