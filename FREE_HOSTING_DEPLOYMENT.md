# FREE Hosting Deployment Guide - Australian Electricity Market Dashboard

## 🏆 Recommended: Railway (100% FREE)

Railway is the **best free option** for your full-stack application. Here's why and how to deploy:

### Why Railway?
- ✅ **$5/month in free credits** (covers small apps completely)
- ✅ **PostgreSQL database included** (or keep SQLite)
- ✅ **No sleep/timeout issues** (unlike Render)
- ✅ **Supports background tasks** (your data scrapers work!)
- ✅ **Both frontend + backend hosting**
- ✅ **Automatic deployments** from GitHub
- ✅ **Custom domains** supported

## Step-by-Step Railway Deployment

### Prerequisites
1. GitHub account with your code
2. Railway account (free): [railway.app](https://railway.app)

### Step 1: Prepare Your Code

1. **Add Railway configuration** to your project root:

```toml
# railway.toml
[build]
builder = "NIXPACKS"

[deploy]
startCommand = "python start_backend.py"
restartPolicyType = "ON_FAILURE"
restartPolicyMaxRetries = 10

[[services]]
name = "backend"
source = "."
```

2. **Update your requirements.txt** (if needed):
```txt
fastapi==0.104.1
uvicorn==0.24.0
pandas==2.1.3
numpy==1.25.2
requests==2.31.0
sqlalchemy==2.0.23
plotly==5.17.0
dash==2.14.2
dash-bootstrap-components==1.5.0
python-dotenv==1.0.0
schedule==1.2.0
beautifulsoup4==4.12.2
lxml==4.9.3
scikit-learn==1.3.2
matplotlib==3.8.2
seaborn==0.13.0
psycopg2-binary==2.9.7  # Add this for PostgreSQL support
```

### Step 2: Deploy Backend to Railway

1. **Go to [railway.app](https://railway.app)** and sign up
2. **Click "New Project"**
3. **Select "Deploy from GitHub repo"**
4. **Choose your repository**
5. **Railway will auto-detect** your Python app

### Step 3: Add Database (Optional but Recommended)

1. **In your Railway project**, click "New Service"
2. **Select "PostgreSQL"**
3. **Railway will create a database** and provide connection details

### Step 4: Configure Environment Variables

In Railway dashboard, add these variables:

```env
# Database (if using PostgreSQL)
DATABASE_URL=${{Postgres.DATABASE_URL}}

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
PYTHON_VERSION=3.11

# CORS Origins (Railway provides a URL like: https://your-app.railway.app)
FRONTEND_URL=https://your-frontend.railway.app
```

### Step 5: Update Your Backend Code

**Option A: Keep SQLite (Simpler)**
Your current setup will work as-is on Railway.

**Option B: Upgrade to PostgreSQL (Recommended)**

Update `backend/database/database.py`:
```python
import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Get database URL from environment
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./sql_app.db")

# Handle Railway's PostgreSQL URL format
if SQLALCHEMY_DATABASE_URL.startswith("postgres://"):
    SQLALCHEMY_DATABASE_URL = SQLALCHEMY_DATABASE_URL.replace("postgres://", "postgresql://", 1)

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
```

### Step 6: Deploy Frontend

**Option A: Same Railway Project**
1. **Create new service** in same project
2. **Set root directory** to `frontend`
3. **Railway auto-detects** React app

**Option B: Separate Deployment (Recommended)**
1. **Create new Railway project** for frontend
2. **Connect same GitHub repo**
3. **Set root directory** to `frontend`
4. **Set build command**: `npm run build`
5. **Set start command**: `npm start`

### Step 7: Configure CORS

Update your backend `main.py`:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://your-frontend.railway.app",  # Your Railway frontend URL
        "https://your-custom-domain.com"      # If you add a custom domain
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Step 8: Update Frontend API URL

In your React app, update API calls to use Railway backend URL:
```javascript
// In your frontend API configuration
const API_BASE_URL = process.env.REACT_APP_API_URL || 'https://your-backend.railway.app';
```

Add to `frontend/.env.production`:
```env
REACT_APP_API_URL=https://your-backend.railway.app
```

### Step 9: Initialize Database

1. **In Railway dashboard**, open your backend service
2. **Go to "Deployments"** tab
3. **Click on latest deployment**
4. **Open "View Logs"**
5. **Your app should auto-initialize** the database on first run

If you need to manually initialize:
1. **Connect to Railway shell**: Use Railway CLI
2. **Run**: `railway run python initialize_data.py`

## Alternative: Render (Also FREE)

If Railway doesn't work for you, Render is the second-best option:

### Render Free Tier
- ✅ **Web services** (backend)
- ✅ **PostgreSQL database** (750 hours/month)
- ✅ **Static sites** (frontend)
- ⚠️ **Services sleep** after 15 minutes inactivity
- ⚠️ **750 hours/month limit**

### Quick Render Setup
1. **Go to [render.com](https://render.com)**
2. **Create Web Service** from your GitHub repo
3. **Add PostgreSQL database**
4. **Create Static Site** for frontend (from `frontend` folder)

## Cost Comparison

| Platform | Backend | Database | Frontend | Monthly Cost |
|----------|---------|----------|----------|--------------|
| **Railway** | ✅ Free | ✅ Free | ✅ Free | **$0** |
| **Render** | ✅ Free* | ✅ Free* | ✅ Free | **$0** |
| **Vercel + Railway** | $5-10 | $5-10 | ✅ Free | **$10-20** |

*Limited hours/month

## Testing Your Deployment

1. **Backend health check**:
   ```bash
   curl https://your-backend.railway.app/api/health
   ```

2. **Frontend access**:
   - Visit: `https://your-frontend.railway.app`
   - Check browser console for errors
   - Test data collection functionality

3. **Database verification**:
   - Check if data loads in dashboard
   - Test data collection triggers

## Troubleshooting

### Common Issues

#### 1. Build Failures
```bash
# Check Railway logs in dashboard
# Common fix: ensure all dependencies in requirements.txt
```

#### 2. Database Connection Errors
```python
# Verify DATABASE_URL environment variable
# Check PostgreSQL service is running
```

#### 3. CORS Errors
```python
# Add your Railway URLs to CORS origins
# Redeploy after CORS changes
```

#### 4. Port Issues
```python
# Railway automatically sets PORT environment variable
# Ensure your app uses: port = int(os.getenv("PORT", 8000))
```

### Getting Help
- **Railway Discord**: Very active community
- **Railway Docs**: Excellent documentation
- **GitHub Issues**: Check your deployment logs

## Monitoring & Maintenance

### Railway Dashboard
- **Monitor resource usage**
- **Check deployment logs**
- **View metrics and uptime**

### Free Tier Limits
- **Railway**: $5/month credits (usually enough)
- **Database storage**: Generous limits
- **Bandwidth**: More than sufficient for most apps

## Scaling Up Later

When you outgrow free tiers:
- **Railway**: Pay-as-you-go pricing (very reasonable)
- **Add custom domain**: $0 on Railway
- **Increase resources**: Easy scaling
- **Add monitoring**: Built-in metrics

## Summary

**Railway is your best bet** for completely free hosting because:

1. ✅ **No major limitations** that affect your app
2. ✅ **Handles your data scrapers** perfectly
3. ✅ **PostgreSQL included** for better performance
4. ✅ **Professional deployment** with custom domains
5. ✅ **Easy to scale** when you need more resources

The deployment process is straightforward, and Railway's interface is user-friendly. Your Australian Electricity Market Dashboard will run smoothly and professionally on their platform.

**Start with Railway - you'll be impressed with how well it handles your full-stack application!**
