# 🛠️ Complete Setup Guide

## Prerequisites

- Python 3.11+
- Docker (for local Supabase)
- Git
- 8GB+ RAM recommended

## Step-by-Step Setup

### 1. Clone & Environment

```bash
git clone <repository-url>
cd agentic-mcp-crawler
python -m venv .venv
source .venv/bin/activate  # or `.venv\Scripts\activate` on Windows
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Database Setup

**Option A: Use Existing Supabase Project**
```bash
# Update .env with your credentials
SUPABASE_URL=your_project_url
SUPABASE_SERVICE_KEY=your_service_key
```

**Option B: Create Fresh Project** 
```bash
# Install Supabase CLI
brew install supabase/tap/supabase

# Create new project
./create_fresh_supabase.sh
```

**Option C: Local Development**
```bash
supabase init
supabase start
# Use local credentials from output
```

### 4. API Keys

Get your API keys:
- **Anthropic**: https://console.anthropic.com/ (required for agentic features)
- **OpenAI**: https://platform.openai.com/ (optional, for embeddings)

Add to `.env`:
```bash
ANTHROPIC_API_KEY=sk-ant-api03-...
OPENAI_API_KEY=sk-...  # optional
```

### 5. Database Schema

```bash
# Run in Supabase SQL editor or local instance
psql -f sql/agentic_crawler_schema.sql
psql -f crawled_pages.sql
```

### 6. Test Installation

```bash
python quick_assess.py
# Should show: 🟢 FULLY OPERATIONAL
```

### 7. Launch System

```bash
python src/enhanced_mcp_server.py
```

## Environment Variables Reference

```bash
# Core Configuration
TRANSPORT=sse
HOST=0.0.0.0
PORT=8051

# Database
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_SERVICE_KEY=eyJh...
SUPABASE_ANON_KEY=eyJh...  # optional

# AI Services  
ANTHROPIC_API_KEY=sk-ant-api03-...  # Required for agentic features
OPENAI_API_KEY=sk-...              # Optional for embeddings

# Optional Configuration
MODEL_CHOICE=                      # Embedding model preference
LOG_LEVEL=INFO                     # DEBUG, INFO, WARNING, ERROR
ENABLE_LEARNING=true               # Enable pattern learning
```

## Troubleshooting

### Common Issues

**"ModuleNotFoundError"**
```bash
pip install -r requirements.txt
source .venv/bin/activate
```

**"Supabase connection failed"**
- Check SUPABASE_URL and SUPABASE_SERVICE_KEY
- Verify project is active in Supabase dashboard
- Test connection: `curl $SUPABASE_URL/rest/v1/`

**"Anthropic API error"**  
- Verify API key at https://console.anthropic.com/
- Check account has sufficient credits
- Ensure key has correct permissions

**"Database table missing"**
- Run SQL schema files in correct order
- Check table creation in Supabase dashboard
- Verify service key has sufficient permissions

### Performance Optimization

**For Heavy Usage:**
```bash
# Increase worker processes
WORKERS=4

# Enable connection pooling
DB_POOL_SIZE=20

# Optimize for large crawls
MAX_CONCURRENT_CRAWLS=10
```

**For Development:**
```bash
# Enable debug logging
LOG_LEVEL=DEBUG

# Disable learning (faster)
ENABLE_LEARNING=false

# Use local Supabase
supabase start --include postgres
```