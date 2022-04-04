import pytest


@pytest.fixture(scope="module", autouse=True)
def setup():
    print("Setup from conftest module")