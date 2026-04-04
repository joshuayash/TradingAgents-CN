# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

TradingAgents-CN is a Chinese-enhanced multi-agent stock analysis platform. It uses a multi-agent architecture with LangGraph/LangChain to orchestrate stock analysis through different analyst roles (market analyst, fundamentals analyst, news analyst, social media analyst).

**Architecture**: FastAPI (backend) + Vue 3 (frontend) + MongoDB + Redis

## Important Licensing Notes

- `tradingagents/` - Core multi-agent framework, Apache 2.0 licensed
- `app/` - FastAPI backend, proprietary (commercial license required)
- `frontend/` - Vue frontend, proprietary (commercial license required)

## Development Commands

### Backend (FastAPI)
```bash
# Run development server
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

# Or directly
python -m app.main
```

### Frontend (Vue 3)
```bash
cd frontend
yarn install
yarn dev          # Development server
yarn build        # Production build
yarn lint         # Lint and fix
yarn type-check   # TypeScript type checking
```

### Docker
```bash
# Build backend
docker build -f Dockerfile.backend -t tradingagents-backend .

# Full stack (using docker-compose)
docker-compose -f docker-compose.v1.0.0.yml up
```

## High-Level Architecture

### Three-Layer Structure

1. **`tradingagents/`** - Core framework (Apache 2.0)
   - `agents/` - Multi-agent system: analysts (market/fundamentals/news/social media), managers (research/risk), traders
   - `graph/` - LangGraph orchestration: `trading_graph.py` is the main state machine
   - `dataflows/` - Data providers for stock data, news, technical indicators
   - `llm_adapters/` - Adapters for various LLM providers (DeepSeek, DashScope, OpenAI-compatible)

2. **`app/`** - FastAPI backend (proprietary)
   - `routers/` - REST API endpoints organized by feature
   - `services/` - Business logic layer
   - `core/` - Configuration, database connections, middleware
   - `models/` - Pydantic models for data validation
   - `worker/` - Background sync tasks for Tushare/AKShare/BaoStock data

3. **`frontend/`** - Vue 3 SPA (proprietary)
   - `views/` - Page components (Analysis, Dashboard, Stocks, Settings, etc.)
   - `api/` - TypeScript API clients
   - `stores/` - Pinia state management
   - `components/` - Reusable Vue components

### Data Flow

```
User Request → FastAPI (app/routers) → Services (app/services) → TradingAgents Core (tradingagents/)
                                                                 ↓
                                                          LangGraph Orchestration
                                                                 ↓
                                    Market/Fundamentals/News Analysts → Risk Manager → Report
```

### Multi-Source Data Architecture

Three data sources are supported with fallback:
- **Tushare** - Professional A-share data (requires token)
- **AKShare** - Free data source (default)
- **BaoStock** - Additional free source

The `tradingagents/dataflows/providers/` directory contains adapters for each source, and the system can fall back between sources.

### Key Configuration

Environment variables are managed via Pydantic Settings in `app/core/config.py`. Key settings:
- `DEBUG`, `HOST`, `PORT` - Server configuration
- `MONGODB_*`, `REDIS_*` - Database connections
- `JWT_*` - Authentication
- `*_API_KEY` - LLM provider keys (DEEPSEEK, DASHSCOPE, etc.)
- `DEFAULT_CHINA_DATA_SOURCE` - Primary data source selection

## Testing

Tests are in `tests/` and `scripts/` directories. Many test files are organized by topic or bug fix:
```bash
# Run specific test
python -m pytest tests/test_analysis.py -v

# Run with coverage
python -m pytest --cov=app tests/
```

## Critical Files

- `app/main.py` - FastAPI app initialization and lifespan management
- `tradingagents/graph/trading_graph.py` - Main LangGraph state machine
- `app/core/config.py` - Pydantic Settings for all configuration
- `app/core/database.py` - MongoDB connection management
- `tradingagents/dataflows/stock_data_service.py` - Unified stock data access
