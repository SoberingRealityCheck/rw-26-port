# usage: fetch.py project gamever versionnumber|latest outdir
# latest = newest *release* for that game version + fabric.
import sys, json, urllib.request, urllib.parse, os
proj, gv, vn, out = sys.argv[1:5]
UA = {"User-Agent": "roadweaver-lab (cg156@rice.edu)"}
def get(url):
    return urllib.request.urlopen(urllib.request.Request(url, headers=UA)).read()
q = urllib.parse.urlencode({"loaders": '["fabric"]', "game_versions": json.dumps([gv])})
for v in json.loads(get(f"https://api.modrinth.com/v2/project/{proj}/version?{q}")):
    if v["version_number"] == vn or (vn == "latest" and v["version_type"] == "release"):
        f = [f for f in v["files"] if f["primary"]][0]
        os.makedirs(out, exist_ok=True)
        open(os.path.join(out, f["filename"]), "wb").write(get(f["url"]))
        print("ok", proj, v["version_number"], f["filename"]); break
else:
    print("NOT FOUND", proj, gv, vn)
