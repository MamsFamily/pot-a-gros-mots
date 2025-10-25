
import os, re, time, sqlite3, asyncio, logging, random
from datetime import timedelta
import aiohttp
import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv

# ---------- ENV & CONFIG ----------
load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
UNB_TOKEN = os.getenv("UNBELIEVABOAT_API_TOKEN")
GUILD_ID = int(os.getenv("GUILD_ID", "0"))
JAR_USER_ID = int(os.getenv("JAR_USER_ID", "0"))
IGNORED_CHANNEL_IDS = [int(x) for x in os.getenv("IGNORED_CHANNEL_IDS", "").split(",") if x.strip().isdigit()]

MONNAIE_NOM = os.getenv("CURRENCY_NAME", "diamants")
MONTANT_DEPART = int(os.getenv("BASE_FINE", "50"))
FENETRE_H = int(os.getenv("WINDOW_HOURS", "24"))
USE_BANK = os.getenv("USE_BANK", "0") == "1"
WORDLIST_PATH = os.getenv("WORDLIST_PATH", "data/wordlist_fr.txt")

UNB_BASE = "https://unbelievaboat.com/api/v1"

# ---------- PUNCHLINES ----------
WARNING_LINES = [
    "Hey {user} ! On garde le campement cosy 😉 La prochaine écartade… ton porte-{money} va maigrir 💎",
    "{user}, petit rappel doux comme une loutre : on évite les gros mots 😇 La prochaine fois, les {money} filent.",
    "Chut {user}… Rockwell te surveille 🤫 Encore un mot qui pique et le pot grignote tes {money}.",
    "Oups {user} ! Même le bulbdog rougit 😳 Une de plus et tes {money} partent en balade.",
    "{user}, restons zen comme un spino au soleil 🌤️ Prochain écart = régime de {money} !",
    "L'ARK appelle au calme, {user} 🌿 Encore une et le bocal se sert en {money}.",
    "Tribu Arki'Family style : chill & smile ✨ {user}, next time… bye-bye quelques {money}.",
    "On respire {user} 😌 Les ravageurs n'aiment pas les gros mots. Prochaine fois : -{money} !",
    "Petit rappel de la base {user} : on parle doux, on survit mieux 🌸",
    "Même le dodo t'a entendu, {user} 🐤! Les {money} n'aiment pas la mauvaise humeur.",
    "Attention {user}, le pot frémit ! 😅 Encore une insulte et c'est la pluie de diamants inversée.",
    "Les spores murmurent : 'Du calme, {user}...' 🌫️ Tu veux pas réveiller le bocal !",
    "Une loutre t'a regardé bizarrement, {user} 🦦... On garde les vibes positives !",
    "Les Reapers entendent tout 👀 Reste cool, {user}, ton portefeuille te dira merci.",
    "Oh oh {user}... même l'Obélisque a clignoté. Prochaine fois, ce sera la taxe du pot 💎",
]
FINE_LINES = [
    "Aïe {user}… le pot a clignoté 💡 -{amount} {money}. Garde tes diamants au chaud 🤝",
    "Oups {user} ! Le bulbdog a tout entendu 👂 → -{amount} {money}. On reste good vibes ?",
    "Le bocal s'est servi, {user} : -{amount} {money}. On range les gros mots, on sort les cœurs 💙",
    "Petite offrande au pot à gros mots 💎 {user} : -{amount} {money}. Next step : zen attitude 🧘",
    "Les loutres jugent un peu… juste un peu 🦦 {user} : -{amount} {money}. On repart sur du friendly !",
    "Ça pique comme une plante d'Aberration 🌵 {user} : -{amount} {money}. On lisse le vocabulaire 😉",
    "Hop, contribution au totem Arki'Family ✨ {user} : -{amount} {money}. Team chill > team sel.",
    "Les diamants glissent de ta poche, {user}… -{amount} {money}. Un câlin de dodo et ça repart 🐤",
    "Rock Drake pas content 🐉 {user} : -{amount} {money}. On repasse en mode câlin ?",
    "Le bocal remercie ta générosité, {user} 😅 -{amount} {money}. La prochaine, pense à respirer !",
    "Les spores se nourrissent de jurons, {user} 😬... et elles coûtent -{amount} {money} chacune.",
    "C'est Rockwell qui rit maintenant 😈 {user}, il t'a pris -{amount} {money} pour sa collection.",
    "Le bulbdog a voté : -{amount} {money} 💎. Il t'envoie quand même un sourire lumineux !",
    "On n'énerve pas le pot sacré, {user} 😅 Tu perds -{amount} {money}, mais tu gagnes en sagesse !",
    "Aberration te regarde, {user}… et elle t'a fait une petite facture : -{amount} {money} 💰",
    "Tu viens de financer le spa des loutres 🦦 Merci pour les -{amount} {money}, {user} !",
    "Alerte pot à gros mots ! {user} perd -{amount} {money}. La prochaine fois, respire avant de taper 😮‍💨",
    "Les Nameless murmurent : *'Encore un mot et on double le tarif…'* 😏 -{amount} {money} prélevés.",
]
CONTEST_ACCEPTED = [
    "✅ Contestation acceptée ! Les esprits de l'ARK sont cléments. {amount} {money} remboursés 💎",
    "Accordé, {user} ! Les loutres ont plaidé ta cause 🦦 +{amount} {money} de retour dans ta besace.",
    "Les spores de bienveillance t'ont entendu 🌫️ {user} récupère {amount} {money}.",
    "Les ancêtres d'Arki'Family te pardonnent 🙏 +{amount} {money}. Fais-en bon usage !",
    "C'est ton jour de chance, {user} ! Le pot a levé la main : {amount} {money} remboursés ✨",
    "Un bulbdog t'a défendu au tribunal des mots doux 🐶 +{amount} {money} récupérés.",
    "Les dinos juges ont voté : *non coupable* 🦖 +{amount} {money} remis à {user}.",
]
CONTEST_DENIED = [
    "❌ Contestation refusée. Les spores sont formelles : on reste fair-play ✨",
    "Pas cette fois, {user}… Le conseil des bulbdogs a tranché 🐶. Respire et garde ton calme !",
    "Les loutres n'ont pas été convaincues 🦦 Verdict : amende maintenue 💎",
    "Les juges de l'ARK ont entendu ton plaidoyer… et se sont endormis 😴 Amende confirmée.",
    "Hmmm {user}, belle tentative, mais le pot n'oublie rien 😏 On passe à autre chose ?",
    "Les ancêtres chuchotent : 'Non, pas cette fois…' 🌌 Amende maintenue !",
    "Le bulbdog a levé un sourcil 👀 → contestation refusée. Essaie avec un câlin la prochaine fois 💙",
]
PING_RESPONSES = [
    "👀 Présent ! Le gardien du pot surveille… Les diamants sont en sécurité 💎",
    "🦦 Les loutres m'ont prévenu ! Je veille, toujours. Le vocabulaire reste propre ici ✨",
    "🌿 Campement Arki'Family sous surveillance ! Tout est calme… pour l'instant 😌",
    "🐉 Actif comme un Rock Drake la nuit ! Le bocal ne dort jamais 👁️",
    "💎 En ligne et à l'écoute ! Les gros mots ne passeront pas inaperçus 🤫",
    "🐤 Même le dodo m'a vu te ping ! Je surveille les ondes du serveur ✨",
    "🌫️ Les spores murmurent… le gardien est là ! Le pot veille sur les conversations 👀",
    "⚡ Opérationnel ! Rockwell m'a donné l'ordre de surveiller ce campement 🛡️",
    "🦖 Éveillé comme un spino affamé ! Le vocabulaire reste sous contrôle 😎",
    "💡 Connecté ! Le bulbdog brille, le pot fonctionne, les amendes sont prêtes… 💎",
    "🌸 Zen mais vigilant ! Les Reapers m'ont appris à tout entendre 👂",
    "✨ Toujours présent pour la tribu ! Le gardien des mots veille sur vous 🤗",
    "🔥 En mode surveillance ! L'Obélisque m'envoie toutes les notifs 📡",
    "🦦 Les loutres ont signalé ton ping ! Tout va bien au campement ? 😊",
    "💎 Bot actif, pot réactif ! Le vocabulaire cosy, c'est mon dada 🌿",
    "🐶 Bulbdog en alerte ! Je scanne chaque message pour garder l'ambiance familiale ✨",
    "⚔️ Gardien du lexique en faction ! Les Nameless ne passeront pas… ni les gros mots 😤",
    "🌙 Actif 24/7 comme les spores d'Aberration ! Le pot ne fait jamais de pause 💪",
    "🏕️ Ici, présent et opérationnel ! Le campement reste friendly sous ma garde 🛡️",
    "🦎 Plus rapide qu'un basilic ! Je détecte tout en temps réel 👀💨",
]
FAMILY_ROAST_RESPONSES = [
    "🦦 Ohhh, on parle de famille maintenant ? Les loutres d'ARK respectent leurs mamans… et toi ? 😏",
    "🐤 Les dodos ont plus de classe que ça ! On garde nos grands-mères en dehors des joutes verbales 💙",
    "🌿 Dans la tribu Arki'Family, on respecte les mamans ! Même les Gigas ont appris ça 🦖",
    "✨ Ta mère ? Sérieux ? Même Rockwell n'oserait pas. Reste respectueux, survivaliste ! 🛡️",
    "🦎 Les basilics sifflent de déception… On ne vise pas les familles dans notre campement 😌",
    "💎 Respecte les mères, les grand-mères et les sœurs ! C'est la règle d'or de l'ARK 🌟",
    "🐶 Le bulbdog secoue la tête… Les familles, c'est sacré. Trouve un autre angle d'attaque ! 😅",
    "🌫️ Les spores murmurent : 'Les mamans sont intouchables…' Même en plaisantant 🤫",
    "🦖 Un Rex respecte sa progéniture et ses ancêtres. Sois à la hauteur de ton dino préféré ! 💪",
    "⚡ L'Obélisque vient de clignoter en rouge… Règle #1 de l'ARK : respect des familles 🚨",
    "🏕️ Dans ce campement, les mères, grands-mères et sœurs sont protégées ! Trouve autre chose 😉",
    "🦦 Les loutres te jugent sévèrement… Elles adorent leurs mamans ! Sois sympa comme elles 💙",
    "🌸 On garde les conversations zen et respectueuses ici. Les familles = zone interdite ! ✋",
    "🐉 Même les Rock Drakes ne touchent pas aux familles adverses. C'est du bas niveau ça ! 😏",
    "💡 Alerte bon sens ! Les mamans, c'est sacré partout… même sur Aberration 🌌",
]

