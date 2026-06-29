# Vynia Bridge Bot

Vynia Bridge Bot is a lightweight, compartmentalised version of the Guild Bridge Bot.

It bridges messages between a Discord server and a Minecraft guild while allowing you to create your own custom commands as Python functions.


## Features

- Discord <-> Minecraft guild bridge
- Custom Python commands
- Docker deployment
- Environment-based configuration
- Minimal and easy to extend


## Deployment

See the deployment guide:

- [Deployment Guide](docs/deployment.md)


## Custom Commands

See the custom commands guide:

- [Custom Commands Guide](docs/custom_commands.md)


## Type checking

Install the development-only type checker dependencies:

```bash
pip install -r src/requirements-dev.txt
```

Run Pyright:

```bash
pyright
```

Or run mypy:

```bash
mypy
```


## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.


## Disclaimer

This bot is not affiliated with or endorsed by Hypixel.

Use it at your own risk and ensure that you comply with Hypixel's Terms of Service. The bot follows Hypixel's API rules by among other things caching api calls in order to minimize the risk of account restrictions.
