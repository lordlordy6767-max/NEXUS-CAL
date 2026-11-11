import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import sympy as sp
from flask import Flask
from threading import Thread

app = Flask(__name__)

@app.route('/')
def home():
    return "NEXUS CAL is online!"

def run_web():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

Thread(target=run_web, daemon=True).start()
load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)

x, y = sp.symbols('x y')

# Premium check - True = open for testing, change to False for launch
def is_premium(ctx):
    return True

@bot.event
async def on_ready():
    print(f"✅ NEXUS CAL Online as {bot.user}")
    await bot.change_presence(activity=discord.Game(name="!help | NEXUS CAL"))

# ============ HELP COMMAND ============
@bot.command(name="help")
async def help_cmd(ctx, command=None):
    if command is None:
        embed = discord.Embed(title="🧮 NEXUS CAL - Help", color=0x00ff00)
        embed.add_field(name="📗 FREE", value="`!calc`\n`!solve`\n`!simplify`\n`!quadratic`", inline=False)
        embed.add_field(name="👑 PREMIUM", value="`!solve-system`\n`!solve-inequality`\n`!derivative`\n`!integrate`\n`!limit`\n`!tangent`\n`!factor`\n`!expand`\n`!matrix`\n`!graph`\n`!convert`", inline=False)
        embed.add_field(name="ℹ️", value="Type `!help solve` for details\nType `!premium` to unlock Premium", inline=False)
        embed.set_footer(text="NEXUS CAL | NEXUS")
        await ctx.send(embed=embed)
        return

    details = {
        "calc": "Usage: `!calc 5*5+10`",
        "solve": "Usage: `!solve 2x+5=15`",
        "derivative": "Usage: `!derivative x**3+2x` - Premium",
        "integrate": "Usage: `!integrate x**2` - Premium",
        "solve-system": "Usage: `!solve-system x+y=10, x-y=2` - Premium",
        "graph": "Usage: `!graph y=x**2` - Premium",
    }
    await ctx.send(details.get(command.lower(), f"No help for `{command}`. Try `!help`"))

# ============ FREE COMMANDS ============
@bot.command()
async def calc(ctx, *, expr):
    try:
        result = sp.sympify(expr)
        await ctx.send(f"🧮 `{expr}` = **{result}**")
    except Exception as e:
        await ctx.send(f"❌ Error: {e}")

@bot.command()
async def solve(ctx, *, eq):
    try:
        left, right = eq.split("=")
        expr = sp.sympify(left) - sp.sympify(right)
        sols = sp.solve(expr, x)
        embed = discord.Embed(title=f"✅ Solve: {eq}", description=f"**Solutions:** {sols}", color=0x00ff00)
        if is_premium(ctx):
            embed.add_field(name="📝 Steps", value=f"1. Move all to one side: `{expr} = 0`\n2. Solve for x\n3. Answer: {sols}")
        else:
            embed.add_field(name="🔒 Premium", value="Want steps? Type `!premium`")
        await ctx.send(embed=embed)
    except:
        await ctx.send("❌ Use like `!solve 2x+5=15`")

@bot.command()
async def simplify(ctx, *, expr):
    try:
        await ctx.send(f"✅ Simplify: **{sp.simplify(sp.sympify(expr))}**")
    except:
        await ctx.send("❌ Use like `!simplify (x**2-1)/(x-1)`")

@bot.command()
async def quadratic(ctx, a: float, b: float, c: float):
    # !quadratic 1 3 2
    disc = b**2 - 4*a*c
    embed = discord.Embed(title=f"✅ Quadratic: {a}x² + {b}x + {c} = 0", color=0x00ff00)
    embed.add_field(name="Discriminant", value=f"{disc}", inline=False)
    if disc >= 0:
        x1 = (-b + disc**0.5) / (2*a)
        x2 = (-b - disc**0.5) / (2*a)
        embed.add_field(name="Solutions", value=f"x1 = {x1}\nx2 = {x2}", inline=False)
    else:
        embed.add_field(name="Solutions", value="No real solutions (complex)", inline=False)
    await ctx.send(embed=embed)

# ============ PREMIUM COMMANDS ============
@bot.command(name="solve-system")
async def solve_system(ctx, *, eqs):
    if not is_premium(ctx):
        return await ctx.send("🔒 Premium only. Type `!premium`")
    try:
        parts = eqs.split(",")
        eq_list = []
        for p in parts:
            l, r = p.split("=")
            eq_list.append(sp.Eq(sp.sympify(l), sp.sympify(r)))
        sol = sp.solve(eq_list, (x, y))
        await ctx.send(f"✅ System: {sol}")
    except:
        await ctx.send("❌ Use like `!solve-system x+y=10, x-y=2`")

@bot.command()
async def derivative(ctx, *, expr):
    if not is_premium(ctx):
        return await ctx.send("🔒 Premium only")
    await ctx.send(f"📈 Derivative of `{expr}` = **{sp.diff(sp.sympify(expr), x)}**")

@bot.command()
async def integrate(ctx, *, expr):
    if not is_premium(ctx):
        return await ctx.send("🔒 Premium only")
    await ctx.send(f"∫ `{expr}` = **{sp.integrate(sp.sympify(expr), x)} + C**")

@bot.command()
async def factor(ctx, *, expr):
    if not is_premium(ctx):
        return await ctx.send("🔒 Premium only")
    await ctx.send(f"✅ Factor: **{sp.factor(sp.sympify(expr))}**")

@bot.command()
async def expand(ctx, *, expr):
    await ctx.send(f"✅ Expand: **{sp.expand(sp.sympify(expr))}**")

@bot.command()
async def limit(ctx, *, args):
    if not is_premium(ctx):
        return await ctx.send("🔒 Premium only")
    try:
        expr_str, val = args.rsplit(" ", 1)
        res = sp.limit(sp.sympify(expr_str), x, float(val))
        await ctx.send(f"✅ Limit = **{res}**")
    except:
        await ctx.send("❌ Use like `!limit (x**2-1)/(x-1) 1`")

@bot.command()
async def premium(ctx):
    await ctx.send("👑 NEXUS CAL Premium - Unlock all advanced maths + steps!\nDM owner to buy.")

bot.run(os.getenv("TOKEN"))
