# Arki'Family — Swear Jar Bot (Discord + UnbelievaBoat)

Bot "pot à gros mots" bon enfant : amendes progressives dès la 1ère infraction (50 → 100 → 150 → 200…) sur 24h,
intégration UnbelievaBoat (débit joueur + crédit de la jarre), contestation 1×/24h, salons ignorés,
liste FR de gros mots **extensible en live** via commandes slash.

**Nouvelle fonctionnalité** : Mentionnez le bot (@BotName) pour vérifier qu'il est en ligne et surveille !

## Déploiement (Replit)
1. Créer un Repl Python et importer ce dossier.
2. Installer les deps : `pip install -r requirements.txt`
3. Copier `.env.example` dans les *Secrets* Replit (adapter les valeurs).
4. Run `bot.py`. Attendre la synchro des slash commands.
5. Inviter le bot (intents activés : Message Content, etc.).

## Fonctionnalités

### Réponse au ping
Mentionnez le bot avec `@BotName` et il répondra avec une phrase aléatoire pour signaler qu'il est actif et surveille (30 variantes thématiques ARK).

### Rappel de respect familial (sans amende)
Le bot détecte automatiquement les phrases comme **"ta mère"**, **"ta grand-mère"**, **"ta sœur"** et répond avec humour pour rappeler le respect des familles. Aucune amende n'est appliquée, juste un petit rappel bon enfant thématique ARK ! 

**Cooldown anti-spam** : Le bot ne répond qu'**une seule fois toutes les 10 secondes** maximum, même si "ta mère" est écrit plusieurs fois.

**Réponses contextuelles** : Le bot choisit des phrases adaptées selon le membre de famille mentionné (mère, grand-mère, ou sœur) pour des réponses cohérentes.

### Commandes slash (admin = Manage Server requis)
- `/pot_ignorer_ajouter channel:` — ignorer un salon
- `/pot_ignorer_retirer channel:` — retirer de la liste d'ignore
- `/pot_ignorer_liste` — afficher la liste

### Contestation (tous les utilisateurs)
- `/contester raison:` — contestation (1×/24h pour chaque joueur)

### Gestion dynamique de la liste de mots (regex)
- `/pot_mot_ajouter motif:` — ajoute un **motif regex** à la liste et recharge
- `/pot_mot_retirer motif:` — supprime un motif existant (match exact de la ligne)
- `/pot_mot_liste page:` — affiche la liste paginée
- `/pot_mot_recharger` — recharge le fichier (utile après édition manuelle)
- `/pot_mot_tester texte:` — teste une phrase et montre les motifs qui détectent

### Gestion du système
- `/pot_reinitialiser joueur:` — réinitialise le compteur d'infractions d'un joueur spécifique

> Les motifs sont des **regex Python**. Voir `data/wordlist_fr.txt` pour des exemples.
> Lignes vides ou commençant par `#` sont ignorées.

## Variables utiles (.env)
- `CURRENCY_NAME` — nom d'affichage de la monnaie (ex: diamants)
- `BASE_FINE` — montant de base de l'amende (50 par défaut, progression : 50 → 100 → 150…)
- `WINDOW_HOURS` — durée de la fenêtre (24h par défaut)
- `USE_BANK` — `1` pour utiliser la *bank* UnbelievaBoat au lieu du *cash*
- `WORDLIST_PATH` — chemin vers le fichier de liste (par défaut `data/wordlist_fr.txt`)

## Sécurité & prudence
- La liste est **large** donc sujette à faux positifs. Ajustez selon vos usages.
- Utilisez `/jar_word_test` avant d'activer des motifs agressifs.
