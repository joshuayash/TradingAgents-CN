# TradingAgents-CN 项目指南

本文件为 AI 编程助手提供关于 TradingAgents-CN 项目的全面指南。

## 项目概述

**TradingAgents-CN** 是一个面向中文用户的多智能体股票分析学习平台，基于多智能体架构和 AI 大模型进行股票研究与策略实验。

- **版本**: v1.0.0-preview
- **Python 版本要求**: >= 3.10
- **项目语言**: 中文为主，代码注释和文档均为中文

### 核心定位

- 面向中文用户的多智能体与大模型股票分析学习平台
- 支持 A股/港股/美股 分析
- 用于研究和教育目的，**不提供实盘交易指令**

## 技术架构

### 三层架构

```
┌─────────────────────────────────────────────────────────────┐
│                    Frontend (Vue 3)                         │
│              前端界面 - 专有授权（商业授权需要）              │
└─────────────────────────┬───────────────────────────────────┘
                          │ RESTful API / WebSocket / SSE
┌─────────────────────────▼───────────────────────────────────┐
│                     Backend (FastAPI)                       │
│            后端 API 服务 - 专有授权（商业授权需要）            │
│         routers/ │ services/ │ models/ │ worker/           │
└─────────────────────────┬───────────────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────────────┐
│              TradingAgents Core (Apache 2.0)                │
│         多智能体核心框架 - 开源授权                          │
│    agents/ │ graph/ │ dataflows/ │ llm_adapters/           │
└─────────────────────────────────────────────────────────────┘
```

### 技术栈

| 层级 | 技术 | 说明 |
|------|------|------|
| 前端 | Vue 3 + Vite + TypeScript | Element Plus UI 组件库 |
| 后端 | FastAPI + Uvicorn | Python 异步 Web 框架 |
| 数据库 | MongoDB + Redis | 数据持久化 + 缓存 |
| 任务调度 | APScheduler | 定时数据同步任务 |
| AI/LLM | LangGraph + LangChain | 多智能体编排框架 |
| 股票数据 | AKShare / Tushare / BaoStock | 中国股票数据源 |
| 容器化 | Docker + Docker Compose | 支持 amd64 / arm64 |

## 代码组织结构

### 目录说明

```
TradingAgents-CN/
├── tradingagents/          # 核心多智能体框架 (Apache 2.0)
│   ├── agents/             # 智能体定义
│   │   ├── analysts/       # 分析师: market, fundamentals, news, social_media
│   │   ├── managers/       # 经理: research_manager, risk_manager
│   │   ├── researchers/    # 研究员: bull/bear researcher
│   │   └── trader/         # 交易决策智能体
│   ├── graph/              # LangGraph 状态机编排
│   │   ├── trading_graph.py    # 主状态机入口
│   │   ├── conditional_logic.py
│   │   ├── propagation.py
│   │   └── reflection.py
│   ├── dataflows/          # 数据流管理
│   │   ├── providers/      # 数据源适配器 (china/hk/us)
│   │   ├── cache/          # 多级缓存实现
│   │   └── stock_data_service.py
│   ├── llm_adapters/       # LLM 提供商适配器
│   │   ├── deepseek_adapter.py
│   │   ├── dashscope_openai_adapter.py
│   │   └── google_openai_adapter.py
│   └── utils/              # 工具函数
│
├── app/                    # FastAPI 后端 (专有授权)
│   ├── routers/            # API 路由端点
│   ├── services/           # 业务逻辑层
│   ├── models/             # Pydantic 数据模型
│   ├── core/               # 配置、数据库连接、中间件
│   │   ├── config.py       # Pydantic Settings 配置
│   │   ├── database.py     # MongoDB 连接管理
│   │   └── redis_client.py # Redis 连接管理
│   ├── worker/             # 后台数据同步任务
│   └── middleware/         # 请求中间件
│
├── frontend/               # Vue 3 前端 (专有授权)
│   ├── src/
│   │   ├── views/          # 页面组件
│   │   ├── components/     # 可复用组件
│   │   ├── api/            # API 客户端
│   │   ├── stores/         # Pinia 状态管理
│   │   └── router/         # Vue Router 路由
│   └── package.json
│
├── tests/                  # 测试文件
├── docs/                   # 项目文档
├── scripts/                # 脚本工具
├── config/                 # 配置文件目录
└── docker/                 # Docker 配置文件
```

