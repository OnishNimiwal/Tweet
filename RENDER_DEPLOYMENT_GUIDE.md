# Deploying Django Project on Render

## Why Render?
- Free tier available
- Built-in PostgreSQL database
- Automatic deployments from GitHub
- Easy environment variables
- Great for Django projects

---

## Step-by-Step Deployment Guide

### **Step 1: Create Render Account**

1. Go to [render.com](https://render.com)
2. Click **"Sign Up"**
3. Sign up with GitHub (recommended)
4. Authorize Render to access your repositories

---

### **Step 2: Create PostgreSQL Database**

1. From Render dashboard, click **"New"** → **"PostgreSQL"**
2. Name: `tweet-db`
3. Database: `tweetdb` (or leave as default)
4. Region: Choose closest to your users
5. Version: Leave as default
6. Plan: Free tier
7. Click **"Create Database"**

**Wait for the database to be created!** (2-3 minutes)

After creation, you'll see:
```
External Database URL: postgresql://user:password@host:port/dbname
```
✅ **Copy this URL - you'll need it!**

---

### **Step 3: Create Web Service**

1. From Render dashboard, click **"New"** → **"Web Service"**
2. Click **"Connect Repository"**
3. Find your `Tweet` or `TweetProject` repository
4. Click **"Connect"**

**Configure the web service:**

| Setting | Value |
|---------|-------|
| **Name** | `tweet-project` |
| **Environment** | `Python 3` |
| **Build Command** | `pip install -r requirements.txt && python TweetProject/manage.py migrate && python TweetProject/manage.py collectstatic --noinput` |
| **Start Command** | `gunicorn TweetProject.wsgi:application` |
| **Plan** | Free |

Click **"Create Web Service"**

---

### **Step 4: Add Environment Variables**

After creating the web service, go to **Settings** → **Environment**

Add these variables:

```
DEBUG=False
ALLOWED_HOSTS=your-service-name.onrender.com
SECRET_KEY=your-secret-key-here
DATABASE_URL=postgresql://user:password@host:port/dbname
PYTHON_VERSION=3.11
```

**Important:** Paste the database URL you copied in Step 2 as `DATABASE_URL`

---

### **Step 5: Deploy**

1. Click **"Manual Deploy"** → **"Deploy Latest Commit"**
2. Watch the logs (click **"Logs"** tab)
3. Wait for it to say **"Your service is live"** ✅

Your app will be available at:
```
https://your-service-name.onrender.com/
```

---

## Environment Variables Explained

| Variable | Value | Where to get |
|----------|-------|--------------|
| `DEBUG` | `False` | Leave as is (production) |
| `SECRET_KEY` | Generate new one | Run: `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"` |
| `ALLOWED_HOSTS` | `your-app.onrender.com` | Render will show after service is created |
| `DATABASE_URL` | PostgreSQL connection | From database page in Render |

---

## Generate SECRET_KEY

Run this command locally:

```powershell
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Copy the output and paste it in `SECRET_KEY` environment variable on Render.

---

## Deployment Flow

```
1. Push to GitHub
   ↓
2. Render detects push
   ↓
3. Render builds your app:
   - pip install requirements
   - python manage.py migrate
   - python manage.py collectstatic
   ↓
4. Gunicorn starts your app
   ↓
5. Your app is LIVE at https://your-app.onrender.com ✅
```

---

## Troubleshooting

### Issue: "Static files not loading"
**Solution:**
- Ensure `WhiteNoiseMiddleware` is in `MIDDLEWARE` ✓ (already configured)
- Re-deploy: Manual Deploy → Deploy Latest Commit

### Issue: "Database connection failed"
**Solution:**
- Verify `DATABASE_URL` is correctly pasted (no spaces)
- Check database is in "Available" state
- Go to database → Settings → Connections tab

### Issue: "502 Bad Gateway"
**Solution:**
- Check logs: Click "Logs" tab
- Ensure `gunicorn` is in requirements.txt ✓
- Make sure build command runs without errors

### Issue: "Migrations failed"
**Solution:**
- Check logs for error details
- Manual deploy from Render dashboard
- Or SSH and run: `python TweetProject/manage.py migrate`

---

## Post-Deployment Commands

### View Logs
```bash
# In Render dashboard → Logs tab
# Or use Render CLI:
render logs --service-id=your-service-id
```

### Run Migrations Manually
```bash
# Via Render dashboard:
# Settings → "Add Shell Command"
# Then: python TweetProject/manage.py migrate
```

### SSH into Service
```bash
# In Render dashboard:
# Settings → SSH Shell
```

---

## Free Tier Limitations

- Web service: Spins down after 15 min inactivity
- Database: 100 MB storage
- Build time: Limited concurrent builds

**Upgrade to paid if you need:**
- Always-on service
- More database storage
- Better performance

---

## Quick Reference

| Step | Command/Action |
|------|----------------|
| Create DB | Render Dashboard → New → PostgreSQL |
| Create Web Service | Render Dashboard → New → Web Service |
| Configure Build | `pip install -r requirements.txt && python TweetProject/manage.py migrate && python TweetProject/manage.py collectstatic --noinput` |
| Configure Start | `gunicorn TweetProject.wsgi:application` |
| Deploy | Manual Deploy → Deploy Latest Commit |

---

## Your App URLs After Deployment

```
Home:               https://tweet-project.onrender.com/
Admin:              https://tweet-project.onrender.com/admin/
Login:              https://tweet-project.onrender.com/accounts/login/
Register:           https://tweet-project.onrender.com/accounts/register/
Tweets:             https://tweet-project.onrender.com/tweets/
```

---

## Next Steps

1. ✅ Code is ready (already pushed to GitHub)
2. Go to [render.com](https://render.com) and sign up
3. Create PostgreSQL database
4. Create Web Service connected to your GitHub repo
5. Add environment variables
6. Click Deploy

Your Django app will be live in ~5 minutes! 🚀
