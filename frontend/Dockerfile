# 构建阶段
FROM node:20-alpine AS builder

WORKDIR /app
COPY package*.json yarn.lock ./
RUN yarn install --frozen-lockfile

COPY . .
RUN yarn build

# 运行阶段 - 使用 Nginx
FROM nginx:alpine

# 复制构建输出
COPY --from=builder /app/dist /usr/share/nginx/html

# 创建 Nginx 配置
RUN echo 'server { \
    listen $PORT; \
    root /usr/share/nginx/html; \
    index index.html; \
    location / { \
        try_files $uri $uri/ /index.html; \
    } \
    location /api/ { \
        proxy_pass https://backend-service-production-14ef.up.railway.app/api/; \
        proxy_http_version 1.1; \
        proxy_set_header Host $host; \
        proxy_set_header X-Real-IP $remote_addr; \
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for; \
        proxy_set_header X-Forwarded-Proto $scheme; \
        add_header Access-Control-Allow-Origin * always; \
        add_header Access-Control-Allow-Methods "GET, POST, PUT, DELETE, OPTIONS" always; \
        add_header Access-Control-Allow-Headers "*" always; \
    } \
}' > /etc/nginx/conf.d/default.conf.template

# 使用 envsubst 替换 $PORT 并启动 Nginx
CMD ["/bin/sh", "-c", "envsubst '\$PORT' < /etc/nginx/conf.d/default.conf.template > /etc/nginx/conf.d/default.conf && nginx -g 'daemon off;'"]
