# 🚂 Déploiement sur Railway

## ✅ Fichiers de configuration Railway

Ce projet contient les fichiers nécessaires pour Railway :
- **`nixpacks.toml`** : Force Python 3.11 (requis pour éviter l'erreur audioop)
- **`runtime.txt`** : Spécifie la version Python
- **`Procfile`** : Commande de démarrage du bot
- **`requirements.txt`** : Dépendances Python

## 🔧 Configuration des variables d'environnement

Dans Railway → Variables, ajoutez **SANS GUILLEMETS** :

### Variables obligatoires :
```
DISCORD_TOKEN=votre_token_discord_ici
UNBELIEVABOAT_API_TOKEN=votre_token_unbelievaboat
GUILD_ID=votre_server_id
JAR_USER_ID=id_du_compte_pot
```

### Variables optionnelles (avec valeurs par défaut) :
```
CURRENCY_NAME=diamants
BASE_FINE=50
WINDOW_HOURS=24
USE_BANK=0
WORDLIST_PATH=data/wordlist_fr.txt
IGNORED_CHANNEL_IDS=
```

## 🚀 Déploiement

1. **Connectez votre repo GitHub** à Railway
2. **Ajoutez les variables** d'environnement (voir ci-dessus)
3. **Déployez** : Railway détectera automatiquement nixpacks.toml
4. **Vérifiez les logs** : Vous devriez voir "Connecté en tant que..."

## ⚠️ Problèmes courants

### Erreur : `ModuleNotFoundError: No module named 'audioop'`
**Cause** : Python 3.13 utilisé au lieu de 3.11
**Solution** : Le fichier `nixpacks.toml` force Python 3.11. Assurez-vous qu'il est bien présent.

### Erreur : Token invalide
**Cause** : Variable DISCORD_TOKEN manquante ou incorrecte
**Solution** : Vérifiez que le token est bien ajouté dans Railway → Variables (pas de guillemets)

### Le bot ne répond pas
**Cause** : GUILD_ID incorrect
**Solution** : Vérifiez que GUILD_ID correspond bien à votre serveur Discord

## 📊 Vérifier que ça fonctionne

Dans les logs Railway, vous devriez voir :
```
Connecté en tant que Pot à gros mots#6347 • Guild: 1156256997403000874 • Wordlist motifs: 127
```

Si vous voyez ce message, le bot est **opérationnel** ! 🎉
