"""Acuerdo entre la codificación original del censo y la segunda codificación ciega.

Protocolo: auditoria_aleatoria/PROTOCOLO_SEGUNDA_CODIFICACION.md (registrado antes de recodificar).
Entradas: auditoria_aleatoria/clasificacion_corpus.csv (original),
          auditoria_aleatoria/segunda_codificacion.csv (subconjunto),
          auditoria_aleatoria/segunda_codificacion_resultado.csv (segunda codificación).
Salida:   resultados/56_segunda_codificacion.json
"""
import csv
import json
import os
from collections import Counter

from scipy.stats import beta

RAIZ = os.path.join(os.path.dirname(__file__), "..", "..")
AUD = os.path.join(RAIZ, "auditoria_aleatoria")


def cp(k, n, a=0.05):
    lo = 0.0 if k == 0 else beta.ppf(a / 2, k, n - k + 1)
    hi = 1.0 if k == n else beta.ppf(1 - a / 2, k + 1, n - k)
    return [round(float(lo), 3), round(float(hi), 3)]


def kappa(a, b):
    """Kappa de Cohen sin ponderar."""
    n = len(a)
    cats = sorted(set(a) | set(b))
    po = sum(x == y for x, y in zip(a, b)) / n
    ca, cb = Counter(a), Counter(b)
    pe = sum(ca[c] * cb[c] for c in cats) / n**2
    return None if pe == 1 else round((po - pe) / (1 - pe), 3), round(po, 3)


def no_supera(c):
    return c in ("FALLA", "CONDICIONAL")


def analizar(orig, seg, sub):
    """orig, seg: dict pmcid -> (aplicable, clase); sub: lista de pmcid recodificados."""
    a1 = [orig[p][0] for p in sub]
    a2 = [seg[p][0] for p in sub]
    r = {"n": len(sub)}
    r["aplicabilidad_3cat"] = dict(zip(("kappa", "acuerdo"), kappa(a1, a2)))
    r["aplicabilidad_si_vs_resto"] = dict(zip(("kappa", "acuerdo"), kappa(
        [x == "si" for x in a1], [x == "si" for x in a2])))
    r["aplicabilidad_silim_vs_no"] = dict(zip(("kappa", "acuerdo"), kappa(
        [x != "no" for x in a1], [x != "no" for x in a2])))
    r["matriz_aplicabilidad"] = {f"{x}->{y}": v for (x, y), v in sorted(Counter(zip(a1, a2)).items())}

    # Falsos negativos: entre los "no" originales recodificados, cuántos ve aplicables el segundo
    negs = [p for p in sub if orig[p][0] == "no"]
    fn_si = sum(seg[p][0] == "si" for p in negs)
    fn_any = sum(seg[p][0] != "no" for p in negs)
    n_no_total = sum(v[0] == "no" for v in orig.values())
    r["falsos_negativos"] = {
        "n_no_recodificados": len(negs),
        "pasan_a_si": fn_si, "ic_si": cp(fn_si, len(negs)),
        "pasan_a_si_o_limite": fn_any, "ic_si_o_limite": cp(fn_any, len(negs)),
        "extrapolado_a_no_totales_si": round(fn_si / len(negs) * n_no_total, 1),
        "n_no_totales": n_no_total,
        "pmcid": [p for p in negs if seg[p][0] != "no"],
    }

    # Clases entre los que ambos consideran aplicables o límite
    ambos = [p for p in sub if orig[p][0] != "no" and seg[p][0] != "no"]
    c1 = [orig[p][1] for p in ambos]
    c2 = [seg[p][1] for p in ambos]
    r["clase"] = {
        "n_ambos_aplicables": len(ambos),
        "kappa_4clases": dict(zip(("kappa", "acuerdo"), kappa(c1, c2))),
        "kappa_no_supera": dict(zip(("kappa", "acuerdo"), kappa(
            [no_supera(x) for x in c1], [no_supera(x) for x in c2]))),
        "matriz": {f"{x}->{y}": v for (x, y), v in sorted(Counter(zip(c1, c2)).items())},
        "desacuerdos": [{"pmcid": p, "original": orig[p], "segunda": seg[p]}
                        for p in ambos if orig[p][1] != seg[p][1]],
    }

    # Tasa principal (solo "si") con cada codificación sobre los 32 positivos originales
    def tasa(cod, ps):
        si = [p for p in ps if cod[p][0] == "si"]
        k = sum(no_supera(cod[p][1]) for p in si)
        return {"k": k, "n": len(si), "p": round(k / len(si), 3) if si else None, "ic": cp(k, len(si)) if si else None}

    pos = [p for p in sub if orig[p][0] != "no"]
    r["tasa"] = {
        "original_si": tasa(orig, pos),
        "segunda_si_entre_positivos_originales": tasa(seg, pos),
        "segunda_si_en_todo_el_subconjunto": tasa(seg, sub),
    }
    inter = [p for p in pos if orig[p][0] == "si" and seg[p][0] == "si"]
    k_int = sum(no_supera(orig[p][1]) and no_supera(seg[p][1]) for p in inter)
    r["tasa"]["interseccion"] = {"k_ambos_no_supera": k_int, "n_ambos_si": len(inter),
                                 "p": round(k_int / len(inter), 3) if inter else None,
                                 "ic": cp(k_int, len(inter)) if inter else None}
    return r


def leer():
    orig = {r["pmcid"]: (r["aplicable"], r["clase"])
            for r in csv.DictReader(open(os.path.join(AUD, "clasificacion_corpus.csv")))}
    sub = [r["pmcid"] for r in csv.DictReader(open(os.path.join(AUD, "segunda_codificacion.csv")))]
    seg = {}
    for r in csv.DictReader(open(os.path.join(AUD, "segunda_codificacion_resultado.csv"))):
        a = r["aplicable"].strip().lower().replace("í", "i")
        c = r["clase"].strip().upper() if a != "no" else "NA"
        seg[r["pmcid"].strip()] = (a, c)
    assert set(sub) <= set(seg), set(sub) - set(seg)
    return orig, seg, sub


if __name__ == "__main__":
    orig, seg, sub = leer()
    r = analizar(orig, seg, sub)
    out = os.path.join(RAIZ, "resultados", "56_segunda_codificacion.json")
    json.dump(r, open(out, "w"), indent=1, ensure_ascii=False)
    print(json.dumps(r, indent=1, ensure_ascii=False))
