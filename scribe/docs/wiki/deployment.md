# SCRIBE Deployment Guide

## 🚀 Deployment Overview

This guide covers all aspects of deploying the SCRIBE Resonance AI System, from development setup to production deployment. SCRIBE supports multiple deployment modes to suit different use cases.

## 📋 Deployment Modes

### 1. Development Mode
- **Purpose**: Local development and testing
- **Features**: Mock audio, debug logging, hot reload
- **Requirements**: Python 3.13+, basic dependencies

### 2. Interactive Mode
- **Purpose**: User interaction and manual operation
- **Features**: Chat interface, real-time feedback
- **Requirements**: Audio hardware (optional), virtual environment

### 3. API Server Mode
- **Purpose**: Programmatic access and integration
- **Features**: REST API, documentation, external integration
- **Requirements**: Network access, web server

### 4. Production Mode
- **Purpose**: Scalable, reliable operation
- **Features**: Monitoring, logging, load balancing
- **Requirements**: Production infrastructure, security

## 🛠️ Quick Deployment

### One-Command Deployment
```bash
# Full deployment with all components
./deploy.sh
```

### Interactive Mode Deployment
```bash
# Start interactive chat interface
./start_interactive.sh
```

### API Server Deployment
```bash
# Start REST API server
./start_api.sh
```

## 🔧 Development Setup

### Prerequisites
- Python 3.13+
- Git
- Virtual environment support
- Audio hardware (optional)

### Step-by-Step Setup

#### 1. Clone Repository
```bash
git clone <repository-url>
cd scribe
```

#### 2. Create Virtual Environment
```bash
python3 -m venv scribe_env
source scribe_env/bin/activate
```

#### 3. Install Dependencies
```bash
# Basic dependencies
pip install numpy scipy

# Audio dependencies (optional)
pip install pyaudio librosa soundfile

# Web dependencies (for API mode)
pip install fastapi uvicorn

# Monitoring dependencies (optional)
pip install prometheus_client

# Development dependencies
pip install pytest black flake8 mypy
```

#### 4. Validate Installation
```bash
python3 validate_system.py
```

#### 5. Start System
```bash
# Interactive mode
python3 main.py

# Or use scripts
./start_interactive.sh
```

## 🏗️ Production Deployment

### System Requirements

#### Minimum Requirements
- **CPU**: 2 cores, 2.0GHz
- **Memory**: 4GB RAM
- **Storage**: 10GB free space
- **OS**: Linux, macOS, or Windows

#### Recommended Requirements
- **CPU**: 4+ cores, 3.0GHz
- **Memory**: 8GB+ RAM
- **Storage**: 50GB+ SSD
- **OS**: Ubuntu 20.04+ or CentOS 8+

#### Production Requirements
- **CPU**: 8+ cores, 3.5GHz
- **Memory**: 16GB+ RAM
- **Storage**: 100GB+ SSD
- **Network**: Gigabit connection
- **OS**: Ubuntu 22.04+ LTS

### Production Setup

#### 1. System Preparation
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install system dependencies
sudo apt install -y python3.13 python3.13-venv python3-pip
sudo apt install -y portaudio19-dev libasound2-dev
sudo apt install -y nginx supervisor
```

#### 2. Create SCRIBE User
```bash
# Create dedicated user
sudo useradd -m -s /bin/bash scribe
sudo usermod -aG audio scribe

# Switch to scribe user
sudo su - scribe
```

#### 3. Deploy Application
```bash
# Clone repository
git clone <repository-url> /opt/scribe
cd /opt/scribe

# Create virtual environment
python3 -m venv scribe_env
source scribe_env/bin/activate

# Install production dependencies
pip install -r requirements.txt
pip install gunicorn

# Configure production settings
cp config.json.example config.json
# Edit config.json for production
```

#### 4. Production Configuration
```json
{
  "system": {
    "production_mode": true,
    "debug_mode": false,
    "log_level": "INFO"
  },
  "audio": {
    "sample_rate": 44100,
    "chunk_size": 1024,
    "use_real_audio": true
  },
  "api": {
    "host": "0.0.0.0",
    "port": 8000,
    "workers": 4
  },
  "monitoring": {
    "prometheus_port": 8001,
    "enable_metrics": true
  },
  "security": {
    "api_key_required": false,
    "rate_limiting": true
  }
}
```

#### 5. Create Systemd Services
```bash
# Create API service
sudo tee /etc/systemd/system/scribe-api.service > /dev/null <<EOF
[Unit]
Description=SCRIBE API Server
After=network.target

[Service]
Type=exec
User=scribe
Group=scribe
WorkingDirectory=/opt/scribe
Environment=PATH=/opt/scribe/scribe_env/bin
ExecStart=/opt/scribe/scribe_env/bin/gunicorn -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000 src.api.main:app
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Create monitoring service
sudo tee /etc/systemd/system/scribe-monitoring.service > /dev/null <<EOF
[Unit]
Description=SCRIBE Monitoring Service
After=scribe-api.service

