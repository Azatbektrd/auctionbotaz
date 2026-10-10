import os
import sys

# Pydroid запускает скрипт через exec, поэтому __file__ может указывать не туда.
# Ищем папку, где лежит game.py, среди нескольких кандидатов.
def _find_base_dir():
    candidates = []
    try:
        candidates.append(os.path.dirname(os.path.abspath(__file__)))
    except NameError:
        pass
    if sys.argv and sys.argv[0]:
        candidates.append(os.path.dirname(os.path.abspath(sys.argv[0])))
    candidates.append(os.getcwd())
    candidates += [
        "/storage/emulated/0/auction",
        "/sdcard/auction",
        "/storage/emulated/0/Download/auction",
    ]
    for d in candidates:
        if os.path.exists(os.path.join(d, "game.py")):
            return d
    return candidates[0]


_BASE_DIR = _find_base_dir()
if _BASE_DIR not in sys.path:
    sys.path.insert(0, _BASE_DIR)
print("BASE_DIR:", _BASE_DIR, "| .env found:", os.path.exists(os.path.join(_BASE_DIR, ".env")))

import asyncio
import html
import logging
import os
import random

_ENV_PATH = os.path.join(_BASE_DIR, ".env")


def load_env_file(path):
    if not os.path.exists(path):
        return
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, _, value = line.partition("=")
            key = key.strip()
            value = value.strip().strip('"').strip("'")
            os.environ.setdefault(key, value)


load_env_file(_ENV_PATH)

from aiogram import Bot, Dispatcher, F, Router
from aiogram.exceptions import TelegramBadRequest, TelegramRetryAfter
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder

from game import Game
from heroes import DIFFICULTIES, hero_pic_line
from locales import CHAT_LANGUAGES, get_chat_lang, get_text, get_text_by_lang

import aiohttp
from heroes import hero_total

API_URL = "https://api.anthropic.com/v1/messages"
DEFAULT_MODEL = "claude-sonnet-5-5"
REQUEST_TIMEOUT = 90


def _gemini_key():
    return os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")


def has_api_key():
    return bool(_gemini_key() or os.environ.get("ANTHROPIC_API_KEY"))


def _team_lines(game, p):
    lines = []
    for h in p.team:
        if game.category == "football":
            lines.append(f"- {h['name']} ({h['position']}, рейтинг {h['power']})")
        else:
            lines.append(
                f"- {h['name']} ({h['universe']}; сила {h['power']}, скорость {h['speed']}, "
                f"интеллект {h['intelligence']}, всего {hero_total(h)})"
            )
    return "\n".join(lines) or "- (пусто)"


def build_battle_data(game, results):
    """results: [(power, PlayerState, detail)] — уже отсортирован по силе. Возвращает данные для промпта."""
    top = results[0][0]
    winners = [p.name for power, p, _ in results if power == top]
    teams = []
    for power, p, _ in results:
        teams.append({"name": p.name, "power": power, "lines": _team_lines(game, p)})
    return {"category": game.category, "teams": teams, "winners": winners}


def build_prompt(data, lang_name):
    is_football = data["category"] == "football"
    teams_block = "\n\n".join(
        f"=== Команда игрока «{t['name']}» (итоговая сила команды: {t['power']}) ===\n{t['lines']}"
        for t in data["teams"]
    )
    if len(data["winners"]) > 1:
        result_rule = (
            "РЕЗУЛЬТАТ (определён игрой, менять нельзя): НИЧЬЯ. Силы команд равны, "
            "в финале никто не может добить соперника."
        )
    else:
        winner = data["winners"][0]
        result_rule = (
            f"РЕЗУЛЬТАТ (определён игрой, менять нельзя): побеждает команда игрока «{winner}». "
            "Победа должна быть объяснена логикой боя: синергия команды, удачное использование "
            "сильных сторон, ошибка соперника. Проигравшие должны сражаться достойно, "
            "ключевые моменты у них тоже есть."
        )

    if is_football:
        return (
            "Ты — спортивный комментатор. Напиши захватывающий репортаж о футбольном матче "
            "между двумя командами из игроков ниже. Статы — это рейтинг игроков и позиции.\n\n"
            f"{teams_block}\n\n{result_rule}\n\n"
            "ТРЕБОВАНИЯ:\n"
            f"- Язык ответа: {lang_name}.\n"
            "- Структура: заголовок со счётом в конце; первый тайм; второй тайм; итог; "
            "лучший игрок матча (MVP); лучший у проигравших.\n"
            "- Счёт должен соответствовать результату. Голы забивают нападающие и полузащитники, "
            "вратарь делает сэйвы, защитники — подкаты и блоки. Используй только игроков из составов.\n"
            "- Пиши живо, с эмоциями, как комментатор. Эмодзи — умеренно.\n"
            "- БЕЗ markdown и HTML (никаких **, #, <b>). Обычный текст.\n"
            "- Длина: 2500–3500 символов."
        )

    return (
        "Ты — автор эпических комиксов и мастер боевых сцен. Напиши зрелищную битву "
        "между двумя командами супергероев из составов ниже.\n\n"
        f"{teams_block}\n\n{result_rule}\n\n"
        "КАК ПИСАТЬ (очень важно):\n"
        "1. Опирайся на НАСТОЯЩИЕ способности и слабости каждого героя из его вселенной "
        "(полёт, магия, броня, регенерация, скорость и т.д.). Не выдумывай героям силы, "
        "которых у них нет. Если не уверен в способности, лучше опиши бой общими словами.\n"
        "2. Учитывай статы: чем выше сила/скорость/интеллект, тем заметнее роль героя. "
        "Слабые по статам герои выигрывают хитростью, но не побеждают в лоб сильнейших.\n"
        "3. Бой — это не 1×1 по очереди: герои взаимодействуют, помогают друг другу, "
        "меняют соперников. Умные герои строят тактику, быстрые заходят с флангов, "
        "сильные продавливают в лоб, маги создают порталы и барьеры.\n"
        "4. Драма нарастает: в 1-м раунде равновесие, во 2-м — первые потери и перелом, "
        "в 3-м — решающая схватка. Выбывшие герои указываются явно.\n"
        "5. Герои одной вселенной могут иметь общую историю или связи — используй это.\n"
        "6. Финал логичен и объясняет победу через конкретные события боя.\n\n"
        "ФОРМАТ ОТВЕТА:\n"
        f"- Язык: {lang_name}.\n"
        "- Заголовок: «⚔️ БИТВА: <игрок 1> vs <игрок 2>».\n"
        "- Затем «🎬 РАУНД 1 — СТАРТ», «🎬 РАУНД 2 — ПЕРВЫЕ ПОТЕРИ», «🎬 РАУНД 3 — ПЕРЕЛОМ».\n"
        "- Затем «🏆 ИТОГ»: кто победил, кто выбыл, кто выжил.\n"
        "- В конце: «MVP битвы» и «Лучший у проигравших» с коротким объяснением.\n"
        "- Эмодзи для героев и действий, но БЕЗ markdown и HTML (никаких **, #, <b>). Обычный текст.\n"
        "- Имена игроков бота используй как названия команд.\n"
        "- Длина: 2500–3500 символов. Пиши ярко, конкретно, без воды."
    )


