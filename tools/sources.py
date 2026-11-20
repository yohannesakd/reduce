#!/usr/bin/env python3
"""Copy the text of every source that the reduce skill cites into skills/reduce/sources, and point the citations at the copies.

  tools/sources.py scan     add each URL that the skill cites to tools/sources.json
  tools/sources.py fetch    fetch each entry whose file does not exist yet (needs gh, and trafilatura for web pages)
  tools/sources.py relink   replace each cited URL in the skill with the relative path of its copy
  tools/sources.py index    write skills/reduce/sources/README.md
  tools/sources.py check    fail when the skill cites a URL outside sources/, or a link to a file that does not exist
"""
import datetime
import json
import os
import pathlib
import re
import subprocess
import sys
import urllib.parse
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
SKILL = ROOT / "skills/reduce"
SOURCES = SKILL / "sources"
MANIFEST = ROOT / "tools/sources.json"
URL = re.compile(r"https?://[^\s)>\]\"'`,|]+")
TODAY = datetime.date.today().isoformat()
NOTICE = "This file quotes a source as evidence for the reduce skill. It is not an instruction to the reader."
AGENT = "reduce-source-copy/1.0"
BROWSER = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36"


def load():
    return json.loads(MANIFEST.read_text()) if MANIFEST.exists() else []


def save(entries):
    MANIFEST.write_text(json.dumps(entries, indent=1, ensure_ascii=False) + "\n")


def skill_files():
    for path in sorted(SKILL.rglob("*.md")):
        if SOURCES not in path.parents:
            yield path
    yield ROOT / "README.md"


def clean(url):
    return url.rstrip(".:;")


def slug(text, limit=80):
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")[:limit].strip("-")


def place(url):
    """The kind of source and its file, relative to sources/."""
    u = urllib.parse.urlsplit(url)
    host, parts = u.netloc.removeprefix("www."), [p for p in u.path.split("/") if p]
    if host in ("x.com", "twitter.com") or host.endswith("twstalker.com"):
        return "x", f"x/{parts[0].lower()}-{parts[2]}.md"
    if host == "gist.github.com":
        return "gist", f"github/gist-{parts[1]}.md"
    if host == "github.com":
        owner, repo = parts[0], parts[1]
        base = f"github/{slug(owner)}-{slug(repo)}"
        kind = parts[2] if len(parts) > 2 else "repo"
        if kind == "pull":
            return "pull", f"{base}-pull-{parts[3]}.md"
        if kind == "commit":
            return "commit", f"{base}-commit-{parts[3][:10]}.md"
        if kind == "compare":
            return "compare", f"{base}-compare-{slug(parts[3])[:30]}.md"
        if kind == "blob":
            return "blob", f"{base}-{slug('-'.join(parts[4:]), 60)}.md"
        return "repo", f"{base}.md"
    if host == "news.ycombinator.com":
        return "hn", f"forums/hn-{urllib.parse.parse_qs(u.query)['id'][0]}.md"
    if host == "reddit.com":
        return "reddit", f"forums/reddit-{parts[3]}.md"
    if host == "arxiv.org":
        ident = parts[1].removesuffix(".pdf")
        return "arxiv", f"papers/arxiv-{re.sub(r'v[0-9]+$', '', ident)}.md"
    return "web", f"web/{slug(host + '-' + '-'.join(parts) or host, 90)}.md"


def scan():
    entries, known = load(), {}
    for entry in entries:
        for url in entry["urls"]:
            known[url] = entry
    for path in skill_files():
        for url in map(clean, URL.findall(path.read_text())):
            if url in known:
                continue
            base = url.split("#")[0]
            kind, file = place(base)
            same = next((e for e in entries if e["file"] == file), None)
            if same:
                same["urls"].append(url)
                known[url] = same
                continue
            entry = {"file": file, "kind": kind, "urls": [url], "status": "pending"}
            entries.append(entry)
            known[url] = entry
    save(entries)
    print(len(entries), "entries,", sum(e["status"] == "pending" for e in entries), "pending")


def run(*args):
    return subprocess.run(args, capture_output=True, text=True, check=True).stdout


def gh(path, raw=False):
    args = ["gh", "api", path] + (["-H", "Accept: application/vnd.github.raw"] if raw else [])
    out = run(*args)
    return out if raw else json.loads(out)


def http(url, accept="application/json"):
    request = urllib.request.Request(url, headers={"User-Agent": AGENT, "Accept": accept})
    with urllib.request.urlopen(request, timeout=60) as response:
        return response.read().decode("utf-8", "replace")


