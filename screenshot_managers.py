import logging
from dataclasses import dataclass, field

import numpy as np
import pyautogui as pg
import uuid
import time
import cv2

from constants import *
import utils.transforms as tf

logger = logging.getLogger(__name__)

@dataclass
class PlayerScreenshotManager:
    team_id: uuid.uuid4
    player_img: np.ndarray
    player_i: int
    config: dict = field(default_factory=dict)

    @property
    def folder_path(self):
        return f"screenshots/{self.config.get('session_id', None)}/screenshots/team_{self.team_id}/"

    def get_name(self, name_img):
        return tf.image_preprocess(name_img, is_label_light=False)

    def get_pos(self, pos_img):
        return tf.image_preprocess(pos_img, is_label_light=True)

    def get_attribute(self, attr_img):
        return tf.image_preprocess(attr_img, is_label_light=True)

    def get_skill(self, skill_img):
        return skill_img

    def get_gift(self, gift_img):
        gift_img = gift_img[0:PLAYERS_TABLE["GIFT_H"] - 5, :]
        return tf.image_preprocess(gift_img, is_label_light=False)

    def get_info(self, info_img):
        return tf.image_preprocess(info_img, is_label_light=False)

    def get_price_glory(self, price_glory_img):
        raise NotImplementedError

    def save_img(self, key, img):
        if key in ["info", "skill_1_level", "skill_2_level"]:
            return
        if key in ["acc", "pas", "df", "ctr", "age", "lvl"]:
            image = self.get_attribute(img)
        elif key == "skill_1":
            image = self.get_skill(img)
        elif key == "skill_2":
            image = self.get_skill(img)
        else:
            image = getattr(self, f"get_{key}")(img)

        filename = f"{self.folder_path}/player_{self.player_i}_{key}.png"
        
        cv2.imwrite(filename, image)


    def save(self):
        for i, coordinate in enumerate(PLAYER_COORDINATES.items()):
            key, x1 = coordinate

            if key in ["end", "pos_img"]:
                continue

            if self.config.get("only_skills"):
                if not key.startswith("skill"):
                    continue

            next_key, x2 = list(PLAYER_COORDINATES.items())[i + 1]

            current_img = self.player_img[:, x1:x2]

            if key in SPLIT_PLAYER_KEYS:
                for k in SPLIT_PLAYER_KEYS[key]:
                    self.save_img(k, current_img)
            else:
                self.save_img(key, current_img)


@dataclass
class TeamScreenshotManager:
    team_id: uuid.uuid4 = field(default_factory=uuid.uuid4)
    team_imgs: list[str] = field(default_factory=list)
    config: dict = field(default_factory=dict)

    @property
    def folder_path(self):
        return f"screenshots/{self.config.get('session_id', None)}/screenshots/team_{self.team_id}/"

    def show_reserve_players(self):
        pg.moveTo(SCROLL_X, SCROLL_Y1)
        pg.mouseDown(button="left")
        pg.moveTo(SCROLL_X, SCROLL_Y2)
        pg.mouseUp(button="left")

    def save_screenshot_team_name(self):
        team_name_img = pg.screenshot(region=tf.to_region(TEAM_NAME))
        team_name_img = tf.get_img_from_screenshot(team_name_img)
        team_name_img = tf.image_preprocess(team_name_img, is_label_light=False)

        if not os.path.exists(self.folder_path):
            os.makedirs(self.folder_path)
        cv2.imwrite(f"{self.folder_path}/team_name.png", team_name_img)

    def save_screenshot_player_table(self):
        team_img = pg.screenshot(region=tf.to_region(PLAYERS_TABLE))
        self.team_imgs.append(team_img)

    def save_screenshot_player_price(self, player_id):
        pg.click(BUY_BTN_X, BTN_Y)
        time.sleep(0.1)
        player_price_img = pg.screenshot(region=tf.to_region(PLAYER_PRICE))
        self.player_price_imgs[player_id] = player_price_img

    def save_player_price_player_table(self, reserves):
        for i in range(PLAYERS_PER_LIST):
            height = PLAYERS_TABLE["PLAYER_H"] * (i if not reserves else PLAYERS_PER_LIST - i)
            player_id = uuid.uuid4()
            self.player_ids.append(player_id)
            pg.click(PLAYERS_TABLE["INITIAL_X"], PLAYERS_TABLE["FIRST_PLAYER_Y"] + height)
            self.save_screenshot_player_price(player_id)
            pg.click(button="right")

    def save_player_prices(self):
        self.player_prices = []
        self.save_player_price_player_table(reserves=False)
        self.show_reserve_players()
        self.save_player_price_player_table(reserves=True)

    def get_player_imgs(self):
        player_imgs = []

        for i, image in enumerate(self.team_imgs):
            img = tf.get_img_from_screenshot(image)
            for p in range(PLAYERS_PER_LIST):
                ix = p if i == 0 else p + PLAYERS_PER_LIST

                if ix + 1 == 12:
                    continue

                if i == 0:
                    y1 = (PLAYERS_TABLE["PLAYER_H"] + PLAYERS_TABLE["PLAYER_GAP"]) * p
                    y2 = y1 + PLAYERS_TABLE["PLAYER_H"]
                else:
                    y1 = img.shape[0] - (PLAYERS_TABLE["PLAYER_H"] + PLAYERS_TABLE["PLAYER_GAP"]) * (p + 1)
                    y2 = y1 + PLAYERS_TABLE["PLAYER_H"]

                player_img = img[y1:y2, :]

                player_imgs.append(player_img)

        return player_imgs

    def save(self):
        logger.info(f"Saving team {self.team_id}")
        time.sleep(0.1)
        self.save_screenshot_team_name()
        self.save_screenshot_player_table()
        self.show_reserve_players()
        self.save_screenshot_player_table()
        player_imgs = self.get_player_imgs()
        for player_i, player_img in enumerate(player_imgs):
            player_manager = PlayerScreenshotManager(
                config=self.config,
                team_id=self.team_id,
                player_i=player_i,
                player_img=player_img
            )
            player_manager.save()

