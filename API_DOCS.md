# 🔧 API Documentation

## Agentic Tools

### `agentic_crawl(url, user_query, context?)`

**Intelligent crawling with strategic thinking**

```python
result = await agentic_crawl(
    url="https://competitor.com/pricing",
    user_query="Find their pricing tiers and compare feature sets",
    context={"urgency": "high", "depth": "comprehensive"}
)
```

**Parameters:**
- `url` (string): Target URL to analyze
- `user_query` (string): Describe what you're looking for in natural language
- `context` (object, optional): Additional context for strategy selection

**Returns:**
```json
{
    "success": true,
    "results": {
        "primary_content": {...},
        "discovered_opportunities": [...],
        "performance_metrics": {...}
    },
    "strategy_used": "deep_research",
    "learning_applied": "Adapted based on 15 previous similar crawls"
}
```

### `discover_opportunities(domain, interests)`

**Proactive discovery of high-value content**

```python
opportunities = await discover_opportunities(
    domain="fintech",
    interests=["API pricing", "security features", "integration examples"]
)
```

### `intelligent_search(query, max_results?)`

**Smart search with relevance insights**

```python
results = await intelligent_search(
    query="pricing models SaaS competitors",
    max_results=20
)
```

## Strategy Types

### Deep Research
- **When**: Comprehensive analysis needed
- **Depth**: 3+ levels of following links
- **Best for**: Competitive research, market analysis
- **Example**: "Analyze their entire product positioning strategy"

### Quick Scanner  
- **When**: Fast overview required
- **Depth**: Surface-level extraction
- **Best for**: Status checks, quick facts
- **Example**: "Check if they've announced new pricing"

### Discovery Mode
- **When**: Exploring new opportunities  
- **Depth**: 2 levels with broad exploration
- **Best for**: Finding related content, market mapping
- **Example**: "Find all companies in their ecosystem"

## Context Parameters

```javascript
{
    "urgency": "high|medium|low",
    "depth": "surface|detailed|comprehensive", 
    "focus": "pricing|features|customers|strategy",
    "learn_patterns": true,
    "follow_social": false,
    "ignore_ads": true
}
```

## Error Handling

The system gracefully handles:
- **Rate limiting**: Automatic backoff and retry
- **Blocked content**: Alternative extraction methods
- **Site changes**: Real-time strategy adaptation
- **Network issues**: Resilient connection handling

## Learning System

Every successful crawl teaches the system:
- Which strategies work best for different site types
- What content patterns indicate high-value information  
- How to recognize and avoid low-quality sources
- User preferences and successful query patterns