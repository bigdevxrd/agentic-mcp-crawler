#!/bin/bash
# 🧠 Complete Fresh Supabase Setup for Agentic MCP

echo "🚀 Creating Fresh Supabase Project for Agentic MCP Crawler"
echo "=================================================="

# Set the CLI path
SUPABASE_CLI="/usr/local/Cellar/supabase/2.23.4/bin/supabase"

# Check if logged in
echo "🔐 Checking login status..."
if ! $SUPABASE_CLI projects list &>/dev/null; then
    echo "❌ Please login first:"
    echo "   $SUPABASE_CLI login"
    echo "   (Browser should open for authentication)"
    exit 1
fi

echo "✅ Successfully logged in!"

# Get organization ID
echo "📋 Getting your organization ID..."
ORG_OUTPUT=$($SUPABASE_CLI orgs list --format json)
ORG_ID=$(echo $ORG_OUTPUT | jq -r '.[0].id')
ORG_NAME=$(echo $ORG_OUTPUT | jq -r '.[0].name')

echo "🏢 Using organization: $ORG_NAME ($ORG_ID)"

# Generate strong password
echo "🔑 Generating secure database password..."
DB_PASSWORD=$(openssl rand -base64 32)

# Create the project
echo "🏗️  Creating 'agentic-mcp-crawler' project..."
PROJECT_OUTPUT=$($SUPABASE_CLI projects create agentic-mcp-crawler \
  --org-id $ORG_ID \
  --db-password "$DB_PASSWORD" \
  --region us-east-1 \
  --format json)

if [ $? -ne 0 ]; then
    echo "❌ Failed to create project. Error:"
    echo "$PROJECT_OUTPUT"
    exit 1
fi

# Get project details
PROJECT_REF=$(echo $PROJECT_OUTPUT | jq -r '.id')
PROJECT_URL="https://$PROJECT_REF.supabase.co"

echo "✅ Project created successfully!"
echo "   Project Ref: $PROJECT_REF"
echo "   Project URL: $PROJECT_URL"

# Get API keys
echo "🔑 Retrieving API keys..."
KEYS_OUTPUT=$($SUPABASE_CLI projects api-keys --project-ref $PROJECT_REF --format json)
ANON_KEY=$(echo $KEYS_OUTPUT | jq -r '.anon')
SERVICE_KEY=$(echo $KEYS_OUTPUT | jq -r '.service_role')

# Update .env file
ENV_FILE="/Users/bigdev/dealhawk-standalone/mcp-crawl4ai-rag/.env"
echo "📝 Updating .env file..."

# Backup existing .env
cp "$ENV_FILE" "$ENV_FILE.backup.$(date +%Y%m%d_%H%M%S)"

# Update with fresh credentials
cat > "$ENV_FILE" << EOF
# MCP Server Configuration
TRANSPORT=sse
HOST=0.0.0.0
PORT=8051

# Fresh Supabase Configuration for Agentic MCP
SUPABASE_URL=$PROJECT_URL
SUPABASE_SERVICE_KEY=$SERVICE_KEY
SUPABASE_ANON_KEY=$ANON_KEY

# Database password (for manual connections)
SUPABASE_DB_PASSWORD=$DB_PASSWORD

# Anthropic API Configuration (add your key)
ANTHROPIC_API_KEY=YOUR_ANTHROPIC_API_KEY_HERE

# OpenAI API Configuration (for embeddings - optional)
OPENAI_API_KEY=
MODEL_CHOICE=
EOF

echo "✅ Environment updated with fresh credentials!"

# Setup database schema
echo "🗄️  Setting up agentic database schema..."
cd /Users/bigdev/dealhawk-standalone/mcp-crawl4ai-rag

# Link project
$SUPABASE_CLI link --project-ref $PROJECT_REF --password "$DB_PASSWORD"

# Apply schema
if [ -f "sql/agentic_crawler_schema.sql" ]; then
    echo "📊 Applying agentic crawler schema..."
    $SUPABASE_CLI db push
else
    echo "⚠️  Schema file not found. You'll need to run the SQL manually."
fi

echo ""
echo "🎉 FRESH AGENTIC MCP SETUP COMPLETE!"
echo "====================================="
echo ""
echo "📋 Project Details:"
echo "   Name: agentic-mcp-crawler"
echo "   URL: $PROJECT_URL"
echo "   Region: us-east-1"
echo "   Ref: $PROJECT_REF"
echo ""
echo "🔑 Next Steps:"
echo "1. Add your Anthropic API key to .env"
echo "2. Run the SQL schema in Supabase dashboard"
echo "3. Test: python src/enhanced_mcp_server.py"
echo ""
echo "🔒 Security:"
echo "   - Fresh API keys generated"
echo "   - Strong database password created"
echo "   - Previous .env backed up"
echo ""
echo "🧠 Ready for agentic intelligence!"
EOF
