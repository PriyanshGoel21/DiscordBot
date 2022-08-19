import discord

from discord.ext import commands
from discord import app_commands

from typing import Union


def bot_has_permissions(**perms: bool):
    """A decorator that add specified permissions to Command.extras and add bot_has_permissions check to Command with specified permissions.

    Warning:
    - This decorator must be on the top of the decorator stack
    - This decorator is not compatible with commands.check()
    """

    def wrapped(
        command: Union[app_commands.Command, commands.HybridCommand, commands.Command]
    ) -> Union[app_commands.Command, commands.HybridCommand, commands.Command]:
        if not isinstance(
            command,
            (app_commands.Command, commands.hybrid.HybridCommand, commands.Command),
        ):
            raise TypeError(
                f"Cannot decorate a class that is not a subclass of Command, get: {type(command)} must be Command"
            )

        valid_required_permissions = [
            perm
            for perm, value in perms.items()
            if getattr(discord.Permissions.none(), perm) != value
        ]
        command.extras.update({"bot_permissions": valid_required_permissions})

        if isinstance(command, (app_commands.Command, commands.HybridCommand)):
            app_commands.checks.bot_has_permissions(**perms)(command)
        if isinstance(command, (commands.Command, commands.HybridCommand)):
            commands.bot_has_permissions(**perms)(command)

        return command

    return wrapped
