from itunes_app_scraper.scraper import AppStoreScraper
from itunes_app_scraper.util import (
    AppStoreException,
    AppStoreCollections,
)

import pytest
import os
import requests
import itunes_app_scraper.scraper as scraper_module


def test_term_no_exception():
    scraper = AppStoreScraper()
    results = scraper.get_app_ids_for_query("mindful", country="gb", lang="en")
    assert len(results) > 0


def test_no_term_gives_exception():
    scraper = AppStoreScraper()
    with pytest.raises(AppStoreException, match="No term was given"):
        scraper.get_app_ids_for_query("", country="gb", lang="en")


def test_no_invalid_id_gives_exception():
    scraper = AppStoreScraper()
    with pytest.raises(AppStoreException, match="No app found with ID 872"):
        scraper.get_app_details("872")


def test_no_invalid_id_in_multiple_is_empty():
    scraper = AppStoreScraper()
    assert len(list(scraper.get_multiple_app_details(["872"]))) == 0


def test_no_invalid_id_in_multiple_writes_log():
    scraper = AppStoreScraper()
    scraper.get_multiple_app_details(["872"])
    assert os.path.exists("log/nl_log.txt")
    fh = open("log/nl_log.txt")
    assert "No app found with ID 872" in fh.read()
    fh.close()


def test_log_file_write_message():
    scraper = AppStoreScraper()
    scraper._log_error("gb", "test")
    assert os.path.exists("log/gb_log.txt")
    fh = open("log/gb_log.txt")
    assert "test" in fh.read()
    fh.close()


def test_country_code_does_exist():
    scraper = AppStoreScraper()
    assert scraper.get_store_id_for_country("gb") == 143444


def test_country_code_does_not_exist():
    scraper = AppStoreScraper()
    with pytest.raises(AppStoreException, match="Country code not found for XZ"):
        scraper.get_store_id_for_country("xz")


def test_query_multiple_pages():
    query = "game"
    scraper = AppStoreScraper()
    results = set()
    for page in range(1, 4):
        page_results = scraper.get_app_ids_for_query(
            query, country="us", lang="en", page=page
        )
        if page_results:
            [results.add(x) for x in page_results]
            assert len(results) > (page - 1) * 50
    print(f"Total results for query {query}: {len(results)}")


def test_get_app_ids_for_collection():
    scraper = AppStoreScraper()
    results = scraper.get_app_ids_for_collection(
        AppStoreCollections.TOP_FREE_IOS, country="us", lang="en"
    )
    assert len(results) > 0


def test_get_app_ids_for_developer_maps_list_of_apps(monkeypatch):
    scraper = AppStoreScraper()

    def fake_get_apps_for_developer(developer_id, country="nl", lang="", timeout=None):
        return [
            {"trackId": 101, "wrapperType": "software"},
            {"trackId": 202, "wrapperType": "software"},
        ]

    monkeypatch.setattr(scraper, "get_apps_for_developer", fake_get_apps_for_developer)

    app_ids = scraper.get_app_ids_for_developer(12345)
    assert app_ids == [101, 202]


def test_get_multiple_app_details_forwards_timeout(monkeypatch):
    scraper = AppStoreScraper()
    captured = {}

    def fake_get_app_details(
        app_id,
        country="nl",
        lang="",
        add_ratings=False,
        flatten=True,
        sleep=None,
        force=False,
        timeout=None,
    ):
        captured["timeout"] = timeout
        return {"trackId": app_id}

    monkeypatch.setattr(scraper, "get_app_details", fake_get_app_details)

    results = list(scraper.get_multiple_app_details([999], timeout=7))
    assert results == [{"trackId": 999}]
    assert captured["timeout"] == 7


def test_get_app_details_reports_http_429(monkeypatch):
    scraper = AppStoreScraper()

    class FakeResponse:
        def __init__(self):
            self.status_code = 429
            self.reason = "Too Many Requests"

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, tb):
            return False

        def raise_for_status(self):
            raise requests.HTTPError(response=self)

        def json(self):
            raise AssertionError("JSON parsing should not be attempted on HTTP errors")

    def fake_get(*args, **kwargs):
        return FakeResponse()

    monkeypatch.setattr(scraper_module.requests, "get", fake_get)

    with pytest.raises(AppStoreException, match="429|rate limit"):
        scraper.get_app_details("1625453623")
