#!/bin/bash
# ── Cricket API Backup Script ─────────────────────────────────────────
# Cron: 0 2 * * * /home/ubuntu/assignment-cricket-api/scripts/backup.sh

BACKUP_DIR="/home/ubuntu/backups"
DATE=$(date +%Y%m%d_%H%M%S)
mkdir -p $BACKUP_DIR

echo "[$(date)] Starting backup..."

# Backup PostgreSQL
docker exec cricket_postgres pg_dump \
    -U cricket_user cricket_db \
    | gzip > "$BACKUP_DIR/db_$DATE.sql.gz"

echo "[$(date)] DB backup: $BACKUP_DIR/db_$DATE.sql.gz"

# Keep only last 7 days
find $BACKUP_DIR -name "*.sql.gz" -mtime +7 -delete
echo "[$(date)] Old backups cleaned"

echo "[$(date)] Backup complete!"