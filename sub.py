from discord.ext import commands
import discord

class ChannelAdmin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.managed_channels = set()
        self.log_channels = set()

    @commands.Cog.listener()
    async def on_ready(self):
        print("---------------------------------")
        for channel in self.bot.get_all_channels():
            print(f"{str(channel.name)} : {str(channel.id)}")
        print("----------------------------------")


    @commands.command()
    async def cmd_help(self, ctx, command="cmd_help"):
        help_msg = {
            "commands":"$channels, $add, $remove, $remove",
            "cmd_help":"\
                cmd_help\n\
                access: all role\n\
                syntax: $cmd_help (command_name)\n\
                arguments: command_name/ The command you want to know the explanation for.\n\
                output: explanation of command\n\
                example: $cmd_help channels\
                ",
            "channels":"\
                channel\n\
                access: all role\n\
                syntax: $channel (ID) (attributes)\n\
                arguments: ID/channel ID, attributes/attributes of channel(https://discordpy.readthedocs.io/ja/latest/api.html#textchannel)\n\
                output: attribute of channel\n\
                example: $channel 1140534096326557817 position nsfw\
                ",
            "channels":"\
                    channels\n\
                    access: all role\n\
                    syntax: $channels\n\
                    arguments: none\n\
                    output: list of all channels:ID, list of managed channels\n\
                    example: $channels\
                ",
            "add":"\
                    add\n\
                    access: all role\n\
                    syntax: $add (mode) (ID)\n\
                    arguments: mode/(log, voice) ID/channel ID\n\
                    output: result of command.\n\
                    example: $add voice 1140534096326557817\
                ",
            "remove":"\
                    remove\n\
                    access: all role\n\
                    syntax: $remove (mode) (ID)\n\
                    arguments:mode/(log, voice) ID/channel ID\n\
                    output: Channel is not managed.\n\
                    example: $remove log 1140534096326557817\
                ",

        }
        if command in help_msg.keys():
            msg = help_msg[command]
        else:
            msg = f"There is no command{command}"
        await ctx.reply(msg)


    @commands.command()
    async def channels(self, ctx):
        embed = discord.Embed(title="ChannelList", timestamp=ctx.message.created_at, color=discord.Colour.blue())
        categories = {channel.id: [] for channel in self.bot.get_all_channels() if channel.category_id is None}
        for key in categories.keys():
            categories[key] = [channel for channel in self.bot.get_all_channels() if channel.category_id == key]

        for key in categories.keys():
            ls = sorted(categories[key], key=lambda x: x.position)
            value = ""
            for channel in ls:
                value += f"{channel.name}:{channel.id}\n"
            embed.add_field(name=f"{self.bot.get_channel(key).name}:{self.bot.get_channel(key).id}", value=value, inline=False)
        await ctx.reply(embed=embed)

        if len(self.managed_channels) == 0:
            embed = discord.Embed(title="There are no managed channels", timestamp=ctx.message.created_at, color=discord.Colour.red())
        else:
            embed = discord.Embed(title="ManagedChannelList", timestamp=ctx.message.created_at, color=discord.Colour.blue())
            for id in self.managed_channels:
                embed.add_field(name=f"{self.bot.get_channel(id).name}:{id}", value="" , inline=False)
        await ctx.reply(embed=embed)

        if len(self.log_channels) == 0:
            embed = discord.Embed(title="There are no log channels", timestamp=ctx.message.created_at, color=discord.Colour.red())
        else:
            embed = discord.Embed(title="ManagedChannelList", timestamp=ctx.message.created_at, color=discord.Colour.blue())
            for id in self.log_channels:
                embed.add_field(name=f"{self.bot.get_channel(id).name}:{id}", value="" , inline=False)
        await ctx.reply(embed=embed)


    @commands.command()
    async def channel(self, ctx, id, *args):
        id = int(id)
        if self.bot.get_channel(id) is not None:
            embed = discord.Embed(title=f"{self.bot.get_channel(id).name}", timestamp=ctx.message.created_at, color=discord.Colour.blue())
            try:
                for arg in args:
                    embed.add_field(name=f"{arg}:{getattr(self.bot.get_channel(id), arg)}", value="" , inline=False)
            except:
                embed.add_field(name=f"{arg}:No attribute", value="" , inline=False)
                raise
        else:
            embed = discord.Embed(title=":x: Failed -ChannelNotFound", description=f"Channel:{id} is not found", timestamp=ctx.message.created_at, color=discord.Colour.red())
        
        await ctx.reply(embed=embed)
    

    @commands.command()
    async def add(self, ctx, mode, id):
        id = int(id)
        if self.bot.get_channel(id) is None:
            embed = discord.Embed(title=":x: Failed -ChannelNotFound", description=f"Channel:{id} is not found", timestamp=ctx.message.created_at, color=discord.Colour.red())
        else:
            channel = self.bot.get_channel(id)
            if mode == "voice":
                if str(channel.type) == "voice":
                    self.managed_channels.add(id)
                    embed = discord.Embed(title=":o: Success -Added", description=f"Channel:{channel.name} is managed", timestamp=ctx.message.created_at, color=discord.Colour.green())
                else:
                    embed = discord.Embed(title=":x: Failed -ChannelTypeError", description=f"Channel:{channel.name} is not voice channel", timestamp=ctx.message.created_at, color=discord.Colour.red())

            elif mode == "log":
                if str(channel.type) == "text":
                    self.log_channels.add(id)
                    embed = discord.Embed(title=":o: Success -Added", description=f"Log will be written in Channel:{channel.name}", timestamp=ctx.message.created_at, color=discord.Colour.green())
                else:
                    embed = discord.Embed(title=":x: Failed -ChannelTypeError", description=f"Channel:{channel.name} is not text channel", timestamp=ctx.message.created_at, color=discord.Colour.red())
            
            else:
                embed = discord.Embed(title=":x: Failed -CommandNotFound", description=f"mode:{mode} is invalid input", timestamp=ctx.message.created_at, color=discord.Colour.red())

        await ctx.reply(embed=embed)


    @commands.command()
    async def remove(self, ctx, mode, id):
        id = int(id)
        if self.bot.get_channel(id) is None:
            embed = discord.Embed(title=":x: Failed -ChannelNotFound", description=f"Channel:{id} is not found", timestamp=ctx.message.created_at, color=discord.Colour.red())

        else:
            if mode == "voice":
                if id in self.managed_channels:
                    self.managed_channels.remove(id)
                    embed = discord.Embed(title=":o: Success -Removed", description=f"Channel:{self.bot.get_channel(id).name} was removed from management", timestamp=ctx.message.created_at, color=discord.Colour.green())
                else:
                    embed = discord.Embed(title=":x: Failed -ChannelNotFound", description=f"Channel:{id} is not found in managed channels", timestamp=ctx.message.created_at, color=discord.Colour.red())
            elif mode == "log":
                if id in self.managed_channels:
                    self.log_channels.remove(id)
                    embed = discord.Embed(title=":o: Success -Removed", description=f"Channel:{self.bot.get_channel(id).name} was removed from log channels", timestamp=ctx.message.created_at, color=discord.Colour.green())
                else:
                    embed = discord.Embed(title=":x: Failed -ChannelNotFound", description=f"Channel:{id} is not found in log channels", timestamp=ctx.message.created_at, color=discord.Colour.red())
        await ctx.reply(embed=embed)


    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if before.channel != after.channel:
            announce_channel_ids = self.managed_channels
            if before.channel is not None and before.channel.id in announce_channel_ids:
                msg = "__" + member.name + "__  has left from **" + before.channel.name + "**"
            if after.channel is not None and after.channel.id in announce_channel_ids:
                msg = "__" + member.name + "__  has joined **" + after.channel.name + "**"
            
            for id in self.log_channels:
                print(msg)
                await self.bot.get_channel(id).send(msg)

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
            embed = discord.Embed(title=":x: Failed -BadArgument", description=f"Occurs when no value is passed for a requested parameter during parameter parsing of a command.", timestamp=ctx.message.created_at, color=discord.Colour.red())
            embed.set_footer(text="If you are having trouble, please mentions the server administrator.")
            await ctx.reply(embed=embed) 
        elif isinstance(error, discord.ext.commands.errors.MissingRequiredAttachment):
            embed = discord.Embed(title=":x: Failed -BadAttachment", description=f"This occurs when a parameter that requires an attachment is not given during the parameter analysis of the command.", timestamp=ctx.message.created_at, color=discord.Colour.red())
            embed.set_footer(text="If you are having trouble, please mentions the server administrator.")
            await ctx.reply(embed=embed) 
        elif isinstance(error, discord.ext.commands.errors.TooManyArguments):
            embed = discord.Embed(title=":x: Failed -TooManyArguments", description=f"Exception raised if the command is passed an excessive number of arguments and the Command.ignore_extra attribute is not True.", timestamp=ctx.message.created_at, color=discord.Colour.red())
            embed.set_footer(text="If you are having trouble, please mentions the server administrator.")
            await ctx.reply(embed=embed)
        elif isinstance(error, discord.ext.commands.errors.MemberNotFound):
            embed = discord.Embed(title=":x: Failed -MemberNotFound", description=f"Exception raised when the member provided was not found in the bot’s cache.", timestamp=ctx.message.created_at, color=discord.Colour.red())
            embed.set_footer(text="If you are having trouble, please mentions the server administrator.")
            await ctx.reply(embed=embed)
        elif isinstance(error, discord.ext.commands.errors.BadArgument):
            embed = discord.Embed(title=":x: Failed -BadArgument", description=f"Exception raised when parsing or conversion of a value passed as an argument to a command fails.", timestamp=ctx.message.created_at, color=discord.Colour.red())
            embed.set_footer(text="If you are having trouble, please mentions the server administrator.")
            await ctx.reply(embed=embed) 
        elif isinstance(error, discord.ext.commands.errors.CommandNotFound):
            embed = discord.Embed(title=":x: Failed -CommandNotFound", description=f"Exception raised when a command with the specified name does not exist when the command is called.", timestamp=ctx.message.created_at, color=discord.Colour.red())
            embed.set_footer(text="If you are having trouble, please mentions the server administrator.")
            await ctx.reply(embed=embed)
        elif isinstance(error, discord.ext.commands.errors.CommandInvokeError):
            embed = discord.Embed(title=":x: Failed -CommandInvokeError", description=f"Exception raised when the command being called raises an exception.", timestamp=ctx.message.created_at, color=discord.Colour.red())
            embed.set_footer(text="If you are having trouble, please mentions the server administrator.")
            await ctx.reply(embed=embed)
        elif isinstance(error, discord.ext.commands.errors.MissingPermissions):
            embed = discord.Embed(title=":x: Failed -MissingPermissions", description=f"Cannot execute because the executor does not have the necessary permissions.", timestamp=ctx.message.created_at, color=discord.Colour.red())
            embed.set_footer(text="If you are having trouble, please mentions the server administrator.")
            await ctx.reply(embed=embed)
        elif isinstance(error, discord.ext.commands.errors.BotMissingPermissions):
            embed = discord.Embed(title=":x: Failed -BotMissingPermissions", description=f"Cannot run because the bot does not have the necessary permissions.", timestamp=ctx.message.created_at, color=discord.Colour.red())
            embed.set_footer(text="If you are having trouble, please mentions the server administrator.")
            await ctx.reply(embed=embed)
        else:
            raise error
        

async def setup(bot):
    await bot.add_cog(ChannelAdmin(bot))
