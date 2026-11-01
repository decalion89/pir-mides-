"""Mapa de exclusión de la Gran Pirámide: ¿dónde podría quedar todavía un hueco sin descubrir?

Uso: PYTHONPATH=. python estudio_cobertura.py [paso_m]
Resultados: ../resultados/19_cobertura.json, ../resultados/19_cobertura.npz, figuras 08_*.
"""
from __future__ import annotations

import os

os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")

import json
import sys
import time
from multiprocessing import Pool

import numpy as np

from piramide import cobertura as cb
from piramide import geometria as g

TAMANOS = [12.0, 8.0, 5.0, 3.0, 2.0]          # de mayor a menor (corte temprano)
UMBRAL_NOMINAL = 5.0
UMBRAL_OPTIMISTA = 3.0
RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

_ESTADO = {}


def _init(paso):
    C = cb.campanas_publicadas()
    f = cb.calibrar(C)
    ref = cb.referencia_actual()
    for c in C:
        cb.preparar(c, ref)
    K = cb.campanas_candidatas()
    for c in K:
        cb.preparar(c, ref)
    _ESTADO.update(C=C, K=K, f=f)


def _trabajo_publicadas(P):
    C, f = _ESTADO["C"], _ESTADO["f"]
    Z = np.zeros((len(P), len(TAMANOS)))
    for i, p in enumerate(P):
        for j, s in enumerate(TAMANOS):
            z2 = 0.0
            for c in C:
                z = cb.z_hueco(c, cb.cubo(p, s))
                if z > 0:
                    z2 += (f[c.familia] * z) ** 2
            Z[i, j] = np.sqrt(z2)
            if Z[i, j] < UMBRAL_OPTIMISTA:
                break                     # los huecos menores tampoco se habrían visto
    return Z


def _trabajo_candidatas(args):
    P, s = args
    K, f = _ESTADO["K"], _ESTADO["f"]
    Z = np.zeros((len(P), len(K)))
    for i, p in enumerate(P):
        for k, c in enumerate(K):
            Z[i, k] = f[c.familia] * cb.z_hueco(c, cb.cubo(p, s))
    return Z


def tamano_minimo(Z, umbral):
    """Menor lado (m) detectado; inf si ni el mayor se habría visto."""
    out = np.full(len(Z), np.inf)
    for j in range(len(TAMANOS) - 1, -1, -1):     # de menor a mayor
        m = (Z[:, j] >= umbral) & ~np.isfinite(out)
        out[m] = TAMANOS[j]
    return out


