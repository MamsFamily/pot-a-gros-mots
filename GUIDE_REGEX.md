# 📝 Guide des expressions régulières (Regex) pour le pot à gros mots

## 🎯 Principe de base : Éviter les faux positifs

Pour éviter que "con" soit détecté dans "content", "second", "acon", etc., il faut utiliser des **délimiteurs de mots** : `\b`

---

## ✅ Exemples corrects

### Mot simple :
```regex
\bcon\b
```
- ✅ Détecte : `con`, `Con`, `CON`
- ❌ Ne détecte PAS : `content`, `second`, `bacon`, `console`

### Mot avec variantes (singulier/pluriel) :
```regex
\bconnard(s)?\b
```
- ✅ Détecte : `connard`, `connards`
- ❌ Ne détecte PAS : `connarde` (il faut ajouter : `\bconnard(s|e|es)?\b`)

### Mot avec variations orthographiques :
```regex
\bpu(te|t[eé]e)s?\b
```
- ✅ Détecte : `pute`, `putes`, `putée`, `putées`

### Expression complète :
```regex
\bva te faire foutre\b
```
- ✅ Détecte : `va te faire foutre`
- ❌ Ne détecte PAS : si les mots sont séparés par plusieurs espaces

### Expression avec espaces variables :
```regex
\bva\s+te\s+faire\s+foutre\b
```
- ✅ Détecte : `va te faire foutre`, `va  te  faire  foutre`

### Expression avec ponctuation/caractères spéciaux :
```regex
\btrou\W*du\W*cul\b
```
- ✅ Détecte : `trou du cul`, `trou-du-cul`, `trou_du_cul`
- `\W*` = zéro ou plusieurs caractères non-alphanumériques

---

## ❌ Erreurs courantes

### ❌ MAUVAIS : Sans délimiteurs
```regex
con
```
- Problème : détecte "con" dans `content`, `second`, `bacon`, etc.

### ❌ MAUVAIS : Délimiteur uniquement au début
```regex
\bcon
```
- Problème : détecte "con" dans `content`, `console`

### ❌ MAUVAIS : Caractères spéciaux non échappés
```regex
c'est quoi ce bordel?
```
- Problème : `?` est un caractère spécial regex
- ✅ CORRECT : `c'est quoi ce bordel\?` ou `c'est quoi ce bordel`

---

## 🔧 Symboles regex utiles

| Symbole | Signification | Exemple |
|---------|---------------|---------|
| `\b` | Délimiteur de mot | `\bcon\b` |
| `?` | 0 ou 1 occurrence | `connard(s)?` = connard ou connards |
| `+` | 1 ou plusieurs | `con+` = con, conn, connn |
| `*` | 0 ou plusieurs | `con*` = co, con, conn |
| `(a\|b)` | a OU b | `(con\|idiot)` |
| `[abc]` | a ou b ou c | `[ée]` = é ou è |
| `\s` | Espace blanc | `ta\s+gueule` |
| `\W` | Non-alphanumérique | `trou\W*du\W*cul` |
| `\d` | Chiffre | `[0-9]` |
| `.` | N'importe quel caractère | `p.tain` |

---

## 💡 Exemples pratiques

### Détecter "con" uniquement :
```regex
\bcon\b
```

### Détecter "con" et "conne" :
```regex
\bconn?e?\b
```

### Détecter toutes les formes de "connard" :
```regex
\bconn?ard(s|e|es)?\b
```
- connard, connards, connarde, connardes

### Détecter "putain" avec leet speak (p@t@in, put4in) :
```regex
p[u@*]t[a@4]in
```

### Détecter "ta gueule" avec/sans espace :
```regex
ta\W?gueule
```
- ta gueule, ta-gueule, tagueule

---

## 🧪 Tester vos regex

Utilisez la commande Discord :
```
/pot_mot_tester texte: votre phrase de test
```

Exemples :
- `/pot_mot_tester texte: je suis content` → ne doit PAS détecter `\bcon\b`
- `/pot_mot_tester texte: t'es con` → DOIT détecter `\bt'es con\b`

---

## ⚠️ Attention aux accents

Les regex sont **insensibles à la casse** (majuscules/minuscules) mais PAS aux accents !

Pour détecter "é" et "e" :
```regex
[eé]
```

Exemple :
```regex
\bp[eé]tain\b
```
- Détecte : pétain, petain, Pétain, PETAIN

---

## 📚 Ressources

- Testeur en ligne : https://regex101.com/ (choisir "Python" en flavor)
- Documentation Python : https://docs.python.org/fr/3/library/re.html

---

## 🎯 Résumé rapide

**Pour éviter les faux positifs, TOUJOURS utiliser `\b` autour des mots !**

✅ Bon : `\bcon\b`
❌ Mauvais : `con`
