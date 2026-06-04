FROM node:22-slim

WORKDIR /app

# Install pnpm
RUN npm install -g pnpm

# Copy package files
COPY package.json pnpm-lock.yaml ./

# Install all dependencies including optional native bindings for linux-x64
RUN pnpm install --no-frozen-lockfile

# Copy the rest of the application
COPY . .

# Expose port
EXPOSE 5173

# Start dev server (re-install if node_modules was overridden by a volume mount)
CMD ["pnpm", "run", "dev", "--", "--host"]