### 关键文件

| 文件路径 | 说明 |
|----------|------|
| `app/main.py` | FastAPI 应用入口和生命周期管理 |
| `tradingagents/graph/trading_graph.py` | 主 LangGraph 状态机 |
| `app/core/config.py` | Pydantic Settings 配置管理 |
| `tradingagents/default_config.py` | 默认配置项 |
| `pyproject.toml` | Python 项目配置和依赖 |

## 开发和运行命令

### 后端开发 (FastAPI)

```bash
# 安装依赖
pip install -e .

# 开发服务器（热重载）
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

# 或者直接运行
python -m app.main

# 生产服务器
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### 前端开发 (Vue 3)

```bash
cd frontend

# 安装依赖
yarn install

# 开发服务器
yarn dev          # 默认端口 3000

# 构建
yarn build        # 生产构建

# 代码检查
yarn lint         # ESLint 检查和修复
yarn type-check   # TypeScript 类型检查
yarn format       # Prettier 格式化
```

### Docker 部署

```bash
# 完整部署（包含前后端、MongoDB、Redis）
docker-compose up -d

# 仅启动核心服务
docker-compose up -d backend mongodb redis

# 查看日志
docker-compose logs -f backend

# 重建镜像
docker-compose build --no-cache backend
```

### 测试运行

```bash
# 运行特定测试
python -m pytest tests/test_analysis.py -v

# 运行测试目录
python -m pytest tests/integration/ -v

# 带覆盖率测试
python -m pytest --cov=app tests/

# 运行单个测试文件
python tests/test_akshare_direct.py
```

## 配置管理

### 环境变量配置

项目使用 `.env` 文件管理配置，主要配置项包括：

```bash
# 必需配置
MONGODB_HOST=localhost
MONGODB_PORT=27017
MONGODB_USERNAME=admin
MONGODB_PASSWORD=tradingagents123
MONGODB_DATABASE=tradingagents

REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_PASSWORD=tradingagents123

JWT_SECRET=your-secret-key
CSRF_SECRET=your-csrf-secret

# LLM API 密钥（至少配置一个）
DEEPSEEK_API_KEY=your_key
DASHSCOPE_API_KEY=your_key
OPENAI_API_KEY=your_key

# 数据源配置
DEFAULT_CHINA_DATA_SOURCE=akshare  # 可选: akshare, tushare, baostock
TUSHARE_TOKEN=your_token
```

详细配置参考 `.env.example` 文件。

### 配置加载机制

1. **Pydantic Settings**: `app/core/config.py` 定义所有配置项
2. **环境变量优先**: `.env` 文件中的配置会覆盖默认值
3. **Docker 环境**: `docker-compose.yml` 中定义容器专用配置

## 数据流和架构

### 多源数据架构

支持三种中国股票数据源，自动降级：

1. **Tushare** - 专业 A 股数据（需要 Token）
2. **AKShare** - 免费数据源（默认推荐）
3. **BaoStock** - 备用免费数据源

### 数据同步机制

- **定时任务**: 使用 APScheduler 执行定时同步
- **按需获取**: 港股/美股数据采用按需获取+缓存模式
- **多级缓存**: 支持 Redis / MongoDB / 文件缓存

### 分析流程

```
用户请求 → FastAPI → 股票数据服务 → 数据源适配器
                                          ↓
分析服务 → LangGraph 状态机 → 各分析师智能体
                                          ↓
                    研究员(Bull/Bear) 辩论 → 风险管理器 → 交易决策
