import re
import subprocess
import sys

PAQUETES_IGNORADOS = {"conda-forge", "pytorch-cuda", "defaults", "channels"}


def limpiar_linea(linea):
    linea = linea.split("#")[0].strip()
    if linea.startswith("-"):
        linea = linea.lstrip("- ").strip()
    if "::" in linea:
        linea = linea.split("::")[-1]
    return linea


def normalizar_para_pip(pkg):
    if not pkg or pkg in PAQUETES_IGNORADOS:
        return None
    if (
        pkg.startswith("python")
        or pkg.startswith("pip")
        or pkg.startswith("name:")
    ):
        return None
    return re.sub(r"([^=><!~])=([^=])", r"\1==\2", pkg)


archivo_yml = "env_ev.yml"
paquetes = []

with open(archivo_yml, "r", encoding="utf-8") as f:
    for linea in f:
        pkg = normalizar_para_pip(limpiar_linea(linea))
        if pkg and pkg not in paquetes:
            paquetes.append(pkg)

print(f"Se encontraron {len(paquetes)} paquetes para instalar.\n")

for pkg in paquetes:
    print(f"📦 Instalando: {pkg} ...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", pkg])
    except Exception:
        print(f"⚠️ Omitiendo o falló: {pkg}\n")