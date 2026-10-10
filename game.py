import asyncio
import random

from heroes import DIFFICULTIES, heroes_for_difficulty, hero_total, hero_pic_line
from football import FOOTBALL_PLAYERS, player_ovr
from locales import get_text_by_lang

# Сколько игроков каждой позиции случайно попадает в пул лотов за одну игру (катку)
FOOTBALL_POOL_COUNTS = {"GK": 3, "DF": 8, "MF": 8, "FW": 8}

# Режим «до конца денег»: сколько героев в пуле в зависимости от числа игроков
MONEY_POOL_SIZES = {2: 15, 3: 25, 4: 30}

# На сколько можно повысить ставку за один ход
BID_STEPS = [1, 2, 3, 5, 10, 15, 20, 25]

# Герои → Классический: свой бюджет, слоты, шаги ставок и лимит скипов
CLASSIC_HEROES_BUDGET = 20
CLASSIC_HEROES_TEAM_SIZE = 4
CLASSIC_HEROES_BID_STEPS = [1, 2, 3, 5, 7]
CLASSIC_HEROES_MAX_SKIPS = 2


def _err(key, **params):
    """Ошибка для бота: ключ из locales + параметры для подстановки."""
    return (key, params)


def build_football_pool():
    """Случайно набирает лоты на одну игру: 3 GK, 8 DF, 8 MF, 8 FW (27 футболистов)."""
    by_pos = {"GK": [], "DF": [], "MF": [], "FW": []}
    for p in FOOTBALL_PLAYERS:
        pos = p.get("position")
        if pos in by_pos:
            by_pos[pos].append(p)

    pool = []
    for pos, need in FOOTBALL_POOL_COUNTS.items():
        candidates = by_pos[pos]
        chosen = random.sample(candidates, min(need, len(candidates)))
        for c in chosen:
            pool.append({
                "name": c["name"],
                "position": pos,
                "power": player_ovr(c),
            })
    random.shuffle(pool)
    return pool


def format_hero_card(hero, lang="ru"):
    t = lambda k: get_text_by_lang(lang, k)
    pic_line = hero_pic_line(hero)
    pic_block = f"\n<code>{pic_line}</code>" if pic_line else ""
    return (
        f"🃏 <b>{hero['name']}</b>\n"
        f"{t('card_universe')}: <b>{hero['universe']}</b>\n"
        f"{t('card_power')}: <b>{hero['power']}</b>   {t('card_speed')}: <b>{hero['speed']}</b>   "
        f"{t('card_int')}: <b>{hero['intelligence']}</b>\n"
        f"{t('card_total')}: <b>{hero_total(hero)}</b>"
        f"{pic_block}"
    )


def format_football_card(hero, lang="ru"):
    t = lambda k: get_text_by_lang(lang, k)
    pos_str = get_text_by_lang(lang, "positions").get(hero["position"], hero["position"])
    return (
        f"⚽ <b>{hero['name']}</b>\n"
        f"{t('card_position')}: <b>{pos_str}</b>\n"
        f"{t('card_rating')}: <b>{hero['power']}</b>"
    )


class PlayerState:
    def __init__(self, user_id, name, budget, username=None):
        self.user_id = user_id
        self.name = name
        self.username = username
        self.budget = budget
        self.team = []
        self.skips_used = 0   # сколько скипов уже потрачено (лимит только в героях → классический)


class AuctionState:
    def __init__(self, hero, current_bid, current_bidder_id, turn_id):
        self.hero = hero
        self.current_bid = current_bid
        self.current_bidder_id = current_bidder_id
        self.turn_id = turn_id
        self.history = []       # [(имя, ставка)] — ставки по этому лоту
        self.auto_passed = []   # user_id тех, кто автоматически спасовал (нечем перебить)


