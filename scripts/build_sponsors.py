#!/usr/bin/env python3
"""Régénère assets/images/sponsors/*.png à partir de assets/images/sponsors/src/.

Pour ajouter ou remplacer un sponsor : dépose un logo (JPEG/PNG/WEBP) ou un PDF
vectoriel dans src/, puis relance ce script. Chaque fichier de src/ produit une
image transparente et recadrée sur le logo dans le dossier parent (le fond uni
des photos/scans est détecté et supprimé, les PDF sont rendus directement en
transparent), et tout nouveau fichier reçoit une entrée de départ dans
_data/sponsors.yml (à compléter/corriger à la main : nom affiché, lien
éventuel).

Le nom de fichier de sortie est dérivé du nom du fichier source (slugifié),
toujours avec l'extension .png (nécessaire pour la transparence) : renomme le
fichier dans src/ si tu veux changer le nom de sortie.

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
import numpy as np
import yaml
from PIL import Image, ImageDraw, ImageFilter

ROOT = Path(__file__).resolve().parent.parent
SRC_DIR = ROOT / "assets/images/sponsors/src"
OUT_DIR = ROOT / "assets/images/sponsors"
DATA_FILE = ROOT / "_data/sponsors.yml"

RASTER_EXTS = {".jpg", ".jpeg", ".png", ".webp"}
MAX_DIM = 1600  # le slideshow affiche au plus ~640x280 ; large marge pour le retina

BG_THRESHOLD = 28  # tolérance de couleur pour repérer le fond uni (0-255)
CROP_PADDING = 16  # marge (px) conservée autour du logo après recadrage
FEATHER = 1  # léger flou des bords de transparence pour éviter les contours crénelés


def slugify(stem: str) -> str:
    stem = unicodedata.normalize("NFKD", stem).encode("ascii", "ignore").decode("ascii")
    stem = re.sub(r"[^a-zA-Z0-9]+", "-", stem).strip("-").lower()
    return stem or "sponsor"


def slug_to_name(slug: str) -> str:
    return " ".join(w.capitalize() for w in slug.split("-"))


def _has_transparency(im: Image.Image) -> bool:
    """Vrai si l'image a déjà un vrai fond transparent (pas juste de l'anti-aliasing)."""
    if im.mode != "RGBA":
        return False
    alpha = np.asarray(im.getchannel("A"))
    return (alpha <= 5).mean() > 0.005


def strip_background(im: Image.Image) -> Image.Image:
    """Rend transparent le fond uni d'un logo photographié/scanné.

    Part des 4 coins et propage (flood fill, avec tolérance de couleur) vers
    l'intérieur : seul le fond connecté aux bords est supprimé, ce qui évite
    de créer des trous si le logo contient des zones de couleur proche du fond.
    """
    rgb = im.convert("RGB")
    mask_src = rgb.copy()
    w, h = mask_src.size
    sentinel = (255, 0, 255)  # couleur improbable dans un logo
    for seed in {(0, 0), (w - 1, 0), (0, h - 1), (w - 1, h - 1)}:
        if mask_src.getpixel(seed) != sentinel:
            ImageDraw.floodfill(mask_src, seed, sentinel, thresh=BG_THRESHOLD)

    bg_mask = np.all(np.asarray(mask_src) == sentinel, axis=-1)
    alpha = Image.fromarray(np.where(bg_mask, 0, 255).astype("uint8"), mode="L")
    if FEATHER:
        alpha = alpha.filter(ImageFilter.GaussianBlur(FEATHER))

    out = rgb.convert("RGBA")
    out.putalpha(alpha)
    return out


def crop_to_content(im: Image.Image, padding: int = CROP_PADDING) -> Image.Image:
    """Recadre sur le rectangle englobant des pixels non transparents."""
    if im.mode != "RGBA":
        return im
    alpha = np.asarray(im.getchannel("A"))
    ys, xs = np.nonzero(alpha > 10)
    if xs.size == 0 or ys.size == 0:
        return im
    left, right = max(int(xs.min()) - padding, 0), min(int(xs.max()) + padding + 1, im.width)
    top, bottom = max(int(ys.min()) - padding, 0), min(int(ys.max()) + padding + 1, im.height)
    return im.crop((left, top, right, bottom))


def _prepare(im: Image.Image) -> Image.Image:
    """Fond transparent (si besoin) + recadrage sur le logo."""
    im = im if _has_transparency(im) else strip_background(im)
    return crop_to_content(im)


def render_pdf(src: Path, dest: Path) -> None:
    doc = fitz.open(src)
    page = doc[0]
    scale = min(4.0, MAX_DIM / max(page.rect.width, page.rect.height))
    scale = max(scale, 1.0)
    pix = page.get_pixmap(matrix=fitz.Matrix(scale, scale), alpha=True)
    im = Image.frombytes("RGBA", (pix.width, pix.height), pix.samples)
    im = _prepare(im)
    im.save(dest)


def resize_raster(src: Path, dest: Path) -> None:
    with Image.open(src) as im:
        im = _prepare(im)
        if max(im.size) > MAX_DIM:
            ratio = MAX_DIM / max(im.size)
            im = im.resize((round(im.width * ratio), round(im.height * ratio)), Image.LANCZOS)
        im.save(dest, optimize=True)


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

        if ext == ".pdf" or ext in RASTER_EXTS:
            dest = OUT_DIR / f"{slug}.png"  # toujours en PNG : le fond est rendu transparent
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

        # Nettoie les anciennes sorties du même sponsor (ex: alto.jpeg -> alto.png)
        for old_ext in RASTER_EXTS | {".png"}:
            stale = OUT_DIR / f"{slug}{old_ext}"
            if stale != dest and stale.exists():
                stale.unlink()

    sponsors = yaml.safe_load(DATA_FILE.read_text(encoding="utf-8")) or []
    known_by_slug = {
        Path(s["file"]).stem: s["file"] for s in sponsors if isinstance(s, dict) and "file" in s
    }
    known_files = set(known_by_slug.values())

    # Migre les entrées existantes dont seule l'extension a changé (ex: passage en PNG),
    # en éditant le texte brut pour préserver commentaires et mise en forme du YAML.
    renames = {
        old: new
        for new in generated_files
        if (old := known_by_slug.get(Path(new).stem)) and old != new
    }
    if renames:
        text = DATA_FILE.read_text(encoding="utf-8")
        for old_name, new_name in renames.items():
            text = re.sub(rf'(file:\s*"){re.escape(old_name)}(")', rf"\g<1>{new_name}\g<2>", text)
        DATA_FILE.write_text(text, encoding="utf-8")
        known_files = (known_files - renames.keys()) | set(renames.values())

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
    if renames:
        print(f"Renomme dans sponsors.yml : {renames}")
    if missing_from_yml:
        print(f"Ajoutes a sponsors.yml (a verifier) : {missing_from_yml}")
    if orphaned_in_yml:
        print(f"/!\\ Dans sponsors.yml mais sans image generee : {orphaned_in_yml}")


if __name__ == "__main__":
    main()