# Коды, при которых имеет смысл повторить запрос / попробовать другую модель
RETRYABLE_STATUSES = {408, 429, 500, 502, 503, 504}
GEMINI_ATTEMPTS_PER_MODEL = int(os.environ.get("GEMINI_ATTEMPTS", "2"))   # попыток на одну модель
GEMINI_RETRY_DELAY = float(os.environ.get("GEMINI_RETRY_DELAY", "3"))     # базовая пауза, растёт х2


class GeminiError(RuntimeError):
    def __init__(self, message, status=None, retryable=False):
        super().__init__(message)
        self.status = status
        self.retryable = retryable


def _gemini_models():
    """Основная модель + запасные (без повторов). Всё можно переопределить через .env:
    GEMINI_MODEL=...            — основная
    GEMINI_FALLBACK_MODELS=a,b  — запасные через запятую"""
    primary = os.environ.get("GEMINI_MODEL", "gemini-flash-latest")
    fallbacks = os.environ.get(
        "GEMINI_FALLBACK_MODELS",
        "gemini-2.5-flash,gemini-2.5-flash-lite,gemini-flash-lite-latest",
    )
    models = [primary] + [m.strip() for m in fallbacks.split(",") if m.strip()]
    seen, result = set(), []
    for m in models:
        if m not in seen:
            seen.add(m)
            result.append(m)
    return result


async def _generate_gemini_once(prompt, api_key, model):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"maxOutputTokens": 6000, "temperature": 0.9},
    }
    headers = {"x-goog-api-key": api_key, "content-type": "application/json"}
    timeout = aiohttp.ClientTimeout(total=REQUEST_TIMEOUT)
    try:
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.post(url, json=payload, headers=headers) as resp:
                try:
                    body = await resp.json(content_type=None)
                except Exception:
                    body = {"raw": (await resp.text())[:300]}
                status = resp.status
    except (asyncio.TimeoutError, aiohttp.ClientError) as e:
        # сеть / таймаут — тоже временная проблема
        raise GeminiError(f"Gemini network error ({model}): {e!r}", retryable=True)

    if status != 200:
        raise GeminiError(
            f"Gemini API error {status} ({model}): {body}",
            status=status,
            retryable=status in RETRYABLE_STATUSES,
        )

    parts = []
    for cand in body.get("candidates", [])[:1]:
        for part in cand.get("content", {}).get("parts", []):
            if part.get("text"):
                parts.append(part["text"])
    text = "".join(parts).strip()
    if not text:
        # пустой ответ (например, сработал фильтр) — пробуем ещё раз / другую модель
        raise GeminiError(f"Gemini returned empty response ({model})", retryable=True)
    return text


async def _generate_gemini(prompt, api_key):
    """Повторы с нарастающей паузой, затем переключение на запасные модели Gemini."""
    last_error = None
    for model in _gemini_models():
        for attempt in range(1, GEMINI_ATTEMPTS_PER_MODEL + 1):
            try:
                text = await _generate_gemini_once(prompt, api_key, model)
                if model != _gemini_models()[0] or attempt > 1:
                    logging.info("Gemini ok: model=%s attempt=%d", model, attempt)
                return text
            except GeminiError as e:
                last_error = e
                logging.warning("Gemini fail: model=%s attempt=%d/%d: %s",
                                model, attempt, GEMINI_ATTEMPTS_PER_MODEL, e)
                if e.status == 404:
                    break   # такой модели нет — сразу к следующей
                if not e.retryable:
                    # 400/401/403 и т.п.: ключ/запрос неверны, другая модель вряд ли поможет
                    raise
                if attempt < GEMINI_ATTEMPTS_PER_MODEL:
                    delay = GEMINI_RETRY_DELAY * (2 ** (attempt - 1)) + random.uniform(0, 1)
                    await asyncio.sleep(delay)
        # эта модель не ответила — переходим к следующей
    raise last_error or RuntimeError("Gemini: all models failed")


async def _generate_claude(prompt, api_key):
    payload = {
        "model": os.environ.get("BATTLE_MODEL", DEFAULT_MODEL),
        "max_tokens": 2000,
        "messages": [{"role": "user", "content": prompt}],
    }
    headers = {
        "x-api-key": api_key,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json",
    }
    timeout = aiohttp.ClientTimeout(total=REQUEST_TIMEOUT)
    async with aiohttp.ClientSession(timeout=timeout) as session:
        async with session.post(API_URL, json=payload, headers=headers) as resp:
            body = await resp.json()
            if resp.status != 200:
                raise RuntimeError(f"Anthropic API error {resp.status}: {body}")
    return "".join(x.get("text", "") for x in body.get("content", []) if x.get("type") == "text").strip()


