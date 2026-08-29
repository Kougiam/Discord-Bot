import asyncio
import discord
from discord.ext import commands

TICKET_CATEGORY_ID = 1542472945744486475
SUPPORT_ROLE_ID = 1542472882943303700


class TicketPanelView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="🎫 Άνοιγμα Ticket", style=discord.ButtonStyle.blurple, custom_id="ticket:open")
    async def open_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        guild = interaction.guild
        author = interaction.user

        existing = discord.utils.get(guild.text_channels, name=f"ticket-{author.name}".lower())
        if existing:
            return await interaction.response.send_message(
                f"Έχεις ήδη ανοιχτό ticket: {existing.mention}", ephemeral=True
            )

        overwrites = {
            guild.default_role: discord.PermissionOverwrite(view_channel=False),
            author: discord.PermissionOverwrite(view_channel=True, send_messages=True, read_message_history=True),
            guild.me: discord.PermissionOverwrite(view_channel=True, send_messages=True),
        }

        if SUPPORT_ROLE_ID:
            support_role = guild.get_role(SUPPORT_ROLE_ID)
            if support_role:
                overwrites[support_role] = discord.PermissionOverwrite(view_channel=True, send_messages=True)

        category = guild.get_channel(TICKET_CATEGORY_ID) if TICKET_CATEGORY_ID else None

        channel = await guild.create_text_channel(
            name=f"ticket-{author.name}",
            category=category,
            overwrites=overwrites,
            topic=f"Ticket του {author} (ID: {author.id})",
        )

        embed = discord.Embed(
            title="🎫 Νέο Ticket",
            description=(
                f"Γεια σου {author.mention}! Περίγραψε το θέμα σου και η ομάδα support "
                f"θα σε εξυπηρετήσει σύντομα."
            ),
            color=discord.Color.blurple(),
        )
        await channel.send(embed=embed, view=CloseTicketView())
        await interaction.response.send_message(f"✅ Το ticket σου δημιουργήθηκε: {channel.mention}", ephemeral=True)


class CloseTicketView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="🔒 Κλείσιμο Ticket", style=discord.ButtonStyle.red, custom_id="ticket:close")
    async def close_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("Το ticket κλείνει σε 5 δευτερόλεπτα...")
        await interaction.channel.edit(name=f"closed-{interaction.channel.name}")
        await interaction.channel.set_permissions(interaction.guild.default_role, view_channel=False)
        await asyncio.sleep(5)
        await interaction.channel.delete()


class Tickets(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def cog_load(self):
        self.bot.add_view(TicketPanelView())
        self.bot.add_view(CloseTicketView())

    @commands.command(name="ticket-panel", help="Στέλνει το panel δημιουργίας tickets σε αυτό το κανάλι.")
    @commands.has_permissions(manage_channels=True)
    async def ticket_panel(self, ctx: commands.Context):
        embed = discord.Embed(
            title="📩 Support Tickets",
            description="Πάτησε το κουμπί παρακάτω για να ανοίξεις ένα ticket με την ομάδα μας.",
            color=discord.Color.blurple(),
        )
        await ctx.send(embed=embed, view=TicketPanelView())
        try:
            await ctx.message.delete()
        except discord.Forbidden:
            pass

    async def cog_command_error(self, ctx: commands.Context, error: commands.CommandError):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("Χρειάζεσαι δικαίωμα Manage Channels.")
        else:
            await ctx.send(f"Σφάλμα: {error}")


async def setup(bot: commands.Bot):
    await bot.add_cog(Tickets(bot))
