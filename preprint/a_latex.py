"""Convierte preprint_en.md en un paquete compilable con pdflatex para arXiv (arxiv/main.tex)."""
import re
import subprocess
from pathlib import Path

md = Path("preprint_en.md").read_text(encoding="utf-8")
md = md.replace("../figuras/", "figuras/")
# superíndices/subíndices
sup = {"⁰": "0", "¹": "1", "²": "2", "³": "3", "⁴": "4", "⁵": "5", "⁶": "6", "⁷": "7", "⁸": "8", "⁹": "9", "⁻": "-"}
md = re.sub(r"([⁰¹²³⁴⁵⁶⁷⁸⁹⁻]+)", lambda m: "$^{" + "".join(sup[c] for c in m.group(1)) + "}$", md)
md = md.replace("E₀", "$E_0$")
simbolos = {
    "σ": r"$\sigma$", "χ": r"$\chi$", "Δ": r"$\Delta$", "θ": r"$\theta$", "μ": r"$\mu$", "φ": r"$\varphi$",
    "δ": r"$\delta$", "ψ": r"$\psi$", "η": r"$\eta$", "β": r"$\beta$", "ε": r"$\epsilon$", "ζ": r"$\zeta$",
    "ρ": r"$\rho$", "π": r"$\pi$", "≥": r"$\geq$", "≤": r"$\leq$", "±": r"$\pm$", "≈": r"$\approx$",
    "×": r"$\times$", "°": r"$^\circ$", "′": r"$'$", "≲": r"$\lesssim$", "→": r"$\to$", "▼": r"$\blacktriangledown$",
}
for k, v in simbolos.items():
    md = md.replace(k, v)
md = md.replace("$$", "")          # fusiona símbolos contiguos ($\sigma$$^{2}$ -> $\sigma^{2}$)
Path("arxiv/main.md").write_text(md, encoding="utf-8")
subprocess.run(["pandoc", "arxiv/main.md", "-s", "-o", "arxiv/main.tex",
                "-V", "geometry:margin=2.2cm", "-V", "fontsize=11pt",
                "--include-in-header=arxiv_cabecera.tex"], check=True)
Path("arxiv/main.md").unlink()
tex = Path("arxiv/main.tex").read_text(encoding="utf-8")
resto = sorted({c for c in tex if ord(c) > 127})
print("caracteres no ASCII que quedan:", "".join(resto))
