#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Check the Simplified Chinese docs tree against the English sources.

Run from anywhere in the repo:

    python scripts/check-cn-parity.py

Verifies, for the `cn` language declared in mintlify-docs/docs.json:

  1. Coverage      — every page in the cn navigation exists on disk.
  2. Parity        — each page matches its English source on heading count,
                     code fences, MDX components, table rows and images.
  3. Links         — every internal link is /cn-prefixed and resolves to a page
                     that is actually in the cn navigation.
  4. Anchors       — every link fragment resolves to a heading id in the target
                     page, whether pinned with {#id} or generated from the text.
  5. Frontmatter   — title and description present, and title actually translated.

Exits non-zero if anything is wrong, so it can gate a PR.

See TRANSLATION-GUIDE.md for the rules this enforces.
"""
from __future__ import print_function

import io
import json
import os
import re
import sys

try:
    from urllib.parse import unquote
except ImportError:  # py2
    from urllib import unquote

# the Windows console defaults to cp1252 and dies on CJK output
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except AttributeError:
    pass

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.join(REPO, "mintlify-docs")
DOCS_JSON = os.path.join(ROOT, "docs.json")
LANG = "cn"

CJK = "[一-鿿]"

# titles that are nothing but product names / acronyms correctly stay English
PROPER_ONLY = re.compile(
    r"^(?:Kaleido\w*|KaleidoSwap|Nostr|Wallet|Connect|SDK|CLI|API|NWC|RGB|MCP|"
    r"LSPS1|RLN|Bitcoin|Lightning|FAQ|WebSocket|REST|Taproot|Assets|"
    r"[-–&/()0-9.]+)(?:\s+|$)"
)


def read(p):
    with io.open(p, encoding="utf-8") as f:
        return f.read()


def strip_code(text):
    return re.sub(r"```.*?```", "", text, flags=re.S)


def headings(text):
    """Ordered [(level, title, pinned_id)] outside code fences."""
    out = []
    in_fence = False
    for line in text.splitlines():
        if re.match(r"^\s*```", line):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        m = re.match(r"^(#{1,6})\s+(.*?)\s*$", line)
        if not m:
            continue
        title = m.group(2)
        idm = re.search(r"\s*\{#([^}]*)\}\s*$", title)
        pinned = idm.group(1) if idm else None
        if idm:
            title = title[: idm.start()].rstrip()
        out.append((len(m.group(1)), title, pinned))
    return out


def slugify(title):
    """Mintlify's heading -> anchor rules, validated against the English docs."""
    s = title.strip().lower()
    s = s.replace("`", "").replace("*", "").replace("_", " ")
    s = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", s)
    s = re.sub(r"[:().,?!'\"|<>{}\[\]+=;$#@~^]", "", s)
    s = s.replace(".", "-")
    s = re.sub(r"\s+", "-", s.strip())
    s = re.sub(r"-{2,}", "-", s)
    return s.strip("-")


def counts(text):
    body = strip_code(text)
    return {
        "headings": len(headings(text)),
        "fences": text.count("```"),
        "images": len(re.findall(r"!\[[^\]]*\]\(", body)),
        "table_rows": len([l for l in body.splitlines() if l.strip().startswith("|")]),
        "components": len(re.findall(r"<([A-Z][A-Za-z]*)", body)),
    }


def collect(node, acc):
    if isinstance(node, list):
        for n in node:
            collect(n, acc)
    elif isinstance(node, str):
        acc.append(node)
    elif isinstance(node, dict):
        for k in ("tabs", "groups", "pages"):
            if k in node:
                collect(node[k], acc)


def path_of(page):
    return os.path.join(ROOT, page.replace("/", os.sep) + ".mdx")


def main():
    doc = json.loads(read(DOCS_JSON))
    try:
        langs = {l["language"]: l for l in doc["navigation"]["languages"]}
    except KeyError:
        print("docs.json has no navigation.languages — nothing to check")
        return 0
    if LANG not in langs:
        print("docs.json declares no '%s' language — nothing to check" % LANG)
        return 0

    default = [k for k, v in langs.items() if v.get("default")] or ["en"]
    en_pages, cn_pages = [], []
    collect(langs[default[0]]["tabs"], en_pages)
    collect(langs[LANG]["tabs"], cn_pages)

    errors, missing, parity, fm_issues, bad_links, anchors, thin = [], [], [], [], [], [], []

    if len(en_pages) != len(cn_pages):
        errors.append(
            "navigation page count differs: %s=%d %s=%d"
            % (default[0], len(en_pages), LANG, len(cn_pages))
        )

    cn_set = set(cn_pages)
    pair = dict(zip(cn_pages, en_pages))

    # ---------------------------------------------------- coverage and parity
    for cn_page, en_page in zip(cn_pages, en_pages):
        cn_path, en_path = path_of(cn_page), path_of(en_page)
        if not os.path.exists(cn_path):
            missing.append(cn_page)
            continue
        if not os.path.exists(en_path):
            errors.append("english source missing for %s" % en_page)
            continue
        ec, cc = counts(read(en_path)), counts(read(cn_path))
        diffs = {k: (ec[k], cc[k]) for k in ec if ec[k] != cc[k]}
        if diffs:
            parity.append((cn_page, diffs))

    # -------------------------------------------------------- heading id index
    ids = {}
    for cn_page in cn_pages:
        p = path_of(cn_page)
        if not os.path.exists(p):
            continue
        s = set()
        for _, title, pinned in headings(read(p)):
            s.add(pinned if pinned else slugify(title))
        ids[cn_page] = s

    # ---------------------------------------------------- links and frontmatter
    LINK = re.compile(r"\]\((/[^)\s]*)\)")
    for cn_page in cn_pages:
        p = path_of(cn_page)
        if not os.path.exists(p):
            continue
        text = read(p)

        for target in sorted(set(LINK.findall(text))):
            path, _, frag = target.partition("#")
            path = path.rstrip("/")
            if path.startswith("/assets/") or path.startswith("/snippets/"):
                continue
            if path and not path.startswith("/%s/" % LANG):
                bad_links.append((cn_page, target, "not /%s-prefixed" % LANG))
                continue
            page = path[1:] if path else cn_page
            if page and page not in cn_set:
                bad_links.append((cn_page, target, "target not in %s navigation" % LANG))
                continue
            if not frag:
                continue
            tgt = page or cn_page
            if unquote(frag) not in ids.get(tgt, set()):
                anchors.append((cn_page, target, "fragment not a heading id in target"))

        if not text.startswith("---"):
            fm_issues.append((cn_page, "no frontmatter"))
        else:
            fm = text[3 : text.find("\n---", 3)]
            if "title:" not in fm:
                fm_issues.append((cn_page, "no title"))
            if "description:" not in fm:
                fm_issues.append((cn_page, "no description"))
            m = re.search(r'^title:\s*[\'"]?(.*?)[\'"]?\s*$', fm, re.M)
            if m and not re.search(CJK, m.group(1)):
                # parenthesised acronyms are part of the proper name
                rest = m.group(1).replace("(", " ").replace(")", " ").strip()
                while rest:
                    mm = PROPER_ONLY.match(rest)
                    if not mm:
                        break
                    rest = rest[mm.end():].strip()
                if rest:
                    fm_issues.append(
                        (cn_page, "title looks untranslated: %s" % m.group(1))
                    )

        if len(re.findall(CJK, strip_code(text))) < 20:
            thin.append(cn_page)

    # ------------------------------------------------------------------ report
    def section(name, items, limit=40):
        print("\n== %s: %d ==" % (name, len(items)))
        for it in items[:limit]:
            print("  ", it)
        if len(items) > limit:
            print("   ... and %d more" % (len(items) - limit))

    print("pages in %s navigation: %d" % (LANG, len(cn_pages)))
    section("hard errors", errors)
    section("missing files", missing)
    section("structural parity issues", parity)
    section("frontmatter issues", fm_issues)
    section("bad links", bad_links)
    section("unresolved anchors", anchors)
    section("suspiciously untranslated", thin)

    fatal = errors or missing or parity or bad_links or anchors
    print("\nRESULT: %s" % ("PROBLEMS FOUND" if fatal else "OK"))
    return 1 if fatal else 0


if __name__ == "__main__":
    sys.exit(main())
