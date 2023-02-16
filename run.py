from setup import bot, dp
from user import user_router
import asyncio
from loguru import logger


async def _start():
    dp.include_router(user_router)
    await dp.start_polling(bot)


def start_bot():
    asyncio.run(_start())


if __name__ == '__main__':
    logger.info("Добро пожаловать! Рады вас видеть :)")
    try:
        start_bot()
    except KeyboardInterrupt:
        logger.info("Бот остановлен админом, обратитесь в тех поддержку @lyftbonusacc")
