import discord
from discord.ext import commands
from config import token

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

@bot.command()
async def start(ctx):
    await ctx.send("Hi! I'm a chat manager bot!")

@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member = None):
    if member:
        if ctx.author.top_role <= member.top_role:
            await ctx.send("It is not possible to ban a user with equal or higher rank!")
        else:
            await ctx.guild.ban(member, reason="Manual ban command")
            await ctx.send(f"User {member.name} was banned.")
    else:
        await ctx.send("Use: `!ban @user`")

@ban.error
async def ban_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You do not have permission.")
    elif isinstance(error, commands.MemberNotFound):
        await ctx.send("User not found.")

# 🔥 AUTO MODERATION HANDLER
@bot.event
async def on_message(message):
    # Abaikan pesan dari bot sendiri
    if message.author.bot:
        return

    # Cek link
    if "https://" in message.content:
        try:
            await message.guild.ban(
                message.author,
                reason="Auto-ban: sending links"
            )
            await message.channel.send(
                f"🚫 {message.author.mention} was banned for sending links!"
            )
        except discord.Forbidden:
            await message.channel.send(
                "❌ I don't have permission to ban this user."
            )

    # Penting agar command tetap bisa dipakai
    await bot.process_commands(message)

bot.run(token)
