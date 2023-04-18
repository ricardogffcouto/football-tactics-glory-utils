import logging
import uuid

import cv2
import re

import easyocr
from keras.utils import load_img, img_to_array

from constants import *

from dataclasses import dataclass, field
from PIL import Image
from keras.models import load_model
import numpy as np

skills_model = load_model(SKILLS_MODEL_FILE)
skill_level_model = load_model(SKILL_LEVEL_MODEL_FILE)
reader = easyocr.Reader(['en'])

logger = logging.getLogger(__name__)

def clean(text):
    if isinstance(text, str):
        return re.sub(r'[^\x20-\x7E]', '', text)
    return text

def clean_and_set(player, attr, text):
    expected_type = Player.__annotations__[attr]

    text = clean(text)

    if not text:
        setattr(player, attr, None)
        return None

    if expected_type == int:
        try:
            text = int(text)
        except:
            text = None

    setattr(player, attr, text)
    return text

@dataclass
class Team:
    id: uuid.uuid4
    name: str = None
    players: list = field(default_factory=list)
    country: str = None
    league: str = None

@dataclass
class Player:
    team_id: uuid.uuid4
    player_i: int
    id: uuid.uuid4 = field(default_factory=uuid.uuid4)
    team_name: str = None
    league_i: int = None
    pos: str = None
    name: str = None
    gift: int = None
    info: str = None
    acc: int = None
    pas: int = None
    df: int = None
    ctr: int = None
    lvl: int = None
    age: int = None
    sk_pot: int = None
    skill_1: str = None
    skill_2: str = None
    skill_1_level: int = None
    skill_2_level: int = None
    is_invalid: bool = False
    is_filtered: bool = False

    def is_equal_to(self, other):
        if self.is_filtered and other.is_filtered or self.is_invalid and other.is_invalid:
            return False
        attr_list = ["gift", "pos", "acc", "pas", "df", "ctr", "lvl", "age"]
        return sum(getattr(self, attr) == getattr(other, attr) for attr in attr_list) / len(attr_list) >= 0.8

    def set_skill_potential(self):
        self.sk_pot = 5 + self.gift if self.gift else None

    def validate_age(self):
        if self.age and not (self.age >= 16 and self.age <= 40):
            self.age = None

    def validate_lvl(self):
        if self.lvl and not (self.lvl >= 1 and self.lvl <= 100):
            self.lvl = None

    def validate_pos(self):
        if self.pos and self.pos not in POSITIONS:
            self.pos = None

    def validate_attributes(self):
        if self.lvl:
            if self.lvl <= 25:
                allowed = self.lvl * 3
            elif self.lvl <= 50:
                allowed = self.lvl * 2.75
            else:
                allowed = self.lvl * 2.5
            if self.acc and self.acc > allowed:
                self.acc = None
            if self.pas and self.pas > allowed:
                self.pas = None
            if self.df and self.df > allowed:
                self.df = None
            if self.ctr and self.ctr > allowed:
                self.ctr = None



@dataclass
class TeamParser:
    team_id: uuid.uuid4
    session_id: uuid.uuid4
    config: dict = field(default_factory=dict)

    @property
    def path(self):
        return f"{SCREENSHOT_PATH}/{self.session_id}/screenshots/{self.team_id}"

    def get_player_image_filenames(self, player_i):
        return [f"{self.path}/{p}" for p in os.listdir(self.path) if p.startswith(f"player_{player_i}_")]

    def get_name_and_country(self):
        team_name = reader.readtext(f"{self.path}/team_name.png")
        if len(team_name):
            team_name = team_name[0][1]
            return clean(team_name)
        return None


    def parse_players(self):
        players = []
        invalid_players = 0
        team_name = self.get_name_and_country()

        for player_i in range(PLAYERS_PER_LIST * 2 - 1):
            if self.config.get("only_players") and player_i not in self.config.get("only_players"):
                continue

            player_parser = PlayerParser(
                image_filenames=self.get_player_image_filenames(player_i),
                team_name=team_name,
                team_id=self.team_id,
                player_i=player_i,
                config=self.config
            )

            logger.info(f"Parsing player {player_i + 1}")

            player = None

            try:
                player = player_parser.parse()
            except Exception as e:
                logger.warning(f"Error parsing player {player_i + 1} from {self.team_id}: {e}")

            if not player or player.is_invalid:
                logger.warning("Player is invalid")
                invalid_players += 1
                if invalid_players >= 3:
                    break
                continue

            if player_i >= PLAYERS_PER_LIST and len(list(filter(lambda pl: player.is_equal_to(pl), players))) > 0:
                logger.warning("Duplicate player found! Team complete.")
                break

            players.append(player)

        return players


