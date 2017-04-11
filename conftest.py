import os

from selenium import webdriver
import pytest
import django


def pytest_configure():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "_project_.settings")
    django.setup()


@pytest.fixture(scope='session')
def base_url(live_server):
    return live_server.url


@pytest.fixture
def driver_class(request):
	return webdriver.Firefox


@pytest.fixture
def driver_kwargs():
	return {}


@pytest.yield_fixture
def driver(request, driver_class, driver_kwargs):
    """Returns a WebDriver instance based on options and capabilities"""
    driver = driver_class(**driver_kwargs)
    yield driver
    driver.quit()


@pytest.fixture(scope='function', autouse=True)
def _skip_sensitive(request):
    """Don't Skip destructive tests"""
