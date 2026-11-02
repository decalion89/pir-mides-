"""Reanálisis de los residuos publicados por Alvarez et al. (1970), figura 10.

Pregunta: las discrepancias entre muones medidos y predichos (χ² = 905 para ~750 bins), ¿están
repartidas al azar o se agrupan en alguna zona, como haría una cámara oculta (exceso de muones en
varios bins contiguos)?

Pruebas (permutaciones de los residuos entre los bins válidos, 2 000 réplicas, y una nula con
correlación espacial de corto y largo alcance; ver nula_correlada):
1. Σ r² frente al χ² publicado (comprobación de la transcripción).
2. Autocorrelación espacial entre vecinos (I de Moran).
3. Máximo de la suma normalizada Σr/√n en ventanas de 2×2, 3×3 y 4×4 bins, para excesos
   (posibles cámaras) y para déficits (posibles masas densas).
4. Valor en la zona que señalan Gutowski et al. (2017).
Los tres valores de signo dudoso se analizan en sus 8 combinaciones.

Uso: PYTHONPATH=. python reanalisis_alvarez.py → ../resultados/23_reanalisis_alvarez.json
"""
from __future__ import annotations

import itertools
import json
import os

import numpy as np

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ARCHIVO = os.path.join(RAIZ, "datos", "alvarez_1970", "fig10_residuos.txt")
N = 30
VENTANAS = (2, 3, 4)
N_PERM = 2000


def cargar(signos=None):
    """Matriz 30×30 (NaN = bin no usado). `signos`: ±1 para cada valor dudoso, en orden."""
    filas = [l for l in open(ARCHIVO, encoding="utf-8") if l.strip() and not l.startswith("#")]
    M = np.full((N, N), np.nan)
    dudosos = []
    k = 0
    for i, l in enumerate(filas):
        izq, der = l.split("|")
        vals = []
        for parte in (izq.split(), der.split()):
            fila = []
            for t in parte:
                if t.endswith("?"):
                    v = float(t[:-1])
                    s = 1 if signos is None else signos[k]
                    fila.append(abs(v) * s)
                    k += 1
                else:
                    fila.append(float(t))
            vals.append(fila)
        r = i + 1                                  # la primera fila de la figura está vacía
        for j, v in enumerate(vals[0]):
            M[r, 15 - len(vals[0]) + j] = v
        for j, v in enumerate(vals[1]):
            M[r, 15 + j] = v
        if signos is None:
            dudosos += [(r, c) for c in range(N) if False]
    return M, k


def moran(M):
    v = ~np.isnan(M)
    x = np.where(v, M - np.nanmean(M), 0.0)
    num, w = 0.0, 0
    for di, dj in ((0, 1), (1, 0)):
        a = x[: N - di, : N - dj]
        b = x[di:, dj:]
        m = v[: N - di, : N - dj] & v[di:, dj:]
        num += 2 * np.sum(a[m] * b[m])
        w += 2 * m.sum()
    return float((v.sum() / w) * num / np.sum(x[v] ** 2))


def max_ventana(M, k, signo=1):
    v = ~np.isnan(M)
    x = np.where(v, M, 0.0)
    mejor, donde = -np.inf, None
    for i in range(N - k + 1):
        for j in range(N - k + 1):
            n = v[i:i + k, j:j + k].sum()
            if n < k * k:                          # solo ventanas completas
                continue
            s = signo * x[i:i + k, j:j + k].sum() / np.sqrt(n)
            if s > mejor:
                mejor, donde = s, (i, j)
    return float(mejor), donde


def permutar(M, rng):
    v = ~np.isnan(M)
    P = M.copy()
    P[v] = rng.permutation(M[v])
    return P


def angulos(i, j):
    """Centro del bin: (θ, φ) en grados; 90° = vertical. Norte arriba, este a la derecha."""
    return 45 + 3 * i + 1.5, 45 + 3 * j + 1.5


