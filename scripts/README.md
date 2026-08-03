# scripts/

## build_sponsors.py

Régénère les images des sponsors (`assets/images/sponsors/*.jpeg|png`) à
partir des fichiers sources déposés dans `assets/images/sponsors/src/`.

### Installation

```bash
pip install -r scripts/requirements.txt
```

### Usage

```bash
python scripts/build_sponsors.py           # génère/actualise ce qui a changé
python scripts/build_sponsors.py --force   # régénère tout, même ce qui est déjà à jour
```

### Ajouter ou remplacer un sponsor

1. Dépose le logo dans `assets/images/sponsors/src/` :
   - image raster (`.jpg`, `.jpeg`, `.png`, `.webp`), ou
   - PDF vectoriel (`.pdf`) — la première page est rendue en PNG transparent.
2. Relance `python scripts/build_sponsors.py`.
3. Si c'est un nouveau sponsor, une entrée de départ est ajoutée en fin de
   `_data/sponsors.yml` avec un nom deviné à partir du nom de fichier
   (commentaire `# TODO: vérifier le nom`) — corrige le nom affiché et ajoute
   un `url` si besoin.
4. Rebuild/serve le site Jekyll pour voir le résultat sur la page d'accueil.

Pour remplacer un logo existant, écrase simplement le fichier correspondant
dans `src/` (même nom) et relance le script.

### Nom du fichier de sortie

Le fichier généré dans `assets/images/sponsors/` reprend le nom du fichier
source, slugifié (minuscules, accents retirés, espaces → tirets). Exemple :
`Crédit Agricole.jpeg` → `credit-agricole.jpeg`.

Renomme le fichier dans `src/` si tu veux changer le nom de sortie — le
script ne fait jamais le lien autrement qu'par ce nom.

### Ce que fait le script, en détail

- **PDF** → rendu de la page 1 en PNG avec canal alpha (transparence
  préservée), mis à l'échelle pour que le plus grand côté fasse ~1600px.
- **Image raster** → redimensionnée si elle dépasse 1600px de long côté,
  réencodée (JPEG en qualité 88, PNG optimisé).
- **Idempotent** : un fichier déjà généré et à jour (comparaison des dates de
  modification source/sortie) est ignoré, sauf avec `--force`.
- **`_data/sponsors.yml`** : uniquement complété en fin de fichier pour les
  nouveaux fichiers détectés — jamais réécrit ni modifié sur les entrées
  existantes. Une entrée de `sponsors.yml` qui ne correspond plus à aucune
  image générée déclenche un avertissement (mais rien n'est supprimé).

### Pourquoi 1600px ?

Le slideshow de la page d'accueil affiche chaque logo dans une vignette de
640×280px max. 1600px de long côté laisse une marge confortable pour les
écrans retina/HiDPI sans gonfler inutilement le poids des images.
