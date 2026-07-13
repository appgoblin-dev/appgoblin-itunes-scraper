from appgoblin_itunes_scraper.scraper import AppStoreScraper


class ScraperSteps:
    def __init__(self, context):
        self.context = context

    def setup_scraper(self):
        self.context.scraper = AppStoreScraper()

    def search_for_term(self, search_term):
        self.context.results = self.context.scraper.get_app_ids_for_query(
            search_term, country="gb", lang="en"
        )

    def assert_result_count(self, text):
        assert len(self.context.results) == int(text)

    def assert_result_length(self, json_len):
        assert len(self.context.results) == int(json_len)

    def assert_title(self, text):
        assert self.context.results["trackName"] == text

    def search_for_result_from_mindful(self):
        results = self.context.scraper.get_app_ids_for_query(
            "mindful", country="gb", lang="en"
        )
        self.context.results = self.context.scraper.get_similar_app_ids_for_app(
            results[0]
        )

    def search_for_topic_topfreeapplications(self):
        self.context.results = self.context.scraper.get_app_ids_for_collection(
            collection="topfreeapplications", category="", num=50, country="gb"
        )

    def search_for_developer(self):
        self.context.results = self.context.scraper.get_app_ids_for_developer(
            "384434796", country="gb"
        )

    def search_for_app_with_id(self, app_id):
        self.context.results = self.context.scraper.get_app_details(
            app_id, country="gb"
        )

    def search_for_num_apps(self, num_apps):
        apps = self.context.scraper.get_app_ids_for_query(
            "mindful", country="gb", lang="en", num=num_apps
        )
        self.context.results = list(
            self.context.scraper.get_multiple_app_details(apps, country="gb")
        )

    def search_for_another_num_apps(self, num_apps):
        apps = self.context.app_id + self.context.scraper.get_app_ids_for_query(
            "mindful", country="gb", lang="en", num=num_apps
        )
        self.context.results = list(
            self.context.scraper.get_multiple_app_details(apps, country="gb")
        )

    def define_incorrect_app_id(self, app_id):
        self.context.app_id = [int(app_id)]
