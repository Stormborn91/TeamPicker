import discord
from discord.ext import commands
import random
import os
from flask import Flask
from threading import Thread

# Web server to bind to port 8080 for Render
app = Flask('')

@app.route('/')
def home():
    return "I'm alive!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

intents = discord.Intents.all()
intents.members = True  # Required for role assignment

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.command()
async def team(ctx):
    team_roles = ['team red', 'team blue', 'team green', 'team yellow']
    user_roles = [role.name for role in ctx.author.roles]

    # Check if user already has a team role
    for team_role in team_roles:
        if team_role in user_roles:
            await ctx.send(f"{ctx.author.mention}, you're already on **{team_role}**! 🎉")
            return
    
    colors = ['red', 'blue', 'green', 'yellow']
    chosen_color = random.choice(colors)
    role_name = f"team {chosen_color}"
    role = discord.utils.get(ctx.guild.roles, name=role_name)

    if role:
        await ctx.author.add_roles(role)
        await ctx.send(f"{ctx.author.mention}, you've been assigned to **{role_name}**! 🎉")
    else:
        await ctx.send(f"Role '{role_name}' not found. Please make sure it exists on the server.")

if __name__ == "__main__":
    keep_alive()
    TOKEN = os.getenv("BOT_TOKEN")

    while True:
	try:
    	    bot.run(TOKEN)
	except Exception as e:
	    print(f"Bot crashed with error: {e}. Restarting...")