def main():
    paso = float(sys.argv[1]) if len(sys.argv) > 1 else 4.0
    t0 = time.time()
    _init(paso)
    C, K, f = _ESTADO["C"], _ESTADO["K"], _ESTADO["f"]
    an = g.anomalias_detectadas()
    ref_val = g.estructuras_conocidas()
    from dataclasses import replace
    validacion = []
    for c in C:
        cv = cb.preparar(replace(c, _pre={}), ref_val)
        validacion.append(dict(campana=c.nombre, referencia=c.referencia, area_m2=c.area_m2,
                               dias=c.dias,
                               z_nfc=round(f[c.familia] * cb.z_hueco(cv, an[0]), 1),
                               z_gran_vacio=round(f[c.familia] * cb.z_hueco(cv, an[1]), 1)))
    print("calibración:", {k: round(v, 3) for k, v in f.items() if k != "z_modelo"})
    for v in validacion:
        print(f"  {v['campana']:45s} NFC {v['z_nfc']:7.1f}σ   Gran Vacío {v['z_gran_vacio']:6.1f}σ")

    P = cb.voxeles(paso)
    ocup = cb.ocupado_por_conocidas(P, cb.referencia_actual())
    trozos = np.array_split(np.arange(len(P)), 64)
    with Pool(os.cpu_count() or 2) as pool:
        partes = pool.map(_trabajo_publicadas, [P[t] for t in trozos])
        Zp = np.vstack(partes)
        print(f"publicadas: {time.time() - t0:.0f} s")
        Zk = {}
        for s in (8.0, 5.0):
            partes = pool.map(_trabajo_candidatas, [(P[t], s) for t in trozos])
            Zk[s] = np.vstack(partes)
            print(f"candidatas s={s}: {time.time() - t0:.0f} s")

    libre = ~ocup
    res = dict(paso_m=paso, n_voxeles=int(libre.sum()),
               volumen_m3=float(libre.sum() * paso ** 3),
               calibracion={k: v for k, v in f.items() if k != "z_modelo"},
               z_modelo_gran_vacio=f["z_modelo"], validacion=validacion,
               umbrales=dict(nominal=UMBRAL_NOMINAL, optimista=UMBRAL_OPTIMISTA),
               campanas=[dict(nombre=c.nombre, familia=c.familia, origen=c.origen.round(1).tolist(),
                              area_m2=c.area_m2, dias=c.dias, referencia=c.referencia) for c in C])
    fr = {}
    for nombre_u, u in (("nominal", UMBRAL_NOMINAL), ("optimista", UMBRAL_OPTIMISTA)):
        fr[nombre_u] = {f"{s:g}": float(np.mean(Zp[libre, j] < u)) for j, s in enumerate(TAMANOS)}
    res["fraccion_sin_explorar"] = fr
    # por alturas
    zc = P[:, 2]
    bandas = [(0, 20), (20, 40), (40, 60), (60, 80), (80, 147)]
    j5 = TAMANOS.index(5.0)
    res["sin_explorar_5m_por_altura"] = {
        f"{a}-{b}": dict(nominal=float(np.mean(Zp[libre & (zc >= a) & (zc < b), j5] < UMBRAL_NOMINAL)),
                         optimista=float(np.mean(Zp[libre & (zc >= a) & (zc < b), j5] < UMBRAL_OPTIMISTA)))
        for a, b in bandas}
    # contribución de cada campaña candidata y plan voraz
    plan = {}
    for s in (8.0, 5.0):
        js = TAMANOS.index(s)
        base2 = Zp[:, js] ** 2
        elegido, cubierto = [], (np.sqrt(base2) >= UMBRAL_NOMINAL) & libre
        individual = {}
        for k, c in enumerate(K):
            nuevo = (np.sqrt(base2 + Zk[s][:, k] ** 2) >= UMBRAL_NOMINAL) & libre & ~cubierto
            individual[c.nombre] = float(nuevo.sum() / libre.sum())
        acum2 = base2.copy()
        pasos = []
        for _ in range(sum(c.area_m2 == 1.0 for c in K)):
            ganancia = []
            for k in range(len(K)):
                if k in elegido or K[k].area_m2 != 1.0:      # el plan usa puestos estándar
                    ganancia.append(-1)
                    continue
                cub = (np.sqrt(acum2 + Zk[s][:, k] ** 2) >= UMBRAL_NOMINAL) & libre
                ganancia.append(cub.sum())
            k = int(np.argmax(ganancia))
            elegido.append(k)
            acum2 = acum2 + Zk[s][:, k] ** 2
            pasos.append(dict(puesto=K[k].nombre,
                              explorado=float(np.mean(np.sqrt(acum2[libre]) >= UMBRAL_NOMINAL))))
        plan[f"{s:g}"] = dict(explorado_hoy=float(np.mean(cubierto[libre])),
                              ganancia_individual=individual, voraz=pasos)
    res["candidatas"] = dict(puestos=[dict(nombre=c.nombre, origen=c.origen.round(1).tolist(),
                                           area_m2=c.area_m2, dias=c.dias)
                                      for c in K], plan=plan)
    res["tiempo_s"] = round(time.time() - t0)
    with open(os.path.join(RAIZ, "resultados", "19_cobertura.json"), "w") as fh:
        json.dump(res, fh, indent=1, ensure_ascii=False, allow_nan=False)
    np.savez_compressed(os.path.join(RAIZ, "resultados", "19_cobertura.npz"), P=P, ocupado=ocup,
                        Z_publicadas=Zp, tamanos=np.array(TAMANOS),
                        Z_candidatas_8=Zk[8.0], Z_candidatas_5=Zk[5.0],
                        candidatas=np.array([c.nombre for c in K]))
    print(json.dumps({k: res[k] for k in ("fraccion_sin_explorar", "sin_explorar_5m_por_altura")},
                     indent=1))
    print(json.dumps(res["candidatas"]["plan"], indent=1, ensure_ascii=False))


if __name__ == "__main__":
    main()
