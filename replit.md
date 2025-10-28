# Arki'Family — Bot Discord "Pot à Gros Mots"

## Vue d'ensemble
Bot Discord français pour serveur de gaming Arki'Family qui détecte automatiquement les gros mots et applique des amendes progressives dès la première infraction via l'API UnbelievaBoat. Système ludique et bon enfant avec des punchlines amusantes inspirées du jeu ARK.

## État actuel (25 octobre 2025)
- ✅ Bot Discord fonctionnel avec détection automatique de gros mots (regex)
- ✅ Système d'amendes progressives dès la 1ère infraction (50 → 100 → 150 → 200 diamants sur 24h)
- ✅ Intégration complète avec UnbelievaBoat API
- ✅ Système de contestation (1 fois par 24h)
- ✅ Gestion dynamique de la liste de mots via commandes slash
- ✅ Salons ignorés configurables
- ✅ Réponse au ping avec 20 phrases thématiques ARK
- ✅ Détection "ta mère/grand-mère/sœur" avec réponse humoristique (sans amende)
- ✅ Base de données SQLite pour la persistance
- ✅ Keep-alive Flask pour Replit

## Architecture du projet

### Structure des fichiers
```
/
├── bot.py                  # Bot Discord principal (404 lignes)
├── keep_alive.py           # Serveur Flask pour maintenir le bot actif
├── test_unbelieva_api.py   # Script de test API UnbelievaBoat
├── requirements.txt        # Dépendances Python
├── data/
│   └── wordlist_fr.txt    # Liste des motifs regex de gros mots (131 lignes)
├── .env.example           # Modèle de configuration
├── .gitignore            # Fichiers à ignorer
├── README.md             # Documentation utilisateur
└── swearjar.sqlite3      # Base de données (créée au runtime)
```

### Technologies utilisées
- **Python 3.11** avec discord.py 2.4.0
- **Discord Bot** avec slash commands
- **UnbelievaBoat API** pour la gestion de la monnaie virtuelle
- **SQLite** pour la persistance des données
- **Flask + Waitress** pour le keep-alive sur Replit
- **Regex Python** pour la détection de mots

## Fonctionnalités principales

### 1. Réponse au ping
- Mentionnez le bot avec `@BotName` dans n'importe quel salon
- Le bot répond avec une phrase aléatoire parmi 20 variantes thématiques ARK
- Confirme qu'il est en ligne et surveille activement
- Système anti-répétition (pas la même phrase deux fois de suite)

### 2. Rappel de respect familial
- Détecte automatiquement "ta mère", "ta grand-mère", "ta sœur" (et variantes)
- Répond avec humour (15 phrases thématiques ARK)
- **Aucune amende** appliquée, juste un rappel bon enfant
- **Cooldown anti-spam** : Une seule réponse par minute maximum
- Fonctionne dans tous les salons (même non ignorés)