[Service]
Type=exec
User=scribe
Group=scribe
WorkingDirectory=/opt/scribe
Environment=PATH=/opt/scribe/scribe_env/bin
ExecStart=/opt/scribe/scribe_env/bin/python3 -m monitoring.metrics_server
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Enable and start services
sudo systemctl daemon-reload
sudo systemctl enable scribe-api scribe-monitoring
sudo systemctl start scribe-api scribe-monitoring
```

#### 6. Configure Nginx (Optional)
```bash
# Create Nginx configuration
sudo tee /etc/nginx/sites-available/scribe > /dev/null <<EOF
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }

    location /metrics {
        proxy_pass http://127.0.0.1:8001;
        proxy_set_header Host \$host;
    }
}
EOF

# Enable site
sudo ln -s /etc/nginx/sites-available/scribe /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

## 🐳 Docker Deployment

### Dockerfile
```dockerfile
FROM python:3.13-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    portaudio19-dev \
    libasound2-dev \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Create non-root user
RUN useradd -m -u 1000 scribe
USER scribe

# Expose ports
EXPOSE 8000 8001

# Start application
CMD ["./start_api.sh"]
```

### Docker Compose
```yaml
version: '3.8'

services:
  scribe-api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - SCRIBE_ENV=production
    volumes:
      - ./data:/app/data
      - ./logs:/app/logs
    restart: unless-stopped

  scribe-monitoring:
    build: .
    ports:
      - "8001:8001"
    environment:
      - SCRIBE_ENV=production
    volumes:
      - ./data:/app/data
      - ./logs:/app/logs
    restart: unless-stopped
    command: ["python3", "-m", "monitoring.metrics_server"]

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - scribe-api
    restart: unless-stopped
```

### Docker Commands
```bash
# Build image
docker build -t scribe:latest .

# Run container
docker run -d \
  --name scribe-api \
  -p 8000:8000 \
  -p 8001:8001 \
  -v $(pwd)/data:/app/data \
  scribe:latest

# Use Docker Compose
docker-compose up -d
docker-compose logs -f
```

## ☁️ Cloud Deployment

### AWS Deployment

#### EC2 Instance Setup
```bash
# Launch EC2 instance (Ubuntu 22.04)
# Instance type: t3.medium or larger
# Security Group: Allow ports 80, 443, 8000, 8001

# Connect to instance
ssh -i key.pem ubuntu@instance-ip

# Deploy SCRIBE
git clone <repository-url>
cd scribe
./deploy.sh
```

#### ECS Deployment
```json
{
  "family": "scribe-api",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "512",
  "memory": "1024",
  "executionRoleArn": "arn:aws:iam::account:role/ecsTaskExecutionRole",
  "containerDefinitions": [
    {
      "name": "scribe-api",
      "image": "your-account.dkr.ecr.region.amazonaws.com/scribe:latest",
      "portMappings": [
        {
          "containerPort": 8000,
          "protocol": "tcp"
        }
      ],
      "environment": [
        {
          "name": "SCRIBE_ENV",
          "value": "production"
        }
      ],
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/scribe",
          "awslogs-region": "us-west-2",
          "awslogs-stream-prefix": "ecs"
        }
      }
    }
  ]
}
```

### Google Cloud Platform

#### Cloud Run Deployment
```bash
# Build and push image
gcloud builds submit --tag gcr.io/project-id/scribe

# Deploy to Cloud Run
gcloud run deploy scribe-api \
  --image gcr.io/project-id/scribe \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --port 8000
```

### Azure Deployment

#### Container Instances
```bash
# Create resource group
az group create --name scribe-rg --location eastus

# Deploy container
az container create \
  --resource-group scribe-rg \
  --name scribe-api \
  --image your-registry/scribe:latest \
  --dns-name-label scribe-api \
  --ports 8000 8001
```

## 🔒 Security Configuration

### Basic Security
```json
{
  "security": {
    "api_key_required": true,
    "api_key": "your-secret-key",
    "rate_limiting": true,
    "max_requests_per_minute": 100,
    "cors_origins": ["https://your-domain.com"],
    "ssl_required": true
  }
}
```

### SSL/TLS Setup
```bash
# Generate SSL certificate (Let's Encrypt)
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com

# Auto-renewal
sudo crontab -e
# Add: 0 12 * * * /usr/bin/certbot renew --quiet
```

### Firewall Configuration
```bash
# Configure UFW
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw allow 8000/tcp
sudo ufw allow 8001/tcp
sudo ufw enable
```

## 📊 Monitoring and Logging

