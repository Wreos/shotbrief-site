from html import escape
from pathlib import Path
import os
from shutil import copy2, copytree
import sys


root = Path(__file__).resolve().parents[1]
output = Path(sys.argv[1])
address = [line.strip() for line in os.environ.get("IMPRESSUM_ADDRESS", "").splitlines() if line.strip()]
if not address:
    raise SystemExit("Set the IMPRESSUM_ADDRESS Actions secret before publishing.")

impressum = (root / "impressum/index.html").read_text(encoding="utf-8")
marker = "<!-- IMPRESSUM_ADDRESS -->"
if impressum.count(marker) != 1:
    raise SystemExit("The Impressum template must contain one address placeholder.")

address_markup = "<br>\n       ".join(escape(line) for line in address)
provider_markup = f"<p>Aleksandr Lozhkovoi<br>\n       {address_markup}<br>\n       Deutschland</p>"

output.mkdir()
for filename in ("index.html", "styles.css", ".nojekyll"):
    copy2(root / filename, output / filename)
for dirname in ("assets", "impressum", "privacy", "support"):
    copytree(root / dirname, output / dirname)
(output / "impressum/index.html").write_text(
    impressum.replace(marker, provider_markup), encoding="utf-8"
)