_last_pick = {"warn": None, "fine": None, "ok": None, "ko": None, "ping": None, "family": None}
_last_family_response_time = 0
_processed_messages = set()

def pick_line(pool, key):
    if not pool: return ""
    if len(pool) == 1: return pool[0]
    choice = random.choice(pool)
    while _last_pick.get(key) == choice:
        choice = random.choice(pool)
    _last_pick[key] = choice
    return choice

# ---------- WORDLIST (regex file) ----------
def load_wordlist(path: str):
    patterns = []
    if not os.path.exists(path):
        return patterns
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            patterns.append(line)
    return patterns

def compile_patterns(patterns):
    if not patterns:
        return None
    try:
        return re.compile("|".join(f"(?:{p})" for p in patterns), re.IGNORECASE)
    except re.error as e:
        logging.exception("Regex compile error: %s", e)
        return None

WORD_PATTERNS = load_wordlist(WORDLIST_PATH)
GROS_MOTS_RE = compile_patterns(WORD_PATTERNS)

def persist_wordlist(path: str, patterns):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        for p in patterns:
            f.write(p.strip() + "\n")

# ---------- DISCORD ----------
INTENTS = discord.Intents.default()
INTENTS.message_content = True
INTENTS.guilds = True
INTENTS.members = True

bot = commands.Bot(command_prefix="!", intents=INTENTS)
tree = bot.tree

