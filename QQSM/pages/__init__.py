import pkgutil
import importlib
from pathlib import Path

# Ruta del paquete actual
package_dir = Path(__file__).parent

# Importa las páginas del paquete una por una
for finder, module_name, is_pkg in pkgutil.iter_modules([str(package_dir)]):
    if not is_pkg and module_name != "__init__":
        importlib.import_module(f"{__name__}.{module_name}")
