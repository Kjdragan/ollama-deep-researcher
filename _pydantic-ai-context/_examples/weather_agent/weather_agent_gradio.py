from __future__ import annotations as _annotations

import asyncio
import os
from contextlib import asynccontextmanager
from typing import AsyncIterator

import gradio as gr
import logfire
from httpx import AsyncClient

from .weather_agent import Deps, weather_agent

# 'if-token-present' means nothing will be sent (and the example will work) if you don't have logfire configured
logfire.configure(send_to_logfire='if-token-present')


@asynccontextmanager
async def get_deps() -> AsyncIterator[Deps]:
    async with AsyncClient() as client:
        # create a free API key at https://www.tomorrow.io/weather-api/
        weather_api_key = os.getenv('WEATHER_API_KEY')
        # create a free API key at https://geocode.maps.co/
        geo_api_key = os.getenv('GEO_API_KEY')
        yield Deps(
            client=client, weather_api_key=weather_api_key, geo_api_key=geo_api_key
        )


async def respond(
    message: str, history: list[list[str]], deps: Deps
) -> AsyncIterator[str]:
    result = await weather_agent.run(message, deps=deps)
    yield result.data


async def main():
    async with get_deps() as deps:
        demo = gr.ChatInterface(
            fn=lambda message, history: respond(message, history, deps),
            title='Weather Agent',
            description=(
                'Ask about the weather in any location! '
                'Note: without API keys, responses will use dummy data.'
            ),
            examples=[
                'What is the weather like in London?',
                'Tell me the weather in Paris and Rome',
                'How is the weather in Tokyo right now?',
            ],
        )
        demo.queue()
        demo.launch(show_api=False)
        # keep the app running
        while True:
            await asyncio.sleep(1)


if __name__ == '__main__':
    asyncio.run(main())