# ---------- PERSISTANCE ----------
DB_PATH = "swearjar.sqlite3"
conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()
cur.execute("""
CREATE TABLE IF NOT EXISTS user_window (
    user_id INTEGER PRIMARY KEY,
    window_start INTEGER NOT NULL,
    offenses_in_window INTEGER NOT NULL,
    contest_used_at INTEGER
)""")
cur.execute("""CREATE TABLE IF NOT EXISTS ignored_channels (channel_id INTEGER PRIMARY KEY)""")
conn.commit()

# Précharger les salons ignorés
if IGNORED_CHANNEL_IDS:
    cur.executemany("REPLACE INTO ignored_channels (channel_id) VALUES (?)",
                    [(cid,) for cid in IGNORED_CHANNEL_IDS])
    conn.commit()

def now_ts() -> int:
    return int(time.time())

def get_user_state(user_id: int):
    cur.execute("SELECT window_start, offenses_in_window, contest_used_at FROM user_window WHERE user_id=?", (user_id,))
    row = cur.fetchone()
    if not row:
        return None
    return {"window_start": row[0], "offenses": row[1], "contest_used_at": row[2]}

def set_user_state(user_id: int, window_start: int, offenses: int, contest_used_at: int | None):
    cur.execute("REPLACE INTO user_window (user_id, window_start, offenses_in_window, contest_used_at) VALUES (?, ?, ?, ?)",
                (user_id, window_start, offenses, contest_used_at))
    conn.commit()

