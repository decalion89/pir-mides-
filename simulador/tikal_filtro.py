"""¿Pudo un filtro de zeolita y cuarzo en la entrada del embalse Corriental (Tikal) purificar su agua?

Tankersley et al. (Sci. Rep. 10:18021, 2020): "the drinking water in the Corriental reservoir
water was filtered through a mixture of zeolite and coarse, sand-sized crystalline quartz";
embalse de ~58 000 m³; esquema "hipotético" de un filtro tras muros de piedra seca "just upstream of,
or within the reservoir ingresses", arrastrado por las riadas; material traído de una toba a ~30 km.
El artículo no da el área del filtro ni la cuenca.

Comprobación de caudal: lluvia horaria estocástica (1 500 mm/año, intensidades exponenciales),
escorrentía C·i·A de una cuenca de 5–50 ha; un filtro de área A_f trata como mucho v·A_f, con v de
0,1–0,4 m/h (filtro lento de arena, el que elimina microbios) o 5–10 m/h (rápido, solo aclara). Se
calcula la fracción de la escorrentía anual que pasa por el filtro y el área necesaria para el 90 %,
con la masa de material que habría que transportar 30 km (lecho de 0,5–1 m, 1,6 t/m³).

Uso: PYTHONPATH=. python tikal_filtro.py → ../resultados/47_tikal_filtro.json
"""
import json
import os

import numpy as np

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def fraccion_filtrada(rng, area_cuenca_m2, C, v_m_h, area_filtro_m2, anos=20, lluvia=1500.0, horas_lluvia=300):
    i_media = lluvia / horas_lluvia                      # mm/h en horas con lluvia
    tot = filt = 0.0
    for _ in range(anos):
        i = rng.exponential(i_media, horas_lluvia)        # mm/h
        Q = C * i / 1000.0 * area_cuenca_m2               # m³/h
        cap = v_m_h * area_filtro_m2                       # m³/h
        tot += Q.sum()
        filt += np.minimum(Q, cap).sum()
    return filt / tot, tot / anos


def area_para_volumen(rng_seed, A, C, v, objetivo_m3, horas):
    """Área mínima para que el filtro (sin agua almacenada delante) deje pasar `objetivo_m3` al año."""
    lo, hi = 0.1, 1e6
    for _ in range(30):
        mid = np.sqrt(lo * hi)
        f, anual = fraccion_filtrada(np.random.default_rng(rng_seed), A, C, v, mid, anos=5, horas_lluvia=horas)
        if f * anual >= objetivo_m3:
            hi = mid
        else:
            lo = mid
    return hi


def revisado():
    """Tras la revisión: objetivo = volumen del embalse (58 000 m³/año), caso con agua embalsada delante
    del filtro y sensibilidad a las horas de lluvia."""
    rng = np.random.default_rng(470)
    out = {}
    for horas in (150, 300, 600):
        areas = []
        for _ in range(150):
            A = rng.uniform(5e4, 5e5)
            C = rng.uniform(0.3, 0.7)
            v = rng.uniform(0.1, 0.4)
            areas.append(area_para_volumen(int(rng.integers(1e9)), A, C, v, 58_000.0, horas))
        a = np.array(areas)
        out[f"sin almacenamiento, {horas} h de lluvia/año"] = dict(
            area_m2=dict(p05=round(float(np.percentile(a, 5))), mediana=round(float(np.median(a))), p95=round(float(np.percentile(a, 95)))),
            masa_t_mediana=round(float(np.median(a) * 0.75 * 1.6)))
        print(horas, out[f"sin almacenamiento, {horas} h de lluvia/año"], flush=True)
    # con agua embalsada delante: el filtro trabaja de forma continua durante la estación de lluvias
    v = np.array([0.1, 0.25, 0.4])
    for dias in (120, 180):
        out[f"con agua embalsada delante, {dias} días de filtrado"] = {f"v={x} m/h": round(float(58_000 / (x * 24 * dias)), 0) for x in v}
    print(out, flush=True)
    return out


def main():
    rng = np.random.default_rng(47)
    res = {}
    for nombre, v in (("filtro lento (0,1–0,4 m/h, elimina microbios)", (0.1, 0.4)),
                      ("filtro rápido (5–10 m/h, solo aclara)", (5.0, 10.0))):
        filas = []
        for _ in range(400):
            A = rng.uniform(5e4, 5e5)
            C = rng.uniform(0.3, 0.7)
            vv = rng.uniform(*v)
            f50, anual = fraccion_filtrada(rng, A, C, vv, 50.0)
            # área para el 90 % (bisección logarítmica)
            lo, hi = 1.0, 1e6
            for _ in range(30):
                mid = np.sqrt(lo * hi)
                if fraccion_filtrada(np.random.default_rng(1), A, C, vv, mid, anos=5)[0] >= 0.9:
                    hi = mid
                else:
                    lo = mid
            masa = hi * rng.uniform(0.5, 1.0) * 1.6        # t
            filas.append(dict(f50=f50, anual=anual, area90=hi, masa90=masa))
        pc = lambda k, f=1.0: dict(p05=float(f"{np.percentile([x[k] for x in filas], 5) * f:.3g}"),
                                   mediana=float(f"{np.median([x[k] for x in filas]) * f:.3g}"),
                                   p95=float(f"{np.percentile([x[k] for x in filas], 95) * f:.3g}"))
        res[nombre] = dict(escorrentia_anual_m3=pc("anual"), fraccion_filtrada_con_50m2=pc("f50"),
                           area_para_90pc_m2=pc("area90"), masa_a_transportar_30km_t=pc("masa90"))
        print(nombre, json.dumps(res[nombre], ensure_ascii=False), flush=True)
    res["revision_objetivo_volumen_del_embalse"] = revisado()
    json.dump(res, open(os.path.join(RAIZ, "resultados", "47_tikal_filtro.json"), "w"), ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()
