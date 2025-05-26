-- Supabase Schema for Agentic Crawler Learning System
-- Run these SQL statements in your Supabase SQL editor

-- Table for storing learned patterns and strategies
CREATE TABLE IF NOT EXISTS learned_patterns (
    id SERIAL PRIMARY KEY,
    pattern_type VARCHAR(100) NOT NULL,
    pattern_data JSONB NOT NULL,
    effectiveness_score DECIMAL(3,2) DEFAULT 0.5,
    usage_count INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Table for crawl learning and performance tracking
CREATE TABLE IF NOT EXISTS crawl_learning (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP DEFAULT NOW(),
    url_pattern VARCHAR(255),
    user_intent TEXT,
    strategy_effectiveness JSONB,
    adaptation_notes TEXT[],
    success_metrics JSONB,
    domain_type VARCHAR(100),
    created_at TIMESTAMP DEFAULT NOW()
);

-- Table for tracking discovered opportunities
CREATE TABLE IF NOT EXISTS discovery_opportunities (
    id SERIAL PRIMARY KEY,
    domain VARCHAR(255),
    suggested_url TEXT,
    reasoning TEXT,
    confidence_score DECIMAL(3,2),
    user_interests TEXT[],
    status VARCHAR(50) DEFAULT 'suggested',
    created_at TIMESTAMP DEFAULT NOW(),
    crawled_at TIMESTAMP,
    results_summary JSONB
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_learned_patterns_type ON learned_patterns(pattern_type);
CREATE INDEX IF NOT EXISTS idx_crawl_learning_domain ON crawl_learning(url_pattern);
CREATE INDEX IF NOT EXISTS idx_discovery_opportunities_domain ON discovery_opportunities(domain);
CREATE INDEX IF NOT EXISTS idx_discovery_opportunities_status ON discovery_opportunities(status);