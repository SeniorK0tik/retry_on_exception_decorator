import asyncio
import inspect
import time
from functools import wraps
from typing import Any, Callable, Tuple, Type, TypeAlias



LOGGER_: TypeAlias = object


def _log_retry_attempt(
        func: object,
        attempts: int,
        logger: LOGGER_,
        exception_type: Type[Exception] | Tuple[Type[Exception]],
        excp: Exception
) -> None:
    """Логирование новой попытки"""
    logger.info(
        f"Retry for {func.__name__} attempt: {attempts + 1} with {exception_type}: {excp}"
    )

def _log_final(
        func: object,
        logger: LOGGER_,
        exception_type: Type[Exception] | Tuple[Type[Exception]],
        message: str
) -> None:
    """Логирование в случае если все попытки исчерпаны"""
    logger.error(
        f"{func.__name__} ended with with {exception_type} | MSG: {message}"
    )


def retry_on_exception(  # noqa: C901
        exception_type: Type[Exception] | Tuple[Type[Exception]],
        logger: LOGGER_,
        message: str,
        retries: int,
        timeout: int = 5,
        reraise: bool = True
) -> Callable:
    """
    Декоратор, который перезапускает целевую функцию

    exception_type: Тип исключения при котором будет активирован RETRY
    logger: объект логгера
    message: Сообщение при окончательном выводе из функции с исключением
    retries: Количество попыток перезапуска
    timeout: Время паузы между попытками перезапуска
    reraise: Нужно ли вызывать ошибку если все попытки выполнились, а ошибка не исчезла
    """
    def decorator(func: Callable) -> Callable:  # noqa: C901
        if inspect.iscoroutinefunction(func):
            @wraps(func)
            async def wrapper(*args, **kwargs) -> Any:
                attempts = 0
                exc_obj = None

                while attempts < retries:
                    try:
                        return await func(*args, **kwargs)
                    except exception_type as e:
                        exc_obj = e
                        _log_retry_attempt(func, attempts, logger, exception_type, e)
                        attempts += 1
                        await asyncio.sleep(timeout)
                    except Exception:
                        raise

                _log_final(func, logger, exception_type, message)
                if reraise:
                    raise exc_obj
                return None

        elif inspect.isasyncgenfunction(func):
            @wraps(func)
            async def wrapper(*args, **kwargs) -> Any:  # noqa: C901
                attempts = 0
                exc_obj = None

                while attempts < retries:
                    try:
                        async for item in func(*args, **kwargs):
                            yield item
                    except exception_type as e:
                        exc_obj = e
                        _log_retry_attempt(func, attempts, logger, exception_type, e)
                        attempts += 1
                        await asyncio.sleep(timeout)
                    except Exception:
                        raise

                    _log_final(func, logger, exception_type, message)
                    if reraise:
                        raise exc_obj
                    yield None

        else:
            @wraps(func)
            def wrapper(*args, **kwargs) -> Any:
                attempts = 0
                exc_obj = None

                while attempts < retries:
                    try:
                        return func(*args, **kwargs)
                    except exception_type as e:
                        exc_obj = e
                        _log_retry_attempt(func, attempts, logger, exception_type, e)
                        attempts += 1
                        time.sleep(timeout)
                    except Exception:
                        raise

                _log_final(func, logger, exception_type, message)
                if reraise:
                    raise exc_obj
                return None

        return wrapper
    return decorator