```

## 智能体系统

### 分析师智能体

| 智能体 | 文件路径 | 职责 |
|--------|----------|------|
| Market Analyst | `china_market_analyst.py` | 技术分析、技术指标计算 |
| Fundamentals Analyst | `fundamentals_analyst.py` | 基本面分析、财务数据 |
| News Analyst | `news_analyst.py` | 新闻情绪分析 |
| Social Media Analyst | `social_media_analyst.py` | 社交媒体情绪分析 |

### 管理智能体

| 智能体 | 文件路径 | 职责 |
|--------|----------|------|
| Research Manager | `research_manager.py` | 协调各分析师，分配任务 |
| Risk Manager | `risk_manager.py` | 风险评估和决策审核 |

### LLM 提供商支持

- DeepSeek
- 阿里百炼 (DashScope)
- Google Gemini
- OpenAI
- 硅基流动 (SiliconFlow)
- 聚合渠道 (302.AI, OpenRouter, One API)

## 代码风格和规范

### Python 代码风格

- 遵循 PEP 8 规范
- 使用中文注释和文档字符串
- 类型提示: 使用 `typing` 模块添加类型注解
- 日志: 使用 `tradingagents.utils.logging_manager.get_logger()`

### 日志规范

```python
from tradingagents.utils.logging_manager import get_logger

logger = get_logger('module_name')
logger.info("中文日志信息")
logger.error(f"错误信息: {error}")
```

### 错误处理

```python
try:
    # 业务逻辑
    pass
except SpecificException as e:
    logger.error(f"具体操作失败: {e}")
    raise CustomException(f"用户友好的错误信息") from e
```

## 测试策略

### 测试目录结构

```
tests/
├── conftest.py              # pytest 配置和 fixtures
├── integration/             # 集成测试
├── unit/                    # 单元测试
├── test_tushare_unified/    # Tushare 模块测试
└── 0.1.14/                  # 版本特定测试
```

### 测试类型

1. **单元测试**: 测试单个函数和类
2. **集成测试**: 测试模块间交互
3. **API 测试**: 测试 REST API 端点
4. **数据源测试**: 测试各数据源适配器

### 运行测试建议

```bash
# 开发前验证环境
python tests/quick_test.py

# 测试特定数据源
python tests/test_akshare_direct.py

# 测试分析流程
python tests/test_analysis.py
```

## 安全注意事项

### 敏感信息保护

- **API 密钥**: 存储在 `.env` 文件，永不提交到 Git
- **JWT 密钥**: 生产环境使用强随机字符串
- **数据库密码**: 避免使用默认密码

### 生产环境检查清单

- [ ] 修改 `JWT_SECRET` 为随机字符串
- [ ] 修改 `CSRF_SECRET` 为随机字符串
- [ ] 修改 MongoDB/Redis 默认密码
- [ ] 设置 `DEBUG=false`
- [ ] 配置 `ALLOWED_ORIGINS` 限制 CORS
- [ ] 启用 HTTPS

## 常见问题排查

### 数据库连接问题

```bash
# 检查 MongoDB 连接
python tests/test_mongodb_connection.py

# 检查 Redis 连接
python tests/quick_redis_test.py
```

### 数据源问题

```bash
# 检查 AKShare 连接
python tests/test_akshare_direct.py

# 检查 Tushare Token
python tests/test_tushare_direct.py
```

### 模块导入问题

确保项目根目录在 `PYTHONPATH` 中，或使用 `pip install -e .` 安装。

## 许可证说明

本项目采用**混合许可证**模式：

| 目录 | 许可证 | 说明 |
|------|--------|------|
| `tradingagents/` | Apache 2.0 | 开源，可自由使用 |
| `app/` | 专有 | 需要商业授权 |
| `frontend/` | 专有 | 需要商业授权 |

**商业使用请联系**: hsliup@163.com

## 文档资源

- 项目文档: `docs/` 目录
- API 文档: 启动后端后访问 `/docs` (Swagger UI)
- 配置指南: `docs/configuration_guide.md`
- Docker 部署: `docs/DOCKER_DEPLOYMENT.md`

## 开发建议

1. **修改前备份**: 重要修改前先创建备份
2. **小步提交**: 频繁提交小的、可工作的改动
3. **测试先行**: 新功能先写测试，再写实现
4. **日志记录**: 关键操作添加详细日志
5. **中文优先**: 用户界面和文档保持中文
