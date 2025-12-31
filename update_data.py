import os
import base64
import urllib.request

WORKDIR = "vless-scan"
os.makedirs(WORKDIR, exist_ok=True)

URLS = [
    "https://raw.githubusercontent.com/sevcator/5ubscrpt10n/main/protocols/vl.txt",
    "https://raw.githubusercontent.com/ebrasha/free-v2ray-public-list/main/vless_configs.txt",
    "https://github.com/Epodonios/v2ray-configs/raw/main/All_Configs_Sub.txt",
    "https://raw.githubusercontent.com/AvenCores/goida-vpn-configs/refs/heads/main/githubmirror/1.txt",
    "https://raw.githubusercontent.com/STR97/STRUGOV/refs/heads/main/STR.BYPASS",
    "https://raw.githubusercontent.com/V2RayRoot/V2RayConfig/refs/heads/main/Config/vless.txt",
    ""
]

URLS_B64 = [
    "https://github.com/Epodonios/v2ray-configs/raw/main/Splitted-By-Protocol/vless.txt",
    "https://raw.githubusercontent.com/AvenCores/goida-vpn-configs/refs/heads/main/githubmirror/4.txt",
    "https://raw.githubusercontent.com/ALIILAPRO/v2rayNG-Config/main/sub.txt",
    "https://raw.githubusercontent.com/Surfboardv2ray/TGParse/main/splitted/mixed",
    "https://raw.githubusercontent.com/coldwater-10/V2ray-Config/main/Splitted-By-Protocol/vless.txt"
]

VLESS_ALL = os.path.join(WORKDIR, "vless.txt")
VLESS_RUNAPP = os.path.join(WORKDIR, "vless_runapp.txt")


def fetch(url):
    try:
        with urllib.request.urlopen(url, timeout=20) as r:
            return r.read()
    except Exception as e:
        print(f"[-] Erreur téléchargement {url} : {e}")
        return b""


def decode_sources(urls, base64_encoded=False):
    sources = []
    for url in urls:
        raw = fetch(url)
        if not raw:
            continue

        try:
            if base64_encoded:
                data = base64.b64decode(raw, validate=False).decode("utf-8", "ignore")
            else:
                data = raw.decode("utf-8", "ignore")

            sources.append({"url": url, "data": data})
        except Exception as e:
            print(f"[-] Erreur décodage {url} : {e}")

    return sources


sources = []
sources += decode_sources(URLS, base64_encoded=False)
sources += decode_sources(URLS_B64, base64_encoded=True)

vless_all = set()
vless_runapp = set()

for src in sources:
    for line in src["data"].splitlines():
        if line.startswith("vless://"):
            vless_all.add(line.strip())
            if ".run.app" in line:
                vless_runapp.add(line.strip())

if not vless_all:
    print("[-] Aucun lien VLESS trouvé")
    exit(0)

with open(VLESS_ALL, "w", encoding="utf-8") as f:
    f.write("\n".join(sorted(vless_all)))

with open(VLESS_RUNAPP, "w", encoding="utf-8") as f:
    f.write("\n".join(sorted(vless_runapp)))

print(f"[✓] Total VLESS uniques : {len(vless_all)}")
print(f"[✓] VLESS .run.app : {len(vless_runapp)}")