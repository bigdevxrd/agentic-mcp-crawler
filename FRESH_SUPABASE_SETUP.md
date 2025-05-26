# 🚀 Fresh Supabase Setup & API Keys for Agentic MCP

**Yes, you absolutely can (and should) create a fresh Supabase project from command line!**

This is the perfect time to set up clean API keys for your agentic system.

## 🏗️ Method 1: CLI Project Creation (Recommended)

### 1. Install Supabase CLI
```bash
# macOS
brew install supabase/tap/supabase

# or via npm
npm install -g supabase
```

### 2. Login to Supabase
```bash
supabase login
```
This opens browser to authenticate and stores your access token locally.

### 3. Create New Project via CLI
```bash
supabase projects create agentic-mcp-crawler \
  --org-id YOUR_ORG_ID \
  --db-password YOUR_STRONG_PASSWORD \
  --region us-east-1 \
  --plan free
```

**To get your org ID:**
```bash
supabase orgs list
```

### 4. Get Project Details
```bash
supabase projects list
# Copy the project ref for next steps
```

### 5. Update .env with Fresh Credentials
```bash
# Get your new project's API keys
supabase projects api-keys --project-ref YOUR_PROJECT_REF

# This will output:
# anon key: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
# service_role key: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

## 🔑 Method 2: Management API (Programmatic)

For automation or if you prefer REST API:

```bash
# Get your Personal Access Token from: https://supabase.com/dashboard/account/tokens

curl -X POST https://api.supabase.com/v1/projects \
  -H "Authorization: Bearer YOUR_PERSONAL_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "agentic-mcp-crawler",
    "organization_id": "YOUR_ORG_ID",
    "region": "us-east-1",
    "plan": "free",
    "db_pass": "YOUR_STRONG_PASSWORD"
  }'
```

## 🔄 Best Practice: Fresh API Keys

**YES - This is the perfect time to rotate keys!** Here's why:

### ✅ Benefits of Fresh Keys:
- **Clean slate** for your agentic system
- **Dedicated project** with proper naming  
- **No legacy permissions** or old integrations
- **Fresh security posture**
- **Easier troubleshooting** with dedicated project

### 🔧 Complete Fresh Setup Process:

1. **Create New Project** (using CLI method above)

2. **Set Up Database Schema**
```bash
# Link your local project to new remote
supabase link --project-ref YOUR_NEW_PROJECT_REF

# Apply your agentic schema
supabase db push
```

3. **Update Environment Variables**
```bash
# Update your .env with new credentials
SUPABASE_URL=https://YOUR_NEW_PROJECT_REF.supabase.co
SUPABASE_SERVICE_KEY=eyJhbGciOiJIUzI1NiIs... # New service key
ANTHROPIC_API_KEY=sk-ant-api03-... # Add your Anthropic key
```

4. **Migrate Data (if needed)**
```bash
# If you have existing data to migrate
supabase db dump --project-ref OLD_PROJECT_REF > old_data.sql
supabase db reset --linked
psql -h YOUR_NEW_PROJECT_HOST -U postgres -d postgres < old_data.sql
```

## 🏆 Recommended Approach

**Create a dedicated "agentic-mcp-crawler" project:**

```bash
# 1. Create fresh project
supabase projects create agentic-mcp-crawler \
  --org-id $(supabase orgs list --format json | jq -r '.[0].id') \
  --db-password $(openssl rand -base64 32) \
  --region us-east-1

# 2. Get project ref
PROJECT_REF=$(supabase projects list --format json | jq -r '.[] | select(.name=="agentic-mcp-crawler") | .id')

# 3. Get API keys
supabase projects api-keys --project-ref $PROJECT_REF

# 4. Set up schema
supabase link --project-ref $PROJECT_REF
supabase db push
```

## 🔒 Security Best Practices

1. **Use service_role key** for server-side agentic operations
2. **Rotate keys quarterly** for production systems  
3. **Use environment variables** never hardcode keys
4. **Enable Row Level Security** on your learning tables
5. **Monitor API usage** via Supabase dashboard

## 🧪 Testing Your Fresh Setup

```bash
# Test the connection
cd /Users/bigdev/dealhawk-standalone/mcp-crawl4ai-rag
source .venv/bin/activate

# Update .env with new credentials, then:
python -c "
from src.utils import get_supabase_client
client = get_supabase_client()
print('✅ Fresh Supabase connection successful!')
print(f'Project: {client.url}')
"
```

**Ready to create your fresh, secure agentic setup?** 

This approach gives you:
- 🆕 **Clean dedicated project**
- 🔑 **Fresh API keys** with no legacy baggage  
- 🧠 **Purpose-built** for agentic intelligence
- 🔒 **Modern security** practices from day one

Would you like me to walk through the CLI setup process with you?
