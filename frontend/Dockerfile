# Use Node.js 18 as base image
FROM node:18

# Set the working directory
WORKDIR /app

# Copy frontend files
COPY . .

# Install dependencies and build the frontend
RUN npm install
RUN npm run build

# Expose the port
EXPOSE 4173

# Start the frontend
CMD ["npm", "run", "preview"]
