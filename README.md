# Discord Bot Template

[![Tests](https://github.com/notchum/discord-bot-template/actions/workflows/test.yml/badge.svg?branch=master)](https://github.com/notchum/discord-bot-template/actions/workflows/test.yml)

Discord bot with slash commands. It uses [MongoDB](https://docs.mongodb.com/) database and [disnake](https://github.com/DisnakeDev/disnake) Discord API wrapper.

### Requirements

- [Python](https://www.python.org/downloads/)
- [MongoDB](https://docs.mongodb.com/manual/installation/)

### How to use this template

To use this template as your project starting point, click "Use this template" at the top of this page, or click [here](https://github.com/notchum/discord-bot-template/generate).

### Feature highlights

* Asynchronous support for files (via [aiofiles](https://github.com/Tinche/aiofiles)), 
  HTTP requests (via [aiohttp](https://github.com/aio-libs/aiohttp)), 
  and MongoDB drivers (via [motor](https://github.com/mongodb/motor) & [Beanie](https://github.com/roman-right/beanie))
* Environment configuration with [python-dotenv](https://github.com/theskumar/python-dotenv)
* Logs via [loguru](https://github.com/delgan/loguru)
* Error handling
* Docker image build workflow to push images to [Docker Hub](https://hub.docker.com/)
* Temporary file directory with scheduled clean-up

### Project structure

```bash
├── requirements.txt
├── bot.py              # The `MyBot` class
├── launcher.py         # Entry point to launch the bot
├── .env                # Environment variables for bot configuration (renamed from .env.example)
├── cogs
│   ├── admin.py        # Slash commands for guild administrators
│   ├── commands.py     # Example cog with some example slash commands
│   ├── events.py       # Discord event listeners
│   ├── owner.py        # Slash commands for the bot owner only
│   └── tasks.py        # Disnake scheduled background tasks
├── helpers
│   ├── __init__.py
│   └── embeds.py       # Common Discord embed templates
├── models
│   ├── __init__.py
│   ├── guild.py        # Example ODM model for guilds
│   └── settings.py     # ODM model for global bot settings
├── utils
│   ├── __init__.py
│   └── utilities.py    # General utilities
├── views
│   ├── __init__.py
│   └── paginator.py    # Example view implementing embed pages
├── Dockerfile
├── README.md
├── DEVELOPMENT.md
└── LICENSE
```

### Todo

- [ ] Tests with pytest
- [ ] CI based on Github actions
- [ ] Dependabot configuration
- [ ] Instructions to create bot application with correct permissions
- [x] Dockerfile
- [ ] Instructions to set up docker hub secrets in Github

## Contributing

Contributors are welcome, please fork and send pull requests! If you find a bug
or have any ideas on how to improve this project please submit an issue.

### Code formatting

[ruff](https://github.com/astral-sh/ruff) is used for code formatting. Always format the code with ruff before submitting a pull request.

## Development

``` sh
# Inside the project root (directory containing this file)
python -m venv venv && source ./venv/bin/activate
pip install -r requirements.txt
pip install -r requirements-test.txt
mypy
pytest
ruff format .
```
