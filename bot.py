import discord
from discord.ext import commands
import openai

# Set up OpenAI API
openai.api_key = "your-openai-api-key"

# Set up Discord bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

@bot.event
async def on_message(message):
    # Ignore bot's own messages
    if message.author == bot.user:
        return
    
    # Check if bot is mentioned
    if bot.user.mentioned_in(message):
        async with message.channel.typing():
            try:
                # Remove bot mention from message
                user_message = message.content.replace(f'<@{bot.user.id}>', '').strip()
                
                # Call OpenAI API
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": user_message}]
                )
                
                # Send response
                reply = response.choices[0].message.content
                await message.reply(reply[:2000])  # Discord limit: 2000 chars
                
            except Exception as e:
                await message.reply(f"Error: {str(e)}")

# Run bot
bot.run("your-discord-bot-token")
