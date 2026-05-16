from __future__ import annotations

from pathlib import Path

ROOT = Path('quartz')
CONTENT = ROOT / 'content'

PAGE_TITLE = 'Th3rD — Write-ups CTF'
BASE_URL = 'Th3rdMan.github.io/write-ups-ctf'

LABELS = {
    'Bleuet 2026': 'Bleuet 2026',
    'bleuet-2026': 'Bleuet 2026',
    '01-prologue': '01 - Prologue',
    '02-dans-la-peau-dun-resistant': '02 - Dans la peau d’un résistant',
    '03-un-devoir-de-memoire': '03 - Un devoir de mémoire',
    '04-lart-de-resister': '04 - L’art de résister',
    '05-laudace-de-resister': '05 - L’audace de résister',
    '06-nos-partenaires': '06 - Nos partenaires',
    'bienvenue': '01 - Bienvenue',
    '01-alpha-ici-bravo': '01 - Alpha ici Bravo',
    '02-decryptage-en-pique': '02 - Décryptage en piqué',
    '03-lettre-dun-soldat': '03 - Lettre d’un soldat',
    '04-plastique-et-crayons': '04 - Plastique et crayons',
    '05-interception-de-code': '05 - Interception de code',
    '06-motif-aleatoire': '06 - Motif aléatoire',
    '07-le-repere': '07 - Le repère',
    '01-plus-quun-numero': '01 - Plus qu’un numéro',
    '02-lequipage': '02 - L’équipage',
    '03-la-charente-liberee': '03 - La Charente libérée',
    '04-les-fusilles-du-mont-valerien': '04 - Les fusillés du Mont-Valérien',
    '05-la-princesse': '05 - La princesse',
    '01-resistant-dans-lart': '01 - Résistant dans l’art',
    '02-une-oreille-pour-se-souvenir': '02 - Une oreille pour se souvenir',
    '03-des-mots-pour-contrer-les-maux': '03 - Des mots pour contrer les maux',
    '04-un-vers-pour-la-liberte': '04 - Un vers pour la liberté',
    '05-lart-et-la-resistance': '05 - L’art et la résistance',
    '01-alias-et-acide': '01 - Alias et acide',
    '02-le-glacier-tenace': '02 - Le glacier tenace',
    '03-le-tract-dissident': '03 - Le tract dissident',
    '01-la-force-du-collectif': '01 - La force du collectif',
    '02-le-refuge-des-dechiffreurs': '02 - Le refuge des déchiffreurs',
    '03-lingenieur-de-lombre': '03 - L’ingénieur de l’ombre',
    '04-leclosion-du-souvenir': '04 - L’éclosion du souvenir',
    '05-medevac-needed': '05 - MEDEVAC NEEDED',
    'index-osint': 'Index OSINT',
}

EXACT_TITLES = {
    'index.md': 'Th3rD — Write-ups CTF',
    'Index OSINT.md': 'Index OSINT',
    'Bleuet 2026/index.md': 'Bleuet de France V5 — 2026',
    'Bleuet 2026/01-prologue/index.md': '01 - Prologue',
    'Bleuet 2026/02-dans-la-peau-dun-resistant/index.md': '02 - Dans la peau d’un résistant',
    'Bleuet 2026/03-un-devoir-de-memoire/index.md': '03 - Un devoir de mémoire',
    'Bleuet 2026/04-lart-de-resister/index.md': '04 - L’art de résister',
    'Bleuet 2026/05-laudace-de-resister/index.md': '05 - L’audace de résister',
    'Bleuet 2026/06-nos-partenaires/index.md': '06 - Nos partenaires',
}


def configure_quartz() -> None:
    cfg = ROOT / 'quartz.config.ts'
    text = cfg.read_text(encoding='utf-8')
    text = text.replace('pageTitle: "Quartz 4"', f'pageTitle: "{PAGE_TITLE}"')
    text = text.replace('locale: "en-US"', 'locale: "fr-FR"')
    text = text.replace('baseUrl: "quartz.jzhao.xyz"', f'baseUrl: "{BASE_URL}"')
    cfg.write_text(text, encoding='utf-8')


def first_h1_title(text: str) -> tuple[str | None, str]:
    lines = text.splitlines()
    for i, line in enumerate(lines):
        if line.startswith('# '):
            title = line[2:].strip()
            new_lines = lines[:i] + lines[i + 1:]
            while new_lines and new_lines[0].strip() == '':
                new_lines.pop(0)
            return title, '\n'.join(new_lines).lstrip() + ('\n' if text.endswith('\n') else '')
    return None, text


def title_for(path: Path, text: str) -> tuple[str, str]:
    rel = path.relative_to(CONTENT).as_posix()
    if rel in EXACT_TITLES:
        return EXACT_TITLES[rel], text

    stem = path.stem
    label = LABELS.get(stem)
    if label:
        return label, text

    h1, stripped = first_h1_title(text)
    if h1:
        return h1, stripped

    return stem, text


def set_frontmatter(text: str, title: str) -> str:
    if text.startswith('---\n'):
        end = text.find('\n---\n', 4)
        if end != -1:
            fm = [line for line in text[4:end].splitlines() if not line.startswith('title:')]
            body = text[end + 5:].lstrip()
            front = '\n'.join([f'title: "{title}"', *fm]).strip()
            return f'---\n{front}\n---\n\n{body}'
    return f'---\ntitle: "{title}"\n---\n\n{text.lstrip()}'


def prepare_markdown() -> None:
    for md in CONTENT.rglob('*.md'):
        text = md.read_text(encoding='utf-8')
        title, body = title_for(md, text)
        # Avoid duplicate headings on the Quartz page: ArticleTitle displays the title already.
        if md.name != 'index.md':
            _, body = first_h1_title(body)
        md.write_text(set_frontmatter(body, title), encoding='utf-8')


def patch_layout() -> None:
    layout = ROOT / 'quartz.layout.ts'
    text = layout.read_text(encoding='utf-8')
    entries = ',\n'.join(f'          "{key}": "{value}"' for key, value in LABELS.items())
    explorer = f'''Component.Explorer({{
      title: "Explorateur",
      useSavedState: false,
      mapFn: (node) => {{
        const labels = {{
{entries}
        }}
        const label = labels[node.slugSegment] ?? labels[node.displayName]
        if (label) node.displayName = label
      }},
    }})'''
    text = text.replace('Component.Explorer(),', explorer + ',')
    layout.write_text(text, encoding='utf-8')


def main() -> None:
    configure_quartz()
    prepare_markdown()
    patch_layout()


if __name__ == '__main__':
    main()
