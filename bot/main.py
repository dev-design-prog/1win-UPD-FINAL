import asyncio
import logging
import os
import aiohttp
from bot import main as bot_main
from api_server import create_app
from aiohttp import web

logging.basicConfig(level=logging.INFO)

def _self_url() -> str:
    """Публичный адрес этого же сервиса (Render подставляет RENDER_EXTERNAL_URL)."""
    return (os.getenv("WEBAPP_URL") or os.getenv("RENDER_EXTERNAL_URL") or "").strip().rstrip("/")


async def keep_alive():
    """Раз в 10 минут дёргаем собственный /health, чтобы сервис не засыпал."""
    while True:
        await asyncio.sleep(600)
        url = _self_url()
        if not url:
            continue
        try:
            async with aiohttp.ClientSession() as session:
                await session.get(f"{url}/health", timeout=aiohttp.ClientTimeout(total=15))
        except Exception:
            pass

async def run_all():
    app = create_app()
    runner = web.AppRunner(app)
    await runner.setup()
    port = int(os.getenv("PORT", os.getenv("API_PORT", "8080")))
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()
    print(f"API server running on port {port}")
    
    asyncio.create_task(keep_alive())
    
    await bot_main()

if __name__ == "__main__":
    asyncio.run(run_all())