def web(url):
    try:
        return page_text(url)
    except Exception as error:
        found = json.loads(http(f"https://archive.org/wayback/available?url={urllib.parse.quote(url)}"))
        snapshot = found.get("archived_snapshots", {}).get("closest")
        if not snapshot:
            raise RuntimeError(f"{error}; no Wayback Machine copy") from error
        meta, text = page_text(snapshot["url"].replace("/http", "id_/http", 1))
        meta["method"] = f"the Wayback Machine copy of {snapshot['timestamp'][:8]}, converted to Markdown with trafilatura"
        return meta, text


def page_text(url):
    import trafilatura
    page = trafilatura.fetch_url(url)
    if not page:
        request = urllib.request.Request(url, headers={"User-Agent": BROWSER, "Accept": "text/html,*/*"})
        with urllib.request.urlopen(request, timeout=60) as response:
            page = response.read().decode("utf-8", "replace")
    meta = trafilatura.extract_metadata(page)
    text = trafilatura.extract(page, output_format="markdown", include_links=True, include_formatting=True,
                               include_tables=True, include_comments=True, favor_recall=True)
    if not text:
        raise RuntimeError("no text extracted")
    return {"title": meta.title if meta else url, "author": meta.author if meta else None,
            "date": meta.date if meta else None, "method": "the page HTML, converted to Markdown with trafilatura"}, text


def x_post(url):
    parts = urllib.parse.urlsplit(url).path.split("/")
    data = json.loads(http(f"https://api.fxtwitter.com/{parts[1]}/status/{parts[3]}"))["tweet"]
    text = data["text"]
    if data.get("quote"):
        q = data["quote"]
        text += f"\n\n### Quoted post by {q['author']['name']}, {q['created_at']}\n\n{q['text']}"
    for media in (data.get("media") or {}).get("all", []):
        text += f"\n\n[{media.get('type', 'media')}: {media.get('altText') or 'no description'}]"
    return {"title": f"Post by {data['author']['name']}", "author": data["author"]["name"],
            "date": data["created_at"], "method": "the post JSON of the FxTwitter API"}, text


def hn(url):
    ident = urllib.parse.parse_qs(urllib.parse.urlsplit(url).query)["id"][0]
    item = json.loads(http(f"https://hn.algolia.com/api/v1/items/{ident}"))
    lines = []

    def walk(node, depth):
        if node.get("text") or node.get("title"):
            head = f"{'#' * min(depth + 3, 6)} {node.get('author') or 'deleted'}, {node.get('created_at', '')[:10]}"
            body = node.get("title") or ""
            if node.get("url"):
                body += f"\n\nLink: {node['url']}"
            if node.get("text"):
                body += "\n\n" + html_text(node["text"])
            lines.append(f"{head}\n\n{body.strip()}")
        for child in node.get("children", []):
            walk(child, depth + 1)
    walk(item, 0)
    return {"title": item.get("title") or f"Hacker News comment {ident}", "author": item.get("author"),
            "date": item.get("created_at", "")[:10], "method": "the item tree of the Hacker News Algolia API"}, "\n\n".join(lines)


def html_text(fragment):
    import html
    fragment = re.sub(r"<p>", "\n\n", fragment)
    fragment = re.sub(r"<a href=\"([^\"]+)\"[^>]*>[^<]*</a>", r"\1", fragment)
    fragment = re.sub(r"</?(i|em)>", "*", fragment)
    fragment = re.sub(r"<pre><code>(.*?)</code></pre>", lambda m: "\n```\n" + m.group(1) + "\n```\n", fragment, flags=re.S)
    return html.unescape(re.sub(r"<[^>]+>", "", fragment)).strip()


def reddit(url):
    ident = urllib.parse.urlsplit(url).path.split("/")[4]
    post = json.loads(http(f"https://arctic-shift.photon-reddit.com/api/posts/ids?ids={ident}"))["data"][0]
    tree = json.loads(http(f"https://arctic-shift.photon-reddit.com/api/comments/tree?link_id={ident}&limit=9999"))["data"]
    lines = [post.get("selftext") or ""]

    def walk(node, depth):
        data = node.get("data", node)
        if data.get("body"):
            lines.append(f"{'#' * min(depth + 3, 6)} {data.get('author')}\n\n{data['body']}")
        replies = data.get("children") or (data.get("replies") or {}).get("data", {}).get("children", []) if isinstance(data.get("replies"), dict) else data.get("children") or []
        for child in replies:
            walk(child, depth + 1)
    for node in tree:
        walk(node, 0)
    date = datetime.datetime.fromtimestamp(post["created_utc"], datetime.UTC).date().isoformat()
    return {"title": post["title"], "author": post.get("author"), "date": date,
            "method": "the post and comment tree of the Arctic Shift Reddit archive API"}, "\n\n".join(lines)