async def generate_battle(data, lang_name):
    """Gemini (бесплатный ключ) в приоритете, иначе Claude."""
    prompt = build_prompt(data, lang_name)
    gkey = _gemini_key()
    akey = os.environ.get("ANTHROPIC_API_KEY")
    if gkey:
        try:
            text = await _generate_gemini(prompt, gkey)
        except Exception:
            if not akey:
                raise
            logging.exception("Gemini unavailable, falling back to Claude")
            text = await _generate_claude(prompt, akey)
    elif akey:
        text = await _generate_claude(prompt, akey)
    else:
        raise RuntimeError("No AI API key set (GEMINI_API_KEY or ANTHROPIC_API_KEY)")
    if not text:
        raise RuntimeError("Empty response from AI")
    return text


logging.basicConfig(level=logging.INFO)

router = Router()
GAMES = {}

LOBBY_TIMEOUT = 120   # секунд от создания игры до автостарта
LOBBY_TICK = 30       # как часто писать отсчёт
TURN_TIMEOUT = 180    # секунд на ход, потом авто-пас / авто-скип

EMOJI_HEROES = "\U0001F9B8"
EMOJI_FOOTBALL = "\u26BD"
EMOJI_MONEY_BAG = "\U0001F4B0"


async def safe_call(func, *args, **kwargs):
    try:
        return await func(*args, **kwargs)
    except TelegramRetryAfter as e:
        await asyncio.sleep(e.retry_after + 1)
        return await func(*args, **kwargs)


def esc(text):
    """Экранирует имя игрока для HTML-сообщений."""
    return html.escape(str(text), quote=False)


def display_name(user):
    return user.first_name or user.username or str(user.id)


def player_name(message_or_user):
    if hasattr(message_or_user, "from_user"):
        return display_name(message_or_user.from_user)
    return display_name(message_or_user)


def player_line(p):
    uname = f" (@{esc(p.username)})" if getattr(p, "username", None) else ""
    return f"{esc(p.name)}{uname}"


def mention(p):
    """Упоминание игрока, чтобы Telegram отправил ему уведомление: @username или ссылка по id."""
    if getattr(p, "username", None):
        return f"@{esc(p.username)}"
    return f'<a href="tg://user?id={p.user_id}">{esc(p.name)}</a>'


def err_text(chat_id, err):
    key, params = err
    return get_text(chat_id, key, **params)


def generic_hidden_text(hero, lang="ru"):
    pos_dict = get_text_by_lang(lang, "positions")
    hidden_msg = get_text_by_lang(lang, "hidden_stats")
    if "position" in hero:
        pos_name = pos_dict.get(hero["position"], hero["position"])
        return f"{EMOJI_FOOTBALL} <b>{hero['name']}</b> ({pos_name})\n{hidden_msg}"
    pic_line = hero_pic_line(hero)
    pic_block = f"\n<code>{pic_line}</code>" if pic_line else ""
    return f"{EMOJI_HEROES} <b>{hero['name']}</b> ({hero['universe']})\n{hidden_msg}{pic_block}"


def build_roster_text(game, p, lang="ru"):
    if game.category != "football":
        names = ", ".join(h["name"] for h in p.team) or "—"
        return names
    groups = {"FW": [], "GK": [], "DF": [], "MF": []}
    for h in p.team:
        pos = h.get("position")
        if pos in groups:
            groups[pos].append(h["name"])
    labels = get_text_by_lang(lang, "positions_plural")
    # Порядок: нападающие, вратари, защитники, полузащитники — все четыре строки всегда
    lines = [f"{labels.get(pos, pos)}: {', '.join(groups[pos]) or '—'}" for pos in ["FW", "GK", "DF", "MF"]]
    return "\n".join(lines)


def cancel_task(game, attr):
    """Отменяет фоновую задачу игры (кроме той, из которой вызвали)."""
    task = getattr(game, attr, None)
    if task and not task.done() and task is not asyncio.current_task():
        task.cancel()
    setattr(game, attr, None if task is not asyncio.current_task() else task)


def cancel_all_tasks(game):
    cancel_task(game, "lobby_task")
    cancel_task(game, "timer_task")


# ---------------------------------------------------------------- язык / правила

@router.message(Command("lang", "language"))
async def cmd_lang(message: Message):
    builder = InlineKeyboardBuilder()
    builder.button(text="🇷🇺 Русский", callback_data="set_lang:ru")
    builder.button(text="🇬🇧 English", callback_data="set_lang:en")
    builder.button(text="🇺🇿 O'zbekcha", callback_data="set_lang:uz")
    builder.adjust(3)
    await message.answer(get_text(message.chat.id, "select_lang"), reply_markup=builder.as_markup())


@router.callback_query(F.data.startswith("set_lang:"))
async def on_lang_select(callback: CallbackQuery):
    lang_code = callback.data.split(":")[1]
    chat_id = callback.message.chat.id
    CHAT_LANGUAGES[chat_id] = lang_code
    await callback.answer()
    await callback.message.edit_text(get_text(chat_id, "lang_changed"))


RULES_KEYS = {"general": "start", "heroes": "rules_heroes", "football": "rules_football"}


def start_keyboard(chat_id, bot_username, view="general", private=True):
    """Кнопки под правилами: категории, «Общие правила» (в разделе категории) и в самом низу — «Добавить в группу»."""
    builder = InlineKeyboardBuilder()
    builder.button(text=get_text(chat_id, "btn_heroes"), callback_data="rules:heroes")
    builder.button(text=get_text(chat_id, "btn_football"), callback_data="rules:football")
    rows = [2]
    if view != "general":
        builder.button(text=get_text(chat_id, "btn_rules_general"), callback_data="rules:general")
        rows.append(1)
    if private and bot_username:
        builder.button(
            text=get_text(chat_id, "btn_add_to_group"),
            url=f"https://t.me/{bot_username}?startgroup=true",
        )
        rows.append(1)
    builder.adjust(*rows)
    return builder.as_markup()


@router.message(Command("start"))
async def cmd_start(message: Message):
    chat_id = message.chat.id
    me = await message.bot.me()
    await message.answer(
        get_text(chat_id, "start"),
        parse_mode="HTML",
        reply_markup=start_keyboard(chat_id, me.username, "general", message.chat.type == "private"),
    )


