# Semi-Marathon Saint-Jory — Site web

Site officiel de la **1ère édition du Semi-Marathon de Saint-Jory**  
📅 Dimanche 29 novembre 2026 — Halle des Sports Allison Pineau, Saint-Jory (31790)

---

## Prérequis

### 1. Installer Ruby (Windows)

1. Aller sur **https://rubyinstaller.org/downloads/**
2. Télécharger **Ruby+Devkit 3.x (x64)** (la version recommandée en gras)
3. Lancer l'installeur en cochant **"Add Ruby executables to your PATH"**
4. À la fin, laisser cocher la case MSYS2/MINGW — appuyer sur **Entrée** pour tout installer, puis **Entrée** pour quitter

### 2. Ouvrir un nouveau terminal PowerShell, puis :

```powershell
ruby -v          # doit afficher ruby 3.x.x
gem install bundler
```

---

## Lancer en local

```powershell
# 1. Installer les dépendances (une seule fois)
bundle install

# 2. Démarrer le serveur de développement
bundle exec jekyll serve --livereload
```

Ouvrir **http://localhost:4000** dans le navigateur.  
Le site se recharge automatiquement à chaque modification de fichier.

### Options utiles

```powershell
# Forcer la reconstruction complète
bundle exec jekyll serve --livereload --force_polling

# Construire sans serveur (génère le dossier _site/)
bundle exec jekyll build
```

---

## Structure du projet

```
_config.yml          — configuration et métadonnées de l'événement
_layouts/            — templates HTML (default, page)
_includes/           — composants réutilisables (header, footer)
_sass/               — styles SCSS (variables, main)
assets/
  css/main.scss      — point d'entrée Jekyll pour le CSS
  js/main.js         — navigation mobile + countdown
  images/            — visuels (hero-bg.jpg, ...)
index.md             — page d'accueil
inscription.md       — tarifs et conditions d'inscription
parcours.md          — tracés et ravitaillement
programme.md         — déroulement de la journée
pratique.md          — accès, parking, vestiaires
resultats.md         — classements (post-course)
contact.md           — coordonnées et formulaire
mentions-legales.md
mockup/              — assets de référence (affiches, photos, logo)
```

---

## Déploiement sur GitHub Pages

### 1. Créer le dépôt GitHub

```powershell
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/VOTRE-USERNAME/VOTRE-REPO.git
git push -u origin main
```

### 2. Mettre à jour `_config.yml`

Remplacer les placeholders selon le type de dépôt :

| Type de dépôt | `url` | `baseurl` |
|---|---|---|
| `username.github.io` (site utilisateur) | `https://username.github.io` | `""` |
| `mon-repo` (site projet) | `https://username.github.io` | `"/mon-repo"` |

### 3. Activer GitHub Pages

Dans le dépôt GitHub : **Settings → Pages → Source → GitHub Actions**

Le workflow `.github/workflows/jekyll.yml` se déclenche automatiquement à chaque push sur `main` et publie le site.

### 4. Commiter le Gemfile.lock

```powershell
git add Gemfile.lock
git commit -m "Add Gemfile.lock for reproducible builds"
git push
```

### Commande locale avec config dev

```powershell
bundle exec jekyll serve --config _config.yml,_config_dev.yml --livereload
```

Le fichier `_config_dev.yml` surcharge l'URL pour le dev local (`localhost:4000`).

---

## Liens utiles

- Inscriptions : <https://chrono-start.fr/Inscription/Course/detail/c/5285>
- Devenir bénévole : <https://docs.google.com/spreadsheets/d/1bnma0w9Ll3AznCTbH063EpCOzyfpi2OBnfMh1i-A_tQ/edit>
