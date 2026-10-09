#!/usr/bin/env python3 -I
"""Error-driven mechanical fixes for the 26.2 port. Reads build.log, edits sources in place.

Each rule matches one javac error message and edits at the caret column javac printed.
Hack: trusts the caret column is a char index into the printed source line (true for
space-indented files, wrong for tabs). Check `git diff` after running.

usage: tools/fix.py [rule ...]   (default: all)
"""
import re, sys, collections

LOG = "build.log"
edits = collections.defaultdict(list)  # path -> [(line, col, old, new)]


def errors():
    """yield (path, line, message, source_line, caret_col, detail_lines)"""
    log = open(LOG).read().split("\n")
    for i, l in enumerate(log):
        m = re.match(r"(/.*\.java):(\d+): error: (.*)", l)
        if not m: continue
        src = log[i + 1] if i + 1 < len(log) else ""
        caret = log[i + 2] if i + 2 < len(log) else ""
        col = caret.find("^")
        detail = log[i + 3:i + 8]
        yield m.group(1), int(m.group(2)), m.group(3), src, col, detail


def rule_chunkpos_xz(path, line, msg, src, col, detail):
    m = re.match(r"([xz]) has private access in ChunkPos", msg)
    if m and src[col:col + 1] == ".":
        name = m.group(1)
        if src[col + 1:col + 2] == name:
            edits[path].append((line, col + 2, "", "()"))  # insert () after the name


def rule_chunkpos_ctor(path, line, msg, src, col, detail):
    if msg.startswith("constructor ChunkPos in record ChunkPos"):
        found = " ".join(detail)
        if "found:    long" in found: new = "ChunkPos.unpack("
        elif "found:    BlockPos" in found: new = "ChunkPos.containing("
        else: return
        if src[col:col + 13] == "new ChunkPos(":
            edits[path].append((line, col, "new ChunkPos(", new))


def rule_chunkpos_names(path, line, msg, src, col, detail):
    if msg == "cannot find symbol":
        d = " ".join(detail)
        if "method asLong(int,int)" in d and src[col:].startswith("ChunkPos.asLong") or "method asLong(int,int)" in d:
            i = src.find("ChunkPos.asLong(")
            if i >= 0: edits[path].append((line, i, "ChunkPos.asLong(", "ChunkPos.pack("))
        if "method toLong()" in d and src[col:col + 7] == ".toLong":
            edits[path].append((line, col, ".toLong()", ".pack()"))


# (symbol "method NAME(...)" , needed substring in location lines or None, old text, new text)
RENAMES = [
    ("location()", None, ".location()", ".identifier()"),
    ("registryOrThrow(", None, ".registryOrThrow(", ".lookupOrThrow("),
    ("serverLevel()", None, ".serverLevel()", ".level()"),
    ("getSharedSpawnPos()", None, ".getSharedSpawnPos()", ".getRespawnData().globalPos().pos()"),
    ("getName()", "GameProfile", ".getName()", ".name()"),
    ("getId()", "GameProfile", ".getId()", ".id()"),
]


def rule_renames(path, line, msg, src, col, detail):
    if msg != "cannot find symbol": return
    d = " ".join(detail)
    for sym, loc, old, new in RENAMES:
        if f"symbol:   method {sym}" in d.replace("  ", " ").replace("symbol: method", "symbol:   method") or f"method {sym}" in d:
            if loc and loc not in d: continue
            i = src.find(old, max(col - 1, 0))
            if i >= 0:
                edits[path].append((line, i, old, new)); return


RULES = {"xz": rule_chunkpos_xz, "ctor": rule_chunkpos_ctor, "names": rule_chunkpos_names, "renames": rule_renames}
want = sys.argv[1:] or list(RULES)
for e in errors():
    for name in want:
        RULES[name](*e)

n = 0
for path, es in edits.items():
    lines = open(path).read().split("\n")
    # apply right-to-left within a line so columns stay valid; dedupe
    for line, col, old, new in sorted(set(es), key=lambda t: (t[0], -t[1])):
        s = lines[line - 1]
        if old and s[col:col + len(old)] != old:
            print(f"skip {path}:{line}:{col} expected {old!r} got {s[col:col+len(old)]!r}"); continue
        lines[line - 1] = s[:col] + new + s[col + len(old):]
        n += 1
    open(path, "w").write("\n".join(lines))
print(f"applied {n} edits in {len(edits)} files")
