# 部署指南：Railway (后端) + Vercel (前端)

## 架构

```
用户 → Vercel (前端) → Railway (后端 API) → MongoDB Atlas + Railway Redis
```

---

## Phase 1: Railway 后端部署

### 1.1 创建 Railway 项目

```bash
# 登录 Railway
railway login

# 初始化项目
cd tradingagents-cn
railway init
# 选择: Empty Project

# 链接到现有项目 (如果需要)
railway link <project-id>
```

### 1.2 配置环境变量

在 Railway Dashboard 中配置以下变量：

| 变量名 | 说明 | 示例值 |
|--------|------|--------|
| `MONGODB_HOST` | MongoDB Atlas 连接串 | `mongodb+srv://xxx:xxx@cluster0.xxx.mongodb.net` |
| `MONGODB_PORT` | MongoDB 端口 | `27017` |
| `MONGODB_DATABASE` | 数据库名 | `tradingagents` |
| `MONGODB_AUTH_SOURCE` | 认证数据库 | `admin` |
| `REDIS_HOST` | Railway Redis Host | 从 Railway Redis 服务获取 |
| `REDIS_PORT` | Redis 端口 | `6379` |
| `REDIS_PASSWORD` | Redis 密码 | 从 Railway Redis 服务获取 |
| `JWT_SECRET` | JWT 密钥 (**必须修改**) | `your-random-secret-here` |
| `CSRF_SECRET` | CSRF 密钥 (**必须修改**) | `your-random-secret-here` |
| `DEBUG` | 调试模式 | `false` |
| `DEEPSEEK_API_KEY` | DeepSeek API 密钥 | `sk-xxx` |
| `DASHSCOPE_API_KEY` | 阿里百炼 API 密钥 | `sk-xxx` |

### 1.3 部署

```bash
# 方式一: 使用 Railway CLI
railway up

# 方式二: Git 部署
# 在 GitHub 上创建空仓库，push 代码，Railway 会自动检测 Dockerfile.backend
```

### 1.4 验证后端

部署成功后访问: `https://xxx.railway.app/api/health`

---

## Phase 2: Vercel 前端部署

### 2.1 创建 Vercel 项目

```bash
cd frontend
vercel
# 按提示操作:
# - Set up: Import Project
# - Framework: Vite
# - Root Directory: ./
# - Build Command: yarn build
# - Output Directory: dist
```

### 2.2 配置环境变量

在 Vercel Dashboard 中配置：

| 变量名 | 值 |
|--------|-----|
| `VITE_API_BASE_URL` | `https://你的Railway项目ID.railway.app/api` |

注意: Railway 部署后会在项目设置中显示 URL，例如: `https://tradingagents-prod.up.railway.app`

### 2.3 部署

```bash
# 开发环境预览
vercel

# 生产环境部署
vercel --prod
```

---

## Phase 3: 验证

1. 访问 Vercel 提供的 URL
2. 首次使用需要注册账号
3. 配置至少一个 LLM API (推荐 DeepSeek)
4. 同步股票数据
5. 测试股票分析功能

---

## 常见问题

### Q: MongoDB 如何获取连接串?
1. 注册 [MongoDB Atlas](https://www.mongodb.com/atlas/database)
2. 创建免费集群 (M0 Sandbox)
3. 在 Connect 页面选择 "Connect your application"
4. 复制连接串，格式: `mongodb+srv://<username>:<password>@cluster0.xxx.mongodb.net/<dbname>?retryWrites=true&w=majority`

### Q: Redis 如何配置?
1. 在 Railway 项目中添加 Redis 服务
2. 在 Redis 服务页面找到 Connection URL
3. 解析 URL 得到 HOST, PORT, PASSWORD

### Q: 如何更新后端代码?
```bash
cd tradingagents-cn
railway up
```

### Q: 前端如何更新?
```bash
cd frontend
vercel --prod
```

### Q: 自定义域名如何配置?
- Vercel: 在项目 Settings → Domains 添加域名
- Railway: 在项目 Settings → Networking 添加自定义域名

---

## 数据源配置 (可选)

如果需要 A 股数据，在 Railway 环境变量中添加:

```bash
TUSHARE_TOKEN=你的tushare_token
TUSHARE_ENABLED=true
FINNHUB_API_KEY=你的finnhub_key  # 美股数据
```
