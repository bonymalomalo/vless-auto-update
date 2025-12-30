import os
import base64
import urllib.request

WORKDIR = "vless-scan"
os.makedirs(WORKDIR, exist_ok=True)
os.chdir(WORKDIR)

URL = "https://raw.githubusercontent.com/sevcator/5ubscrpt10n/main/protocols/vl.txt"

DUMP_RAW = "dump_raw.txt"
DUMP_DECODED = "dump.txt"
VLESS_ALL = "vless.txt"
VLESS_RUNAPP = "vless_runapp.txt"

print("[+] Téléchargement...")
urllib.request.urlretrieve(URL, DUMP_RAW)

print("[+] Décodage Base64...")
with open(DUMP_RAW, "rb") as f:
    raw_data = f.read()

"""
decoded_data = base64.b64decode(
    raw_data, validate=False
).decode("utf-8", errors="ignore")
"""
decoded_data = raw_data.decode()

with open(DUMP_DECODED, "w", encoding="utf-8") as f:
    f.write(decoded_data)

with open(DUMP_DECODED, "r", encoding="utf-8") as f:
    vless_links = [line.strip() for line in f if line.startswith("vless://")]

if not vless_links:
    print("[-] Aucun lien VLESS trouvé")
    exit(0)

with open(VLESS_ALL, "w", encoding="utf-8") as f:
    f.write("\n".join(vless_links))

vless_runapp = [v for v in vless_links if ".run.app" in v]

with open(VLESS_RUNAPP, "w", encoding="utf-8") as f:
    f.write("\n".join(vless_runapp))

print(f"[✓] Total VLESS : {len(vless_links)}")
print(f"[✓] VLESS .run.app : {len(vless_runapp)}")