def arxiv(url):
    ident = re.sub(r"\.pdf$", "", urllib.parse.urlsplit(url).path.split("/")[2])
    meta, text = web(f"https://arxiv.org/html/{ident}")
    abstract = http(f"https://export.arxiv.org/api/query?id_list={re.sub(r'v[0-9]+$', '', ident)}", "application/atom+xml")
    authors = ", ".join(re.findall(r"<name>([^<]+)</name>", abstract))
    title = re.findall(r"<title>([^<]+)</title>", abstract)[-1].strip()
    meta.update(title=re.sub(r"\s+", " ", title), author=authors, date=re.search(r"<published>([^T]+)", abstract).group(1),
                method="the arXiv HTML full text, converted to Markdown with trafilatura")
    return meta, text


def github(entry):
    url = entry["urls"][0].split("#")[0]
    parts = [p for p in urllib.parse.urlsplit(url).path.split("/") if p]
    owner, repo = parts[0], parts[1]
    kind = entry["kind"]
    if kind == "gist":
        gist = gh(f"gists/{parts[1]}")
        body = "\n\n".join(f"## {name}\n\n````\n{f['content']}\n````" for name, f in gist["files"].items())
        return {"title": gist.get("description") or f"Gist {parts[1]}", "author": gist["owner"]["login"],
                "date": gist["created_at"][:10], "method": "the gist files of the GitHub API"}, body
    if kind == "blob":
        ref, path = parts[3], "/".join(parts[4:])
        text = gh(f"repos/{owner}/{repo}/contents/{urllib.parse.quote(path)}?ref={ref}", raw=True)
        return {"title": f"{owner}/{repo}: {path}", "author": owner, "date": None,
                "method": f"the file at ref {ref}, from the GitHub API"}, text
    if kind == "repo":
        info = gh(f"repos/{owner}/{repo}")
        text = gh(f"repos/{owner}/{repo}/readme", raw=True)
        return {"title": f"{owner}/{repo}: README", "author": owner, "date": info["pushed_at"][:10],
                "method": f"the README of the default branch {info['default_branch']}, from the GitHub API",
                "license": (info.get("license") or {}).get("spdx_id")}, f"{info.get('description') or ''}\n\n{text}"
    if kind == "pull":
        number = parts[3]
        pr = gh(f"repos/{owner}/{repo}/pulls/{number}")
        out = [pr.get("body") or "", f"## Change\n\n{pr['commits']} commits, {pr['changed_files']} files, +{pr['additions']} -{pr['deletions']}. Merged: {pr.get('merged_at') or 'no'}."]
        for c in gh(f"repos/{owner}/{repo}/issues/{number}/comments?per_page=100"):
            out.append(f"## Comment by {c['user']['login']}, {c['created_at'][:10]}\n\n{c['body']}")
        for c in gh(f"repos/{owner}/{repo}/pulls/{number}/comments?per_page=100"):
            out.append(f"## Review comment r{c['id']} by {c['user']['login']}, {c['created_at'][:10]}, on {c['path']}\n\n```diff\n{c.get('diff_hunk', '')}\n```\n\n{c['body']}")
        for r in gh(f"repos/{owner}/{repo}/pulls/{number}/reviews?per_page=100"):
            if r.get("body"):
                out.append(f"## Review by {r['user']['login']}, {r['state']}\n\n{r['body']}")
        diff = run("gh", "api", f"repos/{owner}/{repo}/pulls/{number}", "-H", "Accept: application/vnd.github.diff")
        out.append(diff_section(diff))
        return {"title": f"{owner}/{repo} pull request #{number}: {pr['title']}", "author": pr["user"]["login"],
                "date": pr["created_at"][:10], "method": "the pull request, its comments, its reviews, and its diff, from the GitHub API"}, "\n\n".join(out)
    if kind in ("commit", "compare"):
        ref = parts[3]
        path = f"repos/{owner}/{repo}/{'commits' if kind == 'commit' else 'compare'}/{ref}"
        data = gh(path)
        diff = run("gh", "api", path, "-H", "Accept: application/vnd.github.diff")
        if kind == "commit":
            head = data["commit"]["message"]
            meta = {"title": f"{owner}/{repo} commit {data['sha'][:10]}", "author": data["commit"]["author"]["name"],
                    "date": data["commit"]["author"]["date"][:10]}
        else:
            head = "\n".join(f"- {c['sha'][:10]} {c['commit']['message'].splitlines()[0]}" for c in data["commits"])
            meta = {"title": f"{owner}/{repo} compare {ref}", "author": owner, "date": None}
        meta["method"] = "the commit data and diff of the GitHub API"
        return meta, f"{head}\n\n{diff_section(diff)}"
    raise ValueError(kind)


