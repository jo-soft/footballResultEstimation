from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from core.gameData import MatchData, Goal, NormalizedGameDataCollection
import itertools as it

import re


class UefaCrawler:

    def __init__(self, year, normalizers):
        self.url = "http://www.uefa.com/uefaeuro/season={}/matches/all/index.html".format(year)
        self.normalizer = normalizers

    def __enter__(self):
        self.driver = webdriver.Firefox()
        self.driver.get(self.url)

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.driver:
            self.driver.close()

    def _get_game_links(self, length):

        selector = ".session .status a.mr"

        class ElementCountUnchanged(object):

            def __init__(self, selector):
                super(ElementCountUnchanged, self).__init__()
                self.old_selector_count = 0
                self.selector = selector

            def __call__(self, driver):
                el = driver.find_elements_by_css_selector(selector)
                count = len(el)
                if 0 < count == self.old_selector_count:
                    return True
                self.old_selector_count = count
                return False

        WebDriverWait(self.driver, 60).until(
            ElementCountUnchanged(selector)
        )
        full_stat_links = self.driver.find_elements_by_css_selector(selector)[:length]
        return [item.get_attribute('href') for item in full_stat_links]

    def get_game_stats_link(self, length):
        game_links = self._get_game_links(length)

        def make_game_stats_link(link):
            return link.replace(
                '/index.html',
                '/postmatch/statistics/index.html')

        return map(make_game_stats_link,game_links)

    def get_game_data(self, game_url):

        def parse_goals(goal_str):
            mk_goal = lambda t: Goal(t)
            m1 = map(mk_goal, re.findall("\d+", goal_str))

            m2 = map(mk_goal, re.findall("\d+\+\d", goal_str))
            return list(goal for goal in it.chain(m1, m2))


        self.driver.get(game_url)

        team1 = self.driver.find_element_by_css_selector("#teamHomeName a").text
        team2 = self.driver.find_element_by_css_selector("#teamAwayName a").text

        goals_team1 = list(it.chain(
            *(parse_goals(goalElement.text) for goalElement in self.driver.find_elements_by_css_selector("#resultHome li")
              if goalElement)
        ))
        goals_team2 = list(it.chain(
            *(parse_goals(goalElement.text) for goalElement in self.driver.find_elements_by_css_selector("#resultAway li")
              if goalElement)
        ))

        def get_value_by_text(text):

            class ResultObj(object):

                def __init__(self, val1, val2):
                    self.team1 = val1
                    self.team2 = val2

            td_text = self.driver.find_element_by_xpath(
                "//*[@class='statmatch']//td[contains(text(), '{}')]".format(text)
            )

            val_team1 = None
            try:
                val_team1 = int(td_text.find_element_by_xpath("preceding-sibling::td").text)
            except ValueError:
                pass

            val_team2 = None
            try:
                val_team2 = int(td_text.find_element_by_xpath("following-sibling::td").text)
            except ValueError:
                pass

            return ResultObj(
                val1=val_team1,
                val2=val_team2
            )

        possession = get_value_by_text("Possession (%)")
        total_attempts = get_value_by_text("Total attempts")
        on_target = get_value_by_text("on target")
        corners = get_value_by_text("Corners")
        offsides = get_value_by_text("Offsides")
        fouls_committed = get_value_by_text("Fouls committed")
        fouls_suffered = get_value_by_text("Fouls suffered")

        return MatchData(
            team1=team1,
            team2=team2,
            goals_team1=goals_team1,
            goals_team2=goals_team2,
            possession_team1=possession.team1,
            possession_team2=possession.team2,
            attempts_team1=total_attempts.team1,
            attempts_team2=total_attempts.team2,
            attempts_on_target_team1=on_target.team1,
            attempts_on_target_team2=on_target.team2,
            corners_team1=corners.team1,
            corners_team2=corners.team2,
            offside_team1=offsides.team1,
            offside_team2=offsides.team2,
            fouls_committed_team1=fouls_committed.team1,
            fouls_committed_team2=fouls_committed.team2,
            fouls_suffered_team1=fouls_suffered.team1,
            fouls_suffered_team2=fouls_suffered.team2
        )

    def get_normalized_game_data_collection(self, length=None):
        return NormalizedGameDataCollection(
            self.normalizer,
            (
                self.get_game_data(url)
                for url in list(self.get_game_stats_link(length))
            )
        )