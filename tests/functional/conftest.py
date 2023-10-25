import pytest
import asyncio


pytest_plugins = (
    'tests.functional.fixtures.clients',
    'tests.functional.fixtures.http',
)


@pytest.fixture(scope="session")
def event_loop():
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
    yield loop
    loop.close()
