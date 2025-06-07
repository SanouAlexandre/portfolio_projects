# Use official Node.js LTS image
FROM node:18-alpine AS builder

# Set working directory
WORKDIR /app

# Install dependencies
COPY package.json package-lock.json ./
RUN npm ci

# Copy the entire app
COPY . .

# Build the Next.js app
RUN npm run build

# --- Production image ---
FROM node:18-alpine AS runner

# Set working directory
WORKDIR /app

# Install only production dependencies
COPY --from=builder /app/package.json /app/package-lock.json ./
RUN npm ci --omit=dev

# Copy built app and static files
COPY --from=builder /app/.next .next
COPY --from=builder /app/public public
COPY --from=builder /app/next.config.js .
COPY --from=builder /app/node_modules node_modules
COPY --from=builder /app/package.json .

# Copy env file if needed (alternative: use --env or --env-file)
COPY .env.local .env.local

# Expose default Next.js port
EXPOSE 3000

# Start app in production mode
CMD ["npm", "start"]
