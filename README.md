# Volt
**Volt** is yet another discord api wrapper for Python.
It supports python 3.8 +

## How to install [Currently Not Supported.]
```shell
pip install volt.py
```
### Speed up volt.py!
You can install extra dependencies for speeding up library.
```shell
pip install volt.py[speed]
```
`speed` extra requirements are used to speed up library.
This contains `uvloop` for asyncio event loop speedup.
Since uvloop is not supported on Windows platform, you can't use this extra requirements on Windows.
You can use wsl to use speedups on Windows!

### Voice feature with volt.py [Currently Not Supported]
You can install dependencies required for voice features.
```shell
pip install volt.py[voice]
```

### I want all extra requirements to be installed!
You can install all extra dependencies by using following command;
```shell
pip install volt.py[all]
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
### Interaction
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
