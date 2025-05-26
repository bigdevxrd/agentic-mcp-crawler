# 🧠 Agentic MCP Crawler - Setup & Usage Guide

## Quick Setup

### 1. Environment Variables
Add to your `.env` file:
```bash
ANTHROPIC_API_KEY=your_claude_api_key_here
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_anon_key
```

### 2. Database Setup
Run the SQL schema in your Supabase SQL editor:
```bash
cat sql/agentic_crawler_schema.sql
```

### 3. Install Dependencies
```bash
pip install anthropic
```

### 4. Run Enhanced Server
```bash
python src/enhanced_mcp_server.py
```

## 🚀 Agentic Features

### Intelligent Crawling (`agentic_crawl`)
**What it does:** Thinks strategically about how to crawl based on your intent

**Usage:**
```python
# Instead of basic crawling
result = await agentic_crawl(
    url="https://competitor.com/pricing",
    user_query="Find their pricing tiers and feature comparison",
    context='{"urgency": "high", "depth": "comprehensive"}'
)
```

**Why it's better:**
- Claude analyzes your intent and selects optimal strategy
- Adapts crawl depth and focus based on content type
- Learns from previous successful crawls
- Discovers related opportunities automatically

### Proactive Discovery (`discover_opportunities`)
**What it does:** Finds high-value URLs you haven't thought of

**Usage:**
```python
opportunities = await discover_opportunities(
    domain="fintech",
    interests=["API pricing", "security features", "integration guides"]
)
```

**Results:**
- Curated list of promising URLs with reasoning
- Based on learned patterns from successful crawls
- Adapts to your specific interests and domain

### Intelligent Search (`intelligent_search`)
**What it does:** Searches your crawled content with smart insights

**Usage:**
```python
results = await intelligent_search(
    query="pricing models SaaS competitors",
    max_results=15
)
```

**Enhanced Features:**
- Relevance scoring based on your query intent
- Suggested follow-up actions for each result
- Identifies content gaps for future crawling

## 📊 Learning & Adaptation

The system gets smarter with every crawl:

1. **Strategy Selection:** Learns which crawl strategies work best for different sites
2. **Pattern Recognition:** Identifies successful URL patterns and content types  
3. **User Intent:** Better understanding of what you're looking for over time
4. **Adaptation:** Modifies strategies in real-time based on initial results

## 🔄 Migration from Basic MCP

### Option 1: Gradual Migration
Keep using your existing MCP server, but add agentic tools for complex tasks:

```python
# For simple extraction
result = await standard_crawl(url)

# For intelligent research  
result = await agentic_crawl(url, "Find competitive analysis data")
```

### Option 2: Full Replacement
Replace your existing server with `enhanced_mcp_server.py` for all crawling.

## 💡 Best Practices

### Writing Effective User Queries
❌ **Bad:** "Crawl this URL"
✅ **Good:** "Find pricing information and feature comparison for enterprise plans"

❌ **Bad:** "Get content from competitor site"  
✅ **Good:** "Research their go-to-market strategy and customer testimonials"

### Using Context Effectively
```python
context = {
    "urgency": "high",           # high/medium/low
    "depth": "comprehensive",    # surface/detailed/comprehensive  
    "focus": "pricing",          # specific focus area
    "competitor_analysis": True  # special mode flags
}
```

## 🎯 Next Steps

1. **Test the enhanced server** with a simple agentic_crawl
2. **Try discovery mode** on your target domain
3. **Let it learn** from 5-10 successful crawls
4. **Monitor the learning tables** in Supabase to see pattern development
5. **Experiment with different user queries** to see strategy adaptation

The system becomes dramatically more effective after ~10 crawls as it learns your patterns and preferences.
