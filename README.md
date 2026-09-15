# Mímir Discord Bot 🏈

[![Python Version](https://img.shields.io/badge/python-3.11%2B-blue.svg)](https://www.python.org/downloads/)
[![discord.py](https://img.shields.io/badge/discord.py-2.7%2B-blueviolet.svg)](https://github.com/Rapptz/discord.py)
[![Docker](https://img.shields.io/badge/docker-ready-2496ED.svg?logo=docker&logoColor=white)](https://www.docker.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**Mímir** is a Discord bot that connects to the ESPN Fantasy Football API to deliver real-time league updates, matchup box scores, score projections, and detailed team rosters directly to your Discord server.

Named after the Norse god of wisdom and knowledge, Mímir keeps your fantasy league informed and engaged throughout the season without requiring members to leave Discord.

---

## Table of Contents

- [Features](#features)
- [Bot Commands](#bot-commands)
- [Prerequisites & Setup](#prerequisites--setup)
  - [1. Discord Bot Application](#1-discord-bot-application)
  - [2. ESPN Fantasy League Credentials](#2-espn-fantasy-league-credentials)
- [Configuration](#configuration)
  - [Environment Variables (`.env`)](#environment-variables-env)
  - [Team Mappings (`team_mappings.json`)](#team-mappings-team_mappingsjson)
- [Deployment & Usage](#deployment--usage)
  - [Running with Docker (Recommended)](#running-with-docker-recommended)
  - [Running with Docker Compose](#running-with-docker-compose)
  - [Running Locally (Python)](#running-locally-python)
- [Project Structure](#project-structure)
- [Troubleshooting](#troubleshooting)
- [License](#license)

---

## Features

- **🏈 Team Rosters**: View active rosters, positions, lineup slots (Starter/Bench/IR), and current player injury statuses.
- **📈 Weekly Projections**: Quickly compare projected matchups across the league for any regular-season week.
- **⚡ Live & Final Box Scores**: Check ongoing and final scores with head-to-head projections and actual point totals.
- **👥 Manager Aliases**: Map user nicknames and common names to ESPN team IDs so server members don't need to look up team numbers.
- **🐳 Container Ready**: Packaged with a production-ready `Dockerfile` for effortless deployment on servers or home labs.

---

## Bot Commands

The bot uses `?` as its command prefix. Commands are case-insensitive.

| Command | Arguments | Description | Example |
| :--- | :--- | :--- | :--- |
| `?roster` | `<manager_name>` | Display the full roster, positions, lineup slots, and injury status for a team. | `?roster alex` |
| `?projected` | `<week>` | Show projected scores for all league matchups for a given week (1–17). | `?projected 4` |
| `?scores` | `<week> [manager_name]` | Show actual vs. projected box scores for all matchups, or filter by manager. | `?scores 4` or `?scores 4 julie` |

### Command Examples

#### 1. Roster Lookup (`?roster <name>`)
```text
?roster user1
```
Will produce
```
Roster for Gridiron Greats:
Patrick Mahomes      Position: QB    Linup Slot: QB         Status: ACTIVE
Saquon Barkley       Position: RB    Linup Slot: RB         Status: ACTIVE
Justin Jefferson     Position: WR    Linup Slot: WR         Status: QUESTIONABLE
Travis Kelce         Position: TE    Linup Slot: TE         Status: ACTIVE
...
```

#### 2. Weekly Projections (`?projected <week>`)
```text
?projected 1
```
Will produce
```
Projected Scores for week 1:
  Team John: 118.40, Team Jack: 112.15
  Team Jane: 104.50, Team Jill: 98.20
...
```

#### 3. Matchup Scores (`?scores <week> [name]`)
```text
?scores 1 john
```
Will produce
```
 Team john - Projected: 112.15, Actual: 124.60
/
\
 Team Jill - Projected: 118.40, Actual: 115.80
```

---

## Prerequisites & Setup

### 1. Discord Bot Application

1. Navigate to the [Discord Developer Portal](https://discord.com/developers/applications).
2. Click **New Application** and give your bot a name (e.g., `Mimir`).
3. Under the **Bot** tab:
   - Click **Reset Token** to generate a new bot token. Save this token for your `.env` file.
   - Scroll down to **Privileged Gateway Intents** and enable:
     - **Presence Intent**
     - **Server Members Intent**
     - **Message Content Intent** (Required for reading command messages)
4. Under **OAuth2 > URL Generator**:
   - Scopes: Select `bot`.
   - Bot Permissions: Select `Send Messages`, `Read Messages/View Channels`, and `Read Message History`.
   - Copy the generated URL and paste it into your browser to invite the bot to your server.

### 2. ESPN Fantasy League Credentials

To read data from an ESPN Fantasy Football league (especially private leagues), the bot requires specific IDs and browser cookie authentication tokens:

- **`LEAGUE_ID`**: The unique numeric ID of your fantasy league.
  - Visit your ESPN Fantasy League page in a browser.
  - Look at the URL: `https://fantasy.espn.com/football/league?leagueId=12345678`.
  - The number following `leagueId=` is your `LEAGUE_ID`.
- **`YEAR`**: The season year to query (e.g., `2026`).
- **`ESPN_S2` & `SWID`** (Required for private leagues):
  1. Open a browser and log into your account at [ESPN.com](https://www.espn.com).
  2. Open Developer Tools (`F12` or right-click -> **Inspect**).
  3. Go to the **Application** (Chrome/Edge) or **Storage** (Firefox) tab.
  4. Expand **Cookies** in the left sidebar and select `https://espn.com`.
  5. Find and copy the values for:
     - `espn_s2`: A long alphanumeric string.
     - `SWID`: A UUID enclosed in curly braces, e.g., `{12345678-ABCD-EF01-2345-6789ABCDEF01}`.

> [!NOTE]
> Public leagues only require `LEAGUE_ID` and `YEAR`. If your league is public, `ESPN_S2` and `SWID` can be left blank, but setting them is recommended for consistent API access.

---

## Configuration

### Environment Variables (`.env`)

Copy `template.env` to create your local `.env` file:

```bash
cp template.env .env
```

Populate the fields with your credentials:

```dotenv
LEAGUE_ID="12345678"
YEAR="2026"
ESPN_S2="AECxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
SWID="{12345678-ABCD-EF01-2345-6789ABCDEF01}"
DISCORD_TOKEN="YOUR_DISCORD_BOT_TOKEN"
```

| Variable | Type | Description |
| :--- | :--- | :--- |
| `LEAGUE_ID` | Integer | Your numeric ESPN Fantasy Football league ID. |
| `YEAR` | Integer | Fantasy season year (e.g., `2026`). |
| `ESPN_S2` | String | ESPN cookie string for private league authorization. |
| `SWID` | String | ESPN software identification cookie (including curly braces `{...}`). |
| `DISCORD_TOKEN` | String | Bot token from the Discord Developer Portal. |

> [!CAUTION]
> Never commit your `.env` file to version control. It is already included in `.gitignore`.

### Team Mappings (`team_mappings.json`)

The bot maps manager names or nicknames to ESPN team IDs. Create or update `team_mappings.json` in the root of the repository:

```json
{
    "john": "1",
    "jane": "2",
    "jack": "3",
    "jill": "4",
}
```

- **Keys**: Manager names or aliases (must be lowercase). You can add multiple aliases pointing to the same team ID (e.g., `"johnathan"` and `"john"`).
- **Values**: The team ID as a string. To find a team's ID, click on their team in the ESPN Fantasy web interface and inspect the URL for `teamId=X`.

---

## Deployment & Usage

### Running with Docker (Recommended)

Docker provides an isolated and reproducible environment for the bot.

#### 1. Build the Docker image
```bash
docker build -t mimir-discord-bot .
```

#### 2. Run the container
Run the container using your `.env` file and mount `team_mappings.json` so you can update mappings on the host without rebuilding the image:

```bash
docker run -d \
  --name mimir-bot \
  --restart unless-stopped \
  --env-file .env \
  -v "$(pwd)/team_mappings.json:/app/team_mappings.json:ro" \
  mimir-discord-bot
```

*(On Windows PowerShell, use `${PWD}` instead of `$(pwd)`: `-v "${PWD}/team_mappings.json:/app/team_mappings.json:ro"`)*

#### 3. Manage the container
- **View logs**:
  ```bash
  docker logs -f mimir-bot
  ```
- **Stop the bot**:
  ```bash
  docker stop mimir-bot
  ```
- **Restart the bot**:
  ```bash
  docker restart mimir-bot
  ```

---

### Running with Docker Compose

For easy multi-container or daemon management, you can define a `docker-compose.yml`:

```yaml
version: "3.8"

services:
  mimir:
    build: .
    container_name: mimir-discord-bot
    restart: unless-stopped
    env_file:
      - .env
    volumes:
      - ./team_mappings.json:/app/team_mappings.json:ro
```

Launch with:
```bash
docker compose up -d
```

---

### Running Locally (Python)

#### 1. Prerequisites
- Python 3.11 or higher
- `git`

#### 2. Set up virtual environment

- **Linux / macOS**:
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```

- **Windows (PowerShell)**:
  ```powershell
  python -m venv venv
  .\venv\Scripts\Activate.ps1
  ```

#### 3. Install dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

#### 4. Configure files
Ensure `.env` and `team_mappings.json` are populated as described in the [Configuration](#configuration) section.

#### 5. Run the bot
```bash
python main.py
```

---

## Project Structure

```text
mimir-discord-bot/
├── fantasy_management/
│   └── fantasy_management.py   # Wrapper class around espn-api League interface
├── Dockerfile                  # Container build instructions (Python 3.11-slim)
├── LICENSE                     # MIT License
├── README.md                   # Project documentation
├── main.py                     # Discord bot entry point, events, and command handlers
├── requirements.txt            # Python dependencies (discord.py, espn-api, etc.)
├── team_mappings.json          # Mapping of user aliases to ESPN team IDs
└── template.env                # Example environment configuration template
```

---

## Troubleshooting

### 1. `discord.errors.PrivilegedIntentsRequired`
- **Cause**: The bot code requests `Intents.all()`, but privileged intents are disabled in the Discord Developer Portal.
- **Fix**: Go to the [Discord Developer Portal](https://discord.com/developers/applications) > your app > **Bot** > **Privileged Gateway Intents**, and toggle ON **Message Content Intent**, **Server Members Intent**, and **Presence Intent**.

### 2. ESPN 401 Unauthorized / Private League Errors
- **Cause**: The `ESPN_S2` or `SWID` cookie values are incorrect or have expired.
- **Fix**: Re-authenticate on ESPN.com in your browser, copy fresh `espn_s2` and `SWID` cookie values, update `.env`, and restart the bot.

### 3. `Team name '<name>' not found in team mappings`
- **Cause**: The specified name was not found in `team_mappings.json`.
- **Fix**: Add the manager's name/nickname in lowercase to `team_mappings.json` paired with their numeric ESPN team ID.

### 4. Box scores or roster not refreshing
- **Cause**: ESPN data might be cached by the running instance.
- **Fix**: In `fantasy_management.py`, `league.refresh()` is called during manual runs; restart the bot process or container to force an immediate cache invalidation.

---

## License

This project is licensed under the [MIT License](LICENSE).