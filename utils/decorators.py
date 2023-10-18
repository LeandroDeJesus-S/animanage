from typing import Any


def try_exceptions(exceptions=Exception, logger=None, log_type='warn', 
                                                    default_return=None) -> Any:
    """A decorator function to try except statement

    Args:
        exceptions (Exception, optional): The exception class. Defaults to Exception.
        logger (_type_, optional): an logger object. Defaults to None.
        log_type (str, optional): the type of the exception log having 
        ['warn', 'info', 'debug', 'error']. Defaults to 'warn'.
        default_return (_type_, optional): default return when the exception 
        is raised. Defaults to None.

    Returns:
        Any: Any|None
    """
    levels = {
        'warn': logger.warning,
        'info': logger.info,
        'debug': logger.debug,
        'error': logger.error
    } if logger is not None else {}
    
    def decorator(func):
        def inner(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except exceptions as exp:
                if logger is not None:
                    levels[log_type](exp)
                
                return default_return
                    
        return inner
    return decorator
