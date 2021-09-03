import asyncio

from volt.gateway import GatewayBot, GatewayOpcodes


async def test():
    print('Initialize GatewayBot instance.')
    bot = GatewayBot('Njk2Nzc4MjI3NjAzMjEwMjkw.XotrSg.zpo_4Bx6Co3Za0aeD10TlxfGNqs')

    async def close_bot():
        await asyncio.sleep(20)
        print('Close the bot!')
        await bot.close()

    asyncio.create_task(close_bot())
    await bot.run()


asyncio.get_event_loop().run_until_complete(test())

