"""
🤖 AGENTIC DISCORD BOT - Intelligent Web Crawling via Discord
Connects Discord users to your deployed agentic MCP crawler on Railway
"""

import discord
from discord.ext import commands
from discord import app_commands
import aiohttp
import json
import os
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

class AgenticDiscordBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(command_prefix='!', intents=intents)
        
        # Your Railway deployment URL
        self.agentic_crawler_url = os.getenv('AGENTIC_CRAWLER_URL', 'https://your-railway-url.up.railway.app')
        
    async def setup_hook(self):
        """Called when bot is starting up"""
        print(f"🧠 Agentic Discord Bot starting...")
        print(f"🔗 Connected to crawler: {self.agentic_crawler_url}")
        
        # Sync commands
        try:
            synced = await self.tree.sync()
            print(f"✅ Synced {len(synced)} commands")
        except Exception as e:
            print(f"❌ Failed to sync commands: {e}")

bot = AgenticDiscordBot()

@bot.event
async def on_ready():
    """Bot is ready"""
    print(f'🤖 {bot.user} is now connected to Discord!')
    print(f'🧠 Ready to provide agentic web crawling intelligence!')

# Helper function to check admin permissions
def is_admin():
    async def predicate(interaction: discord.Interaction):
        if not interaction.guild:
            await interaction.response.send_message("This command can only be used in a server.", ephemeral=True)
            return False
            
        member = interaction.user
        admin_role = discord.utils.get(member.guild.roles, name="Admin")
        
        if (admin_role and admin_role in member.roles) or member.guild_permissions.administrator:
            return True
            
        await interaction.response.send_message("❌ You need Admin role or Administrator permissions.", ephemeral=True)
        return False
        
    return app_commands.check(predicate)

@bot.tree.command(name="agentic_crawl", description="🧠 Intelligently crawl a website with strategic thinking")
@app_commands.describe(
    url="The website URL to crawl",
    query="Describe what you're looking for (e.g., 'Find their pricing strategy and competitive gaps')",
    context="Optional: Additional context like urgency=high, depth=comprehensive"
)
async def agentic_crawl(interaction: discord.Interaction, url: str, query: str, context: Optional[str] = None):
    """Main agentic crawling command"""
    
    await interaction.response.defer(thinking=True)
    
    try:
        # Prepare request to your Railway deployment
        payload = {
            "url": url,
            "user_query": query
        }
        
        if context:
            try:
                # Try to parse context as JSON
                context_dict = json.loads(context) if context.startswith('{') else {"note": context}
                payload["context"] = context_dict
            except:
                payload["context"] = {"note": context}
        
        # Call your deployed agentic crawler
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{bot.agentic_crawler_url}/agentic_crawl",
                json=payload,
                timeout=aiohttp.ClientTimeout(total=60)
            ) as response:
                
                if response.status == 200:
                    result = await response.json()
                    
                    # Create rich embed with results
                    embed = discord.Embed(
                        title="🧠 Agentic Crawl Results",
                        description=f"**Query:** {query}",
                        color=discord.Color.blue()
                    )
                    
                    embed.add_field(
                        name="🎯 Target URL",
                        value=f"[{url}]({url})",
                        inline=False
                    )
                    
                    if result.get("success"):
                        # Extract key insights
                        insights = result.get("results", {}).get("primary_content", {})
                        strategy_used = result.get("strategy_used", "adaptive")
                        opportunities = result.get("results", {}).get("discovered_opportunities", [])
                        
                        embed.add_field(
                            name="✅ Status",
                            value="Intelligent crawl completed successfully",
                            inline=True
                        )
                        
                        embed.add_field(
                            name="🧩 Strategy Used",
                            value=strategy_used.replace('_', ' ').title(),
                            inline=True
                        )
                        
                        if opportunities:
                            embed.add_field(
                                name="🔍 Opportunities Discovered",
                                value=f"Found {len(opportunities)} additional sources",
                                inline=True
                            )
                        
                        # Add content preview (truncated)
                        if insights.get("content"):
                            content_preview = str(insights["content"])[:500]
                            if len(content_preview) == 500:
                                content_preview += "..."
                                
                            embed.add_field(
                                name="📄 Content Preview",
                                value=f"```{content_preview}```",
                                inline=False
                            )
                        
                        embed.color = discord.Color.green()
                        
                    else:
                        embed.add_field(
                            name="❌ Error",
                            value=result.get("error", "Unknown error occurred"),
                            inline=False
                        )
                        embed.color = discord.Color.red()
                        
                else:
                    embed = discord.Embed(
                        title="❌ Crawl Failed",
                        description=f"Server responded with status {response.status}",
                        color=discord.Color.red()
                    )
                    
    except aiohttp.ClientTimeout:
        embed = discord.Embed(
            title="⏰ Timeout",
            description="The crawl took too long. Complex sites may need more time.",
            color=discord.Color.orange()
        )
        
    except Exception as e:
        embed = discord.Embed(
            title="❌ Error",
            description=f"An error occurred: {str(e)}",
            color=discord.Color.red()
        )
    
    embed.set_footer(text="Powered by Agentic MCP Crawler")
    await interaction.followup.send(embed=embed)