@router.callback_query(F.data.startswith("rules:"))
async def on_rules(callback: CallbackQuery):
    view = callback.data.split(":", 1)[1]
    key = RULES_KEYS.get(view)
    if not key:
        await callback.answer()
        return
    chat_id = callback.message.chat.id
    me = await callback.bot.me()
    try:
        await callback.message.edit_text(
            get_text(chat_id, key),
            parse_mode="HTML",
            reply_markup=start_keyboard(chat_id, me.username, view, callback.message.chat.type == "private"),
        )
    except TelegramBadRequest:
        pass  # то же сообщение уже открыто
    await callback.answer()


# ---------------------------------------------------------------- создание игры и лобби

@router.message(Command("newgame"))
async def cmd_newgame(message: Message):
    chat_id = message.chat.id
    existing = GAMES.get(chat_id)
    if existing and not existing.finished:
        await message.answer(get_text(chat_id, "already_game"))
        return
    builder = InlineKeyboardBuilder()
    builder.button(text=get_text(chat_id, "btn_heroes"), callback_data=f"cat:heroes:{message.from_user.id}")
    builder.button(text=get_text(chat_id, "btn_football"), callback_data=f"cat:football:{message.from_user.id}")
    builder.adjust(2)
    await message.answer(get_text(chat_id, "choose_cat"), reply_markup=builder.as_markup())


@router.callback_query(F.data.startswith("cat:"))
async def on_category_choice(callback: CallbackQuery):
    _, category, creator_id_str = callback.data.split(":")
    creator_id = int(creator_id_str)
    chat_id = callback.message.chat.id

    if callback.from_user.id != creator_id:
        await callback.answer(get_text(chat_id, "only_creator_cat"), show_alert=True)
        return
    existing = GAMES.get(chat_id)
    if existing and not existing.finished:
        await callback.answer(get_text(chat_id, "already_game"), show_alert=True)
        return

    if category == "heroes":
        # У супергероев есть выбор режима
        builder = InlineKeyboardBuilder()
        builder.button(text=get_text(chat_id, "btn_mode_classic"), callback_data=f"mode:classic:{creator_id}")
        builder.button(text=get_text(chat_id, "btn_mode_money"), callback_data=f"mode:money:{creator_id}")
        builder.adjust(1)
        await callback.answer()
        await safe_call(callback.message.edit_text, get_text(chat_id, "choose_mode"), reply_markup=builder.as_markup())
        return

    await create_game(callback, "football", "classic", creator_id)


@router.callback_query(F.data.startswith("mode:"))
async def on_mode_choice(callback: CallbackQuery):
    _, mode, creator_id_str = callback.data.split(":")
    creator_id = int(creator_id_str)
    chat_id = callback.message.chat.id

    if mode not in ("classic", "money"):
        await callback.answer()
        return
    if callback.from_user.id != creator_id:
        await callback.answer(get_text(chat_id, "only_creator_cat"), show_alert=True)
        return
    existing = GAMES.get(chat_id)
    if existing and not existing.finished:
        await callback.answer(get_text(chat_id, "already_game"), show_alert=True)
        return

    # Следующий шаг — выбор сложности (набора героев)
    builder = InlineKeyboardBuilder()
    builder.button(text=get_text(chat_id, "btn_diff_easy"), callback_data=f"diff:easy:{mode}:{creator_id}")
    builder.button(text=get_text(chat_id, "btn_diff_normal"), callback_data=f"diff:normal:{mode}:{creator_id}")
    builder.button(text=get_text(chat_id, "btn_diff_hard"), callback_data=f"diff:hard:{mode}:{creator_id}")
    builder.adjust(1)
    await callback.answer()
    await safe_call(callback.message.edit_text, get_text(chat_id, "choose_difficulty"), reply_markup=builder.as_markup())


@router.callback_query(F.data.startswith("diff:"))
async def on_difficulty_choice(callback: CallbackQuery):
    _, difficulty, mode, creator_id_str = callback.data.split(":")
    creator_id = int(creator_id_str)
    chat_id = callback.message.chat.id

    if difficulty not in DIFFICULTIES or mode not in ("classic", "money"):
        await callback.answer()
        return
    if callback.from_user.id != creator_id:
        await callback.answer(get_text(chat_id, "only_creator_cat"), show_alert=True)
        return
    existing = GAMES.get(chat_id)
    if existing and not existing.finished:
        await callback.answer(get_text(chat_id, "already_game"), show_alert=True)
        return

    await create_game(callback, "heroes", mode, creator_id, difficulty)


async def create_game(callback, category, mode, creator_id, difficulty="hard"):
    chat_id = callback.message.chat.id
    old = GAMES.get(chat_id)
    if old:
        cancel_all_tasks(old)

    game = Game(
        chat_id, creator_id, display_name(callback.from_user),
        category=category, creator_username=callback.from_user.username, mode=mode,
        difficulty=difficulty,
    )
    GAMES[chat_id] = game
    await callback.answer(f"{get_text(chat_id, 'category_label')}: {get_text(chat_id, game.category_key)}")

    sent = await safe_call(
        callback.message.edit_text,
        lobby_text(game, chat_id),
        reply_markup=lobby_keyboard(game, chat_id),
        parse_mode="HTML",
    )
    game.lobby_message_id = sent.message_id if isinstance(sent, Message) else callback.message.message_id
    game.lobby_task = asyncio.create_task(lobby_countdown(callback.bot, game))