### Log Configuration
```json
{
  "logging": {
    "level": "INFO",
    "file": "/var/log/scribe/scribe.log",
    "max_size": "100MB",
    "backup_count": 5,
    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
  }
}
```

### Monitoring Setup
```bash
# Install Prometheus
wget https://github.com/prometheus/prometheus/releases/download/v2.40.0/prometheus-2.40.0.linux-amd64.tar.gz
tar xvf prometheus-2.40.0.linux-amd64.tar.gz

# Configure Prometheus
tee prometheus.yml > /dev/null <<EOF
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'scribe'
    static_configs:
      - targets: ['localhost:8001']
EOF

# Start Prometheus
./prometheus --config.file=prometheus.yml
```

### Health Checks
```bash
# Create health check script
#!/bin/bash
# health_check.sh

API_URL="http://localhost:8000/health"
RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" $API_URL)

if [ $RESPONSE -eq 200 ]; then
    echo "SCRIBE API is healthy"
    exit 0
else
    echo "SCRIBE API is unhealthy (HTTP $RESPONSE)"
    exit 1
fi
```

## 🔄 Backup and Recovery

### Database Backup
```bash
# Create backup script
#!/bin/bash
# backup.sh

BACKUP_DIR="/opt/backups/scribe"
DATE=$(date +%Y%m%d_%H%M%S)

mkdir -p $BACKUP_DIR

# Backup database
cp scribe_learning.db $BACKUP_DIR/scribe_learning_$DATE.db

# Backup configuration
cp config.json $BACKUP_DIR/config_$DATE.json

# Backup logs
tar -czf $BACKUP_DIR/logs_$DATE.tar.gz logs/

# Clean old backups (keep 7 days)
find $BACKUP_DIR -name "*.db" -mtime +7 -delete
find $BACKUP_DIR -name "*.json" -mtime +7 -delete
find $BACKUP_DIR -name "*.tar.gz" -mtime +7 -delete
```

### Recovery Procedure
```bash
# Restore from backup
#!/bin/bash
# restore.sh

BACKUP_FILE=$1

if [ -z "$BACKUP_FILE" ]; then
    echo "Usage: $0 <backup_file>"
    exit 1
fi

# Stop services
sudo systemctl stop scribe-api scribe-monitoring

# Restore database
cp $BACKUP_FILE scribe_learning.db

# Restart services
sudo systemctl start scribe-api scribe-monitoring
```

## 🚀 Performance Optimization

### System Tuning
```bash
# Optimize system limits
echo "* soft nofile 65536" >> /etc/security/limits.conf
echo "* hard nofile 65536" >> /etc/security/limits.conf

# Optimize kernel parameters
echo "net.core.somaxconn = 65536" >> /etc/sysctl.conf
echo "net.ipv4.tcp_max_syn_backlog = 65536" >> /etc/sysctl.conf
sysctl -p
```

### Application Tuning
```json
{
  "performance": {
    "worker_processes": 4,
    "worker_connections": 1000,
    "keepalive_timeout": 65,
    "max_concurrent_scans": 10,
    "cache_size": "256MB"
  }
}
```

## 📈 Scaling Strategies

### Horizontal Scaling
```bash
# Load balancer configuration
upstream scribe_api {
    server 127.0.0.1:8000;
    server 127.0.0.1:8001;
    server 127.0.0.1:8002;
}

server {
    listen 80;
    location / {
        proxy_pass http://scribe_api;
    }
}
```

### Vertical Scaling
```bash
# Increase resources
# Edit systemd service
ExecStart=/opt/scribe/scribe_env/bin/gunicorn -w 8 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000 src.api.main:app
```

## 🔧 Maintenance

### Regular Maintenance Tasks
```bash
# Create maintenance script
#!/bin/bash
# maintenance.sh

# Update dependencies
source scribe_env/bin/activate
pip install --upgrade pip
pip install --upgrade -r requirements.txt

# Clean logs
find logs/ -name "*.log" -mtime +30 -delete

# Validate system
python3 validate_system.py

# Restart services
sudo systemctl restart scribe-api scribe-monitoring
```

### Automated Maintenance
```bash
# Add to crontab
0 2 * * * /opt/scribe/maintenance.sh
0 3 * * 0 /opt/scribe/backup.sh
*/5 * * * * /opt/scribe/health_check.sh
```

## 📞 Support and Monitoring

### Monitoring Dashboard
- **Prometheus**: Metrics collection
- **Grafana**: Visualization dashboard
- **Alertmanager**: Alert management

### Support Channels
- **Email**: support@scribe.ai
- **Slack**: #scribe-support
- **Documentation**: This wiki
- **GitHub Issues**: Bug reports and features

---

**Last Updated**: 2026-05-06  
**Deployment Guide Version**: 1.0.0  
**Status**: Production Ready
