# KrushiAI Disease Recognition System - Deployment Guide

This guide will help you deploy the Disease Recognition System to work like the Crop Recommendation System.

## Architecture Overview

- **Frontend**: Static HTML/CSS/JS deployed on Netlify
- **Backend**: Python Flask API deployed on Render
- **Connection**: Netlify proxies API requests to Render backend via `netlify.toml`

## Backend Deployment (Render)

### Prerequisites
1. Create an account on [Render](https://render.com)
2. Connect your GitHub repository

### Steps

1. **Push your code to GitHub** (if not already done)
   ```bash
   cd KrushiAI-Disease-Recognition-System
   git add .
   git commit -m "Add deployment configuration"
   git push origin main
   ```

2. **Create a new Web Service on Render**
   - Go to https://dashboard.render.com/
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Select the repository: `KrushiAI-Disease-Recognition-System`

3. **Configure the service** (Render will auto-detect `render.yaml`, but verify):
   - **Name**: `ai-disease-backend` (or your preferred name)
   - **Environment**: Python 3
   - **Root Directory**: `backend`
   - **Build Command**: `pip install --upgrade pip setuptools wheel && pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app --preload --workers 2 --threads 4 --timeout 120 --bind 0.0.0.0:$PORT`
   - **Plan**: Free

4. **Add Environment Variables** (if needed):
   - `PYTHON_VERSION`: `3.11.9`

5. **Deploy**
   - Click "Create Web Service"
   - Wait for the build to complete (5-10 minutes)
   - Note your backend URL (e.g., `https://ai-disease-backend.onrender.com`)

6. **Important: Upload Model File**
   - The backend expects a trained model at `backend/model/model.joblib`
   - You need to either:
     - Commit the model file to your repository (if < 100MB)
     - Upload it via Render Dashboard after deployment
     - Train a model using `backend/train.py` and upload

## Frontend Deployment (Netlify)

### Prerequisites
1. Create an account on [Netlify](https://www.netlify.com)

### Steps

1. **Update the API URL in `netlify.toml`**
   - Open `frontend/netlify.toml`
   - Replace the backend URLs with your actual Render backend URL:
   ```toml
   [[redirects]]
   from = "/predict-image"
   to = "https://YOUR-BACKEND-URL.onrender.com/predict-image"
   status = 200
   force = true
   ```

2. **Deploy to Netlify**

   **Option A: Drag & Drop (Easiest)**
   - Go to https://app.netlify.com/drop
   - Drag the entire `frontend` folder
   - Netlify will deploy your site and provide a URL

   **Option B: Git Integration**
   - Go to https://app.netlify.com/
   - Click "Add new site" → "Import an existing project"
   - Connect your GitHub repository
   - Configure:
     - **Base directory**: `frontend` (or leave empty and set Publish directory)
     - **Build command**: (leave empty)
     - **Publish directory**: `frontend` (if base directory is empty)
   - Click "Deploy site"

3. **Configure Site Settings**
   - Go to Site settings → Build & deploy
   - Verify the Publish directory is set correctly
   - Netlify will automatically use `netlify.toml` for redirects

4. **Test Your Deployment**
   - Visit your Netlify URL (e.g., `https://your-site-name.netlify.app`)
   - Upload a plant leaf image
   - Click "Predict"
   - You should see disease recognition results!

## Verification Checklist

✅ **Backend (Render)**
- [ ] Service is running and shows "Live"
- [ ] Health check endpoint works: `https://YOUR-BACKEND-URL.onrender.com/` returns JSON
- [ ] Model is loaded (check health endpoint response: `"model_loaded": true`)

✅ **Frontend (Netlify)**
- [ ] Site is accessible via Netlify URL
- [ ] Page loads with proper styling
- [ ] File upload button works
- [ ] Form submission triggers prediction
- [ ] Results are displayed properly

✅ **Integration**
- [ ] Frontend can communicate with backend (check browser console for errors)
- [ ] API requests are proxied correctly (no CORS errors)
- [ ] Predictions work end-to-end

## Troubleshooting

### Backend Issues

**Problem**: "Model not loaded" error
- **Solution**: Upload `model.joblib` to `backend/model/` directory and redeploy

**Problem**: Build fails on Render
- **Solution**: Check `requirements.txt` has all dependencies
- **Solution**: Verify Python version in `render.yaml` matches your local version

**Problem**: Backend times out
- **Solution**: Increase timeout in start command (already set to 120s)
- **Solution**: Render free tier may sleep after inactivity - first request wakes it up

### Frontend Issues

**Problem**: Page loads but API calls fail
- **Solution**: Check `netlify.toml` has correct backend URL
- **Solution**: Verify backend is running on Render
- **Solution**: Check browser console for CORS errors

**Problem**: "Backend unreachable" error
- **Solution**: Verify the backend URL in `netlify.toml`
- **Solution**: Test backend directly: `curl https://YOUR-BACKEND-URL.onrender.com/`

**Problem**: Styling is broken
- **Solution**: Ensure all CSS files are in the `frontend` directory
- **Solution**: Check relative paths in HTML

## File Structure

```
KrushiAI-Disease-Recognition-System/
├── backend/
│   ├── app.py                 # Flask API
│   ├── model.py              # Model loading/prediction logic
│   ├── requirements.txt      # Python dependencies
│   ├── Procfile             # Alternative deployment config
│   └── model/
│       └── model.joblib     # Trained ML model (required!)
├── frontend/
│   ├── index.html           # Main HTML page
│   ├── script.js           # Frontend JavaScript
│   ├── styles.css          # Page styles
│   ├── config.js           # API configuration
│   └── netlify.toml        # Netlify proxy configuration
├── render.yaml             # Render deployment config
└── DEPLOYMENT_GUIDE.md     # This file
```

## Custom Domain (Optional)

1. **Netlify**: Site settings → Domain management → Add custom domain
2. **Render**: Settings → Custom Domain → Add domain

## Updates

To update your deployment after making changes:

1. **Backend**: 
   - Push changes to GitHub
   - Render will auto-deploy (if auto-deploy is enabled)

2. **Frontend**:
   - Push changes to GitHub (if using Git integration)
   - Or drag & drop the updated `frontend` folder to Netlify

## Support

- Check the browser console for frontend errors (F12 → Console)
- Check Render logs for backend errors (Dashboard → Service → Logs)
- Verify API endpoints using curl or Postman

---

**Made by Team KrushiAI** 🌾
