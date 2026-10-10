# -*- coding: utf-8 -*-

TEXTS = {
    "ru": {
        "start": (
            "🎮 <b>Аукцион</b>\n\n"
            "В игре две категории: 🦸 Супергерои и ⚽ Футбол. Нажми кнопку ниже, чтобы узнать правила каждой.\n\n"
            "Общие правила:\n"
            "• У каждого игрока бюджет $100 (у героев в классическом режиме — $20)\n"
            "• Бот по очереди показывает лоты (статы скрыты до покупки)\n"
            "• На каждый лот — аукцион: повышаете ставку или пасуете\n"
            "• Скип — лот не нужен: ход переходит сопернику, а если скипнули все — лот никому не достаётся (в конце вернётся, если не хватает игроков)\n"
            "• Пас — сдаться после ставки: лот достаётся сопернику по текущей ставке\n"
            "• Нужно собрать полную команду\n"
            "• В конце считается суммарная сила команды\n"
            "• В классическом режиме ставка не может оставить меньше $1 на каждый недостающий слот\n"
            "• Игра стартует автоматически через 2 минуты после создания\n"
            "• Если игрок не ходит 3 минуты, бот сам пасует или скипает за него\n\n"
            "Команды:\n"
            "/start — правила и добавление бота в группу\n"
            "/lang — Выбрать язык чата / Choose chat language / Tilni tanlash\n"
            "/newgame — создать игру (выбор категории)\n"
            "/join — присоединиться к игре\n"
            "/status — текущее состояние\n"
            "/endgame — завершить игру принудительно"
        ),
        "rules_heroes": (
            "🦸 <b>Супергерои</b>\n\n"
            "• Игроков: от 2 до 4\n"
            "• Нужно собрать команду из 4 героев (в классическом режиме)\n"
            "• Бюджет у каждого — $20 в классическом режиме, $100 в режиме «До конца денег»\n"
            "• У героя три стата: 💪 Сила, ⚡ Скорость, 🧠 Интеллект. Они скрыты, пока герой не куплен\n"
            "• Сила команды — сумма статов всех героев\n"
            "• 🌌 Синергия вселенных: 2 героя из одной вселенной — +10% к силе команды, 3 и больше — +20% (считается по каждой вселенной, бонусы складываются)\n"
            "• Режимы: 🎯 Классический — команда из 4 героев, бюджет $20, максимум 2 скипа за игру; 💰 До конца денег — слотов нет, героев покупают, пока не кончатся деньги (в пуле 15 героев при 2 игроках, 25 при 3, 30 при 4)\n"
            "• Сложность (набор героев): 🟢 Лёгкий — около 60 самых известных героев (Железный человек, Супермен, Бэтмен…); 🟡 Нормальный — плюс менее известные герои (Гамора, Серебряный Сёрфер…) и часть усиленных версий; 🔴 Сложный — все герои, включая все усиленные версии\n"
            "• Побеждает команда с наибольшей итоговой силой"
        ),
        "rules_football": (
            "⚽ <b>Футбол</b>\n\n"
            "• Игроков: 2\n"
            "• Нужно собрать состав из 11 футболистов\n"
            "• Бюджет у каждого — $100\n"
            "• В каждой игре на аукцион попадают 27 случайных футболистов: 3 вратаря, 8 защитников, 8 полузащитников, 8 нападающих\n"
            "• У футболиста один общий рейтинг (по EA SPORTS FC 26). Он скрыт, пока игрок не куплен\n"
            "• Сила команды — сумма рейтингов игроков\n"
            "• 🎯 Правило состава: нужно минимум 1 вратарь, 3 защитника, 3 полузащитника и 3 нападающих. За каждую выполненную позицию +15% к силе, за каждую невыполненную −15%\n"
            "• Побеждает команда с наибольшей итоговой силой"
        ),
        "btn_rules_general": "📖 Общие правила",
        "btn_add_to_group": "➕ Добавить в группу",
        "select_lang": "Выберите язык для этого чата / Choose language for this chat / Tilni tanlang:",
        "lang_changed": "Язык чата успешно изменён на Русский 🇷🇺!",
        "already_game": "В этом чате уже есть активная игра.",
        "choose_cat": "Выбери категорию для игры:",
        "btn_heroes": "🦸 Супергерои",
        "btn_football": "⚽ Футбол",
        "only_creator_cat": "Категорию выбирает создатель игры.",
        "game_created_title": "Игра создана!",
        "category_label": "Категория",
        "player_1": "Игрок 1",
        "join_instruction": "Второй игрок — /join или кнопка, затем создатель нажимает «Начать игру».",
        "football_rule": (
            "\n\n🎯 Важное правило по составу:\n"
            "Если у тебя в команде 3 или больше защитников — команда становится сильнее на 15%.\n"
            "Если защитников меньше 3 — команда слабее на 15%.\n"
            "Точно так же работает для полузащитников и для нападающих — отдельно по каждой роли."
        ),
        "no_game": "Сначала создайте игру командой /newgame.",
        "need_2_players": "Нужно ровно 2 игрока.",
        "game_started": "🚀 Игра начинается! У каждого ${budget}, нужно собрать {team_size}.",
        "already_ended": "Игра уже завершена.",
        "game_stopped": "🛑 Игра принудительно завершена.",
        "pass_btn": "🚫 Пас",
        "skip_btn": "⏭ Скип",
        "bid_accepted": "Ставка ${amount} принята",
        "pass_accepted": "Пас",
        "lot_won": "✅ {hero} достаётся игроку <b>{winner}</b> за ${price}!\n\n{card}\n\n<b>Состав {winner}:</b>\n{roster}",
        "lot_skipped": "⏭ Все скипнули <b>{hero}</b> — лот никому не достался. Если в конце кому-то не хватит игроков, он вернётся.",
        "skip_accepted": "Скип",
        "lots_returned": "🔁 Лоты закончились, но не все команды собраны. Возвращаем скипнутые лоты ({count}) — теперь их нужно брать!",
        "no_money_auto": (
            "🛑 У игрока <b>{loser}</b> не хватает денег на этот лот.\n"
            "✅ {hero} достаётся игроку <b>{winner}</b> за ${price}!\n\n"
            "{card}\n\n<b>Состав {winner}:</b>\n{roster}"
        ),
        "game_over": "🏁 <b>Игра окончена!</b>",
        "winner": "🏆 Победитель: <b>{name}</b>!",
        "draw": "🤝 Ничья!",
        "hidden_stats": "❓ Статы скрыты — узнаешь после покупки!",
        "current_bid": "💵 Текущая ставка: ${bid}",
        "leading": " (лидирует {name})",
        "turn": "👉 Ход игрока: <b>{name}</b>",
        "positions": {"GK": "Вратарь", "DF": "Защитник", "MF": "Полузащитник", "FW": "Нападающий"},
        "positions_plural": {"GK": "Вратари", "DF": "Защитники", "MF": "Полузащитники", "FW": "Нападающие"},
        "choose_mode": "Выбери режим игры в супергероях:",
        "btn_mode_classic": "🎯 Классический (4 слота)",
        "btn_mode_money": "💰 До конца денег",
        "mode_label": "Режим",
        "mode_classic": "Классический (4 слота)",
        "mode_money": "До конца денег",
        "choose_difficulty": "Выбери сложность (набор героев):",
        "btn_diff_easy": "🟢 Лёгкий",
        "btn_diff_normal": "🟡 Нормальный",
        "btn_diff_hard": "🔴 Сложный",
        "difficulty_label": "Сложность",
        "diff_easy": "Лёгкий",
        "diff_normal": "Нормальный",
        "diff_hard": "Сложный",
        "cat_heroes": "Герои",
        "cat_football": "Футбол",
        "btn_join": "🎮 Присоединиться",
        "btn_start": "🚀 Начать игру",
        "lobby_players": "Игроки ({n}/{max}):",
        "lobby_join_hint": "Нажмите кнопку ниже или введите /join, чтобы зайти в игру!",
        "lobby_hint_min": "Нажмите «Начать игру», когда наберётся минимум 2 игрока.",
        "lobby_hint_ready": "Можно нажать «Начать игру» прямо сейчас, или дождаться ещё игроков.",
        "lobby_autostart": "⏳ Игра начнётся автоматически через 2 минуты после создания.",
        "joined_ok": "Вы успешно присоединились!",
        "game_starting": "🎉 <b>Игра начинается! ({n} игроков)</b>\n\nУчастники:\n{players}\n\n",
        "game_started_money": "🚀 Режим «До конца денег»! У каждого ${budget}, слотов нет — покупайте героев, пока не кончатся деньги. Героев в пуле: {pool}.",
        "alert_no_start": "Игра уже начата или не найдена.",
        "only_creator_start": "Начать игру может только создатель.",
        "need_min_players": "Нужно минимум {n} игрока, чтобы начать.",
        "toast_started": "Игра началась!",
        "countdown": "⏳ Игра начнётся через {time}",
        "time_min": "мин",
        "time_sec": "сек",
        "lobby_cancelled": "❌ Игра отменена: за 2 минуты не набралось минимум {n} игрока.",
        "err_not_active": "Аукцион не активен.",
        "err_not_turn": "Сейчас не твой ход.",
        "err_cant_act": "Ты не можешь участвовать в этом лоте (команда полная или нет денег).",
        "err_over_budget": "У тебя недостаточно средств! Твой бюджет: ${budget}.",
        "err_bid_low": "Ставка должна быть больше текущей (${bid}).",
        "err_bad_option": "Такой ставки сейчас нет среди вариантов.",
        "err_skip_after_bid": "Ставка уже сделана — можно повысить или нажать «Пас».",
        "err_skip_leftover": "Этот лот вернулся в конце игры — его нужно взять.",
        "err_skip_limit": "Скипы закончились (максимум {n} за игру) — сделай ставку.",
        "err_pass_no_bid": "Пас доступен только после ставки. Если лот не нужен — нажми «Скип».",
        "err_game_started": "Игра уже началась.",
        "err_already_in": "Ты уже в игре.",
        "err_max_players": "В игре уже максимальное число игроков ({n}).",
        "err_stale": "Это устаревшее сообщение аукциона.",
        "only_players_end": "Завершить игру могут только её участники.",
        "history_title": "📜 Ставки",
        "auto_passed": "⏩ Авто-пас (нечем перебить): {names}",
        "afk_pass": "⏰ {name} не ходил 3 минуты — автоматический пас.",
        "afk_skip": "⏰ {name} не ходил 3 минуты — автоматический скип.",
        "afk_bid": "⏰ {name} не ходил 3 минуты — автоматическая ставка ${amount}.",
        "card_universe": "🌌 Вселенная",
        "card_power": "💪 Сила",
        "card_speed": "⚡ Скорость",
        "card_int": "🧠 Интеллект",
        "card_total": "📊 Суммарный стат",
        "card_position": "📌 Позиция",
        "card_rating": "⚡ Рейтинг",
        "status_lot": "Лот {n}/{total}",
        "status_line": "<b>{name}</b>: ${budget}, команда ({count}): {names}",
        "end_power": "<b>{name}</b> — сила: {power}{bonus}\n{team}\n(остаток бюджета: ${budget})",
        "end_synergy": " (+{pct}% синергия: {list})",
        "draw_names": "🤝 Ничья! Одинаковая сила у: <b>{names}</b>",
        "end_teams": "<b>{name}</b>\n{team}\n(остаток бюджета: ${budget})",
        "end_hidden_note": "🙈 <b>Победитель пока скрыт!</b>\nСгенерируй битву — ИИ расскажет, как всё было, или сразу узнай результат.",
        "btn_gen_battle": "⚔️ Сгенерировать битву",
        "btn_reveal_winner": "🏆 Узнать победителя без битвы",
        "battle_generating": "⏳ ИИ придумывает битву, подожди немного…",
        "battle_error": "😕 Не удалось сгенерировать битву. Попробуй ещё раз или узнай победителя без битвы.",
        "battle_no_key": "ИИ не подключён (нет ключа). Нажми «Узнать победителя без битвы».",
        "battle_busy": "Битва уже генерируется, подожди.",
        "battle_only_players": "Только участники игры могут нажать эту кнопку.",
        "battle_expired": "Эта игра уже закончилась.",
        "battle_lang_name": "русский",
        "auto_award": "🛑 Остальные не могут участвовать в этом лоте (команда полная или нет денег).\n✅ {hero} достаётся игроку <b>{winner}</b> за ${price}!\n\n{card}\n\n<b>Состав {winner}:</b>\n{roster}",
    },
    "en": {
        "start": (
            "🎮 <b>Auction</b>\n\n"
            "The game has two categories: 🦸 Superheroes and ⚽ Football. Tap a button below to see the rules of each.\n\n"
            "General rules:\n"
            "• Every player has a $100 budget (heroes in classic mode — $20)\n"
            "• The bot shows lots one by one (stats are hidden until purchase)\n"
            "• Auction per lot: raise the bid or pass\n"
            "• Skip — you don't want the lot: the turn goes to the opponent, and if everyone skips, nobody gets it (it returns at the end if squads are not full)\n"
            "• Pass — give up after a bid: the lot goes to the opponent at the current bid\n"
            "• You need to assemble a full team\n"
            "• At the end, the total team power is calculated\n"
            "• In classic mode a bid can't leave you with less than $1 for each missing slot\n"
            "• The game starts automatically 2 minutes after creation\n"
            "• If a player doesn't move for 3 minutes, the bot passes or skips for them\n\n"
            "Commands:\n"
            "/start — rules and adding the bot to a group\n"
            "/lang — Choose chat language\n"
            "/newgame — create a game (category selection)\n"
            "/join — join the game\n"
            "/status — current status\n"
            "/endgame — end the game forcibly"
        ),
        "rules_heroes": (
            "🦸 <b>Superheroes</b>\n\n"
            "• Players: 2 to 4\n"
            "• Assemble a team of 4 heroes (in classic mode)\n"
            "• Each player has a $20 budget in classic mode, $100 in «Until money runs out» mode\n"
            "• A hero has three stats: 💪 Power, ⚡ Speed, 🧠 Intelligence. They are hidden until the hero is bought\n"
            "• Team power is the sum of all heroes' stats\n"
            "• 🌌 Universe synergy: 2 heroes from the same universe give +10% team power, 3 or more give +20% (counted per universe, bonuses add up)\n"
            "• Modes: 🎯 Classic — a team of 4 heroes, $20 budget, max 2 skips per game; 💰 Until money runs out — no slot limit, buy heroes until the money is gone (pool of 15 heroes for 2 players, 25 for 3, 30 for 4)\n"
            "• Difficulty (hero pool): 🟢 Easy — about 60 of the best-known heroes (Iron Man, Superman, Batman…); 🟡 Normal — adds less famous heroes (Gamora, Silver Surfer…) and some powered-up versions; 🔴 Hard — every hero, including all powered-up versions\n"
            "• The team with the highest final power wins"
        ),
        "rules_football": (
            "⚽ <b>Football</b>\n\n"
            "• Players: 2\n"
            "• Assemble a squad of 11 footballers\n"
            "• Each player has a $100 budget\n"
            "• Every game puts 27 random footballers up for auction: 3 goalkeepers, 8 defenders, 8 midfielders, 8 forwards\n"
            "• A footballer has one overall rating (from EA SPORTS FC 26). It is hidden until the player is bought\n"
            "• Team power is the sum of players' ratings\n"
            "• 🎯 Squad rule: you need at least 1 goalkeeper, 3 defenders, 3 midfielders and 3 forwards. Each position requirement met gives +15% power, each one missed gives −15%\n"
            "• The team with the highest final power wins"
        ),
        "btn_rules_general": "📖 General rules",
        "btn_add_to_group": "➕ Add to group",
        "select_lang": "Choose language for this chat / Выберите язык / Tilni tanlang:",
        "lang_changed": "Chat language changed to English 🇬🇧!",
        "already_game": "There is already an active game in this chat.",
        "choose_cat": "Choose a category for the game:",
        "btn_heroes": "🦸 Superheroes",
        "btn_football": "⚽ Football",
        "only_creator_cat": "Only the game creator can choose the category.",
        "game_created_title": "Game created!",
        "category_label": "Category",
        "player_1": "Player 1",
        "join_instruction": "Second player — /join or the button, then the creator presses «Start game».",
        "football_rule": (
            "\n\n🎯 Important squad rule:\n"
            "If you have 3 or more defenders in your team, the team gets 15% stronger.\n"
            "If you have fewer than 3 defenders, the team is 15% weaker.\n"
            "Works the same for midfielders and forwards individually."
        ),
        "no_game": "Create a game first using /newgame.",
        "need_2_players": "Exactly 2 players are required.",
        "game_started": "🚀 Game started! Each player has ${budget}, need to collect {team_size}.",
        "already_ended": "The game has already ended.",
        "game_stopped": "🛑 The game was forcibly ended.",
        "pass_btn": "🚫 Pass",
        "skip_btn": "⏭ Skip",
        "bid_accepted": "Bid ${amount} accepted",
        "pass_accepted": "Pass",
        "lot_won": "✅ {hero} goes to <b>{winner}</b> for ${price}!\n\n{card}\n\n<b>{winner}'s Squad:</b>\n{roster}",
        "lot_skipped": "⏭ Everyone skipped <b>{hero}</b> — nobody got the lot. It will come back at the end if someone's squad isn't full.",
        "skip_accepted": "Skip",
        "lots_returned": "🔁 The lots are over, but not all squads are full. Bringing back the skipped lots ({count}) — now they must be taken!",
        "no_money_auto": (
            "🛑 Player <b>{loser}</b> doesn't have enough money for this lot.\n"
            "✅ {hero} goes to <b>{winner}</b> for ${price}!\n\n"
            "{card}\n\n<b>{winner}'s Squad:</b>\n{roster}"
        ),
        "game_over": "🏁 <b>Game Over!</b>",
        "winner": "🏆 Winner: <b>{name}</b>!",
        "draw": "🤝 Draw!",
        "hidden_stats": "❓ Hidden stats — revealed after purchase!",
        "current_bid": "💵 Current bid: ${bid}",
        "leading": " (leading: {name})",
        "turn": "👉 Turn: <b>{name}</b>",
        "positions": {"GK": "Goalkeeper", "DF": "Defender", "MF": "Midfielder", "FW": "Forward"},
        "positions_plural": {"GK": "Goalkeepers", "DF": "Defenders", "MF": "Midfielders", "FW": "Forwards"},
        "choose_mode": "Choose the superheroes game mode:",
        "btn_mode_classic": "🎯 Classic (4 slots)",
        "btn_mode_money": "💰 Until money runs out",
        "mode_label": "Mode",
        "mode_classic": "Classic (4 slots)",
        "mode_money": "Until money runs out",
        "choose_difficulty": "Choose difficulty (hero pool):",
        "btn_diff_easy": "🟢 Easy",
        "btn_diff_normal": "🟡 Normal",
        "btn_diff_hard": "🔴 Hard",
        "difficulty_label": "Difficulty",
        "diff_easy": "Easy",
        "diff_normal": "Normal",
        "diff_hard": "Hard",
        "cat_heroes": "Heroes",
        "cat_football": "Football",
        "btn_join": "🎮 Join",
        "btn_start": "🚀 Start game",
        "lobby_players": "Players ({n}/{max}):",
        "lobby_join_hint": "Press the button below or type /join to enter the game!",
        "lobby_hint_min": "Press «Start game» once at least 2 players have joined.",
        "lobby_hint_ready": "You can press «Start game» right now, or wait for more players.",
        "lobby_autostart": "⏳ The game starts automatically 2 minutes after creation.",
        "joined_ok": "You joined successfully!",
        "game_starting": "🎉 <b>The game begins! ({n} players)</b>\n\nParticipants:\n{players}\n\n",
        "game_started_money": "🚀 «Until money runs out» mode! Each player has ${budget}, no slot limit — buy heroes until your money is gone. Heroes in the pool: {pool}.",
        "alert_no_start": "The game has already started or was not found.",
        "only_creator_start": "Only the creator can start the game.",
        "need_min_players": "At least {n} players are needed to start.",
        "toast_started": "The game has started!",
        "countdown": "⏳ The game starts in {time}",
        "time_min": "min",
        "time_sec": "sec",
        "lobby_cancelled": "❌ Game cancelled: fewer than {n} players joined within 2 minutes.",
        "err_not_active": "The auction is not active.",
        "err_not_turn": "It's not your turn.",
        "err_cant_act": "You can't take part in this lot (squad is full or no money).",
        "err_over_budget": "Not enough money! Your budget: ${budget}.",
        "err_bid_low": "The bid must be higher than the current one (${bid}).",
        "err_bad_option": "That bid is not among the available options.",
        "err_skip_after_bid": "A bid has been made — you can raise or press «Pass».",
        "err_skip_leftover": "This lot came back at the end of the game — it must be taken.",
        "err_skip_limit": "No skips left (max {n} per game) — place a bid.",
        "err_pass_no_bid": "Pass is only available after a bid. If you don't want the lot — press «Skip».",
        "err_game_started": "The game has already started.",
        "err_already_in": "You are already in the game.",
        "err_max_players": "The game already has the maximum number of players ({n}).",
        "err_stale": "This auction message is outdated.",
        "only_players_end": "Only participants can end the game.",
        "history_title": "📜 Bids",
        "auto_passed": "⏩ Auto-pass (can't outbid): {names}",
        "afk_pass": "⏰ {name} didn't move for 3 minutes — automatic pass.",
        "afk_skip": "⏰ {name} didn't move for 3 minutes — automatic skip.",
        "afk_bid": "⏰ {name} didn't move for 3 minutes — automatic bid ${amount}.",
        "card_universe": "🌌 Universe",
        "card_power": "💪 Power",
        "card_speed": "⚡ Speed",
        "card_int": "🧠 Intelligence",
        "card_total": "📊 Total stats",
        "card_position": "📌 Position",
        "card_rating": "⚡ Rating",
        "status_lot": "Lot {n}/{total}",
        "status_line": "<b>{name}</b>: ${budget}, team ({count}): {names}",
        "end_power": "<b>{name}</b> — power: {power}{bonus}\n{team}\n(budget left: ${budget})",
        "end_synergy": " (+{pct}% synergy: {list})",
        "draw_names": "🤝 Draw! Equal power: <b>{names}</b>",
        "end_teams": "<b>{name}</b>\n{team}\n(budget left: ${budget})",
        "end_hidden_note": "🙈 <b>The winner is still hidden!</b>\nGenerate a battle — the AI will tell the story — or just find out the result.",
        "btn_gen_battle": "⚔️ Generate battle",
        "btn_reveal_winner": "🏆 Reveal winner without battle",
        "battle_generating": "⏳ The AI is writing the battle, please wait…",
        "battle_error": "😕 Could not generate the battle. Try again or reveal the winner without it.",
        "battle_no_key": "AI is not connected (no key). Press “Reveal winner without battle”.",
        "battle_busy": "The battle is already being generated, please wait.",
        "battle_only_players": "Only players of this game can press this button.",
        "battle_expired": "This game is already over.",
        "battle_lang_name": "English",
        "auto_award": "🛑 The others can't take part in this lot (squad is full or no money).\n✅ {hero} goes to <b>{winner}</b> for ${price}!\n\n{card}\n\n<b>{winner}'s Squad:</b>\n{roster}",
    },
    "uz": {
        "start": (
            "🎮 <b>Auksion</b>\n\n"
            "O'yinda ikki toifa bor: 🦸 Superqahramonlar va ⚽ Futbol. Har birining qoidalarini bilish uchun pastdagi tugmani bosing.\n\n"
            "Umumiy qoidalar:\n"
            "• Har bir o'yinchining budgeti $100 (qahramonlar klassik rejimda — $20)\n"
            "• Bot lotlarni navbat bilan ko'rsatadi (ko'rsatkichlar xariddan oldin yashirin)\n"
            "• Har bir lot uchun: stavkani oshiring yoki 'pas' deng\n"
            "• Skip — lot kerak emas: navbat raqibga o'tadi, hamma skip qilsa lot hech kimga tegmaydi (tarkib to'lmasa, oxirida qaytariladi)\n"
            "• Pas — stavkadan keyin taslim bo'lish: lot raqibga joriy narxda o'tadi\n"
            "• To'liq jamoani yig'ish kerak\n"
            "• Yakunda jamoaning umumiy kuchi hisoblanadi\n"
            "• Klassik rejimda stavka har bir yetishmayotgan o'rin uchun kamida $1 qoldirishi kerak\n"
            "• O'yin yaratilgandan 2 daqiqa o'tgach avtomatik boshlanadi\n"
            "• O'yinchi 3 daqiqa yurmasa, bot uning o'rniga pas yoki skip qiladi\n\n"
            "Buyruqlar:\n"
            "/start — qoidalar va botni guruhga qo'shish\n"
            "/lang — Guruh tilini tanlash / Choose chat language\n"
            "/newgame — o'yin yaratish (toifani tanlash)\n"
            "/join — o'yinga qo'shilish\n"
            "/status — joriy holat\n"
            "/endgame — o'yinni majburiy yakunlash"
        ),
        "rules_heroes": (
            "🦸 <b>Superqahramonlar</b>\n\n"
            "• O'yinchilar: 2 tadan 4 tagacha\n"
            "• 4 ta qahramondan iborat jamoa yig'ish kerak (klassik rejimda)\n"
            "• Har birining budgeti — klassik rejimda $20, «Pul tugaguncha» rejimida $100\n"
            "• Qahramonning uchta ko'rsatkichi bor: 💪 Kuch, ⚡ Tezlik, 🧠 Aql. Xarid qilinmaguncha ular yashirin turadi\n"
            "• Jamoa kuchi — barcha qahramonlar ko'rsatkichlari yig'indisi\n"
            "• 🌌 Olamlar sinergiyasi: bir olamdan 2 qahramon — jamoa kuchiga +10%, 3 va undan ko'p — +20% (har bir olam bo'yicha hisoblanadi, bonuslar qo'shiladi)\n"
            "• Rejimlar: 🎯 Klassik — 4 ta qahramondan iborat jamoa, budget $20, o'yinda ko'pi bilan 2 ta skip; 💰 Pul tugaguncha — o'rinlar cheklanmagan, pul tugaguncha qahramonlar sotib olinadi (2 o'yinchida 15 ta, 3 tada 25 ta, 4 tada 30 ta qahramon)\n"
            "• Qiyinlik (qahramonlar to'plami): 🟢 Oson — eng mashhur ~60 ta qahramon (Iron Man, Superman, Batman…); 🟡 Oddiy — kamroq mashhur qahramonlar (Gamora, Silver Surfer…) va kuchaytirilgan versiyalarning bir qismi; 🔴 Qiyin — barcha qahramonlar, jumladan barcha kuchaytirilgan versiyalar\n"
            "• Yakuniy kuchi eng katta jamoa g'alaba qozonadi"
        ),
        "rules_football": (
            "⚽ <b>Futbol</b>\n\n"
            "• O'yinchilar: 2 ta\n"
            "• 11 ta futbolchidan iborat tarkib yig'ish kerak\n"
            "• Har birining budgeti — $100\n"
            "• Har bir o'yinda auksionga 27 ta tasodifiy futbolchi tushadi: 3 darvozabon, 8 himoyachi, 8 yarim himoyachi, 8 hujumchi\n"
            "• Futbolchining bitta umumiy reytingi bor (EA SPORTS FC 26 bo'yicha). Xarid qilinmaguncha u yashirin turadi\n"
            "• Jamoa kuchi — futbolchilar reytinglari yig'indisi\n"
            "• 🎯 Tarkib qoidasi: kamida 1 darvozabon, 3 himoyachi, 3 yarim himoyachi va 3 hujumchi kerak. Bajarilgan har bir pozitsiya uchun kuchga +15%, bajarilmaganiga −15%\n"
            "• Yakuniy kuchi eng katta jamoa g'alaba qozonadi"
        ),
        "btn_rules_general": "📖 Umumiy qoidalar",
        "btn_add_to_group": "➕ Guruhga qo'shish",
        "select_lang": "Ushbu guruh uchun tilni tanlang / Choose language / Выберите язык:",
        "lang_changed": "Guruh tili O'zbek tiliga o'zgartirildi 🇺🇿!",
        "already_game": "Bu chatda faol o'yin mavjud.",
        "choose_cat": "O'yin toifasini tanlang:",
        "btn_heroes": "🦸 Superqahramonlar",
        "btn_football": "⚽ Futbol",
        "only_creator_cat": "Toifani faqat o'yin yaratuvchisi tanlaydi.",
        "game_created_title": "O'yin yaratildi!",
        "category_label": "Toifa",
        "player_1": "1-o'yinchi",
        "join_instruction": "Ikkinchi o'yinchi — /join yoki tugma, so'ng yaratuvchi «Boshlash» tugmasini bosadi.",
        "football_rule": (
            "\n\n🎯 Tarkib bo'yicha muhim qoida:\n"
            "Jamoangizda 3 va undan ortiq himoyachi bo'lsa — jamoa 15% kuchliroq bo'ladi.\n"
            "Himoyachilar 3 ta dan kam bo'lsa — 15% kuchsizroq bo'ladi.\n"
            "Yarim himoyachilar va hujumchilar uchun ham alohida ishlaydi."
        ),
        "no_game": "Avval /newgame buyrug'i orqali o'yin yarating.",
        "need_2_players": "Aynan 2 ta o'yinchi kerak.",
        "game_started": "🚀 O'yin boshlandi! Har biriga ${budget}, tarkib hajmi {team_size}.",
        "already_ended": "O'yin allaqachon yakunlangan.",
        "game_stopped": "🛑 O'yin majburan to'xtatildi.",
        "pass_btn": "🚫 Pas",
        "skip_btn": "⏭ Skip",
        "bid_accepted": "Stavka ${amount} qabul qilindi",
        "pass_accepted": "Pas",
        "lot_won": "✅ {hero} <b>{winner}</b> ga ${price} evaziga nasib etdi!\n\n{card}\n\n<b>{winner} tarkibi:</b>\n{roster}",
        "lot_skipped": "⏭ Hamma <b>{hero}</b> ni skip qildi — lot hech kimga nasib etmadi. Oxirida kimningdir tarkibi to'lmasa, u qaytariladi.",
        "skip_accepted": "Skip",
        "lots_returned": "🔁 Lotlar tugadi, lekin hamma tarkib to'lmadi. Skip qilingan lotlar ({count}) qaytariladi — endi ularni olish kerak!",
        "no_money_auto": (
            "🛑 O'yinchi <b>{loser}</b> da bu lot uchun mablag' yetarli emas.\n"
            "✅ {hero} <b>{winner}</b> ga ${price} evaziga nasib etdi!\n\n"
            "{card}\n\n<b>{winner} tarkibi:</b>\n{roster}"
        ),
        "game_over": "🏁 <b>O'yin tugadi!</b>",
        "winner": "🏆 G'olib: <b>{name}</b>!",
        "draw": "🤝 Durang!",
        "hidden_stats": "❓ Ko'rsatkichlar yashirin — xarid qilgach bilasiz!",
        "current_bid": "💵 Joriy stavka: ${bid}",
        "leading": " (yetakchi: {name})",
        "turn": "👉 O'yinchi yurishi: <b>{name}</b>",
        "positions": {"GK": "Darvozabon", "DF": "Himoyachi", "MF": "Yarim himoyachi", "FW": "Hujumchi"},
        "positions_plural": {"GK": "Darvozabonlar", "DF": "Himoyachilar", "MF": "Yarim himoyachilar", "FW": "Hujumchilar"},
        "choose_mode": "Superqahramonlar o'yin rejimini tanlang:",
        "btn_mode_classic": "🎯 Klassik (4 ta o'rin)",
        "btn_mode_money": "💰 Pul tugaguncha",
        "mode_label": "Rejim",
        "mode_classic": "Klassik (4 ta o'rin)",
        "mode_money": "Pul tugaguncha",
        "choose_difficulty": "Qiyinlik darajasini tanlang (qahramonlar to'plami):",
        "btn_diff_easy": "🟢 Oson",
        "btn_diff_normal": "🟡 Oddiy",
        "btn_diff_hard": "🔴 Qiyin",
        "difficulty_label": "Qiyinlik",
        "diff_easy": "Oson",
        "diff_normal": "Oddiy",
        "diff_hard": "Qiyin",
        "cat_heroes": "Qahramonlar",
        "cat_football": "Futbol",
        "btn_join": "🎮 Qo'shilish",
        "btn_start": "🚀 O'yinni boshlash",
        "lobby_players": "O'yinchilar ({n}/{max}):",
        "lobby_join_hint": "O'yinga kirish uchun pastdagi tugmani bosing yoki /join yozing!",
        "lobby_hint_min": "Kamida 2 ta o'yinchi to'plangach «O'yinni boshlash» tugmasini bosing.",
        "lobby_hint_ready": "«O'yinni boshlash» tugmasini hoziroq bosishingiz yoki yana o'yinchilarni kutishingiz mumkin.",
        "lobby_autostart": "⏳ O'yin yaratilgandan 2 daqiqa o'tgach avtomatik boshlanadi.",
        "joined_ok": "Siz muvaffaqiyatli qo'shildingiz!",
        "game_starting": "🎉 <b>O'yin boshlanmoqda! ({n} o'yinchi)</b>\n\nQatnashchilar:\n{players}\n\n",
        "game_started_money": "🚀 «Pul tugaguncha» rejimi! Har biriga ${budget}, o'rinlar cheklanmagan — pulingiz tugaguncha qahramonlarni sotib oling. Ro'yxatdagi qahramonlar: {pool}.",
        "alert_no_start": "O'yin allaqachon boshlangan yoki topilmadi.",
        "only_creator_start": "O'yinni faqat yaratuvchi boshlashi mumkin.",
        "need_min_players": "Boshlash uchun kamida {n} ta o'yinchi kerak.",
        "toast_started": "O'yin boshlandi!",
        "countdown": "⏳ O'yin boshlanishiga {time} qoldi",
        "time_min": "daq",
        "time_sec": "soniya",
        "lobby_cancelled": "❌ O'yin bekor qilindi: 2 daqiqa ichida kamida {n} ta o'yinchi to'planmadi.",
        "err_not_active": "Auksion faol emas.",
        "err_not_turn": "Hozir sizning navbatingiz emas.",
        "err_cant_act": "Siz bu lotda qatnasha olmaysiz (jamoa to'la yoki pul yo'q).",
        "err_over_budget": "Mablag' yetarli emas! Budgetingiz: ${budget}.",
        "err_bid_low": "Stavka joriy stavkadan (${bid}) yuqori bo'lishi kerak.",
        "err_bad_option": "Bunday stavka hozir variantlar orasida yo'q.",
        "err_skip_after_bid": "Stavka qilingan — oshirishingiz yoki «Pas» bosishingiz mumkin.",
        "err_skip_leftover": "Bu lot o'yin oxirida qaytarilgan — uni olish kerak.",
        "err_skip_limit": "Skiplar tugadi (o'yinda ko'pi bilan {n} ta) — stavka qiling.",
        "err_pass_no_bid": "Pas faqat stavkadan keyin mumkin. Lot kerak bo'lmasa — «Skip» bosing.",
        "err_game_started": "O'yin allaqachon boshlangan.",
        "err_already_in": "Siz allaqachon o'yindasiz.",
        "err_max_players": "O'yinda maksimal o'yinchilar soni ({n}) to'lgan.",
        "err_stale": "Bu eskirgan auksion xabari.",
        "only_players_end": "O'yinni faqat qatnashchilar yakunlashi mumkin.",
        "history_title": "📜 Stavkalar",
        "auto_passed": "⏩ Avto-pas (oshira olmaydi): {names}",
        "afk_pass": "⏰ {name} 3 daqiqa yurmadi — avtomatik pas.",
        "afk_skip": "⏰ {name} 3 daqiqa yurmadi — avtomatik skip.",
        "afk_bid": "⏰ {name} 3 daqiqa yurmadi — avtomatik stavka ${amount}.",
        "card_universe": "🌌 Olam",
        "card_power": "💪 Kuch",
        "card_speed": "⚡ Tezlik",
        "card_int": "🧠 Aql",
        "card_total": "📊 Umumiy ko'rsatkich",
        "card_position": "📌 Pozitsiya",
        "card_rating": "⚡ Reyting",
        "status_lot": "Lot {n}/{total}",
        "status_line": "<b>{name}</b>: ${budget}, jamoa ({count}): {names}",
        "end_power": "<b>{name}</b> — kuch: {power}{bonus}\n{team}\n(qolgan budget: ${budget})",
        "end_synergy": " (+{pct}% sinergiya: {list})",
        "draw_names": "🤝 Durang! Kuchi teng: <b>{names}</b>",
        "end_teams": "<b>{name}</b>\n{team}\n(qolgan budget: ${budget})",
        "end_hidden_note": "🙈 <b>G'olib hozircha yashirin!</b>\nJangni generatsiya qiling — AI hikoya qilib beradi — yoki natijani darhol bilib oling.",
        "btn_gen_battle": "⚔️ Jangni generatsiya qilish",
        "btn_reveal_winner": "🏆 Jangsiz g'olibni bilish",
        "battle_generating": "⏳ AI jangni o'ylab topmoqda, biroz kuting…",
        "battle_error": "😕 Jangni generatsiya qilib bo'lmadi. Qayta urinib ko'ring yoki g'olibni jangsiz bilib oling.",
        "battle_no_key": "AI ulanmagan (kalit yo'q). «Jangsiz g'olibni bilish» tugmasini bosing.",
        "battle_busy": "Jang allaqachon generatsiya qilinmoqda, kuting.",
        "battle_only_players": "Bu tugmani faqat o'yin ishtirokchilari bosa oladi.",
        "battle_expired": "Bu o'yin allaqachon tugagan.",
        "battle_lang_name": "o'zbek",
        "auto_award": "🛑 Boshqalar bu lotda qatnasha olmaydi (jamoa to'la yoki pul yo'q).\n✅ {hero} <b>{winner}</b> ga ${price} evaziga nasib etdi!\n\n{card}\n\n<b>{winner} tarkibi:</b>\n{roster}",
    },
}

# Храним язык всей группы по chat_id
CHAT_LANGUAGES = {}


def get_chat_lang(chat_id: int) -> str:
    return CHAT_LANGUAGES.get(chat_id, "ru")


def get_text(chat_id: int, key: str, **kwargs) -> str:
    lang = get_chat_lang(chat_id)
    text = TEXTS.get(lang, TEXTS["ru"]).get(key, TEXTS["ru"].get(key, ""))
    if isinstance(text, str) and kwargs:
        return text.format(**kwargs)
    return text


def get_text_by_lang(lang: str, key: str):
    return TEXTS.get(lang, TEXTS["ru"]).get(key, TEXTS["ru"].get(key, ""))