def channel_ignored(channel_id: int) -> bool:
    cur.execute("SELECT 1 FROM ignored_channels WHERE channel_id=?", (channel_id,))
    return cur.fetchone() is not None

def window_expired(window_start_ts: int) -> bool:
    if window_start_ts == 0: return True
    return now_ts() - window_start_ts >= FENETRE_H * 3600

# ---------- UNBELIEVABOAT API ----------
async def unb_update_balance(session: aiohttp.ClientSession, guild_id: int, user_id: int, delta: int):
    headers = {"Authorization": UNB_TOKEN, "Content-Type": "application/json"}
    payload = {"cash": delta} if not USE_BANK else {"bank": delta}
    url = f"{UNB_BASE}/guilds/{guild_id}/users/{user_id}"
    async with session.patch(url, headers=headers, json=payload) as resp:
        if resp.status >= 400:
            raise RuntimeError(f"UnbelievaBoat API error {resp.status}: {await resp.text()}")

async def apply_fine(user_id: int, amount: int):
    if amount <= 0: return
    async with aiohttp.ClientSession() as session:
        await unb_update_balance(session, GUILD_ID, user_id, -amount)
        if JAR_USER_ID and JAR_USER_ID != user_id:
            await unb_update_balance(session, GUILD_ID, JAR_USER_ID, amount)

async def refund_from_jar_to_user(user_id: int, amount: int):
    if amount <= 0: return
    async with aiohttp.ClientSession() as session:
        if JAR_USER_ID and JAR_USER_ID != user_id:
            await unb_update_balance(session, GUILD_ID, JAR_USER_ID, -amount)
        await unb_update_balance(session, GUILD_ID, user_id, amount)

def looks_like_context(msg: str, reason: str) -> bool:
    text = (msg + " " + (reason or "")).lower()
    keys = ["je cite", "citation", "contexte", "censur", "désolé", "pardon", "excuse", "quote", "context"]
    return any(k in text for k in keys) or ("*" in msg)

# ---------- COMMANDES IGNORED CHANNELS ----------
@tree.command(description="Ajouter un salon à la liste ignorée (exempt de détection)")
@app_commands.checks.has_permissions(manage_guild=True)
async def jar_ignore_add(interaction: discord.Interaction, channel: discord.TextChannel):
    cur.execute("REPLACE INTO ignored_channels (channel_id) VALUES (?)", (channel.id,))
    conn.commit()
    await interaction.response.send_message(f"✅ {channel.mention} sera ignoré.")

@tree.command(description="Retirer un salon de la liste ignorée")
@app_commands.checks.has_permissions(manage_guild=True)
async def jar_ignore_remove(interaction: discord.Interaction, channel: discord.TextChannel):
    cur.execute("DELETE FROM ignored_channels WHERE channel_id=?", (channel.id,))
    conn.commit()
    await interaction.response.send_message(f"✅ {channel.mention} est à nouveau surveillé.")

@tree.command(description="Lister les salons ignorés")
async def jar_ignore_list(interaction: discord.Interaction):
    cur.execute("SELECT channel_id FROM ignored_channels")
    rows = cur.fetchall()
    if not rows:
        return await interaction.response.send_message("Aucun salon ignoré.")
    mentions = []
    for (cid,) in rows:
        ch = interaction.guild.get_channel(cid)
        mentions.append(ch.mention if ch else f"<#{cid}>")
    await interaction.response.send_message("Salons ignorés : " + ", ".join(mentions))

# ---------- COMMANDES WORDLIST (ADMIN) ----------
def ensure_compiled(interaction: discord.Interaction):
    global GROS_MOTS_RE
    if GROS_MOTS_RE is None:
        return False
    return True

