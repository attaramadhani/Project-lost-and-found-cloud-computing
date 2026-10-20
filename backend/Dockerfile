# Base image ringan berbasis alpine
FROM node:20-alpine

# Set direktori kerja
WORKDIR /app

# Copy dependencies
COPY package*.json ./

# Install dependensi produksi
RUN npm ci --only=production

# Copy seluruh source code
COPY . .

# Expose port aplikasi
EXPOSE 5000

# Jalankan server
CMD ["node", "server.js"]
