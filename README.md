discord.py
  python-dotenv
  pytz
  ```

## Setup Instructions

1. **Clone the Repository**
   ```bash
   git clone <your-repository-url>
   cd <repository-name>
   ```

2. **Install Dependencies**
   ```bash
   pip install discord.py python-dotenv pytz
   ```

3. **Environment Setup**
   Create a `.env` file in the root directory with:
   ```
   DISCORD_BOT_TOKEN=your_bot_token_here
   ```

4. **Configuration**
   - Update `utils/config.py` with your server's:
     - Default server ID
     - Test channel ID
     - Other configuration as needed

## Running the Bot

1. **Local Development**
   ```bash
   python main.py
   ```

2. **Hosting Services (e.g., Glacier Hosting)**
   - Upload all files maintaining the directory structure
   - Set the environment variables in your hosting platform
   - Ensure Python 3.8+ is available
   - Use `main.py` as your entry point

## Project Structure

```
├── cogs/
│   ├── calculator.py
│   └── events.py
├── utils/
│   ├── config.py
│   └── logger.py
├── main.py
├── README.md
└── .env
```

## Environment Variables

- `DISCORD_BOT_TOKEN`: Your Discord bot token (required)

## Usage

1. **Event Creation**
   ```
   /createevent [title] [date] [time] [timezone] [custom_triggers] [description]
   ```

2. **Calculator**
   ```
   /calc [expression]