def diff_section(diff, limit=120_000):
    if len(diff) > limit:
        files = re.findall(r"^diff --git a/(\S+)", diff, re.M)
        return f"## Diff\n\nThe diff has {len(diff)} characters, more than {limit}. Its files:\n\n" + "\n".join(f"- {f}" for f in files)
    return f"## Diff\n\n````diff\n{diff}\n````"


def fetch_one(entry):
    url = entry.get("fetch") or entry["urls"][0].split("#")[0]
    kind = entry["kind"]
    if entry.get("local"):
        return {"title": entry["title"], "author": entry.get("author"), "date": None,
                "method": entry["method"]}, pathlib.Path(entry["local"]).expanduser().read_text()
    if entry.get("html"):
        import trafilatura
        page = pathlib.Path(entry["html"]).read_text()
        text = trafilatura.extract(page, output_format="markdown", include_links=True, include_formatting=True,
                                   include_tables=True, favor_recall=True)
        meta = trafilatura.extract_metadata(page)
        return {"title": entry.get("title") or meta.title, "author": meta.author, "date": meta.date,
                "method": entry["method"]}, text
    if entry.get("raw"):
        repo, ref_path = entry["raw"].split("@", 1)
        ref, path = ref_path.split(":", 1)
        text = gh(f"repos/{repo}/contents/{urllib.parse.quote(path)}?ref={ref}", raw=True)
        sha = gh(f"repos/{repo}/commits/{ref}")["sha"]
        return {"title": entry.get("title") or path, "author": entry.get("author"), "date": None,
                "method": f"the source file {path} of {repo} at commit {sha[:12]}, from the GitHub API"}, text
    if kind == "x":
        return x_post(url)
    if kind == "hn":
        return hn(url)
    if kind == "reddit":
        return reddit(url)
    if kind == "arxiv":
        return arxiv(url)
    if kind == "web":
        return web(url)
    return github(entry)


def write(entry, meta, text):
    meta = {**meta, **{k: entry[k] for k in ("title", "author", "license") if entry.get(k)}}
    head = [f"# {meta['title']}", "", NOTICE, ""]
    if str(meta.get("date", "")).startswith("2000-01-01"):
        meta["date"] = None
    for label, value in (("Author", meta.get("author")), ("Date", meta.get("date")), ("License", meta.get("license"))):
        if value:
            head.append(f"- {label}: {value}")
    head += [f"- Original location: {entry['urls'][0].split('#')[0]}", f"- Copied: {TODAY}, from {meta['method']}", "", "## Text", ""]
    path = SOURCES / entry["file"]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(head) + text.strip() + "\n")
    entry.update(title=meta["title"], author=meta.get("author"), status="ok")
    entry.pop("error", None)


def fetch(only=None):
    entries = load()
    for entry in entries:
        if (SOURCES / entry["file"]).exists() and entry["status"] == "ok":
            continue
        if only and only not in entry["file"]:
            continue
        try:
            write(entry, *fetch_one(entry))
            print("ok  ", entry["file"])
        except Exception as error:
            entry.update(status="failed", error=f"{type(error).__name__}: {error}"[:300])
            print("FAIL", entry["file"], entry["error"])
        save(entries)


def relink():
    entries = {url: e for e in load() for url in e["urls"]}
    for path in skill_files():
        text = path.read_text()

        def local(match):
            url = clean(match.group(0))
            entry = entries.get(url)
            if not entry or entry["status"] != "ok":
                return match.group(0)
            return os.path.relpath(SOURCES / entry["file"], path.parent) + match.group(0)[len(url):]
        new = URL.sub(local, text)
        new = re.sub(r"\[@([\w.]+)\]\(([^)]*sources/x/[^)]+)\)", lambda m: f"[{author_of(m[2])}]({m[2]})", new)
        if new != text:
            path.write_text(new)
            print("relinked", path.relative_to(ROOT))