def lobby_text(game, chat_id):
    players_list = "\n".join(f"{i+1}. {player_line(p)}" for i, p in enumerate(game.players.values()))
    extra_rule = get_text(chat_id, "football_rule") if game.category == "football" else ""
    hint = (
        get_text(chat_id, "lobby_hint_min")
        if len(game.players) < game.min_players
        else get_text(chat_id, "lobby_hint_ready")
    )
    mode_line = ""
    if game.category == "heroes":
        mode_line = (
            f"{get_text(chat_id, 'mode_label')}: <b>{get_text(chat_id, 'mode_' + game.mode)}</b>.\n"
            f"{get_text(chat_id, 'difficulty_label')}: <b>{get_text(chat_id, 'diff_' + game.difficulty)}</b>.\n"
        )
    return (
        f"<b>{get_text(chat_id, 'game_created_title')}</b> "
        f"{get_text(chat_id, 'category_label')}: <b>{get_text(chat_id, game.category_key)}</b>.\n"
        f"{mode_line}\n"
        f"{get_text(chat_id, 'lobby_players', n=len(game.players), max=game.max_players)}\n"
        f"{players_list}\n\n"
        f"{get_text(chat_id, 'lobby_join_hint')}\n"
        f"{hint}\n"
        f"{get_text(chat_id, 'lobby_autostart')}"
        f"{extra_rule}"
    )


def lobby_keyboard(game, chat_id):
    builder = InlineKeyboardBuilder()
    builder.button(text=get_text(chat_id, "btn_join"), callback_data="join_game")
    if len(game.players) >= game.min_players and not game.started:
        builder.button(text=get_text(chat_id, "btn_start"), callback_data=f"start_game:{game.player_order[0]}")
    builder.adjust(1)
    return builder.as_markup()


def format_time_left(chat_id, seconds):
    mins, secs = divmod(seconds, 60)
    parts = []
    if mins:
        parts.append(f"{mins} {get_text(chat_id, 'time_min')}")
    if secs:
        parts.append(f"{secs} {get_text(chat_id, 'time_sec')}")
    return " ".join(parts)


async def lobby_countdown(bot, game):
    """Отсчёт до автостарта: сообщения каждые 30 секунд, на 2:00 игра стартует (или отменяется)."""
    chat_id = game.chat_id
    try:
        left = LOBBY_TIMEOUT
        while left > LOBBY_TICK:
            await asyncio.sleep(LOBBY_TICK)
            left -= LOBBY_TICK
            if game.started or game.finished:
                return
            await safe_call(
                bot.send_message, chat_id,
                get_text(chat_id, "countdown", time=format_time_left(chat_id, left)),
            )
        await asyncio.sleep(LOBBY_TICK)

        async with game.lock:
            if game.started or game.finished:
                return
            if game.can_begin():
                await start_game_flow(bot, game)
            else:
                game.finished = True
                await safe_call(
                    bot.send_message, chat_id,
                    get_text(chat_id, "lobby_cancelled", n=game.min_players),
                )
                if game.lobby_message_id:
                    try:
                        await bot.edit_message_reply_markup(
                            chat_id=chat_id, message_id=game.lobby_message_id, reply_markup=None,
                        )
                    except Exception:
                        pass
    except asyncio.CancelledError:
        raise
    except Exception:
        logging.exception("lobby_countdown failed")


@router.callback_query(F.data == "join_game")
async def on_join_btn(callback: CallbackQuery):
    chat_id = callback.message.chat.id
    game = GAMES.get(chat_id)
    if not game:
        await callback.answer(get_text(chat_id, "no_game"), show_alert=True)
        return

    user = callback.from_user
    ok, err = game.add_player(user.id, display_name(user), username=user.username)
    if not ok:
        await callback.answer(err_text(chat_id, err), show_alert=True)
        return

    await callback.answer(get_text(chat_id, "joined_ok"))
    await process_player_join(callback.bot, game)


@router.message(Command("join"))
async def cmd_join(message: Message):
    chat_id = message.chat.id
    game = GAMES.get(chat_id)
    if not game or game.finished:
        await message.answer(get_text(chat_id, "no_game"))
        return
    ok, err = game.add_player(message.from_user.id, player_name(message), username=message.from_user.username)
    if not ok:
        await message.answer(err_text(chat_id, err))
        return
    await process_player_join(message.bot, game)


async def process_player_join(bot, game):
    chat_id = game.chat_id
    text = lobby_text(game, chat_id)
    kb = lobby_keyboard(game, chat_id)

    if game.lobby_message_id:
        try:
            await bot.edit_message_text(
                chat_id=chat_id,
                message_id=game.lobby_message_id,
                text=text,
                reply_markup=kb,
                parse_mode="HTML",
            )
            return
        except TelegramBadRequest:
            pass

    sent = await safe_call(bot.send_message, chat_id, text, reply_markup=kb, parse_mode="HTML")
    game.lobby_message_id = sent.message_id


async def start_game_flow(bot, game):
    """Общий запуск игры (кнопка создателя и автостарт). Вызывать под game.lock."""
    chat_id = game.chat_id
    game.begin()
    players_list = "\n".join(f"{i+1}. {player_line(p)}" for i, p in enumerate(game.players.values()))
    if game.unlimited:
        started = get_text(chat_id, "game_started_money", budget=game.budget_start, pool=len(game.hero_pool))
    else:
        started = get_text(chat_id, "game_started", budget=game.budget_start, team_size=game.team_size)
    await safe_call(
        bot.send_message,
        chat_id,
        get_text(chat_id, "game_starting", n=len(game.players), players=players_list) + started,
        parse_mode="HTML",
    )
    if game.lobby_message_id:
        try:
            await bot.edit_message_reply_markup(chat_id=chat_id, message_id=game.lobby_message_id, reply_markup=None)
        except Exception:
            pass
    await flush_pending_events(bot, game)
    await send_auction_message(bot, game)


@router.callback_query(F.data.startswith("start_game:"))
async def on_start_game(callback: CallbackQuery):
    _, creator_id_str = callback.data.split(":")
    creator_id = int(creator_id_str)
    chat_id = callback.message.chat.id
    game = GAMES.get(chat_id)

    if not game:
        await callback.answer(get_text(chat_id, "alert_no_start"), show_alert=True)
        return

    async with game.lock:
        if game.started or game.finished:
            await callback.answer(get_text(chat_id, "alert_no_start"), show_alert=True)
            return
        if callback.from_user.id != creator_id:
            await callback.answer(get_text(chat_id, "only_creator_start"), show_alert=True)
            return
        if not game.can_begin():
            await callback.answer(get_text(chat_id, "need_min_players", n=game.min_players), show_alert=True)
            return

        cancel_task(game, "lobby_task")
        await callback.answer(get_text(chat_id, "toast_started"))
        await start_game_flow(callback.bot, game)


