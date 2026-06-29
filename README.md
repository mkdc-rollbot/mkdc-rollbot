# RollBot

A cloud-native tabletop RPG assistant built around Discord.

RollBot allows players and game masters to store character sheets, manage campaigns, and perform game actions directly through Discord while maintaining persistent data across sessions.

The project began as a small utility for a Dungeons & Dragons campaign and has evolved into a full-stack application used as both a real product and a platform for exploring modern software architecture and DevOps practices.

---

# Motivation

Tabletop roleplaying games frequently rely on character sheets, dice rolls, and campaign-specific information.

While many digital tools exist, they often require players to leave the platform where the game is actually taking place. During online campaigns this platform is usually Discord.

RollBot aims to bring character management and game interactions directly into Discord while maintaining a persistent backend capable of supporting multiple campaigns, game systems, and future web-based management tools.

The project also serves as a practical environment for exploring software engineering concepts such as service separation, deployment automation, observability, and infrastructure management.

---

# Features

## Current

* Discord bot interface
* Persistent PostgreSQL storage
* Character creation and retrieval
* Multi-channel campaign support
* Character-to-channel assignment
* REST API for administration and integrations
* Web dashboard for data management
* Dockerized deployment

## Planned

* Attack and damage roll workflows
* Support for additional tabletop systems
* Campaign management tools
* Scheduling and reminder utilities
* Character sheet editing from the dashboard
* Authentication and user management
* Observability stack (Prometheus + Grafana)
* CI/CD automation

---

# Domain Model

A core design goal of RollBot is separating a player's character identity from campaign-specific state.

A player may wish to reuse the same character concept across multiple campaigns, one-shots, or alternate timelines. These versions often diverge over time due to differing equipment, progression, injuries, or story developments.

To support this use case RollBot distinguishes between:

* Characters
* Character Variants
* Channels (campaign instances)

This allows a single character to maintain multiple campaign-specific representations without duplicating all character data.

---

# Architecture

Current deployment consists of four services:

```text
Discord
   │
   ▼
Discord Client
   │
   ▼
REST API
   │
   ├── PostgreSQL
   │
   └── Web Dashboard
```

## Components

### Discord Client

Handles Discord interactions and command processing.

Responsibilities:

* Receiving commands
* Formatting responses
* Communicating with the API service

### API Service

Central application service.

Responsibilities:

* Business logic
* Data validation
* Character management
* Campaign management
* Persistence orchestration

### PostgreSQL

Persistent storage layer.

Stores:

* Guilds
* Channels
* Players
* Characters
* Character variants

### Dashboard

React-based administration interface.

Provides:

* Character browsing
* Guild inspection
* Channel inspection
* Data management tools

---

# Technology Stack

## Backend

* Python
* FastAPI
* SQLAlchemy
* PostgreSQL

## Frontend

* React
* Vite
* Mantine
* TanStack Query

## Infrastructure

* Docker
* Docker Compose

## Future Infrastructure

* GitHub Actions
* Prometheus
* Grafana
* Terraform
* Kubernetes

---

# Running Locally

## Requirements

* Docker
* Docker Compose

## Start

```bash
docker compose up --build
```

Services:

| Service    | Port  |
| ---------- | ----- |
| Frontend   | 5173  |
| API        | 11037 |
| PostgreSQL | 5432  |

---

# Design Goals

RollBot is intentionally designed as something more substantial than a tutorial application.

The objective is to build a real system with evolving requirements and genuine domain constraints. Architectural decisions are driven primarily by product requirements and only secondarily by technology choices.

The project therefore serves two purposes:

1. A useful tabletop RPG platform.
2. A long-term software engineering and DevOps laboratory.

---

# Roadmap

## Application

* Campaign management
* Multi-system support
* Character editing UI
* Authentication
* Player self-service tools

## Platform

* Automated testing
* CI/CD pipelines
* Cloud deployment
* Metrics and monitoring
* Infrastructure as code
* Production-grade operations

---

# Author

Dor Arie Lotan

B.Sc. Computational Linguistics

Focused on software architecture, DevOps, formal reasoning, and language technologies.

