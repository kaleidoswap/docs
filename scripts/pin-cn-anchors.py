#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Pin explicit anchor ids on translated headings that links point at.

    python scripts/pin-cn-anchors.py            # dry run, reports what it would do
    python scripts/pin-cn-anchors.py --apply    # write the ids

Mintlify derives a heading's anchor from its text, so translating a heading
breaks every link aimed at it. Instead of rewriting each link fragment to a
guessed Chinese slug, this pins the original English slug onto the translated
heading using Mintlify's `{#custom-id}` syntax:

    ## 客户端配置 {#client-configuration}

The link then stays `](/cn/ai-tools/mcp-servers#client-configuration)` and keeps
resolving no matter how the heading text is later reworded.

Which heading to pin is decided by POSITION: the nth heading of the English page
corresponds to the nth heading of its translation. So translated pages must keep
headings in the same order and count as their source — which is what
scripts/check-cn-parity.py enforces.

Only headings that actually receive a link get an id.

See TRANSLATION-GUIDE.md.
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

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except AttributeError:
    pass

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.join(REPO, "mintlify-docs")
DOCS_JSON = os.path.join(ROOT, "docs.json")
LANG = "cn"
APPLY = "--apply" in sys.argv


def read(p):
    with io.open(p, encoding="utf-8") as f:
        return f.read()


def write(p, s):
    with io.open(p, "w", encoding="utf-8", newline="\n") as f:
        f.write(s)


def heading_lines(text):
    """Ordered [(line_index, level, title, pinned_id)] outside code fences."""
    out = []
    in_fence = False
    for i, line in enumerate(text.splitlines()):
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
        out.append((i, len(m.group(1)), title, pinned))
    return out


def safe_id(frag):
    """Normalise a fragment to characters whose handling is unambiguous.

    Mintlify preserves `&` when it generates a slug from heading text, but how it
    treats `&` inside an explicit {#id} is not documented. Since both the id and
    the link live in the translated tree, we sidestep the question: pin an id
    with no ambiguous characters and rewrite the links to match.
    """
    s = frag.replace("&", "and")
    s = re.sub(r"[^0-9a-z一-鿿-]+", "-", s)
    s = re.sub(r"-{2,}", "-", s)
    return s.strip("-")


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
    langs = {l["language"]: l for l in doc["navigation"]["languages"]}
    default = [k for k, v in langs.items() if v.get("default")] or ["en"]

    en_pages, cn_pages = [], []
    collect(langs[default[0]]["tabs"], en_pages)
    collect(langs[LANG]["tabs"], cn_pages)
    pair = dict(zip(cn_pages, en_pages))

    # ------------------------------------------ which fragments are asked for
    LINK = re.compile(r"\]\((/[^)\s]*#[^)\s]*)\)")
    needed = {}
    for cn_page in cn_pages:
        p = path_of(cn_page)
        if not os.path.exists(p):
            continue
        for target in LINK.findall(read(p)):
            path, _, frag = target.partition("#")
            path = path.rstrip("/")
            if path.startswith("/assets/") or path.startswith("/snippets/"):
                continue
            tgt = path[1:] if path else cn_page
            if tgt not in pair:
                print("WARN link to unknown page: %s (in %s)" % (target, cn_page))
                continue
            needed.setdefault(tgt, set()).add(unquote(frag))

    pinned = 0
    already = 0
    unresolved = []
    # target page -> [(original fragment, normalised id)] for links to follow
    rewrites = {}

    for cn_page, frags in sorted(needed.items()):
        cn_path, en_path = path_of(cn_page), path_of(pair[cn_page])
        if not (os.path.exists(cn_path) and os.path.exists(en_path)):
            unresolved.append((cn_page, sorted(frags), "file missing"))
            continue
        cn_text = read(cn_path)
        en_h = heading_lines(read(en_path))
        cn_h = heading_lines(cn_text)
        if len(en_h) != len(cn_h):
            unresolved.append(
                (cn_page, sorted(frags),
                 "heading count differs: en=%d cn=%d" % (len(en_h), len(cn_h)))
            )
            continue

        # index by raw slug and by normalised slug, so a fragment this script
        # already normalised on an earlier run still finds its heading
        en_slug_idx = {}
        for idx, (_, _, title, _) in enumerate(en_h):
            slug = slugify(title)
            en_slug_idx.setdefault(slug, idx)
            en_slug_idx.setdefault(safe_id(slug), idx)

        lines = cn_text.splitlines()
        changed = False
        for frag in sorted(frags):
            idx = en_slug_idx.get(frag)
            if idx is None:
                unresolved.append((cn_page, frag, "no english heading matches"))
                continue
            li, level, title, existing = cn_h[idx]
            wanted = safe_id(frag)
            if existing == wanted:
                already += 1
                if wanted != frag:
                    rewrites.setdefault(cn_page, []).append((frag, wanted))
                continue
            if existing and existing != frag:
                unresolved.append(
                    (cn_page, frag, "heading already pinned to #%s" % existing)
                )
                continue
            lines[li] = "%s %s {#%s}" % ("#" * level, title, wanted)
            cn_h[idx] = (li, level, title, wanted)
            changed = True
            pinned += 1
            note = "" if wanted == frag else "  (normalised from #%s)" % frag
            print("pin %-50s #%-40s %s%s" % (cn_page, wanted, title, note))
            if wanted != frag:
                rewrites.setdefault(cn_page, []).append((frag, wanted))
        if changed and APPLY:
            write(cn_path, "\n".join(lines) + ("\n" if cn_text.endswith("\n") else ""))

    # ------------------------- point links at the ids we actually pinned
    link_fixes = 0
    if rewrites:
        try:
            from urllib.parse import quote
        except ImportError:
            from urllib import quote
        for cn_page in cn_pages:
            p = path_of(cn_page)
            if not os.path.exists(p):
                continue
            text = original = read(p)
            for tgt, pairs in rewrites.items():
                for frag, wanted in pairs:
                    for encoded in {frag, quote(frag, safe="-")}:
                        for base in ("/" + tgt, ""):
                            old = "](%s#%s)" % (base, encoded)
                            if old in text:
                                text = text.replace(
                                    old, "](%s#%s)" % (base, wanted)
                                )
                                link_fixes += text.count("](%s#%s)" % (base, wanted))
            if text != original:
                print("link %s -> normalised fragment(s)" % cn_page)
                if APPLY:
                    write(p, text)

    print("\npinned: %d   already pinned: %d   links repointed: %d%s"
          % (pinned, already, link_fixes,
             "" if APPLY else "   (dry run — pass --apply)"))
    if unresolved:
        print("\nUNRESOLVED: %d" % len(unresolved))
        for u in unresolved:
            print("  ", u)
        return 1
    print("all anchor targets resolved")
    return 0


if __name__ == "__main__":
    sys.exit(main())
