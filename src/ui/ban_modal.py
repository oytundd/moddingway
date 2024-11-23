import discord
from services.ban_service import ban_user
from .helper import create_modal_embed
from commands.helper import create_response_context


class BanModal(discord.ui.Modal):

    def __init__(self, user: discord.Member) -> None:
        self.user = user
        super().__init__(title=f"Ban User {user.display_name}")

    reason = discord.ui.TextInput(
        label="Ban Reason",
        style=discord.TextStyle.long,
        placeholder="Reason for banning user",
        max_length=512,
        required=True,
    )

    delete_messages = discord.ui.TextInput(
        label="Delete Messages? (Y/N)",
        style=discord.TextStyle.short,
        placeholder='Type "Y" for Yes or "N" for No',
        max_length=1,
        required=True,
    )

    async def on_submit(self, interaction: discord.Interaction):
        delete_messages_value = (
            self.delete_messages.value.strip().upper()
        )  # Normalize input
        if delete_messages_value not in ["Y", "N"]:
            await interaction.response.send_message(
                "Invalid input for 'Delete Messages'. Please enter 'Y' or 'N'.",
                ephemeral=True,
            )
            return

        delete_messages_flag = delete_messages_value == "Y"  # Convert to boolean
        async with create_response_context(interaction) as response_message:
            async with create_modal_embed(
                interaction,
                "Ban User",
                user=self.user,
                reason=self.reason.value,
            ) as logging_embed:
                result = await ban_user(
                    interaction.user, self.user, self.reason.value, delete_messages_flag
                )

                if result[0]:  # Ban was successful
                    response_message.set_string(
                        f"Successfully banned {self.user.mention}."
                    )
                else:  # Ban failed
                    response_message.set_string(result[2])
                    logging_embed.add_field(name="Error", value=result[2], inline=False)
