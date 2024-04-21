# Utility
- Будет полезен с flaky функциями. Например, с работой по сети, где ответ от сервера может быть не стабильный.

# Installation
`poetry add git+https://github.com/SeniorK0tik/retry_on_exception_decorator.git`

# Examples
```python

logger = <YOUR_LOGGER>

@retry_on_exception(
    exception_type=Exception,
    logger=logger,
    message="DEFAULT MSG",
    retries=5,
    timeout=1,
    reraise=True
)
def flaky_fn():
    # DO SMTH
    raise Exception

flaky_fn()


########################################
INFO:root:Retry for flaky_fn attempt: 1 with <class 'Exception'>: 
INFO:root:Retry for flaky_fn attempt: 2 with <class 'Exception'>: 
INFO:root:Retry for flaky_fn attempt: 3 with <class 'Exception'>: 
INFO:root:Retry for flaky_fn attempt: 4 with <class 'Exception'>: 
INFO:root:Retry for flaky_fn attempt: 5 with <class 'Exception'>: 
ERROR:root:flaky_fn ended with with <class 'Exception'> | MSG: DEFAULT MSG
Traceback (most recent call last):
...

```
