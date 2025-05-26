# 🆘 Help & Support

## Quick Help

### Getting Started
```bash
# Check system status
python quick_assess.py

# Test a simple crawl
curl -X POST http://localhost:8051/agentic_crawl \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com", "user_query": "Find main features"}'
```

### Common Commands

| Task | Command |
|------|---------|
| System check | `python quick_assess.py` |
| Start server | `python src/enhanced_mcp_server.py` |
| Test connection | `curl http://localhost:8051/health` |
| View logs | `tail -f logs/agentic_mcp.log` |
| Reset database | `supabase db reset` |

## Example Queries

### Research & Analysis
- `"Analyze their pricing strategy and identify gaps"`
- `"Find customer testimonials and case studies"`  
- `"Research their partnership program and requirements"`
- `"Identify their target market and positioning"`

### Competitive Intelligence
- `"Compare their features against our product roadmap"`
- `"Find their recent funding announcements and growth metrics"`
- `"Analyze their content strategy and thought leadership"`
- `"Discover their integration ecosystem and API offerings"`

### Content Discovery
- `"Find all their whitepapers and technical documentation"`
- `"Locate their developer resources and API examples"`
- `"Discover their community forums and support channels"`
- `"Find their recent blog posts about industry trends"`

## Best Practices

### Query Writing
✅ **Good**: `"Find their enterprise security features and compliance certifications"`  
❌ **Avoid**: `"Get page content"`

✅ **Good**: `"Research their customer onboarding process and user experience"`  
❌ **Avoid**: `"Crawl website"`

### Context Usage
```javascript
// For comprehensive research
{"depth": "comprehensive", "focus": "competitive_analysis"}

// For quick updates  
{"urgency": "high", "depth": "surface"}

// For discovery
{"mode": "exploration", "follow_related": true}
```

### Performance Tips
- Use specific queries rather than broad ones
- Set appropriate depth levels for your needs
- Enable learning for repeated similar tasks
- Use discovery mode to find new opportunities

## Troubleshooting

### System Issues

**Server won't start**
1. Check port availability: `lsof -i :8051`
2. Verify environment variables: `python quick_assess.py`
3. Check logs: `python src/enhanced_mcp_server.py --debug`

**Slow responses**
1. Check internet connection and DNS
2. Verify target website accessibility  
3. Reduce crawl depth or concurrent requests
4. Check Supabase connection latency

**Poor results quality**
1. Refine your query with more specific intent
2. Adjust context parameters for better strategy selection
3. Check if the target site has anti-bot measures
4. Try discovery mode to find alternative sources

### API Issues

**Authentication errors**
- Verify API keys are correctly set in .env
- Check key permissions and account status
- Ensure no trailing spaces in environment variables

**Rate limiting**  
- Built-in backoff handling should manage this automatically
- Check your API quotas and usage
- Consider upgrading API tier for heavy usage

## Getting Support

### Self-Help Resources
1. **System Assessment**: `python quick_assess.py`
2. **Documentation**: Check API_DOCS.md and SETUP_GUIDE.md
3. **Examples**: Review example queries above
4. **Logs**: Check application logs for detailed error info

### Advanced Support
- **GitHub Issues**: Report bugs and feature requests
- **Documentation**: Contribute improvements via PR
- **Community**: Join discussions in project repository

### Debugging Mode
```bash
# Enable verbose logging
LOG_LEVEL=DEBUG python src/enhanced_mcp_server.py

# Test individual components
python -c "from src.agentic_crawler import AgenticCrawler; print('Agentic system OK')"
```

## Performance Monitoring

### Health Checks
```bash
# Basic health
curl http://localhost:8051/health

# System status
curl http://localhost:8051/status

# Performance metrics
curl http://localhost:8051/metrics
```

### Learning System Stats
```bash
# View learned patterns
curl http://localhost:8051/learning/stats

# Recent crawl performance
curl http://localhost:8051/analytics/recent
```