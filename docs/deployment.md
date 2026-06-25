# Deployment

## Requirements

1. Install `git`
2. Install `docker`
3. Install `docker compose`


## Discord Bot

1. Create a Discord application.
2. Create a bot.
3. Enable the required intents.
4. Copy the bot token.

Tutorial:
https://www.youtube.com/watch?v=Oy5HGvrxM4o (first two minutes)


## Discord Server

1. Invite the bot to your Discord server.
2. Create or choose the bridge channel.
3. Copy the channel ID.

Tutorial:
https://www.youtube.com/watch?v=rbwvcyEx_Uc


## Installation

1. Clone the repository

   ```sh
   git clone https://github.com/Vaenyx/vynia-bridge-bot.git
   cd vynia-bridge-bot
   ```

2. Configure the environment

   Copy `.env.example` to `.env`

   ```sh
   cp .env.example .env
   ```

   Fill in all required values.

3. Build and start the project

   - Build only

     ```sh
     docker compose build
     ```

     > Use `--no-cache` to force a complete rebuild.

   - Start only

     ```sh
     docker compose up -d
     ```

   - Build and start together

     ```sh
     docker compose up -d --build
     ```

4. Wait until all containers have started.

5. Verify that the container is running.

   ```sh
   docker ps
   ```

6. Authenticate the Minecraft account.

   ```sh
   docker logs vynia-bridge-bot
   ```

   Follow the instructions printed in the logs.

7. Done.