@tree.command(description="Ajouter un motif (regex) à la liste de gros mots")
@app_commands.checks.has_permissions(manage_guild=True)
async def jar_word_add(interaction: discord.Interaction, motif: str):
    global WORD_PATTERNS, GROS_MOTS_RE
    motif = motif.strip()
    if not motif:
        return await interaction.response.send_message("Motif vide.", ephemeral=True)
    if motif in WORD_PATTERNS:
        return await interaction.response.send_message("Ce motif existe déjà.", ephemeral=True)
    try:
        re.compile(motif, re.IGNORECASE)
    except re.error as e:
        return await interaction.response.send_message(f"Regex invalide : {e}", ephemeral=True)
    WORD_PATTERNS.append(motif)
    persist_wordlist(WORDLIST_PATH, WORD_PATTERNS)
    GROS_MOTS_RE = compile_patterns(WORD_PATTERNS)
    await interaction.response.send_message(f"✅ Motif ajouté et rechargé : `{motif}`")

@tree.command(description="Supprimer un motif existant (match exact de la ligne)")
@app_commands.checks.has_permissions(manage_guild=True)
async def jar_word_remove(interaction: discord.Interaction, motif: str):
    global WORD_PATTERNS, GROS_MOTS_RE
    motif = motif.strip()
    if motif not in WORD_PATTERNS:
        return await interaction.response.send_message("Motif introuvable.", ephemeral=True)
    WORD_PATTERNS = [m for m in WORD_PATTERNS if m != motif]
    persist_wordlist(WORDLIST_PATH, WORD_PATTERNS)
    GROS_MOTS_RE = compile_patterns(WORD_PATTERNS) if WORD_PATTERNS else None
    await interaction.response.send_message(f"🗑️ Motif supprimé et liste rechargée : `{motif}`")

@tree.command(description="Lister les motifs (paginé)")
@app_commands.checks.has_permissions(manage_guild=True)
async def jar_word_list(interaction: discord.Interaction, page: int = 1, page_size: int = 20):
    if page < 1: page = 1
    start = (page - 1) * page_size
    end = start + page_size
    total = len(WORD_PATTERNS)
    chunk = WORD_PATTERNS[start:end]
    if not chunk:
        return await interaction.response.send_message(f"Page vide. Total motifs: {total}", ephemeral=True)
    body = "\n".join(f"{i+1}. `{p}`" for i,p in enumerate(chunk, start=start))
    await interaction.response.send_message(f"**Motifs (page {page})**\n{body}\n\nTotal: {total}")

@tree.command(description="Recharger la wordlist depuis le fichier")
@app_commands.checks.has_permissions(manage_guild=True)
async def jar_word_reload(interaction: discord.Interaction):
    global WORD_PATTERNS, GROS_MOTS_RE
    WORD_PATTERNS = load_wordlist(WORDLIST_PATH)
    GROS_MOTS_RE = compile_patterns(WORD_PATTERNS)
    await interaction.response.send_message(f"🔁 Wordlist rechargée ({len(WORD_PATTERNS)} motifs).")

@tree.command(description="Tester un texte contre la wordlist (affiche les motifs correspondants)")
@app_commands.checks.has_permissions(manage_guild=True)
async def jar_word_test(interaction: discord.Interaction, texte: str):
    if not GROS_MOTS_RE:
        return await interaction.response.send_message("La wordlist est vide ou invalide.", ephemeral=True)
    matches = []
    for pat in WORD_PATTERNS:
        try:
            rg = re.compile(pat, re.IGNORECASE)
            if rg.search(texte):
                matches.append(pat)
        except re.error:
            continue
    if not matches:
        return await interaction.response.send_message("✅ Aucun motif ne détecte ce texte.")
    preview = "\n".join(f"- `{m}`" for m in matches[:30])
    extra = "" if len(matches) <= 30 else f"\n… et {len(matches)-30} de plus."
    await interaction.response.send_message(f"⚠️ Motifs détectés ({len(matches)}) :\n{preview}{extra}")

@tree.command(description="Réinitialiser le compteur d'infractions d'un joueur (Admin)")
@app_commands.checks.has_permissions(manage_guild=True)
async def jar_reset(interaction: discord.Interaction, joueur: discord.User):
    user_id = joueur.id
    conn = sqlite3.connect("jar.db")
    c = conn.cursor()
    c.execute("DELETE FROM user_state WHERE user_id = ?", (user_id,))
    conn.commit()
    deleted = c.rowcount
    conn.close()
    if deleted > 0:
        await interaction.response.send_message(f"🔄 Compteur réinitialisé pour {joueur.mention} ! Prochain gros mot = 50 {MONNAIE_NOM}.")
    else:
        await interaction.response.send_message(f"Aucune infraction trouvée pour {joueur.mention}.", ephemeral=True)