@dataclass
class LeagueScreenshotManager:
    team_amount: int
    config: dict = field(default_factory=dict)

    def save(self):
        logger.info(f"Saving league...")
        for team_i in range(self.team_amount):
            team = TeamScreenshotManager(
                config=self.config
            )

            y = TABLE_INITIAL_Y + TABLE_H * team_i
            if team_i == ELEMENTS_PER_TABLE:
                y = TABLE_18_Y

            pg.click(TABLE_X, y)
            pg.click(BTN_X, BTN_Y)
            team.save()
            pg.click(button="right")

@dataclass
class CountryScreenshotManager:
    config: dict = field(default_factory=dict)

    def save(self):
        logger.info("Saving country...")
        parse_five_divisions = self.config.get("has_five_divisions") and not self.config.get("first_division_only")
        division_teams = DIVISION_TEAMS_FULL if parse_five_divisions else DIVISION_TEAMS_PREMIER

        for division_i, team_amount in enumerate(division_teams):
            if parse_five_divisions:
                pg.click(DIVISION_INITIAL_X + DIVISION_W * division_i, DIVISION_Y)
            league = LeagueScreenshotManager(
                config=self.config,
                team_amount=team_amount,
            )
            league.save()

@dataclass
class ContinentScreenshotManager:
    country_amount: int
    config: dict = field(default_factory=dict)

    def show_bottom_countries(self):
        pg.moveTo(SCROLL_X, SCROLL_Y1)
        pg.mouseDown(button="left")
        pg.moveTo(SCROLL_X, SCROLL_Y2)
        pg.mouseUp(button="left")

    def save(self):
        logger.info(f"Saving continent...")
        for country_i in range(self.country_amount):
            if self.config.get("skip_countries"):
                if country_i + 1 in self.config.get("skip_countries"):
                    continue

            if country_i == ELEMENTS_PER_TABLE:
                self.show_bottom_countries()

            if country_i < ELEMENTS_PER_TABLE:
                y = TABLE_INITIAL_Y + TABLE_H * country_i
            else:
                y = TABLE_18_Y - (TABLE_H / 2) - TABLE_H * (country_i - ELEMENTS_PER_TABLE)

            country = CountryScreenshotManager(config=self.config)

            pg.click(TABLE_X, y)
            pg.click(BTN_X, BTN_Y)

            country.save()

            pg.click(button="right")

@dataclass
class FullScreenshotManager:
    screenshots_id: str
    country_amount: int
    current_country_rank: int

    def save(self):
        your_country_manager = CountryScreenshotManager(config={"has_five_divisions": True, "session_id": self.screenshots_id})
        your_country_manager.save()
        pg.moveTo(740, 80)
        pg.click()
        continent = ContinentScreenshotManager(
            country_amount=self.country_amount,
            config={"skip_countries": [self.current_country_rank], "session_id": self.screenshots_id},
        )
        continent.save()