class Game:
    def __init__(self, chat_id, creator_id, creator_name, category="heroes",
                 creator_username=None, mode="classic", difficulty="hard"):
        self.chat_id = chat_id
        self.category = category
        self.budget_start = 100
        self.min_players = 2
        self.bid_steps = BID_STEPS
        self.max_skips = None   # None — скипы без лимита

        # Режим «до конца денег» есть только у супергероев
        self.mode = "money" if (category == "heroes" and mode == "money") else "classic"
        self.unlimited = self.mode == "money"
        self.classic_heroes = category == "heroes" and not self.unlimited

        # Сложность (набор героев) есть только у супергероев: easy / normal / hard
        self.difficulty = difficulty if (category == "heroes" and difficulty in DIFFICULTIES) else "hard"

        if category == "football":
            self.category_key = "cat_football"
            self.card_func = format_football_card
            self.team_size = 11
            self.max_players = 2
            pool = build_football_pool()
        else:
            self.category_key = "cat_heroes"
            self.card_func = format_hero_card
            self.max_players = 4
            if self.unlimited:
                self.team_size = None      # слотов нет — покупаем, пока есть деньги
                pool = []                  # пул набирается при старте (зависит от числа игроков)
            else:
                self.team_size = CLASSIC_HEROES_TEAM_SIZE
                self.budget_start = CLASSIC_HEROES_BUDGET
                self.bid_steps = CLASSIC_HEROES_BID_STEPS
                self.max_skips = CLASSIC_HEROES_MAX_SKIPS
                pool = heroes_for_difficulty(self.difficulty)

        random.shuffle(pool)
        self.hero_pool = pool
        self.hero_index = 0

        self.players = {creator_id: PlayerState(creator_id, creator_name, self.budget_start, username=creator_username)}
        self.player_order = [creator_id]

        self.started = False
        self.finished = False
        self.end_announced = False
        self.end_message_id = None   # сообщение с итогами (кнопки «битва» / «победитель»)
        self.reveal_text = None      # полный текст итогов с победителем (показывается по кнопке)
        self.battle_data = None      # данные для ИИ-битвы
        self.battle_busy = False
        self.revealed = False
        self.auction = None
        self.passed_players = set()

        self.last_message_id = None
        self.lot_message_ids = []   # сообщения с раскрытыми картами лотов — удаляются после игры
        self.pending_events = []
        self.lobby_message_id = None

        # Лоты, которые все скипнули. Если в конце у кого-то не хватает игроков — возвращаются в аукцион
        self.skipped_lots = []
        self.leftover_round = False  # True, когда идёт повторный круг по скипнутым лотам

        # Служебное для бота: блокировка, таймеры
        self.lock = asyncio.Lock()
        self.lobby_task = None
        self.timer_task = None
        self.turn_token = 0

    # ---------- лобби ----------

    def add_player(self, user_id, name, username=None):
        if self.started:
            return False, _err("err_game_started")
        if user_id in self.players:
            return False, _err("err_already_in")
        if len(self.players) >= self.max_players:
            return False, _err("err_max_players", n=self.max_players)
        self.players[user_id] = PlayerState(user_id, name, self.budget_start, username=username)
        self.player_order.append(user_id)
        return True, None

    def can_begin(self):
        return len(self.players) >= self.min_players and not self.started and not self.finished

    def begin(self):
        if self.started:
            return
        self.started = True
        if self.unlimited:
            size = MONEY_POOL_SIZES.get(len(self.players), 15)
            candidates = heroes_for_difficulty(self.difficulty)
            pool = random.sample(candidates, min(size, len(candidates)))
            random.shuffle(pool)
            self.hero_pool = pool
        self._start_next_auction()

    # ---------- помощники ----------

    def team_full(self, user_id):
        return self.team_size is not None and len(self.players[user_id].team) >= self.team_size

    def slots_left(self, user_id):
        if self.team_size is None:
            return None
        return self.team_size - len(self.players[user_id].team)

    def skips_left(self, user_id):
        """Сколько скипов осталось у игрока (None — без лимита)."""
        if self.max_skips is None:
            return None
        return max(0, self.max_skips - self.players[user_id].skips_used)

    def can_skip(self, user_id):
        left = self.skips_left(user_id)
        return left is None or left > 0

    def can_act(self, user_id):
        """Игрок ещё участвует в торгах: есть место в команде и деньги."""
        return (not self.team_full(user_id)) and self.players[user_id].budget > 0

    def max_bid(self, user_id):
        """Максимальная ставка. В обычном режиме нужно оставить $1 на каждый недостающий слот."""
        p = self.players[user_id]
        left = self.slots_left(user_id)
        if left is None:
            return p.budget
        return min(p.budget, max(1, p.budget - (left - 1)))

    def _nobody_can_act(self):
        return not any(self.can_act(uid) for uid in self.player_order)

    def _finish(self):
        self.auction = None
        self.finished = True

    def _rivals(self, user_id):
        """Соперники, которые ещё участвуют в торгах за текущий лот (не скипнули/не спасовали)."""
        return [
            uid for uid in self.player_order
            if uid != user_id and uid not in self.passed_players and self.can_act(uid)
        ]

    def valid_bid_options(self, user_id):
        a = self.auction
        if not a or not self.can_act(user_id):
            return []
        cap = self.max_bid(user_id)

        # Все остальные уже скипнули этот лот — его можно только взять за $1
        if a.current_bid == 0 and not self._rivals(user_id):
            return [1] if cap >= 1 else []

        return [a.current_bid + s for s in self.bid_steps if a.current_bid + s <= cap]

    # ---------- ход аукциона ----------

    def _return_skipped_lots(self):
        """Лоты закончились, но у кого-то команда неполная — возвращаем скипнутые лоты в аукцион.
        В режиме «до конца денег» лоты не возвращаются: закончились герои — игра окончена."""
        if self.unlimited or not self.skipped_lots:
            return False
        if self._nobody_can_act():
            return False
        lots = self.skipped_lots
        self.skipped_lots = []
        random.shuffle(lots)
        self.hero_pool.extend(lots)
        self.leftover_round = True
        self.pending_events.append({"type": "skipped_returned", "count": len(lots)})
        return True

    def _start_next_auction(self):
        """Переходит к следующему лоту, автоматически разыгрывая лоты, где участвовать может только один."""
        while True:
            if self._nobody_can_act():
                self._finish()
                return
            if self.hero_index >= len(self.hero_pool):
                if not self._return_skipped_lots():
                    self._finish()
                    return

            hero = self.hero_pool[self.hero_index]
            active = [uid for uid in self.player_order if self.can_act(uid)]

            if len(active) == 1:
                # Остальные не могут участвовать (команда полная или нет денег) — лот за $1
                winner = self.players[active[0]]
                winner.budget -= 1
                winner.team.append(hero)
                self.pending_events.append({
                    "type": "auto_award",
                    "hero": hero,
                    "winner_id": winner.user_id,
                    "price": 1,
                })
                self.hero_index += 1
                continue

            # Первым ходит тот, кто реально может участвовать (по кругу)
            first_bidder = active[self.hero_index % len(active)]
            self.auction = AuctionState(
                hero=hero,
                current_bid=0,
                current_bidder_id=None,
                turn_id=first_bidder,
            )
            self.passed_players = set()
            return

    def _after_lot(self):
        """Лот разыгран (куплен или скипнут) — переходим к следующему."""
        self.hero_index += 1
        self._start_next_auction()

    def _award_lot(self, winner_id, price):
        a = self.auction
        winner = self.players[winner_id]
        winner.budget -= price
        winner.team.append(a.hero)
        res = {"winner_id": winner_id, "hero": a.hero, "price": price}
        self._after_lot()
        return res

    def _advance_turn(self, from_uid):
        """Передаёт ход следующему участнику. Тех, кто не может перебить ставку, пасует автоматически.
        Возвращает результат лота, если торги закончились, иначе None."""
        a = self.auction
        leader = a.current_bidder_id
        n = len(self.player_order)
        idx = self.player_order.index(from_uid)
        for i in range(1, n):
            uid = self.player_order[(idx + i) % n]
            if uid == leader or uid in self.passed_players or not self.can_act(uid):
                continue
            if a.current_bid > 0 and not self.valid_bid_options(uid):
                self.passed_players.add(uid)
                a.auto_passed.append(uid)
                continue
            a.turn_id = uid
            return None

        if a.current_bid > 0:
            return self._award_lot(leader, a.current_bid)

        # Ставок нет и никого не осталось — все скипнули
        hero = a.hero
        self.skipped_lots.append(hero)
        res = {"skipped": True, "hero": hero}
        self._after_lot()
        return res

    def _check_turn(self, user_id):
        a = self.auction
        if a is None:
            return _err("err_not_active")
        if a.turn_id != user_id:
            return _err("err_not_turn")
        if not self.can_act(user_id):
            return _err("err_cant_act")
        return None

    def place_bid(self, user_id, amount):
        """Возвращает (ok, err, result). result не None, если лот сразу достался (остальные не могут перебить)."""
        err = self._check_turn(user_id)
        if err:
            return False, err, None
        a = self.auction
        p = self.players[user_id]
        if amount > p.budget:
            return False, _err("err_over_budget", budget=p.budget), None
        if amount <= a.current_bid:
            return False, _err("err_bid_low", bid=a.current_bid), None
        if amount not in self.valid_bid_options(user_id):
            return False, _err("err_bad_option"), None

        a.current_bid = amount
        a.current_bidder_id = user_id
        a.history.append((p.name, amount))
        return True, None, self._advance_turn(user_id)

    def skip_lot(self, user_id):
        """Скип: «мне этот лот не нужен». Доступен, пока никто не сделал ставку."""
        err = self._check_turn(user_id)
        if err:
            return False, err, None
        a = self.auction
        if a.current_bid > 0:
            return False, _err("err_skip_after_bid"), None
        if self.leftover_round:
            return False, _err("err_skip_leftover"), None
        if not self.can_skip(user_id):
            return False, _err("err_skip_limit", n=self.max_skips), None
        self.players[user_id].skips_used += 1
        self.passed_players.add(user_id)
        return True, None, self._advance_turn(user_id)

    def pass_bid(self, user_id):
        """Пас: «сдаюсь в гонке за игрока» — лот уходит сопернику по текущей ставке."""
        err = self._check_turn(user_id)
        if err:
            return False, err, None
        a = self.auction
        if a.current_bid <= 0:
            return False, _err("err_pass_no_bid"), None
        self.passed_players.add(user_id)
        return True, None, self._advance_turn(user_id)

    # ---------- подсчёт силы ----------

    def team_power(self, user_id):
        p = self.players[user_id]

        if self.category == "heroes":
            raw = sum(hero_total(h) for h in p.team)
        else:
            raw = sum(h["power"] for h in p.team)

        if self.category == "football":
            counts = {"GK": 0, "DF": 0, "MF": 0, "FW": 0}
            for h in p.team:
                pos = h.get("position")
                if pos in counts:
                    counts[pos] += 1

            reqs = {"GK": 1, "DF": 3, "MF": 3, "FW": 3}
            multiplier = 1.0
            pos_detail = {}

            for pos, req_cnt in reqs.items():
                actual = counts[pos]
                matched = actual >= req_cnt
                pos_detail[pos] = {"count": actual, "threshold": req_cnt, "matched": matched}
                if matched:
                    multiplier += 0.15
                else:
                    multiplier -= 0.15

            multiplier = max(multiplier, 0.2)
            final_power = round(raw * multiplier)
            return final_power, {
                "raw": raw,
                "multiplier": round(multiplier, 2),
                "position_detail": pos_detail,
            }
        else:
            univ_counts = {}
            for h in p.team:
                u = h["universe"]
                univ_counts[u] = univ_counts.get(u, 0) + 1

            bonus_mult = 1.0
            bonuses = []
            for u, cnt in univ_counts.items():
                if cnt >= 3:
                    bonus_mult += 0.20
                    bonuses.append(f"{u} (x{cnt})")
                elif cnt == 2:
                    bonus_mult += 0.10
                    bonuses.append(f"{u} (x2)")

            final_power = round(raw * bonus_mult)
            return final_power, {
                "raw": raw,
                "multiplier": round(bonus_mult, 2),
                "bonus_universes": bonuses,
            }
