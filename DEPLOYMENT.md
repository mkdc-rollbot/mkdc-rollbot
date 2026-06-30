# Deployment Guide

This document describes how to deploy RollBot to a fresh Ubuntu EC2 instance.

## Prerequisites

* AWS EC2 Ubuntu 24.04 instance
* Security Group allowing:

  * TCP 22 (SSH) from your IP
  * TCP 80 (HTTP) from Anywhere
* SSH key pair for the EC2 instance
* Docker Compose project checked into GitHub
* Local copies of all required `.env` files

---

# 1. Connect to the instance

```bash
ssh -i <key.pem> ubuntu@<PUBLIC_IP>
```

---

# 2. Update the system

```bash
sudo apt update
sudo apt upgrade -y
```

---

# 3. Install Docker

```bash
sudo apt install docker.io docker-compose-v2 git -y
```

Enable Docker:

```bash
sudo systemctl enable docker
sudo systemctl start docker
```

Allow the current user to use Docker without `sudo`:

```bash
sudo usermod -aG docker ubuntu
```

Apply the new group membership:

```bash
newgrp docker
```

Verify the installation:

```bash
docker ps
```

---

# 4. Clone the repository

Since the repository is public, clone it over HTTPS:

```bash
git clone https://github.com/mkdc-rollbot/mkdc-rollbot.git
cd mkdc-rollbot
```

---

# 5. Copy configuration files

The repository intentionally does not contain secrets.

Copy the required `.env` files from the development machine:

```bash
scp .env ubuntu@<PUBLIC_IP>:~/mkdc-rollbot/
scp api_service/.env ubuntu@<PUBLIC_IP>:~/mkdc-rollbot/api_service/
scp discord_client/.env ubuntu@<PUBLIC_IP>:~/mkdc-rollbot/discord_client/
scp frontend/.env.production ubuntu@<PUBLIC_IP>:~/mkdc-rollbot/discord_client/.env
```

---

# 6. Build and start the application

```bash
docker compose up -d --build
```

The stack consists of:

* PostgreSQL
* API Service (FastAPI)
* Discord Client
* Frontend (Nginx + React)

---

# 7. Verify the deployment

Check container status:

```bash
docker compose ps
```

Inspect logs if necessary:

```bash
docker compose logs postgres
docker compose logs api_service
docker compose logs frontend
docker compose logs discord_client
```

---

# 8. Verify locally

Check that the frontend is responding:

```bash
curl localhost
```

Check that the reverse proxy reaches the API:

```bash
curl localhost/api/health
```

Expected response:

```json
{"status":"OK"}
```

---

# 9. Verify from a browser

Navigate to:

```
http://<PUBLIC_IP>
```

The RollBot dashboard should load successfully.

---

# Updating an existing deployment

SSH into the instance:

```bash
ssh -i <key.pem> ubuntu@<PUBLIC_IP>
```

Update the repository:

```bash
cd ~/mkdc-rollbot
git pull
```

Rebuild and restart:

```bash
docker compose up -d --build
```

---

# Common troubleshooting

## Check running containers

```bash
docker compose ps
```

## View service logs

```bash
docker compose logs api_service
docker compose logs frontend
docker compose logs postgres
docker compose logs discord_client
```

## Restart the stack

```bash
docker compose down
docker compose up -d --build
```

## Recreate the database

**Warning:** This deletes all stored data.

```bash
docker compose down -v
docker compose up -d --build
```

---

# Architecture

```
Browser
    │
    ▼
Nginx (Frontend)
    │
    └── /api
          │
          ▼
      FastAPI
          │
          ▼
     PostgreSQL

Discord Gateway
        │
        ▼
Discord Client
        │
        ▼
FastAPI
```

The frontend communicates only with the reverse proxy (`/api`), while all inter-service communication occurs over Docker's internal network.