# ---------------------------------------------------------------- статус / завершение

@router.message(Command("status"))
async def cmd_status(message: Message):
    game = GAMES.get(message.chat.id)
    if not game:
        await message.answer(get_text(message.chat.id, "no_game"))
        return
    await message.answer(build_status_text(game), parse_mode="HTML")


@router.message(Command("endgame"))
async def cmd_endgame(message: Message):
    chat_id = message.chat.id
    game = GAMES.get(chat_id)
    if not game:
        await message.answer(get_text(chat_id, "no_game"))
        return
    if game.finished:
        await message.answer(get_text(chat_id, "already_ended"))
        return
    if message.from_user.id not in game.players:
        await message.answer(get_text(chat_id, "only_players_end"))
        return

    async with game.lock:
        if game.finished:
            await message.answer(get_text(chat_id, "already_ended"))
            return
        game.finished = True
        game.auction = None
        cancel_all_tasks(game)
        await delete_last_message(message.bot, game)
        await message.answer(get_text(chat_id, "game_stopped"))
        if game.started:
            await announce_game_end(message.bot, game)


def build_status_text(game):
    chat_id = game.chat_id
    total_lots = len(game.hero_pool) if game.hero_pool else 0
    lines = [get_text(chat_id, "status_lot", n=min(game.hero_index + 1, total_lots), total=total_lots) + "\n"]
    for uid in game.player_order:
        p = game.players[uid]
        names = ", ".join(h["name"] for h in p.team) or "—"
        count = str(len(p.team)) if game.team_size is None else f"{len(p.team)}/{game.team_size}"
        lines.append(get_text(chat_id, "status_line", name=esc(p.name), budget=p.budget, count=count, names=names))
    return "\n".join(lines)


# ---------------------------------------------------------------- аукцион

def build_auction_keyboard(game, chat_id):
    builder = InlineKeyboardBuilder()
    a = game.auction
    for amount in game.valid_bid_options(a.turn_id):
        builder.button(text=f"{EMOJI_MONEY_BAG} ${amount}", callback_data=f"bid:{amount}")
    if a.current_bid > 0:
        # Пас — сдаться и отдать лот сопернику по текущей ставке
        builder.button(text=get_text(chat_id, "pass_btn"), callback_data="pass")
    elif not game.leftover_round and game.can_skip(a.turn_id):
        # Скип — лот не нужен; если скипнут все, он достаётся никому
        skip_text = get_text(chat_id, "skip_btn")
        left = game.skips_left(a.turn_id)
        if left is not None:
            skip_text += f" ({left}/{game.max_skips})"
        builder.button(text=skip_text, callback_data="skip")
    builder.adjust(3)
    return builder


async def delete_last_message(bot, game):
    mid = game.last_message_id
    game.last_message_id = None
    if mid:
        try:
            await bot.delete_message(chat_id=game.chat_id, message_id=mid)
        except Exception:
            logging.debug("could not delete auction message %s", mid)


def start_turn_timer(bot, game):
    cancel_task(game, "timer_task")
    game.turn_token += 1
    game.timer_task = asyncio.create_task(turn_timeout(bot, game, game.turn_token))


async def turn_timeout(bot, game, token):
    """Если игрок не ходит TURN_TIMEOUT секунд — бот пасует / скипает за него."""
    try:
        await asyncio.sleep(TURN_TIMEOUT)
        async with game.lock:
            if game.finished or game.auction is None or game.turn_token != token:
                return
            await handle_afk(bot, game)
    except asyncio.CancelledError:
        raise
    except Exception:
        logging.exception("turn_timeout failed")


async def handle_afk(bot, game):
    chat_id = game.chat_id
    a = game.auction
    uid = a.turn_id
    name = esc(game.players[uid].name)

    raise_amount = a.current_bid + 1
    if game.classic_heroes and raise_amount in game.valid_bid_options(uid):
        # Герои → классический: при AFK бот повышает ставку на $1 (скипы не тратятся)
        ok, err, result = game.place_bid(uid, raise_amount)
        text = get_text(chat_id, "afk_bid", name=name, amount=raise_amount)
    elif a.current_bid > 0:
        ok, err, result = game.pass_bid(uid)
        text = get_text(chat_id, "afk_pass", name=name)
    elif not game.leftover_round and game.can_skip(uid):
        ok, err, result = game.skip_lot(uid)
        text = get_text(chat_id, "afk_skip", name=name)
    else:
        # Вернувшийся лот нужно взять — минимальная ставка
        options = game.valid_bid_options(uid)
        if not options:
            ok, err, result = False, None, None
        else:
            ok, err, result = game.place_bid(uid, options[0])
            text = get_text(chat_id, "afk_bid", name=name, amount=options[0])

    if not ok:
        logging.warning("AFK action failed: %s", err)
        await send_auction_message(bot, game)  # перезапускает таймер
        return

    await safe_call(bot.send_message, chat_id, text, parse_mode="HTML")
    await finish_action(bot, game, result)