def main():
    rng = np.random.default_rng(1970)
    M0, n_dud = cargar()
    v = ~np.isnan(M0)
    res = dict(fuente="Alvarez et al., Science 167, 832 (1970), fig. 10", n_bins=int(v.sum()),
               chi2_publicado=905, n_dudosos=n_dud, combinaciones={})
    # distribución nula: permutaciones (para cada estadístico)
    nulos = {f"exceso_{k}": [] for k in VENTANAS} | {f"deficit_{k}": [] for k in VENTANAS} | {"moran": []}
    for _ in range(N_PERM):                    # la nula no depende de los signos dudosos
        P = permutar(M0, rng)
        nulos["moran"].append(moran(P))
        for k in VENTANAS:
            nulos[f"exceso_{k}"].append(max_ventana(P, k, 1)[0])
            nulos[f"deficit_{k}"].append(max_ventana(P, k, -1)[0])
    nulos = {k: np.array(x) for k, x in nulos.items()}
    for signos in itertools.product((1, -1), repeat=n_dud):
        M, _ = cargar(signos)
        r = dict(suma_r2=float(np.nansum(M ** 2)), media=float(np.nanmean(M)),
                 desv=float(np.nanstd(M)), n_abs_ge_3=int(np.sum(np.abs(M[v]) >= 3)),
                 moran=moran(M))
        r["moran_p"] = float(np.mean(nulos["moran"] >= r["moran"]))
        for k in VENTANAS:
            for nombre, s in (("exceso", 1), ("deficit", -1)):
                val, (i, j) = max_ventana(M, k, s)
                th, ph = angulos(i + (k - 1) / 2, j + (k - 1) / 2)
                r[f"{nombre}_{k}x{k}"] = dict(valor=round(val, 2),
                                              p_global=float(np.mean(nulos[f"{nombre}_{k}"] >= val)),
                                              theta=th, phi=ph)
        res["combinaciones"]["".join("+" if s > 0 else "-" for s in signos)] = r
    # zona de Gutowski et al.: ~30° del cenit, acimut 62–72° (convención desconocida: se dan
    # las cuatro lecturas del acimut, desde el norte o desde el este, en ambos sentidos)
    M, _ = cargar()
    zonas = {}
    t = np.degrees(np.arctan(np.tan(np.radians(30))))
    for nombre, (de, dn) in {
            "N→E (67° desde el norte hacia el este)": (np.sin(np.radians(67)), np.cos(np.radians(67))),
            "E→N (67° desde el este hacia el norte)": (np.cos(np.radians(67)), np.sin(np.radians(67))),
            "N→O": (-np.sin(np.radians(67)), np.cos(np.radians(67))),
            "E→S": (np.cos(np.radians(67)), -np.sin(np.radians(67)))}.items():
        ax = np.degrees(np.arctan(np.tan(np.radians(30)) * de))     # proyección este-oeste
        ay = np.degrees(np.arctan(np.tan(np.radians(30)) * dn))     # proyección norte-sur
        j = int((90 + ax - 45) // 3)
        i = int((90 - ay - 45) // 3)
        bloque = M[max(i - 1, 0):i + 2, max(j - 1, 0):j + 2]
        n = np.sum(~np.isnan(bloque))
        zonas[nombre] = dict(fila=i, columna=j, suma_3x3_sobre_raiz_n=round(float(np.nansum(bloque) / np.sqrt(n)), 2),
                             valores=bloque.tolist())
    res["zona_gutowski"] = zonas
    res["nota"] = ("p_global: fracción de permutaciones con un máximo igual o mayor en cualquier lugar "
                   "del mapa (incluye el efecto de mirar en todas partes).")
    with open(os.path.join(RAIZ, "resultados", "23_reanalisis_alvarez.json"), "w") as fh:
        json.dump(res, fh, indent=1, ensure_ascii=False, allow_nan=False)
    for c, r in res["combinaciones"].items():
        print(c, f"Σr²={r['suma_r2']:.0f} media={r['media']:+.3f} desv={r['desv']:.2f} |r|≥3: {r['n_abs_ge_3']} "
                 f"Moran={r['moran']:+.3f} (p={r['moran_p']:.3f})")
        for k in VENTANAS:
            e, d = r[f"exceso_{k}x{k}"], r[f"deficit_{k}x{k}"]
            print(f"   {k}x{k}: exceso {e['valor']:.2f} p={e['p_global']:.3f} en θ={e['theta']:.0f} φ={e['phi']:.0f} | "
                  f"déficit {d['valor']:.2f} p={d['p_global']:.3f} en θ={d['theta']:.0f} φ={d['phi']:.0f}")
    print(json.dumps({k: {a: b for a, b in v.items() if a != 'valores'} for k, v in zonas.items()}, ensure_ascii=False))


if __name__ == "__main__":
    main()


# --- Nula con correlación espacial (más exigente) ---------------------------------------------
RETARDOS = ((0, 1), (1, 0), (1, 1), (1, -1), (0, 2), (2, 0), (0, 3), (3, 0), (2, 2))


def correlaciones(M):
    """Correlación de los residuos a varias distancias (filas, columnas) entre bins válidos."""
    v = ~np.isnan(M)
    x = np.where(v, M - np.nanmean(M), 0.0)
    out = []
    for di, dj in RETARDOS:
        a = x[max(0, -di):N - max(0, di), max(0, -dj):N - max(0, dj)]
        va = v[max(0, -di):N - max(0, di), max(0, -dj):N - max(0, dj)]
        b = x[max(0, di):N + min(0, di), max(0, dj):N + min(0, dj)]
        vb = v[max(0, di):N + min(0, di), max(0, dj):N + min(0, dj)]
        m = va & vb
        out.append(float(np.sum(a[m] * b[m]) / np.sqrt(np.sum(a[m] ** 2) * np.sum(b[m] ** 2))))
    return np.array(out)


def campo_correlado(mascara, sigma_k, desv, rng, frac=1.0, media=0.0):
    """Campo gaussiano: fracción `frac` de varianza suavizada (núcleo sigma_k) + resto blanco.

    Se reescala para que, TRAS redondear a enteros, tenga la dispersión `desv` y la media `media`
    observadas (la reescala previa al redondeo se corrige con un factor fijo calibrado aparte).
    """
    from scipy.ndimage import gaussian_filter
    g = gaussian_filter(rng.normal(size=(N + 16, N + 16)), sigma_k, mode="wrap")[8:-8, 8:-8]
    g = (g - g[mascara].mean()) / g[mascara].std()
    w = rng.normal(size=(N, N))
    z = np.sqrt(frac) * g + np.sqrt(1 - frac) * w
    z = (z - z[mascara].mean()) / z[mascara].std() * desv + media
    out = np.full((N, N), np.nan)
    out[mascara] = np.round(z[mascara])
    return out


def calibrar_nula(M, rng, n=120):
    """Elige (sigma_k, frac, escala) para reproducir correlaciones y dispersión tras redondeo."""
    v = ~np.isnan(M)
    obs = correlaciones(M)
    desv_obs, media_obs = float(np.nanstd(M)), float(np.nanmean(M))
    mejor = None
    for sk in (0.5, 1.0, 1.5, 2.0, 3.0, 4.0):
        for frac in (0.05, 0.08, 0.11, 0.14, 0.18, 0.25, 0.35, 0.5, 1.0):
            sims = [campo_correlado(v, sk, desv_obs * 0.93, rng, frac, media_obs) for _ in range(n)]
            c = np.mean([correlaciones(S) for S in sims], axis=0)
            e = float(np.sum((c - obs) ** 2))
            if mejor is None or e < mejor[0]:
                mejor = (e, sk, frac, c)
    _, sk, frac, c = mejor
    # escala previa al redondeo para que la dispersión final coincida
    esc = 0.93
    for _ in range(6):
        d = np.mean([np.nanstd(campo_correlado(v, sk, desv_obs * esc, rng, frac, media_obs)) for _ in range(n)])
        esc *= desv_obs / d
    return dict(sigma_nucleo_bins=sk, fraccion_correlada=frac, escala=float(esc),
                correlaciones_observadas=[round(x, 3) for x in obs],
                correlaciones_simuladas=[round(float(x), 3) for x in c],
                retardos=[list(r) for r in RETARDOS])


def nula_correlada(n_sim=4000, semilla=7):
    rng = np.random.default_rng(semilla)
    M, _ = cargar()
    v = ~np.isnan(M)
    cal = calibrar_nula(M, rng)
    desv, media = float(np.nanstd(M)), float(np.nanmean(M))
    nul = {f"{n}_{k}": [] for n in ("exceso", "deficit") for k in VENTANAS}
    maximo_global = []
    for _ in range(n_sim):
        P = campo_correlado(v, cal["sigma_nucleo_bins"], desv * cal["escala"], rng,
                            cal["fraccion_correlada"], media)
        fila = []
        for k in VENTANAS:
            e = max_ventana(P, k, 1)[0]
            d = max_ventana(P, k, -1)[0]
            nul[f"exceso_{k}"].append(e)
            nul[f"deficit_{k}"].append(d)
            fila.append((e, d))
        maximo_global.append(fila)
    out = dict(calibracion=cal, n_sim=n_sim)
    # p de cada estadístico y p conjunto (el más extremo de los seis, en rango, frente a la nula)
    obs_p = []
    for k in VENTANAS:
        for n, s in (("exceso", 1), ("deficit", -1)):
            val, (i, j) = max_ventana(M, k, s)
            p = float(np.mean(np.array(nul[f"{n}_{k}"]) >= val))
            obs_p.append(p)
            th, ph = angulos(i + (k - 1) / 2, j + (k - 1) / 2)
            out[f"{n}_{k}x{k}"] = dict(valor=round(val, 2), p_global=p, theta=th, phi=ph)
    # p conjunto: fracción de simulaciones cuyo MENOR p entre los seis estadísticos es ≤ el observado
    arr = {key: np.array(val) for key, val in nul.items()}
    pmin_sim = []
    for t in range(n_sim):
        ps = []
        for k in VENTANAS:
            for n in ("exceso", "deficit"):
                ps.append(np.mean(arr[f"{n}_{k}"] >= arr[f"{n}_{k}"][t]))
        pmin_sim.append(min(ps))
    out["p_minimo_observado"] = min(obs_p)
    out["p_conjunto_seis_estadisticos"] = float(np.mean(np.array(pmin_sim) <= min(obs_p)))
    return out


if __name__ == "__main__" and os.environ.get("NULA_CORRELADA"):
    r = nula_correlada()
    p = os.path.join(RAIZ, "resultados", "23_reanalisis_alvarez.json")
    d = json.load(open(p))
    d["nula_correlada"] = r
    json.dump(d, open(p, "w"), indent=1, ensure_ascii=False, allow_nan=False)
    print(json.dumps(r, indent=1, ensure_ascii=False))
