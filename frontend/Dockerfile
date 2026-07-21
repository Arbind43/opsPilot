# Stage 1: Development
FROM node:20-alpine AS development
WORKDIR /app
COPY package*.json ./
RUN npm install --legacy-peer-deps
COPY . .
# Start dev server directly in development target
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]

# Stage 2: Build the React application (Production)
FROM development AS build
RUN npm run build

# Stage 3: Serve the application with Nginx (Production)
FROM nginx:alpine AS production
COPY --from=build /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