async def send_auction_message(bot, game):
    """Удаляет старое сообщение аукциона и отправляет новое — чтобы оно всегда было внизу чата."""
    a = game.auction
    if a is None:
        await delete_last_message(bot, game)
        await announce_game_end(bot, game)
        return

    chat_id = game.chat_id
    turn_player = game.players[a.turn_id]
    lang = get_chat_lang(chat_id)

    leading_str = ""
    if a.current_bidder_id:
        leading_str = get_text(chat_id, "leading", name=esc(game.players[a.current_bidder_id].name))

    parts = [generic_hidden_text(a.hero, lang), ""]
    if a.history:
        recent = a.history[-6:]
        history = " → ".join(f"{esc(name)} ${amount}" for name, amount in recent)
        parts.append(f"{get_text(chat_id, 'history_title')}: {history}")
    parts.append(f"{get_text(chat_id, 'current_bid', bid=a.current_bid)}{leading_str}")
    if a.auto_passed:
        names = ", ".join(esc(game.players[u].name) for u in a.auto_passed)
        parts.append(get_text(chat_id, "auto_passed", names=names))
    parts.append("")
    parts.append(get_text(chat_id, "turn", name=mention(turn_player)))
    text = "\n".join(parts)

    kb = build_auction_keyboard(game, chat_id)

    # Сначала отправляем новое сообщение, и только потом удаляем старое
    old_message_id = game.last_message_id
    sent = await safe_call(bot.send_message, chat_id, text, reply_markup=kb.as_markup(), parse_mode="HTML")
    game.last_message_id = sent.message_id
    if old_message_id:
        try:
            await bot.delete_message(chat_id=chat_id, message_id=old_message_id)
        except Exception:
            logging.debug("could not delete auction message %s", old_message_id)
    start_turn_timer(bot, game)


async def announce_game_end(bot, game):
    if game.end_announced:
        return
    game.end_announced = True
    cancel_all_tasks(game)

    results = []
    for uid in game.player_order:
        power, detail = game.team_power(uid)
        results.append((power, game.players[uid], detail))

    # Сортируем по силе команды от большей к меньшей
    results.sort(key=lambda x: x[0], reverse=True)

    chat_id = game.chat_id
    lang = get_chat_lang(chat_id)

    def item_line(h, lang_code):
        pos_map = get_text_by_lang(lang_code, "positions")
        if "position" in h:
            pos_name = pos_map.get(h["position"], h["position"])
            return f"  • {h['name']} ({pos_name})"
        return f"  • {h['name']} ({h['universe']})"

    def team_block(p, power, detail, lang_code):
        team_str = "\n".join(item_line(h, lang_code) for h in p.team) or "  —"
        if detail.get("bonus_universes"):
            bonus_str = get_text(
                chat_id, "end_synergy",
                pct=round((detail["multiplier"] - 1) * 100),
                list=", ".join(detail["bonus_universes"]),
            )
        elif detail.get("position_detail"):
            pos_dict = get_text_by_lang(lang_code, "positions_plural")
            parts = []
            for pos, info in detail["position_detail"].items():
                sign = "+15%" if info["matched"] else "-15%"
                parts.append(f"{pos_dict.get(pos, pos)} {info['count']}/{info['threshold']} ({sign})")
            bonus_str = f"\n({'; '.join(parts)})"
        else:
            bonus_str = ""
        return get_text(
            chat_id, "end_power",
            name=esc(p.name), power=power, bonus=bonus_str, team=team_str, budget=p.budget,
        )

    blocks = [team_block(p, power, detail, lang) for power, p, detail in results]

    top_power = results[0][0]
    winners = [p for power, p, _ in results if power == top_power]
    if len(winners) > 1:
        winner_line = get_text(chat_id, "draw_names", names=", ".join(esc(p.name) for p in winners))
    else:
        winner_line = get_text(chat_id, "winner", name=esc(winners[0].name))

    # Полный текст с силой и победителем — показывается только по кнопке
    game.reveal_text = (
        f"{get_text(chat_id, 'game_over')}\n\n"
        + "\n\n".join(blocks)
        + "\n\n"
        + winner_line
    )
    game.battle_data = build_battle_data(game, results)

    # Пока победитель скрыт: только составы и остатки бюджета, без силы
    hidden_blocks = [
        get_text(
            chat_id, "end_teams",
            name=esc(p.name),
            team="\n".join(item_line(h, lang) for h in p.team) or "  —",
            budget=p.budget,
        )
        for p in (game.players[uid] for uid in game.player_order)  # порядок игроков, а не по силе — иначе победитель виден
    ]
    hidden_text = (
        f"{get_text(chat_id, 'game_over')}\n\n"
        + "\n\n".join(hidden_blocks)
        + "\n\n"
        + get_text(chat_id, "end_hidden_note")
    )
    builder = InlineKeyboardBuilder()
    builder.button(text=get_text(chat_id, "btn_gen_battle"), callback_data="battle:gen")
    builder.button(text=get_text(chat_id, "btn_reveal_winner"), callback_data="battle:reveal")
    builder.adjust(1)
    sent = await safe_call(bot.send_message, chat_id, hidden_text, reply_markup=builder.as_markup(), parse_mode="HTML")
    game.end_message_id = sent.message_id

    # Чистим чат от карточек лотов, чтобы в следующей игре статы нельзя было подсмотреть
    await delete_lot_messages(bot, game)


async def send_lot_message(bot, game, text):
    """Отправляет сообщение с итогом лота и запоминает его id — после игры оно будет удалено."""
    sent = await safe_call(bot.send_message, game.chat_id, text, parse_mode="HTML")
    if sent is not None:
        game.lot_message_ids.append(sent.message_id)
    return sent


async def delete_lot_messages(bot, game):
    """После окончания игры удаляет из чата все сообщения с раскрытыми героями/игроками,
    чтобы в следующей игре по ним нельзя было узнать статы."""
    ids = game.lot_message_ids
    game.lot_message_ids = []
    for mid in ids:
        try:
            await safe_call(bot.delete_message, chat_id=game.chat_id, message_id=mid)
        except Exception:
            logging.debug("could not delete lot message %s", mid)
        await asyncio.sleep(0.05)


async def announce_lot_result(bot, game, result):
    chat_id = game.chat_id
    lang = get_chat_lang(chat_id)
    if result.get("skipped"):
        await send_lot_message(
            bot, game,
            get_text(chat_id, "lot_skipped", hero=result["hero"]["name"]),
        )
        return
    winner = game.players[result["winner_id"]]
    await send_lot_message(
        bot, game,
        get_text(
            chat_id,
            "lot_won",
            hero=result["hero"]["name"],
            winner=esc(winner.name),
            price=result["price"],
            card=game.card_func(result["hero"], lang),
            roster=build_roster_text(game, winner, lang),
        ),
    )


