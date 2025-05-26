# 🚂 Railway Deployment Guide

## Environment Variables for Railway

Copy and paste these into Railway's Variables section:

### Required Variables:
```
SUPABASE_URL=https://ciiyqazfvdznyxfcpjwm.supabase.co
SUPABASE_SERVICE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImNpaXlxYXpmdmR6bnl4ZmNwandtIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc0MDYyNDU3MiwiZXhwIjoyMDU2MjAwNTcyfQ.WNFrTZJ7XbYUFgSCIpHK_exyBZNlpbC5859oUL0K-8o
PORT=8051
HOST=0.0.0.0
TRANSPORT=sse
```

### For Full Agentic Features:
```
ANTHROPIC_API_KEY=your_anthropic_key_here
```

### Optional Enhancement:
```
OPENAI_API_KEY=your_openai_key_here
```

## Steps:
1. Go to https://railway.app/
2. New Project → Deploy from GitHub repo
3. Select: bigdevxrd/agentic-mcp-crawler
4. Add environment variables above
5. Deploy automatically!

## Testing Your Deployment:
Once deployed, Railway will give you a URL like:
`https://agentic-mcp-crawler-production.up.railway.app`

Test with:
```bash
curl https://your-railway-url.railway.app/health
```

Your agentic MCP crawler will be live and ready for intelligent web crawling!
