# MediDrishti AI - Deployment Guide

Complete guide for deploying MediDrishti AI to various platforms.

## Table of Contents

1. [Local Deployment](#local-deployment)
2. [Streamlit Cloud](#streamlit-cloud)
3. [Docker Deployment](#docker-deployment)
4. [Cloud Platforms](#cloud-platforms)
5. [Production Checklist](#production-checklist)

---

## Local Deployment

### Prerequisites
- Python 3.8+
- pip or conda
- Git (optional)

### Step-by-Step

1. **Clone or Download the Project**
   ```bash
   cd MediDrishtiAI
   ```

2. **Create Virtual Environment**
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate
   
   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment**
   ```bash
   cp .env.example .env
   # Edit .env and add your GOOGLE_API_KEY
   ```

5. **Run Application**
   ```bash
   streamlit run app.py
   ```

6. **Access Application**
   - Open browser to: http://localhost:8501

### Troubleshooting Local Deployment

**Port Already in Use**
```bash
streamlit run app.py --server.port 8502
```

**Memory Issues with Large PDFs**
- Increase system RAM or optimize PDF processing
- Use `--logger.level=debug` for troubleshooting

**EasyOCR Installation Issues**
- On some systems, it requires additional dependencies
- Alternative: Skip EasyOCR and use PDFPlumber only

---

## Streamlit Cloud

### Prerequisites
- GitHub account
- Streamlit account
- Project pushed to GitHub

### Step-by-Step

1. **Push to GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial commit: MediDrishti AI"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/MediDrishtiAI.git
   git push -u origin main
   ```

2. **Create Streamlit Account**
   - Visit https://streamlit.io/cloud
   - Sign in with GitHub

3. **Deploy Application**
   - Click "New app"
   - Select your GitHub repository
   - Choose branch (main)
   - Set main file path: `app.py`
   - Click "Deploy"

4. **Configure Secrets**
   - Go to app settings
   - Click "Secrets"
   - Add environment variable:
     ```
     GOOGLE_API_KEY = your_api_key_here
     ```

5. **Access Application**
   - URL will be: `https://your-username-medidristi-ai.streamlit.app`

### Managing Streamlit Cloud Deployment

**Update Application**
- Push changes to GitHub
- Streamlit automatically redeploys

**View Logs**
- Click "Manage App" → "View logs"

**Restart App**
- Settings → "Reboot app"

**Custom Domain** (Streamlit Pro)
- Add custom domain in settings
- Update DNS records

---

## Docker Deployment

### Prerequisites
- Docker installed
- Docker Hub account (optional)

### Create Dockerfile

Create `Dockerfile` in project root:

```dockerfile
FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Copy files
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Set environment variables
ENV GOOGLE_API_KEY=your_key_here
ENV STREAMLIT_SERVER_PORT=8501
ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0

# Run app
CMD ["streamlit", "run", "app.py"]
```

### Build and Run Locally

```bash
# Build image
docker build -t medidristi-ai:latest .

# Run container
docker run -p 8501:8501 \
  -e GOOGLE_API_KEY=your_api_key \
  medidristi-ai:latest
```

Access at: http://localhost:8501

### Push to Docker Hub

```bash
# Tag image
docker tag medidristi-ai:latest YOUR_USERNAME/medidristi-ai:latest

# Login to Docker Hub
docker login

# Push image
docker push YOUR_USERNAME/medidristi-ai:latest
```

---

## Cloud Platforms

### AWS EC2

1. **Launch EC2 Instance**
   - AMI: Ubuntu 20.04 LTS
   - Instance type: t2.micro (free tier)

2. **SSH into Instance**
   ```bash
   ssh -i key.pem ubuntu@your-ec2-public-ip
   ```

3. **Install Dependencies**
   ```bash
   sudo apt-get update
   sudo apt-get install -y python3-pip python3-venv
   ```

4. **Clone Project**
   ```bash
   git clone https://github.com/YOUR_USERNAME/MediDrishtiAI.git
   cd MediDrishtiAI
   ```

5. **Setup Environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

6. **Configure**
   ```bash
   cp .env.example .env
   # Add GOOGLE_API_KEY to .env
   ```

7. **Run with Systemd**
   
   Create `/etc/systemd/system/medidristi.service`:
   ```ini
   [Unit]
   Description=MediDrishti AI
   After=network.target
   
   [Service]
   Type=simple
   User=ubuntu
   WorkingDirectory=/home/ubuntu/MediDrishtiAI
   Environment="PATH=/home/ubuntu/MediDrishtiAI/venv/bin"
   EnvironmentFile=/home/ubuntu/MediDrishtiAI/.env
   ExecStart=/home/ubuntu/MediDrishtiAI/venv/bin/streamlit run app.py \
     --server.port 8501 \
     --server.address 0.0.0.0
   Restart=always
   
   [Install]
   WantedBy=multi-user.target
   ```

   Enable and start:
   ```bash
   sudo systemctl enable medidristi
   sudo systemctl start medidristi
   ```

8. **Configure Nginx Reverse Proxy**
   ```bash
   sudo apt-get install -y nginx
   ```

   Create `/etc/nginx/sites-available/medidristi`:
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;
       
       location / {
           proxy_pass http://localhost:8501;
           proxy_http_version 1.1;
           proxy_set_header Upgrade $http_upgrade;
           proxy_set_header Connection "upgrade";
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
           proxy_set_header X-Forwarded-Proto $scheme;
       }
   }
   ```

   Enable site:
   ```bash
   sudo ln -s /etc/nginx/sites-available/medidristi /etc/nginx/sites-enabled/
   sudo nginx -t
   sudo systemctl restart nginx
   ```

### Google Cloud Platform (GCP)

1. **Create Cloud Run Service**
   ```bash
   gcloud run deploy medidristi-ai \
     --source . \
     --platform managed \
     --region us-central1 \
     --memory 1Gi \
     --set-env-vars GOOGLE_API_KEY=your_key
   ```

2. **Access Application**
   - URL provided after deployment

### Azure Container Instances

1. **Push to Azure Container Registry**
   ```bash
   az acr build --registry YOUR_REGISTRY \
     --image medidristi-ai:latest .
   ```

2. **Deploy Container**
   ```bash
   az container create \
     --resource-group YOUR_RESOURCE_GROUP \
     --name medidristi-ai \
     --image YOUR_REGISTRY.azurecr.io/medidristi-ai:latest \
     --ports 8501 \
     --cpu 1 --memory 1 \
     --environment-variables GOOGLE_API_KEY=your_key
   ```

---

## Production Checklist

### Security
- [ ] Remove hardcoded API keys
- [ ] Use environment variables for all secrets
- [ ] Enable HTTPS (SSL/TLS)
- [ ] Set strong passwords for any admin access
- [ ] Enable file upload validation
- [ ] Implement rate limiting
- [ ] Regular security updates

### Performance
- [ ] Enable caching for frequently used data
- [ ] Optimize PDF processing
- [ ] Monitor memory usage
- [ ] Set appropriate timeout values
- [ ] Use CDN for static assets (if applicable)

### Monitoring & Logging
- [ ] Set up error logging
- [ ] Monitor API rate limits
- [ ] Track application metrics
- [ ] Alert on failures
- [ ] Regular backup of important data

### Testing
- [ ] Run full test suite before deployment
- [ ] Test with various report formats
- [ ] Load testing with multiple concurrent users
- [ ] Test with different LLM responses
- [ ] Verify all pages work correctly

### Documentation
- [ ] Update README with deployment info
- [ ] Document any custom configurations
- [ ] Create troubleshooting guide
- [ ] Maintain API documentation
- [ ] Document environment variables

### Maintenance
- [ ] Plan for regular updates
- [ ] Monitor dependency security
- [ ] Keep Python packages updated
- [ ] Regular performance reviews
- [ ] User feedback collection

---

## Environment Variables Reference

### Required Variables
- `GOOGLE_API_KEY`: Your Google Gemini API key

### Optional Variables
```bash
# Streamlit configuration
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_ADDRESS=0.0.0.0
STREAMLIT_LOGGER_LEVEL=info

# Application configuration
LOG_LEVEL=INFO
MAX_FILE_SIZE_MB=50
```

---

## Troubleshooting Deployment Issues

### Issue: "Module not found" errors
**Solution**: Ensure all dependencies are installed
```bash
pip install -r requirements.txt
```

### Issue: API key not recognized
**Solution**: Verify environment variable is set correctly
```bash
echo $GOOGLE_API_KEY  # Check if set
```

### Issue: Slow performance on Cloud
**Solution**: 
- Increase allocated memory
- Use faster instance type
- Enable caching
- Optimize PDF processing

### Issue: File upload fails in production
**Solution**:
- Check file size limits
- Verify permissions
- Check disk space
- Enable debug logging

---

## Monitoring in Production

### Key Metrics to Monitor
- Application uptime
- Response time
- Error rate
- API rate limit usage
- Memory and CPU usage
- File upload success rate

### Logging Strategy
```python
import logging

logger = logging.getLogger(__name__)
logger.info("Application started")
logger.error("Error processing report", exc_info=True)
```

---

## Support and Updates

- Check Streamlit documentation: https://docs.streamlit.io
- Google Gemini API docs: https://ai.google.dev/
- Docker documentation: https://docs.docker.com/
- AWS documentation: https://docs.aws.amazon.com/

---

**Last Updated**: June 2026
