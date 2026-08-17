# Using Vercel Postgres with Django

## Quick Setup Guide

### 1. **Create Vercel Postgres Database**

**Via Vercel Dashboard:**
1. Go to your project: [vercel.com/dashboard](https://vercel.com/dashboard)
2. Click on your **TweetProject** app
3. Navigate to **Storage** tab (top menu)
4. Click **"Create"** → **Postgres**
5. Select your region (choose closest to your users)
6. Name it: `tweet-db` or similar
7. Click **Create**

**Via Vercel CLI:**
```bash
npm install -g vercel
vercel postgres create
```

---

### 2. **Connect Database to Your Project**

After creation, you'll see the database in your Storage tab. Vercel automatically:
- Creates environment variables
- Links them to your Vercel project

**To view the connection string:**
```bash
vercel env pull  # Downloads .env.local with all database credentials
```

You'll get these environment variables:
```
POSTGRES_URL=postgresql://user:password@host:port/database
POSTGRES_URL_NON_POOLING=postgresql://... (non-connection pooling)
POSTGRES_HOST=host
POSTGRES_PASSWORD=password
POSTGRES_USER=user
POSTGRES_DATABASE=database
```

---

### 3. **Configure Django for Vercel Postgres**

Your `production_settings.py` already handles Vercel Postgres! It automatically detects `POSTGRES_URL`.

**Update your environment variables in Vercel:**

Go to Project Settings → Environment Variables and add:

```
DJANGO_SETTINGS_MODULE=TweetProject.production_settings
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=your-app.vercel.app
```

Vercel Postgres variables are **added automatically** ✓

---

### 4. **Test Connection Locally**

Pull environment variables and test:

```powershell
# Download .env.local from Vercel
vercel env pull

# Test Django can connect
python TweetProject/manage.py dbshell

# Run migrations
python TweetProject/manage.py migrate
```

---

### 5. **Deploy to Vercel**

```powershell
# Commit all changes
git add .
git commit -m "Setup Vercel Postgres"
git push origin main

# Deploy (or use GitHub to auto-deploy)
vercel --prod
```

Vercel will automatically:
1. Install dependencies (`pip install -r requirements.txt`)
2. Run build commands (migrations, collectstatic)
3. Deploy your app with database connection

---

### 6. **Verify Database Connection**

After deployment, check your app's logs:

```powershell
vercel logs
```

Look for successful migration messages:
```
Running migrations...
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, sessions, messages, tweet
Running migrations:
  Applying ... OK
```

---

## Useful Commands

### View Database Status
```bash
# Via Dashboard
vercel storage  # Lists all databases

# Check connection
vercel postgres info tweet-db
```

### Query Your Database (via CLI)
```bash
# Connect to database
vercel postgres connect <database-name>

# You'll get a psql prompt to query
SELECT * FROM tweet_tweet;
SELECT COUNT(*) FROM auth_user;
```

### Backup/Export Data
```bash
# Create a backup
vercel postgres backup create <database-name>

# List backups
vercel postgres backup list <database-name>

# Restore from backup
vercel postgres backup restore <database-name> <backup-id>
```

---

## Troubleshooting

### Issue: "No database connection"
**Solution:**
- Run `vercel env pull` to ensure you have latest env variables
- Check POSTGRES_URL is set in Vercel project settings
- Restart deployment

### Issue: "relation does not exist" error
**Solution:**
Run migrations:
```bash
vercel exec python TweetProject/manage.py migrate
```

### Issue: "SSL certificate verify failed"
**Solution:**
Your `production_settings.py` handles this. If you get SSL errors, ensure `dj-database-url` is installed:
```bash
pip install dj-database-url
```

### Issue: Connection Pooling
**Use `POSTGRES_URL_NON_POOLING` for:**
- Django ORM (already configured)
- Long-running queries

**Use `POSTGRES_URL` for:**
- Applications with many concurrent connections

---

## Architecture Overview

```
Your Django App (Vercel)
        ↓
   WSGI Server (Gunicorn)
        ↓
   Django ORM (psycopg2)
        ↓
   Vercel Postgres
```

---

## Environment Variables Summary

| Variable | Purpose | Example |
|----------|---------|---------|
| `POSTGRES_URL` | Full connection string | `postgresql://user:pass@host/db` |
| `POSTGRES_HOST` | Database host | `db.abcxyz.postgres.vercel-storage.com` |
| `POSTGRES_USER` | Database user | `default` |
| `POSTGRES_PASSWORD` | Database password | (secure token) |
| `POSTGRES_DATABASE` | Database name | `verceldb` |
| `SECRET_KEY` | Django secret key | Generate with: `python manage.py shell` |
| `DEBUG` | Debug mode | `False` (production) |
| `ALLOWED_HOSTS` | Allowed domain | `your-app.vercel.app` |

---

## Next Steps

1. ✅ Create Vercel Postgres (you can do this now)
2. ✅ Pull environment variables locally
3. ✅ Test migrations: `python TweetProject/manage.py migrate`
4. ✅ Push to GitHub
5. ✅ Deploy to Vercel
6. ✅ Monitor logs: `vercel logs`

Your Django app is now ready for production! 🚀
