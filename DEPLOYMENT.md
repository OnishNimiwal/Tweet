# Vercel Deployment Guide for TweetProject

## Prerequisites
1. A [Vercel account](https://vercel.com/signup)
2. GitHub account with this repository
3. A PostgreSQL database (recommended: [Vercel Postgres](https://vercel.com/storage/postgres))

## Steps to Deploy

### 1. **Update Requirements**
Add the following packages (already added to requirements.txt):
- `gunicorn` - WSGI server
- `whitenoise` - Static file handling
- `python-decouple` - Environment variables
- `psycopg2-binary` - PostgreSQL driver

### 2. **Set Up Database**
Since Vercel doesn't support persistent SQLite storage:

#### Option A: Use Vercel Postgres (Recommended)
```bash
# Via Vercel CLI
vercel postgres create
```

#### Option B: Use External PostgreSQL
- Use services like: Railway, Render, Supabase, or AWS RDS
- Get your `DATABASE_URL` connection string

### 3. **Environment Variables on Vercel**

Set these in your Vercel project settings (Settings → Environment Variables):

```
SECRET_KEY=your-new-secret-key-here
DEBUG=False
ALLOWED_HOSTS=your-app-name.vercel.app,your-domain.com
DATABASE_URL=postgresql://user:password@host:port/dbname
```

**Generate a secure SECRET_KEY:**
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 4. **Push to GitHub**
```bash
git add .
git commit -m "Setup Vercel deployment"
git push origin main
```

### 5. **Deploy on Vercel**

#### Using Vercel CLI:
```bash
npm i -g vercel
vercel
```

#### Using Vercel Dashboard:
1. Go to [vercel.com/new](https://vercel.com/new)
2. Import your GitHub repository
3. Set environment variables (from step 3)
4. Deploy

### 6. **Post-Deployment**

After deployment, run migrations on the production database:
```bash
vercel env pull  # Pull production environment variables
python TweetProject/manage.py migrate
```

Or use the Vercel CLI to run a one-time command:
```bash
vercel exec python TweetProject/manage.py migrate
```

## Troubleshooting

### Static Files Not Loading
- Make sure `STATIC_ROOT` is set to `staticfiles/`
- Verify `WhiteNoiseMiddleware` is in MIDDLEWARE
- Run `collectstatic` locally to test

### Database Connection Errors
- Verify `DATABASE_URL` is correctly set in environment variables
- Ensure IP whitelist allows Vercel servers (if applicable)
- Check database credentials and connection limits

### Import Errors
- Verify all packages in `requirements.txt` are correctly listed
- Check Python version (currently using 3.11)

## Local Development

To test production settings locally:
```bash
# Set environment variables in .env file
set VERCEL=1
python TweetProject/manage.py runserver
```

## Additional Resources
- [Vercel Python Documentation](https://vercel.com/docs/functions/python)
- [Django Deployment Checklist](https://docs.djangoproject.com/en/6.0/howto/deployment/checklist/)