@dataclass
class PlayerParser:
    image_filenames: list
    team_id: uuid.uuid4
    player_i: int
    team_name: str = None
    config: dict = field(default_factory=dict)

    def get_filename_by_key(self, key):
        return [f for f in self.image_filenames if key in f.split("/")[-1]][0]

    def get_image_by_key(self, key, flag=cv2.IMREAD_UNCHANGED):
        filename = self.get_filename_by_key(key)
        return cv2.imread(filename, flag)

    def get_text_from_image(self, img, config={}):
        if config.get("allowlist"):
            text = reader.readtext(img, allowlist=config.get("allowlist"))
        else:
            text = reader.readtext(img)
        if len(text):
            return text[0][1]
        return None
    def get_name(self, name_img):
        return self.get_text_from_image(name_img)

    def get_pos(self, pos_img):
        text = self.get_text_from_image(pos_img)
        if text:
            return text.upper()
        return None

    def get_attribute(self, attr_img):
        return self.get_text_from_image(attr_img, config={"allowlist": "0123456789"})

    def get_skill(self, skill_filename):
        img = load_img(skill_filename, target_size=TARGET_SIZE)
        img = img_to_array(img)
        img = np.expand_dims(img, axis=0)
        img = img / 255

        pred = skills_model.predict(img)
        label = sorted(SKILLS)[np.argmax(pred)]
        if label == "None":
            return None
        return label

    def get_skill_level(self, skill_lvl_filename):
        skill_lvl_img = Image.open(skill_lvl_filename)
        skill_lvl_img = skill_lvl_img.crop((
            SKILL_LEVEL["X1"], SKILL_LEVEL["Y1"], SKILL_LEVEL["X2"], SKILL_LEVEL["Y2"]
        ))
        img = skill_lvl_img.resize(TARGET_SIZE, resample=Image.BICUBIC)
        img = img_to_array(img)
        img = np.expand_dims(img, axis=0)
        img = img / 255

        pred = skill_level_model.predict(img)
        label = [1, 2, 3][np.argmax(pred)]

        return label

    def get_sk_pot(self, skill_pot_img):
        skill_pot_img = skill_pot_img[SKILL_POT["Y1"]:SKILL_POT["Y2"], SKILL_POT["X1"]:SKILL_POT["X2"]]
        return self.get_text_from_image(skill_pot_img)

    def get_gift(self, gift_img):
        def _has_star(img):
            star = img[0:5, :]
            min_val = np.min(star)
            max_val = np.max(star)
            if min_val == max_val:
                return False

            height, width = img.shape
            center_x = int(width / 2)
            center_y = int(height / 2) - 2
            return img[center_y, center_x] == 0

        gift_img = gift_img[0:PLAYERS_TABLE["GIFT_H"] - 5, :]
        gift = 0
        for gift in range(MAX_GIFT):
            x1 = gift_img.shape[1] - (gift + 1) * PLAYERS_TABLE["STAR_W"]
            x2 = gift_img.shape[1] - gift * PLAYERS_TABLE["STAR_W"]
            star_img = gift_img[:, x1:x2]
            if _has_star(star_img):
                gift += 1
            else:
                break

        return min(gift, MAX_GIFT)

    def get_info(self, info_img):
        info_img = info_img[PLAYERS_TABLE["GIFT_H"]:, :]
        return self.get_text_from_image(info_img)

    def get_price_glory(self, price_glory_img):
        raise NotImplementedError

    def set_value(self, player, key, img):
        if key in ["acc", "pas", "df", "ctr", "age", "lvl"]:
            text = self.get_attribute(img)
        elif key == "skill_1":
            text = self.get_skill(img)
        elif key == "skill_1_level":
            if not player.skill_1:
                return
            text = self.get_skill_level(img)
        elif key == "skill_2":
            if not player.skill_1:
                return
            text = self.get_skill(img)
        elif key == "skill_2_level":
            if not player.skill_2:
                return
            text = self.get_skill_level(img)
        else:
            text = getattr(self, f"get_{key}")(img)

        return clean_and_set(player, key, text)

    def set_key_value(self, player, key):
        ignore_keys = ["info", "end", "pos_img"]

        if key in ignore_keys:
            return

        if key in ["skill_1", "skill_2"]:
            current_img = self.get_filename_by_key(key)
        else:
            current_img = self.get_image_by_key(key)

        if key in SPLIT_PLAYER_KEYS:
            for k in SPLIT_PLAYER_KEYS[key]:
                if k in ignore_keys:
                    return
                self.set_value(player, k, current_img)
        else:
            self.set_value(player, key, current_img)

    def is_player_key_valid(self, player, key):
        key_filter = self.config.get("filter_players", {}).get(key)
        if key_filter:
            if key == "pos":
                return getattr(player, key) in key_filter
            if key == "skills":
                return player.skill_1 in key_filter or player.skill_2 in key_filter
            if isinstance(key_filter, list):
                return key_filter[0] <= getattr(player, key) <= key_filter[1]
        return True

    def parse(self):
        player = Player(team_name=self.team_name, team_id=self.team_id, player_i=self.player_i)

        for key in self.config.get("filter_players", {}):
            if key == "skills":
                self.set_key_value(player, "skill_1")
                self.set_key_value(player, "skill_2")
            else:
                self.set_key_value(player, key)
            if not self.is_player_key_valid(player, key):
                player.is_filtered = True
                logger.info(f"Stopped parsing player {self.player_i + 1}. Filtered.")
                return player

        player_coordinates = [coordinate for coordinate in PLAYER_COORDINATES if coordinate not in self.config.get("filter_players", {})]
        if self.config.get("filter_players", {}).get("skills"):
            player_coordinates = [coordinate for coordinate in player_coordinates if coordinate not in ["skill_1", "skill_2"]]

        for key in player_coordinates:
            self.set_key_value(player, key)

        return player