async def flush_pending_events(bot, game):
    chat_id = game.chat_id
    lang = get_chat_lang(chat_id)
    while game.pending_events:
        event = game.pending_events.pop(0)
        if event.get("type") == "skipped_returned":
            await safe_call(
                bot.send_message,
                chat_id,
                get_text(chat_id, "lots_returned", count=event["count"]),
                parse_mode="HTML",
            )
            continue
        if event.get("type") == "auto_award":
            winner = game.players[event["winner_id"]]
            hero = event["hero"]
            await send_lot_message(
                bot, game,
                get_text(
                    chat_id,
                    "auto_award",
                    winner=esc(winner.name),
                    hero=hero["name"],
                    price=event["price"],
                    card=game.card_func(hero, lang),
                    roster=build_roster_text(game, winner, lang),
                ),
            )


async def finish_action(bot, game, result):
    """Общий хвост после любого действия (ставка / скип / пас / авто-действие)."""
    if result:
        await announce_lot_result(bot, game, result)
    await flush_pending_events(bot, game)
    await send_auction_message(bot, game)


async def run_action(callback, action):
    """Общая обработка нажатий на кнопки аукциона под блокировкой игры."""
    chat_id = callback.message.chat.id
    game = GAMES.get(chat_id)
    if not game or game.auction is None:
        await callback.answer(get_text(chat_id, "already_ended"), show_alert=True)
        return
    async with game.lock:
        if game.auction is None:
            await callback.answer(get_text(chat_id, "already_ended"), show_alert=True)
            return
        if callback.message.message_id != game.last_message_id:
            await callback.answer(get_text(chat_id, "err_stale"), show_alert=True)
            return
        ok, err, result, toast = action(game)
        if not ok:
            await callback.answer(err_text(chat_id, err), show_alert=True)
            return
        await callback.answer(toast(chat_id))
        await finish_action(callback.bot, game, result)


@router.callback_query(F.data.startswith("bid:"))
async def on_bid(callback: CallbackQuery):
    amount = int(callback.data.split(":", 1)[1])
    uid = callback.from_user.id

    def action(game):
        ok, err, result = game.place_bid(uid, amount)
        return ok, err, result, lambda cid: get_text(cid, "bid_accepted", amount=amount)

    await run_action(callback, action)


@router.callback_query(F.data == "skip")
async def on_skip(callback: CallbackQuery):
    uid = callback.from_user.id

    def action(game):
        ok, err, result = game.skip_lot(uid)
        return ok, err, result, lambda cid: get_text(cid, "skip_accepted")

    await run_action(callback, action)


@router.callback_query(F.data == "pass")
async def on_pass(callback: CallbackQuery):
    uid = callback.from_user.id

    def action(game):
        ok, err, result = game.pass_bid(uid)
        return ok, err, result, lambda cid: get_text(cid, "pass_accepted")

    await run_action(callback, action)


# ---------------------------------------------------------------- итоги: битва / победитель

def split_message(text, limit=4000):
    """Режет длинный текст на куски для Telegram (по абзацам)."""
    chunks, cur = [], ""
    for para in text.split("\n\n"):
        if cur and len(cur) + len(para) + 2 > limit:
            chunks.append(cur)
            cur = ""
        while len(para) > limit:
            chunks.append(para[:limit])
            para = para[limit:]
        cur = f"{cur}\n\n{para}" if cur else para
    if cur:
        chunks.append(cur)
    return chunks


async def show_reveal(bot, game):
    """Заменяет сообщение с итогами на полный вариант (сила + победитель) и убирает кнопки."""
    game.revealed = True
    try:
        await safe_call(
            bot.edit_message_text,
            chat_id=game.chat_id, message_id=game.end_message_id,
            text=game.reveal_text, parse_mode="HTML", reply_markup=None,
        )
    except TelegramBadRequest:
        await safe_call(bot.send_message, game.chat_id, game.reveal_text, parse_mode="HTML")


@router.callback_query(F.data.in_({"battle:gen", "battle:reveal"}))
async def on_battle_choice(callback: CallbackQuery):
    chat_id = callback.message.chat.id
    game = GAMES.get(chat_id)
    if (
        not game or not game.end_announced or game.revealed
        or callback.message.message_id != game.end_message_id
    ):
        await callback.answer(get_text(chat_id, "battle_expired"), show_alert=True)
        return
    if callback.from_user.id not in game.players:
        await callback.answer(get_text(chat_id, "battle_only_players"), show_alert=True)
        return
    if game.battle_busy:
        await callback.answer(get_text(chat_id, "battle_busy"), show_alert=True)
        return

    if callback.data == "battle:reveal":
        await callback.answer()
        await show_reveal(callback.bot, game)
        return

    # Генерация битвы через ИИ
    if not has_api_key():
        await callback.answer(get_text(chat_id, "battle_no_key"), show_alert=True)
        return

    game.battle_busy = True
    await callback.answer()
    original_markup = callback.message.reply_markup
    try:
        await callback.message.edit_reply_markup(reply_markup=None)
    except TelegramBadRequest:
        pass
    wait_msg = await safe_call(callback.bot.send_message, chat_id, get_text(chat_id, "battle_generating"))
    try:
        story = await generate_battle(game.battle_data, get_text(chat_id, "battle_lang_name"))
    except Exception:
        logging.exception("battle generation failed")
        game.battle_busy = False
        try:
            await callback.message.edit_reply_markup(reply_markup=original_markup)
        except TelegramBadRequest:
            pass
        try:
            await wait_msg.edit_text(get_text(chat_id, "battle_error"))
        except TelegramBadRequest:
            pass
        return

    try:
        await wait_msg.delete()
    except TelegramBadRequest:
        pass
    for chunk in split_message(story):
        await safe_call(callback.bot.send_message, chat_id, chunk)
    game.battle_busy = False
    # После сюжета показываем официальные итоги с силой и победителем
    await show_reveal(callback.bot, game)



async def main():
    token = os.environ.get("BOT_TOKEN")
    if not token:
        raise RuntimeError("Установите переменную окружения BOT_TOKEN с токеном вашего бота.")
    bot = Bot(token=token)
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
