import disnake


# fmt: off
class SuccessEmbed(disnake.Embed):
    def __init__(self, description: str = None):
        super().__init__(
            title="Success! ✅",
            description=description,
            color=disnake.Color.green()
        )


class ErrorEmbed(disnake.Embed):
    def __init__(self, description: str = None):
        super().__init__(
            title="Error! 💢",
            description=description,
            color=disnake.Color.red()
        )
# fmt: on
