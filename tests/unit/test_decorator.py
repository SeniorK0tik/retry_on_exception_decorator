import logging
from urllib.error import HTTPError

import pytest

from retry_decorator.retry_deco import retry_on_exception



logging.basicConfig(level=logging.DEBUG)


@retry_on_exception(
    exception_type=HTTPError,
    logger=logging,
    message="MESSAGE",
    retries=2,
    timeout=1,
    reraise=True
)
async def async_func_to_test(exc: Exception) -> None:
    raise exc


@retry_on_exception(
    exception_type=HTTPError,
    logger=logging,
    message="MESSAGE",
    retries=2,
    timeout=1,
    reraise=True
)
def func_to_test(exc: Exception) -> None:
    raise exc


@pytest.mark.asyncio
async def test_retry_on_exception() -> None:
    """Тестирование декоратора"""
    logging.basicConfig(level=logging.DEBUG)

    exc = HTTPError(url="test_url.com", code=500, msg="ERROR", hdrs=None, fp=None)
    # Проверка, что именно ЭКЗЕМПЛЯР класса исключения вызывается при ошибке
    with pytest.raises(HTTPError) as e:
        await async_func_to_test(exc)
        assert e == exc

    with pytest.raises(HTTPError) as e:
        func_to_test(exc)
        assert e == exc