### 3. Détection automatique et amendes
- Scan de tous les messages du serveur
- Détection via regex (liste extensible)
- **Amende dès la 1ère infraction** (pas d'avertissement gratuit)
- **Fenêtre de 24h** : Les infractions s'accumulent sur 24h
- **Progression** : 50 → 100 → 150 → 200 → 250 diamants... (progression de 50 en 50)
- **Débit automatique** via UnbelievaBoat
- **Crédit du pot** : Les amendes vont au compte-jarre

### 4. Contestation
- 1 contestation par joueur toutes les 24h
- Acceptation automatique si raison valable (contexte, citation, etc.)
- Remboursement depuis le pot vers le joueur
- **Résultats publics** : Acceptations et refus visibles de tous dans le salon

### 5. Commandes slash (Admin)

**Gestion des salons ignorés :**
- `/jar_ignore_add #salon` - Ignorer un salon
- `/jar_ignore_remove #salon` - Retirer de la liste
- `/jar_ignore_list` - Afficher la liste

**Gestion de la liste de mots :**
- `/jar_word_add motif:` - Ajouter un motif regex
- `/jar_word_remove motif:` - Supprimer un motif
- `/jar_word_list page:` - Lister les motifs (paginé)
- `/jar_word_reload` - Recharger depuis le fichier
- `/jar_word_test texte:` - Tester un texte

**Gestion du système :**
- `/jar_reset joueur:` - Réinitialiser le compteur d'infractions d'un joueur spécifique

**Contestation (utilisateurs) :**
- `/contester raison:` - Contester la dernière amende

## Configuration

### Variables d'environnement requises
Configurer dans les **Secrets Replit** :

```env
# Obligatoires
DISCORD_TOKEN=votre_token_discord
UNBELIEVABOAT_API_TOKEN=votre_token_unbelievaboat
GUILD_ID=123456789012345678
JAR_USER_ID=234567890123456789

# Optionnels
IGNORED_CHANNEL_IDS=1234567890,9876543210
CURRENCY_NAME=diamants
BASE_FINE=100
WINDOW_HOURS=24
USE_BANK=0
WORDLIST_PATH=data/wordlist_fr.txt
```

### Étapes de déploiement

1. **Configurer les secrets Replit** avec vos tokens Discord et UnbelievaBoat
2. **Inviter le bot** sur votre serveur Discord avec les permissions :
   - Read Messages/View Channels
   - Send Messages
   - Use Slash Commands
   - Message Content Intent (activé dans Discord Developer Portal)
3. **Démarrer le bot** : Le workflow lancera automatiquement `python bot.py`
4. **Attendre la synchronisation** des slash commands (quelques secondes)
5. **Tester** avec `/jar_word_test` pour vérifier la détection

### Test de l'API UnbelievaBoat
Avant de lancer le bot, testez votre configuration :
```bash
python test_unbelieva_api.py
```

## Base de données

### Tables SQLite

**user_window** : Fenêtre d'infractions par utilisateur
- `user_id` : ID Discord de l'utilisateur
- `window_start` : Timestamp de début de fenêtre
- `offenses_in_window` : Nombre d'infractions dans la fenêtre
- `contest_used_at` : Timestamp de la dernière contestation

**ignored_channels** : Salons ignorés
- `channel_id` : ID du salon Discord

## Wordlist (Liste de mots)

### Format
- Fichier texte avec motifs regex Python (un par ligne)
- Lignes vides et commençant par `#` sont ignorées
- Support des bornes de mots `\b`, caractères spéciaux, etc.

### Exemples de motifs
```regex
\bmerde(s)?\b              # Détecte "merde" ou "merdes"
\bput[ae]in(s)?\b          # Détecte "putain", "putin", "putains"
p\W*?t[ua]in               # Détecte variations avec espaces/ponctuation
fdp                        # Détecte l'acronyme
```

### Gestion dynamique
La liste peut être modifiée :
- En ligne via `/jar_word_add` et `/jar_word_remove`
- Manuellement en éditant `data/wordlist_fr.txt` puis `/jar_word_reload`

## Punchlines

Le bot utilise des messages aléatoires thématiques ARK pour :
- **Ping/Mention** (20 variantes) : Quand le bot est mentionné
- **Rappel familial** (15 variantes) : Détection "ta mère", "ta grand-mère", "ta sœur"
- **Amendes** (18 variantes) : Détection de gros mots (dès la 1ère infraction)
- **Contestation acceptée** (7 variantes)
- **Contestation refusée** (7 variantes)

Système anti-répétition pour éviter le même message deux fois de suite dans chaque catégorie.

## Sécurité

### Bonnes pratiques
- ✅ Tokens stockés dans les Secrets Replit (jamais dans le code)
- ✅ API UnbelievaBoat utilisée de manière sécurisée
- ✅ Gestion d'erreurs pour éviter les crashes
- ✅ Validation regex avant ajout de motifs
- ✅ Permissions Discord requises pour les commandes admin

### Avertissements
- La wordlist est large et peut générer des faux positifs
- Testez avec `/jar_word_test` avant d'ajouter des motifs agressifs
- Le bot ne détecte que dans le serveur configuré (GUILD_ID)
- Les amendes ne s'appliquent que si l'utilisateur a assez de fonds UnbelievaBoat

## Maintenance

### Logs à surveiller
- Erreurs de connexion à l'API UnbelievaBoat
- Échecs de synchronisation des slash commands
- Erreurs de regex lors du chargement de la wordlist
- Problèmes de connexion Discord

### Commandes utiles
```bash
# Tester l'API UnbelievaBoat
python test_unbelieva_api.py

# Voir les logs du bot
# (disponibles dans la console Replit)

# Recharger la wordlist sans redémarrer
# Utiliser /jar_word_reload dans Discord
```

## Améliorations futures possibles

### Phase 2 (Non implémentée)
- Dashboard web pour visualiser les statistiques
- Historique complet des infractions avec export CSV
- Badges/récompenses pour les joueurs les plus calmes
- Graphiques d'évolution du pot dans le temps
- Système de vote communautaire pour les contestations
- Notifications hebdomadaires avec classement

## Support

Pour toute question ou problème :
1. Vérifier que tous les secrets sont configurés
2. Tester l'API avec `test_unbelieva_api.py`
3. Consulter les logs dans la console Replit
4. Vérifier que les intents Discord sont activés dans le Developer Portal

## Notes de développement

### Changements récents (25/10/2025)
- Configuration initiale du projet sur Replit
- Installation de Python 3.11 et dépendances
- Création de la structure de fichiers
- Configuration du workflow
- Ajout de la fonctionnalité de réponse au ping (30 phrases thématiques → doublé !)
- Ajout de la détection "ta mère/grand-mère/sœur" avec réponses contextuelles (14 mère, 13 grand-mère, 14 sœur)
- Modification du système d'amendes : suppression de l'avertissement gratuit, amendes dès la 1ère infraction (50 → 100 → 150...)
- Ajout de la commande admin `/jar_reset joueur:` pour réinitialiser le compteur d'un joueur spécifique
- Ajout d'un rappel automatique pour contester l'amende (quand encore possible)
- Ajout d'un cooldown de 10 secondes sur les réponses "famille" pour éviter le spam
- Ajout d'un système de déduplication des messages pour garantir une seule réponse par message
- Ping systématique du joueur au début du message d'amende pour notification garantie
- Résultats de contestation rendus publics (visible de tous au lieu de privé)
- **Enrichissement massif des phrases** : 33 amendes, 15 acceptations, 15 refus, 30 pings, 41 réponses famille
- **Amélioration de la rotation** : système anti-répétition pour toutes les catégories de phrases
- **Réponses famille contextuelles** : le bot répond avec des phrases cohérentes selon le membre mentionné (mère/grand-mère/sœur)
- **Traduction complète en français** : toutes les commandes slash ont été traduites (pot_mot_ajouter, pot_ignorer_liste, etc.)
- **Configuration Railway** : ajout de nixpacks.toml, Procfile, runtime.txt pour déploiement sur Railway (force Python 3.11)

### Conventions de code
- Python avec type hints partiel (`int | None`)
- Variables globales en MAJUSCULES
- Fonctions async pour Discord et UnbelievaBoat
- Commentaires en français pour la lisibilité

### Dépendances critiques
- `discord.py==2.4.0` : API Discord avec slash commands
- `aiohttp>=3.9.5` : Requêtes HTTP async pour UnbelievaBoat
- `python-dotenv>=1.0.1` : Gestion des variables d'environnement
- `Flask>=3.0.0` + `waitress>=3.0.0` : Keep-alive sur Replit