@bot.tree.command(name="discover", description="🔍 Proactively discover valuable content opportunities")
@app_commands.describe(
    domain="Domain or topic to explore (e.g., 'fintech', 'ecommerce')",
    interests="Your specific interests (comma-separated)"
)
async def discover_opportunities(interaction: discord.Interaction, domain: str, interests: str):
    """Proactive discovery command"""
    
    await interaction.response.defer(thinking=True)
    
    try:
        interests_list = [i.strip() for i in interests.split(',')]
        
        payload = {
            "domain": domain,
            "interests": interests_list
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{bot.agentic_crawler_url}/discover_opportunities",
                json=payload,
                timeout=aiohttp.ClientTimeout(total=30)
            ) as response:
                
                if response.status == 200:
                    result = await response.json()
                    
                    embed = discord.Embed(
                        title="🔍 Discovery Results",
                        description=f"**Domain:** {domain}",
                        color=discord.Color.purple()
                    )
                    
                    if result.get("success"):
                        opportunities = result.get("opportunities", [])
                        
                        embed.add_field(
                            name="📊 Opportunities Found",
                            value=f"Discovered {len(opportunities)} high-value sources",
                            inline=False
                        )
                        
                        # Show top opportunities
                        for i, opp in enumerate(opportunities[:3], 1):
                            embed.add_field(
                                name=f"🎯 Opportunity #{i}",
                                value=f"**URL:** {opp.get('url', 'N/A')}\n**Reasoning:** {opp.get('reasoning', 'High relevance detected')[:100]}...",
                                inline=False
                            )
                            
                        if len(opportunities) > 3:
                            embed.add_field(
                                name="➕ More Results",
                                value=f"...and {len(opportunities) - 3} more opportunities found",
                                inline=False
                            )
                    else:
                        embed.add_field(
                            name="❌ Error",
                            value=result.get("error", "Discovery failed"),
                            inline=False
                        )
                        embed.color = discord.Color.red()
                else:
                    embed = discord.Embed(
                        title="❌ Discovery Failed", 
                        color=discord.Color.red()
                    )
                    
    except Exception as e:
        embed = discord.Embed(
            title="❌ Error",
            description=f"Discovery error: {str(e)}",
            color=discord.Color.red()
        )
    
    embed.set_footer(text="Use /agentic_crawl on promising URLs")
    await interaction.followup.send(embed=embed)

