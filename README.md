# Volt
**Volt** is yet another discord api wrapper for Python.
It supports python 3.7 +

## How to install
```shell
pip install volt
```

## Planned Structure (Can be changed!)
### Event listener
```python
from volt import Client, Intents, Message

client = Client(intents=Intents.all())

@client.listen('message')
async def on_message(msg: Message):
    if not msg.author.bot:
        # echo user message
        await msg.reply(msg.content)

client.run('BOT_TOKEN')
```
### Slash Commands
```python
from volt import Client, Intents, interaction, User

client = Client(intents=Intents.all())

@client.command(
    name='greeting'
)
async def greeting_slash(ctx: interaction.Context, user: User):
    await ctx.respond(...)

client.run('BOT_TOKEN')
```
```python
### Message Components
from volt import Client, Intents, interaction, components, User

client = Client(intents=Intents.all())

@client.command(
    name='greeting'
)
async def greeting_slash(ctx: interaction.Context, user: User):
    await ctx.respond(components=[
        components.ActionRow([
            components.Button(
                custom_id='my_btn',
                style=components.ButtonStyle.Primary
            )
        ])
    ])

client.run('BOT_TOKEN')
```
