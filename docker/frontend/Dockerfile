# Multi-stage Dockerfile for React Frontend

# ==========================================
# Base Stage - Node.js base
# ==========================================
FROM node:18-alpine as base

WORKDIR /app

# ==========================================
# Dependencies Stage - Install dependencies
# ==========================================
FROM base as dependencies

# Copy package files
COPY package.json package-lock.json ./

# Install all dependencies (including dev dependencies for building)
RUN npm ci

# ==========================================
# Development Stage
# ==========================================
FROM base as development

# Copy node_modules from dependencies stage
COPY --from=dependencies /app/node_modules ./node_modules

# Copy application code
COPY . .

# Expose port
EXPOSE 3000

# Development server with hot reload
CMD ["npm", "start"]

# ==========================================
# Build Stage - Build production bundle
# ==========================================
FROM base as build

# Copy node_modules from dependencies stage
COPY --from=dependencies /app/node_modules ./node_modules

# Copy application code
COPY . .

# Build application
ENV NODE_ENV=production
RUN npm run build

# ==========================================
# Production Stage - Serve with Nginx
# ==========================================
FROM nginx:alpine as production

# Copy built assets from build stage
COPY --from=build /app/build /usr/share/nginx/html

# Copy custom nginx configuration (if needed)
# COPY docker/nginx/frontend.conf /etc/nginx/conf.d/default.conf

# Expose port
EXPOSE 80

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD wget --quiet --tries=1 --spider http://localhost/ || exit 1

# Start nginx
CMD ["nginx", "-g", "daemon off;"]