# ---------- CONTESTATION ----------
@tree.command(description="Contester la dernière amende (1 fois / 24h)")
async def contester(interaction: discord.Interaction, raison: str):
    user_id = interaction.user.id
    st = get_user_state(user_id)
    now = now_ts()
    if not st or st["offenses"] <= 1 or window_expired(st["window_start"]):
        return await interaction.response.send_message("Rien à contester pour l'instant 👍", ephemeral=True)
    if st["contest_used_at"] and now - st["contest_used_at"] < 24*3600:
        return await interaction.response.send_message("⛔ Tu as déjà contesté dans les dernières 24h.", ephemeral=True)

    last_amount = (st["offenses"] - 1) * MONTANT_DEPART
    approve = looks_like_context("", raison)

    if approve:
        try:
            await refund_from_jar_to_user(user_id, last_amount)
        except Exception as e:
            return await interaction.response.send_message(f"Erreur API lors du remboursement : {e}", ephemeral=True)
        new_off = st["offenses"] - 1
        set_user_state(user_id, st["window_start"], new_off, now)
        line = random.choice(CONTEST_ACCEPTED).format(user=interaction.user.mention, amount=last_amount, money=MONNAIE_NOM)
        await interaction.response.send_message(line)
    else:
        set_user_state(user_id, st["window_start"], st["offenses"], now)
        line = random.choice(CONTEST_DENIED).format(user=interaction.user.mention)
        await interaction.response.send_message(line, ephemeral=True)

# ---------- EVENTS ----------
@bot.event
async def on_ready():
    try:
        await tree.sync()
    except Exception as e:
        logging.exception(e)
    print(f"Connecté en tant que {bot.user} • Guild: {GUILD_ID} • Wordlist motifs: {len(WORD_PATTERNS)}")

@bot.event
async def on_message(message: discord.Message):
    if message.guild is None or message.author.bot:
        return
    if message.guild.id != GUILD_ID:
        return
    
    global _processed_messages
    if message.id in _processed_messages:
        return
    _processed_messages.add(message.id)
    if len(_processed_messages) > 1000:
        _processed_messages = set(list(_processed_messages)[-500:])
    
    content = message.content or ""
    
    if bot.user in message.mentions:
        line = pick_line(PING_RESPONSES, "ping")
        await message.channel.send(line)
        return
    
    if channel_ignored(message.channel.id):
        return
    if not content:
        return
    
    family_pattern = re.compile(r'\b(ta\s+(m[eè]re|grand[\s\-]?m[eè]re|s[oœ]eur|daronne|reume))\b', re.IGNORECASE)
    if family_pattern.search(content):
        global _last_family_response_time
        now = now_ts()
        if now - _last_family_response_time >= 60:
            _last_family_response_time = now
            line = pick_line(FAMILY_ROAST_RESPONSES, "family")
            await message.channel.send(line)
        return
    
    if not GROS_MOTS_RE:
        return

    if GROS_MOTS_RE.search(content):
        user_id = message.author.id
        st = get_user_state(user_id)
        now = now_ts()

        if (not st) or window_expired(st["window_start"]):
            offenses = 1
            set_user_state(user_id, now, offenses, None)
        else:
            offenses = st["offenses"] + 1
            set_user_state(user_id, st["window_start"], offenses, st["contest_used_at"])

        fine = offenses * MONTANT_DEPART
        try:
            await apply_fine(user_id, fine)
        except Exception as e:
            await message.channel.send(f"⚠️ Impossible d'appliquer l'amende (API) : {e}")
            return
        line = random.choice(FINE_LINES).format(user=message.author.mention, amount=fine, money=MONNAIE_NOM)
        
        can_contest = not (st and st["contest_used_at"] and now - st["contest_used_at"] < 24*3600)
        if can_contest:
            line += f"\n💡 Tu peux contester avec `/contester raison:` (1×/24h)."
        
        await message.channel.send(line)

    await bot.process_commands(message)

# ---------- RUN ----------
if __name__ == "__main__":
    if not all([DISCORD_TOKEN, UNB_TOKEN, GUILD_ID]):
        raise SystemExit("⚠️ Configure DISCORD_TOKEN, UNBELIEVABOAT_API_TOKEN et GUILD_ID dans l'environnement.")
    try:
        from keep_alive import keep_alive
        keep_alive()
    except Exception as e:
        print("Keep-alive non démarré (optionnel):", e)
    bot.run(DISCORD_TOKEN)
