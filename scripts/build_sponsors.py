#!/usr/bin/env python3
"""Régénère assets/images/sponsors/*.{png,jpg,...} à partir de assets/images/sponsors/src/.

Pour ajouter ou remplacer un sponsor : dépose un logo (JPEG/PNG/WEBP) ou un PDF
vectoriel dans src/, puis relance ce script. Chaque fichier de src/ produit une
image web dans le dossier parent (les PDF sont rendus en PNG transparent), et
tout nouveau fichier reçoit une entrée de départ dans _data/sponsors.yml (à
compléter/corriger à la main : nom affiché, lien éventuel).

Le nom de fichier de sortie est dérivé du nom du fichier source (slugifié) :
renomme le fichier dans src/ si tu veux changer le nom de sortie.

Usage :
    pip install -r scripts/requirements.txt
    python scripts/build_sponsors.py [--force]

--force régénère même les fichiers déjà à jour (utile après un changement
de MAX_DIM ou de la logique de rendu).
"""
import argparse
import re
import sys
import unicodedata
from pathlib import Path

import fitz  # PyMuPDF
import yaml
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
SRC_DIR = ROOT / "assets/images/sponsors/src"
OUT_DIR = ROOT / "assets/images/sponsors"
DATA_FILE = ROOT / "_data/sponsors.yml"

RASTER_EXTS = {".jpg", ".jpeg", ".png", ".webp"}
MAX_DIM = 1600  # le slideshow affiche au plus ~640x280 ; large marge pour le retina


def slugify(stem: str) -> str:
    stem = unicodedata.normalize("NFKD", stem).encode("ascii", "ignore").decode("ascii")
    stem = re.sub(r"[^a-zA-Z0-9]+", "-", stem).strip("-").lower()
    return stem or "sponsor"


def slug_to_name(slug: str) -> str:
    return " ".join(w.capitalize() for w in slug.split("-"))


def render_pdf(src: Path, dest: Path) -> None:
    doc = fitz.open(src)
    page = doc[0]
    scale = min(4.0, MAX_DIM / max(page.rect.width, page.rect.height))
    scale = max(scale, 1.0)
    pix = page.get_pixmap(matrix=fitz.Matrix(scale, scale), alpha=True)
    pix.save(dest)


def resize_raster(src: Path, dest: Path) -> None:
    with Image.open(src) as im:
        if max(im.size) > MAX_DIM:
            ratio = MAX_DIM / max(im.size)
            im = im.resize((round(im.width * ratio), round(im.height * ratio)), Image.LANCZOS)
        save_kwargs = {"optimize": True}
        if dest.suffix.lower() in (".jpg", ".jpeg"):
            im = im.convert("RGB")
            save_kwargs["quality"] = 88
        im.save(dest, **save_kwargs)


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--force", action="store_true", help="régénère même les fichiers déjà à jour")
    args = parser.parse_args()

    if not SRC_DIR.is_dir():
        sys.exit(f"Introuvable : {SRC_DIR}")

    OUT_DIR.mkdir(parents=True, exist_ok=True)

    generated_files = set()
    created, updated, skipped = [], [], []

    for src in sorted(SRC_DIR.iterdir()):
        if not src.is_file() or src.name.startswith("."):
            continue
        ext = src.suffix.lower()
        slug = slugify(src.stem)

        if ext == ".pdf":
            dest = OUT_DIR / f"{slug}.png"
        elif ext in RASTER_EXTS:
            dest = OUT_DIR / f"{slug}{ext}"
        else:
            print(f"Ignore (extension non supportee) : {src.name}")
            continue

        generated_files.add(dest.name)

        if dest.exists() and not args.force and dest.stat().st_mtime >= src.stat().st_mtime:
            skipped.append(dest.name)
            continue

        is_new = not dest.exists()
        if ext == ".pdf":
            render_pdf(src, dest)
        else:
            resize_raster(src, dest)

        (created if is_new else updated).append(dest.name)

    sponsors = yaml.safe_load(DATA_FILE.read_text(encoding="utf-8")) or []
    known_files = {s["file"] for s in sponsors if isinstance(s, dict) and "file" in s}

    missing_from_yml = sorted(generated_files - known_files)
    orphaned_in_yml = sorted(known_files - generated_files)

    if missing_from_yml:
        with DATA_FILE.open("a", encoding="utf-8") as f:
            for filename in missing_from_yml:
                guess = slug_to_name(Path(filename).stem)
                f.write(f'- name: "{guess}"  # TODO: vérifier le nom\n  file: "{filename}"\n')

    print(f"Generes      : {created or '-'}")
    print(f"Mis a jour   : {updated or '-'}")
    print(f"Deja a jour  : {skipped or '-'}")
    if missing_from_yml:
        print(f"Ajoutes a sponsors.yml (a verifier) : {missing_from_yml}")
    if orphaned_in_yml:
        print(f"/!\\ Dans sponsors.yml mais sans image generee : {orphaned_in_yml}")


if __name__ == "__main__":
    main()
