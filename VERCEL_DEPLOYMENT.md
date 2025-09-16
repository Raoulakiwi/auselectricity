# Vercel Deployment Guide for Australian Electricity Market Dashboard

## Overview

This guide provides instructions for deploying your Australian Electricity Market Dashboard to Vercel. Due to the full-stack nature of your application, we recommend a **hybrid deployment approach**.

## Deployment Architecture

### Recommended: Hybrid Deployment
- **Frontend**: Vercel (React app)
- **Backend**: Railway/Render/DigitalOcean (FastAPI + Database)
- **Database**: External service (PlanetScale, Supabase, or PostgreSQL on Railway)

### Why Hybrid?
Vercel's serverless functions have limitations that make your current backend challenging to deploy:
- No persistent file system (SQLite won't work)
- 10-second execution timeout (your data scrapers need longer)
- Limited memory and CPU for intensive operations

## Prerequisites

1. **Vercel account**: Sign up at [vercel.com](https://vercel.com)
2. **GitHub repository**: Your code should be in a GitHub repo
3. **Backend hosting**: Account with Railway, Render, or similar
4. **Database service**: External database provider

## Step 1: Prepare Your Backend for External Hosting

### Option A: Deploy Backend to Railway

1. **Create Railway account**: Go to [railway.app](https://railway.app)

2. **Create new project from GitHub**:
   ```bash
   # Connect your GitHub repository
   # Railway will auto-detect your Python app
   ```

3. **Add environment variables in Railway dashboard**:
   ```env
   DATABASE_URL=postgresql://user:pass@host:port/dbname
   API_HOST=0.0.0.0
   API_PORT=8000
   PYTHON_VERSION=3.11
   ```

4. **Create `railway.toml`** in your project root:
   ```toml
   [build]
   builder = "NIXPACKS"
   buildCommand = "pip install -r requirements.txt"

   [deploy]
   startCommand = "python start_backend.py"
   restartPolicyType = "ON_FAILURE"
   restartPolicyMaxRetries = 10
   ```

### Option B: Deploy Backend to Render

1. **Create Render account**: Go to [render.com](https://render.com)

2. **Create new Web Service**:
   - Connect GitHub repository
   - Set build command: `pip install -r requirements.txt`
   - Set start command: `python start_backend.py`

3. **Add environment variables**:
   ```env
   DATABASE_URL=postgresql://user:pass@host:port/dbname
   PYTHON_VERSION=3.11
   ```

## Step 2: Set Up External Database

### Option A: Railway PostgreSQL

1. **Add PostgreSQL service** in Railway dashboard
2. **Copy connection string** from Railway
3. **Update your backend configuration**

### Option B: PlanetScale (MySQL)

1. **Create PlanetScale account**: [planetscale.com](https://planetscale.com)
2. **Create database**
3. **Get connection string**
4. **Update SQLAlchemy configuration**:
   ```python
   # In backend/database/database.py
   SQLALCHEMY_DATABASE_URL = "mysql://user:pass@host:port/dbname?ssl_ca=/etc/ssl/certs/ca-certificates.crt"
   ```

### Option C: Supabase (PostgreSQL)

1. **Create Supabase project**: [supabase.com](https://supabase.com)
2. **Get PostgreSQL connection string**
3. **Update configuration**

## Step 3: Update Backend Configuration

### Update CORS settings
```python
# In backend/api/main.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://your-vercel-app.vercel.app",  # Add your Vercel domain
        "https://your-custom-domain.com"       # Add custom domain if you have one
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Update Database Configuration
```python
# In backend/database/database.py
import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Use environment variable for database URL
SQLALCHEMY_DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "sqlite:///./sql_app.db"  # Fallback for local development
)

# Handle PostgreSQL URL format differences
if SQLALCHEMY_DATABASE_URL.startswith("postgres://"):
    SQLALCHEMY_DATABASE_URL = SQLALCHEMY_DATABASE_URL.replace("postgres://", "postgresql://", 1)

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
```

## Step 4: Deploy Backend First

1. **Push changes to GitHub**
2. **Deploy to Railway/Render**
3. **Run database migrations**:
   ```bash
   # SSH into your deployment or use Railway CLI
   python initialize_data.py
   ```
4. **Test backend**: Visit `https://your-backend-url.railway.app/docs`
5. **Note your backend URL** for frontend configuration

## Step 5: Configure Frontend for Vercel

### Update package.json build script
```json
{
  "scripts": {
    "build": "GENERATE_SOURCEMAP=false react-scripts build"
  }
}
```

### Create production environment file
Create `frontend/.env.production`:
```env
REACT_APP_API_URL=https://your-backend-service.railway.app
GENERATE_SOURCEMAP=false
```

### Update API calls (if needed)
Ensure your frontend API calls use the environment variable:
```javascript
// In your frontend API calls
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';
```

## Step 6: Deploy Frontend to Vercel

### Method 1: Vercel Dashboard

1. **Go to Vercel dashboard**: [vercel.com/dashboard](https://vercel.com/dashboard)
2. **Click "New Project"**
3. **Import your GitHub repository**
4. **Configure project**:
   - Framework Preset: `Create React App`
   - Root Directory: `frontend`
   - Build Command: `npm run build`
   - Output Directory: `build`
5. **Add environment variables**:
   ```env
   REACT_APP_API_URL=https://your-backend-service.railway.app
   ```
6. **Deploy**

### Method 2: Vercel CLI

1. **Install Vercel CLI**:
   ```bash
   npm i -g vercel
   ```

2. **Login to Vercel**:
   ```bash
   vercel login
   ```

3. **Deploy from frontend directory**:
   ```bash
   cd frontend
   vercel --prod
   ```

4. **Set environment variables**:
   ```bash
   vercel env add REACT_APP_API_URL production
   # Enter your backend URL when prompted
   ```

## Step 7: Configure Custom Domain (Optional)

1. **In Vercel dashboard**, go to your project
2. **Go to Settings > Domains**
3. **Add your custom domain**
4. **Update DNS records** as instructed by Vercel
5. **Update CORS settings** in your backend to include the new domain

## Step 8: Test Deployment

1. **Visit your Vercel URL**
2. **Check browser console** for any API errors
3. **Test all functionality**:
   - Dashboard loads
   - Data displays correctly
   - API calls work
   - Data collection works (if applicable)

## Troubleshooting

### Common Issues

#### 1. CORS Errors
```
Access to fetch at 'https://backend.railway.app' from origin 'https://app.vercel.app' has been blocked by CORS policy
```
**Solution**: Add your Vercel domain to CORS origins in backend

#### 2. API Not Found (404)
**Solution**: Ensure `REACT_APP_API_URL` is set correctly and backend is deployed

#### 3. Build Failures
**Solution**: Check build logs in Vercel dashboard, ensure all dependencies are in package.json

#### 4. Environment Variables Not Working
**Solution**: Restart deployment after adding environment variables

### Debug Steps

1. **Check Vercel build logs**
2. **Check backend logs** in Railway/Render dashboard
3. **Test backend directly**: Visit `/docs` endpoint
4. **Check browser network tab** for failed requests

## Alternative: Full Vercel Deployment

If you want to deploy everything to Vercel (more complex):

### Requirements
- Rewrite backend as Vercel serverless functions
- Use external database (mandatory)
- Implement cron jobs via Vercel Cron or external service

### Steps
1. **Create `api/` directory** in project root
2. **Convert FastAPI routes** to Vercel functions
3. **Use Vercel Postgres** or external database
4. **Deploy with both frontend and API**

This approach requires significant code restructuring and is not recommended unless you specifically need everything on Vercel.

## Cost Considerations

### Vercel (Frontend only)
- **Hobby plan**: Free for personal projects
- **Pro plan**: $20/month for commercial use

### Railway (Backend + Database)
- **Free tier**: $5/month in credits
- **Paid plans**: Pay-as-you-go, typically $5-20/month

### Total estimated cost: $0-40/month depending on usage

## Maintenance

1. **Monitor both services**: Vercel and Railway dashboards
2. **Update environment variables** when needed
3. **Scale backend** if traffic increases
4. **Regular backups** of database

## Conclusion

The hybrid approach gives you:
- ✅ Fast, global frontend delivery via Vercel
- ✅ Full backend functionality maintained
- ✅ Easier migration from current setup
- ✅ Better performance and reliability

This is the recommended approach for your full-stack application.
