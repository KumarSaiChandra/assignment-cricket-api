# Cricket Players API 🏏

Production-ready FastAPI application deployed on AWS EC2 with Docker,
NGINX, PostgreSQL, Redis, and automated CI/CD via GitHub Actions.

## Architecture

![Architecture Diagram](cricket_api_architecture.png)

GitHub Push → Actions CI/CD → Docker Hub → EC2 Deploy

## Tech Stack

| Layer | Technology |
|-------|-----------|
| API | FastAPI + Uvicorn |
| Database | PostgreSQL 16 |
| Cache | Redis 7 |
| Proxy | NGINX (rate limiting + SSL) |
| Container | Docker + Docker Compose |
| CI/CD | GitHub Actions |
| Registry | Docker Hub |
| Server | AWS EC2 (Ubuntu 22.04) |
| Security | UFW + fail2ban + non-root containers |

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/players/register` | Register a new cricket player |
| GET | `/players/{id}` | Get player by ID |
| GET | `/players` | Get all players |
| GET | `/health` | Health check (DB + Redis status) |

## Quick Start

### Prerequisites
- Docker + Docker Compose
- AWS EC2 (Ubuntu 22.04)

### Run locally

```bash
git clone https://github.com/YOUR_USERNAME/assignment-cricket-api
cd assignment-cricket-api
cp .env.example .env      # fill in your values
docker compose up --build
```

Open http://localhost/docs

### Run from Docker Hub

```bash
docker pull YOUR_DOCKERHUB_USERNAME/cricket-api:latest
```

## CI/CD Pipeline

Every push to `main` branch:
Run Tests     (pytest with real PostgreSQL + Redis)
Build Image   (Docker buildx with layer caching)
Push to Hub   (Docker Hub — tagged with :latest + :commit-sha)
Deploy EC2    (SSH → git pull → docker compose up)
Health Check  (confirms deployment succeeded)

## Security Measures

- **UFW Firewall** — only ports 22, 80, 443 open
- **fail2ban** — bans IPs after 3 failed SSH attempts (24h ban)
- **Non-root containers** — app runs as `appuser`, not root
- **Internal services** — PostgreSQL and Redis never exposed publicly
- **NGINX rate limiting** — 30 requests/minute per IP
- **Security headers** — X-Frame-Options, X-Content-Type, HSTS
- **TLS 1.2/1.3 only** — weak ciphers disabled
- **Resource limits** — CPU and memory limits on all containers

## SSL Setup

### With domain (production) — Let's Encrypt
```bash
sudo certbot certonly --standalone -d yourdomain.com
```

### Without domain (current setup) — Self-signed
```bash
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout nginx/certs/privkey.pem \
  -out nginx/certs/fullchain.pem \
  -subj "/C=IN/ST=TamilNadu/O=CricketAPI/CN=cricket-api"
```

## Health Checks

All containers have health checks configured:

```bash
# Check all container statuses
docker compose ps

# API health
curl http://localhost/health

# Returns:
# {"status":"ok","database":"connected","total_players":5}
```

## Backup Strategy

Automated daily backup at 2AM via cron:

```bash
# Manual backup
./scripts/backup.sh

# Backups stored at
ls /home/ubuntu/backups/

# Restore
gunzip -c backups/db_20250622_020000.sql.gz \
  | docker exec -i cricket_postgres psql -U cricket_user cricket_db
```

Retention: 7 days (older backups auto-deleted)

## Logging

```bash
# All containers
docker compose logs -f

# API only
docker compose logs -f api

# NGINX access logs
docker compose logs -f nginx
```

Log rotation: 10MB max per file, 5 files kept per service.

## Monitoring

Watchtower monitors Docker Hub for new images every 30 seconds
and automatically restarts containers when updates are detected.

## Environment Variables

Copy `.env.example` to `.env` and fill in:

```env
DATABASE_URL=postgresql://cricket_user:PASSWORD@postgres:5432/cricket_db
REDIS_URL=redis://redis:6379/0
```

## Project Structure

```
assignment-cricket-api/
├── app/
│   ├── database.py          # SQLAlchemy engine + session
│   ├── models.py            # DB table definitions
│   └── schemas.py           # Pydantic request/response models
├── nginx/
│   ├── nginx.conf           # Reverse proxy + rate limiting + SSL
│   └── certs/               # SSL certificates (gitignored)
├── scripts/
│   └── backup.sh            # PostgreSQL backup with rotation
├── .github/
│   └── workflows/
│       └── deploy.yml       # CI/CD pipeline
├── main.py                  # FastAPI app + all endpoints
├── Dockerfile               # Multi-stage production image
├── docker-compose.yml       # All services configuration
├── requirements.txt
├── .env.example             # Environment variable template
└── README.md
```
