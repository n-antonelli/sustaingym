import re
import subprocess
import sys

# Elementos o metapaquetes exclusivos de Conda a omitir
PAQUETES_IGNORADOS = {
    "conda-forge",
    "pytorch-cuda",
    "defaults",
    "channels",
}


def limpiar_linea(linea):
    # 1. Eliminar comentarios al final de la línea (# ...)
    linea = linea.split("#")[0].strip()

    # 2. Quitar viñetas de lista
    if linea.startswith("-"):
        linea = linea.lstrip("- ").strip()

    # 3. Limpiar canales de conda (ej. conda-forge::cvxpy)
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

    # Convertir operador de versión de Conda '=' a '==' de pip
    # (respetando '==', '>=', '<=')
    pkg = re.sub(r"([^=><!~])=([^=])", r"\1==\2", pkg)

    return pkg


def instalar_desde_yml(archivo_yml="environment.yml"):
    paquetes = []

    with open(archivo_yml, "r", encoding="utf-8") as f:
        for linea in f:
            linea_limpia = limpiar_linea(linea)
            pkg = normalizar_para_pip(linea_limpia)
            if pkg and pkg not in paquetes:
                paquetes.append(pkg)

    print(f"Se identificaron {len(paquetes)} paquetes válidos para pip.\n")

    fallidos = []
    for pkg in paquetes:
        print(f"📦 Instalando: {pkg} ...")
        try:
            subprocess.check_call(
                [sys.executable, "-m", "pip", "install", pkg]
            )
        except subprocess.CalledProcessError:
            print(f"⚠️ No se pudo instalar: {pkg}\n")
            fallidos.append(pkg)

    print("\n--------------------------------------------------")
    if fallidos:
        print("❌ Los siguientes paquetes fallaron y requieren atención:")
        for f_pkg in fallidos:
            print(f" - {f_pkg}")
    else:
        print("✅ ¡Todos los paquetes se instalaron correctamente!")


if __name__ == "__main__":
    # Asegúrate de colocar el nombre correcto de tu archivo .yml aquí
    instalar_desde_yml("environment.yml")