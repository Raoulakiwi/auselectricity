# 🚂 Railway Deployment Instructions - Ready to Deploy!

Your Australian Electricity Market Dashboard is now **100% ready for Railway deployment**! All configurations have been updated.

## 🎯 What's Been Configured

### ✅ Backend Changes Made:
- **Database**: Now supports both SQLite (local) and PostgreSQL (Railway)
- **CORS**: Configured for Railway URLs (`*.railway.app`)
- **Port handling**: Uses Railway's `PORT` environment variable
- **SSL support**: PostgreSQL connections use SSL
- **Production optimization**: Disabled debug logging in production

### ✅ Frontend Changes Made:
- **API configuration**: Uses `REACT_APP_API_URL` environment variable
- **Build optimization**: Source maps disabled for faster builds
- **Railway-specific build script**: `npm run build:railway`

### ✅ New Files Created:
- `railway.toml` - Railway deployment configuration
- `Procfile` - Process definition for Railway
- `runtime.txt` - Python version specification
- `frontend/src/config/api.js` - API configuration
- Updated `requirements.txt` - Added PostgreSQL support

## 🚀 Deploy in 3 Simple Steps

### Step 1: Push to GitHub
```bash
# Commit all the changes
git add .
git commit -m "Railway deployment ready"
git push origin main
```

### Step 2: Deploy Backend to Railway

1. **Go to [railway.app](https://railway.app)** and sign up (free)
2. **Click "New Project"**
3. **Select "Deploy from GitHub repo"**
4. **Choose your repository** (auselectricity)
5. **Railway auto-detects** your Python app and deploys it!

### Step 3: Add PostgreSQL Database (Recommended)

1. **In your Railway project**, click "New Service"
2. **Select "PostgreSQL"**
3. **Railway automatically connects** it to your app
4. **Your app will restart** and use PostgreSQL

## 🔧 Environment Variables (Auto-configured)

Railway automatically sets these for you:
- `PORT` - Server port (Railway provides this)
- `DATABASE_URL` - PostgreSQL connection (if you add the database)
- `RAILWAY_ENVIRONMENT_NAME` - Production detection

## 📱 Deploy Frontend (Optional Separate Deployment)

### Option A: Same Railway Project
Your backend can serve the React app (current setup works).

### Option B: Separate Frontend Service
1. **Create new Railway project** for frontend
2. **Connect same GitHub repo**
3. **Set root directory** to `frontend`
4. **Add environment variable**: `REACT_APP_API_URL=https://your-backend.railway.app`

## 🎯 After Deployment

### 1. Get Your URLs
Railway will provide URLs like:
- Backend: `https://your-backend-abc123.railway.app`
- API Docs: `https://your-backend-abc123.railway.app/docs`

### 2. Test Your App
```bash
# Test backend health
curl https://your-backend-abc123.railway.app/api/health

# Test API
curl https://your-backend-abc123.railway.app/api/electricity/prices/current
```

### 3. Update Frontend (if separate)
If you deployed frontend separately, update the environment variable:
```env
REACT_APP_API_URL=https://your-backend-abc123.railway.app
```

## 🔍 Troubleshooting

### Build Issues
- **Check Railway logs** in the dashboard
- **Common fix**: Ensure `requirements.txt` is in root directory

### Database Issues
- **PostgreSQL connection**: Make sure PostgreSQL service is added
- **Data initialization**: Your app auto-initializes with sample data

### CORS Issues
- **Frontend can't connect**: Check `REACT_APP_API_URL` is correct
- **API calls fail**: Verify CORS origins include your frontend URL

## 💰 Cost Estimate

With Railway's free tier:
- **$5/month in credits** (free)
- **Your app usage**: ~$2-4/month
- **Your cost**: **$0/month** 🎉

## 🎊 You're Ready!

Your app is now **Railway deployment ready**! The configuration supports:

- ✅ **Both SQLite and PostgreSQL**
- ✅ **Local development and production**
- ✅ **Automatic database initialization**
- ✅ **CORS configured for Railway**
- ✅ **Environment-specific settings**
- ✅ **Production optimizations**

## 🚀 Quick Deploy Command Summary

```bash
# 1. Commit changes
git add . && git commit -m "Railway ready" && git push

# 2. Go to railway.app and deploy from GitHub

# 3. Add PostgreSQL service (optional but recommended)

# 4. Your app is live! 🎉
```

**That's it!** Your Australian Electricity Market Dashboard will be running on Railway with professional hosting, automatic deployments, and a PostgreSQL database.

The entire process should take less than 10 minutes! 🚀
