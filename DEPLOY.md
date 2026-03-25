# Deployment Guide

## Free Hosting Options

### Option 1: Render (Recommended)

**Pros:** Free tier available, good for Docker containers, easy setup
**Cons:** Cold starts (goes to sleep after 15 min of inactivity)

**Steps:**
1. Push your code to GitHub
2. Go to [render.com](https://render.com) and sign up
3. Click "New" → "Web Service"
4. Connect your GitHub repo
5. Configure:
   - Build Command: (leave empty)
   - Start Command: `sh start.sh`
6. Add environment variables:
   - `GOOGLE_API_KEY`: Your Google AI Studio API key
7. Click "Create Web Service"

**Note:** The free tier sleeps after 15 minutes of inactivity. First request after sleep will take 30-60 seconds.

### Option 2: Railway

**Pros:** More generous free tier, faster cold starts
**Cons:** Requires credit card for verification (won't be charged)

**Steps:**
1. Push your code to GitHub
2. Go to [railway.app](https://railway.app) and sign up
3. Click "New Project" → "Deploy from GitHub repo"
4. Select your repo
5. Add environment variables in the Railway dashboard:
   - `GOOGLE_API_KEY`: Your Google AI Studio API key
6. Deploy

### Option 3: Fly.io

**Pros:** Good performance, persistent storage support
**Cons:** Requires credit card, more complex setup

**Steps:**
1. Install flyctl: `curl -L https://fly.io/install.sh | sh`
2. Login: `flyctl auth login`
3. Launch: `flyctl launch`
4. Add secrets: `flyctl secrets set GOOGLE_API_KEY=your_key`
5. Deploy: `flyctl deploy`

---

## Getting a Google API Key

1. Go to [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Create a new API key
3. Copy the key and add it to your hosting environment

---

## Local Development with Docker

```bash
# Clone and setup
cp .env.example .env
# Edit .env and add your GOOGLE_API_KEY

# Build and run
docker-compose up --build

# Access at http://localhost:8501
```

---

## Important Notes

1. **ChromaDB Persistence:** The vector database is stored in `chroma_db/`. On free hosting, this may be ephemeral. Consider uploading PDFs each session.

2. **Cold Starts:** Free tiers have cold starts. Be patient on first request.

3. **API Costs:** Google Gemini has a free tier with generous limits. Monitor usage at [Google AI Studio](https://aistudio.google.com/app/usage).

4. **HTTPS:** Free tiers typically provide HTTPS automatically.

---

## For Recruiters

When showing this project to recruiters:

1. **Live Demo:** Deploy to Render (easiest) and share the URL
2. **Code Quality:** Highlight:
   - Clean separation of concerns (backend/frontend)
   - Proper error handling
   - Type hints and documentation
   - Docker containerization
3. **Architecture:** Explain RAG pipeline, embeddings, and LLM integration
4. **Challenges:** Mention handling large PDFs, embedding model selection, and prompt engineering