@bot.tree.command(name="search_crawls", description="🔎 Search through previous crawl results")
@app_commands.describe(query="What to search for in previous crawls")
async def search_crawls(interaction: discord.Interaction, query: str):
    """Search previous crawl results"""
    
    await interaction.response.defer(thinking=True)
    
    try:
        payload = {"query": query, "max_results": 10}
        
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{bot.agentic_crawler_url}/intelligent_search",
                json=payload,
                timeout=aiohttp.ClientTimeout(total=20)
            ) as response:
                
                if response.status == 200:
                    result = await response.json()
                    
                    embed = discord.Embed(
                        title="🔎 Search Results",
                        description=f"**Query:** {query}",
                        color=discord.Color.blue()
                    )
                    
                    if result.get("success"):
                        results = result.get("results", [])
                        
                        if results:
                            embed.add_field(
                                name="📊 Results Found",
                                value=f"Found {len(results)} relevant crawl results",
                                inline=False
                            )
                            
                            # Show top results
                            for i, res in enumerate(results[:3], 1):
                                content_preview = str(res.get("content", ""))[:150]
                                if len(content_preview) == 150:
                                    content_preview += "..."
                                    
                                embed.add_field(
                                    name=f"📄 Result #{i}",
                                    value=f"**Source:** {res.get('metadata', {}).get('url', 'Unknown')}\n**Content:** {content_preview}",
                                    inline=False
                                )
                        else:
                            embed.add_field(
                                name="🤷 No Results",
                                value="No previous crawls match your query. Try using /discover or /agentic_crawl first.",
                                inline=False
                            )
                            embed.color = discord.Color.orange()
                    else:
                        embed.add_field(
                            name="❌ Error",
                            value=result.get("error", "Search failed"),
                            inline=False
                        )
                        embed.color = discord.Color.red()
                else:
                    embed = discord.Embed(
                        title="❌ Search Failed",
                        color=discord.Color.red()
                    )
                    
    except Exception as e:
        embed = discord.Embed(
            title="❌ Error", 
            description=f"Search error: {str(e)}",
            color=discord.Color.red()
        )
    
    await interaction.followup.send(embed=embed)

@bot.tree.command(name="crawler_status", description="📊 Check agentic crawler system status")
async def crawler_status(interaction: discord.Interaction):
    """Check the status of the agentic crawler system"""
    
    await interaction.response.defer(thinking=True)
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{bot.agentic_crawler_url}/health",
                timeout=aiohttp.ClientTimeout(total=10)
            ) as response:
                
                embed = discord.Embed(
                    title="📊 Agentic Crawler Status",
                    color=discord.Color.green() if response.status == 200 else discord.Color.red()
                )
                
                if response.status == 200:
                    embed.add_field(name="🟢 Status", value="Online and Ready", inline=True)
                    embed.add_field(name="🧠 Intelligence", value="Agentic AI Active", inline=True)
                    embed.add_field(name="🔗 URL", value=f"[Live Service]({bot.agentic_crawler_url})", inline=True)
                else:
                    embed.add_field(name="🔴 Status", value="Service Unavailable", inline=True)
                    
    except Exception as e:
        embed = discord.Embed(
            title="❌ Status Check Failed",
            description=f"Could not reach crawler service: {str(e)}",
            color=discord.Color.red()
        )
    
    await interaction.followup.send(embed=embed)

@bot.tree.command(name="help_agentic", description="ℹ️ Learn how to use agentic crawling commands")
async def help_agentic(interaction: discord.Interaction):
    """Help command for agentic features"""
    
    embed = discord.Embed(
        title="🧠 Agentic Crawler Help",
        description="Transform your web research with AI-powered intelligence",
        color=discord.Color.blue()
    )
    
    embed.add_field(
        name="🎯 /agentic_crawl",
        value="Intelligently crawl websites with strategic thinking\n**Example:** `/agentic_crawl https://competitor.com analyze their pricing strategy`",
        inline=False
    )
    
    embed.add_field(
        name="🔍 /discover",
        value="Proactively find valuable content opportunities\n**Example:** `/discover fintech API pricing, security, integrations`",
        inline=False
    )
    
    embed.add_field(
        name="🔎 /search_crawls", 
        value="Search through previous crawl results\n**Example:** `/search_crawls SaaS pricing models`",
        inline=False
    )
    
    embed.add_field(
        name="📊 /crawler_status",
        value="Check if the agentic crawler system is online",
        inline=False
    )
    
    embed.add_field(
        name="💡 Pro Tips",
        value="• Use natural language queries for better results\n• Be specific about what you're looking for\n• The AI learns from your crawling patterns",
        inline=False
    )
    
    embed.set_footer(text="Powered by Claude 4 + Agentic Intelligence")
    
    await interaction.response.send_message(embed=embed)

if __name__ == "__main__":
    # Run the bot
    discord_token = os.getenv('DISCORD_BOT_TOKEN')
    
    if not discord_token:
        print("❌ DISCORD_BOT_TOKEN not found in environment variables")
        print("Please add your Discord bot token to .env file")
        exit(1)
        
    print("🚀 Starting Agentic Discord Bot...")
    bot.run(discord_token)
