import random
import time
from threading import Thread

from d_util import Singleton


class TestSingleton(Singleton):
    def _init_class_(self) -> None:
        if not hasattr(self, "init_count"):
            self.init_count = 0
        self.init_count += 1


def test_singleton_instance_identity():
    a = TestSingleton()
    b = TestSingleton()
    assert a is b


def test_init_class_called_once():
    instance = TestSingleton()
    instance = TestSingleton()
    instance = TestSingleton()
    assert instance.init_count == 1


def test_singleton_thread_safety():
    # Collect instances from multiple threads to test thread safety
    instances = []

    def create_instance():
        # create some delay so we create the objects after threads spawn
        time.sleep(random.uniform(0.2, 0.5))
        instances.append(TestSingleton())

    threads = [Thread(target=create_instance) for _ in range(10)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    # All instances must be the same
    assert all(inst is instances[0] for inst in instances), "Instances from threads are not the same"

