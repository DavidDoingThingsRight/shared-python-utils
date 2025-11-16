import threading
from typing import Any, TypeVar, cast

T = TypeVar("T", bound="Singleton")

class Singleton:
    _instances: dict[type["Singleton"], "Singleton"] = {}
    _singleton_lock: threading.Lock = threading.Lock()

    def __new__(cls: type[T], *args: Any, **kwargs: Any) -> T:
        with cls._singleton_lock:
            if cls not in cls._instances:
                instance = super().__new__(cls)
                instance._init_class_()
                cls._instances[cls] = instance
        return cast(T, cls._instances[cls])

    def _init_class_(self) -> None:
        """Override this in subclass to initialize the subclass."""
        pass