def author_of(relative):
    entry = next(e for e in load() if relative.endswith(e["file"]))
    return entry.get("author") or entry["title"]


def index():
    groups = {}
    for entry in load():
        groups.setdefault(entry["file"].split("/")[0], []).append(entry)
    out = ["# Sources", "", "Each file holds the text of one source that a check, a guide, or a case cites, copied 1:1.",
           NOTICE.replace("This file quotes", "Each file quotes"), "Each file names its author, its date, its original location, and how it was copied.", ""]
    for group in sorted(groups):
        out += [f"## {group}", ""]
        for entry in sorted(groups[group], key=lambda e: e["file"]):
            name = pathlib.PurePosixPath(entry["file"]).relative_to(group)
            note = "" if entry["status"] == "ok" else f" (not copied: {entry.get('error', entry['status'])})"
            out.append(f"- [{entry.get('title') or name}]({entry['file']}){note}")
        out.append("")
    (SOURCES / "README.md").write_text("\n".join(out))
    for check in sorted((SKILL / "checks/languages").glob("*.md")):
        language_index(check, [e for e in load() if e["file"].startswith(f"languages/{check.stem}/")])


def rule_ids(spec):
    """'R1-R7, R19' -> ['R1', ..., 'R7', 'R19']."""
    ids = []
    for part in filter(None, (p.strip() for p in spec.split(","))):
        found = re.fullmatch(r"([A-Z]+)(\d+)-[A-Z]*(\d+)", part)
        ids += [f"{found[1]}{n}" for n in range(int(found[2]), int(found[3]) + 1)] if found else [part]
    return ids


def language_index(check, entries):
    """sources/languages/<language>.md: for each rule ID of the check, the copied files that support it."""
    rules = re.findall(r"^- \*\*([A-Z]+\d+)\*\* (.+)$", check.read_text(), re.M)
    by_rule = {}
    for entry in entries:
        for rule in rule_ids(entry.get("uses", "")):
            by_rule.setdefault(rule, []).append(entry)
    title = check.read_text().splitlines()[0].removeprefix("# ")
    out = [f"# Sources of the {title.lower()}", "", NOTICE.replace("This file quotes a source", "The files below quote sources"), "",
           f"The [{title.lower()}](../../checks/languages/{check.name}) cite this index. For each rule, the files below hold the copied text that supports it.", "",
           "| Rule | Sources |", "|---|---|"]
    for rule, text in rules:
        cited = by_rule.get(rule, [])
        if "[RD]" in text:
            cell = "Rule of reduce, from the [refactoring algorithm](../../checks/every-feature/refactoring.md)"
        else:
            cell = ", ".join(f"[{e['title']}]({pathlib.PurePosixPath(e['file']).relative_to('languages')})" for e in cited) or "NONE"
        out.append(f"| {rule} | {cell} |")
    out += ["", "## All files", ""] + [f"- [{e['title']}]({pathlib.PurePosixPath(e['file']).relative_to('languages')}): {e.get('license') or 'license not stated'}" for e in entries]
    (SOURCES / f"languages/{check.stem}.md").write_text("\n".join(out) + "\n")


def check():
    bad = []
    for path in skill_files():
        text = path.read_text()
        bad += [f"{path.relative_to(ROOT)}: {u}" for u in URL.findall(text)]
        prose = re.sub(r"^```.*?^```", "", text, flags=re.M | re.S)
        for target in re.findall(r"\]\(([^)#\s]+)(?:#[^)]*)?\)", prose):
            if not target.startswith(("http", "mailto")) and not (path.parent / target).exists():
                bad.append(f"{path.relative_to(ROOT)}: missing {target}")
    for index_file in sorted((SOURCES / "languages").glob("*.md")):
        bad += [f"{index_file.relative_to(ROOT)}: {rule} has no source" for rule in re.findall(r"^\| (\w+) \| NONE \|$", index_file.read_text(), re.M)]
    for entry in load():
        if entry["status"] != "ok" or not (SOURCES / entry["file"]).stat().st_size:
            bad.append(f"tools/sources.json: {entry['file']} {entry['status']}")
    print("\n".join(bad) or "ok")
    return not bad


if __name__ == "__main__":
    command = sys.argv[1]
    if command == "check":
        sys.exit(0 if check() else 1)
    {"scan": scan, "fetch": lambda: fetch(sys.argv[2] if len(sys.argv) > 2 else None), "relink": relink, "index": index}[command]()
