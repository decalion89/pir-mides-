"""¿Cómo orientaron los egipcios las pirámides al norte? El método del "tránsito simultáneo".

Spence (Nature 2000) propuso que se esperaba a que dos estrellas, una por encima y otra por
debajo del polo, quedaran en la misma vertical (plomada), y se tomaba esa dirección como el
norte. Como el polo celeste se desplaza por la precesión, el error de esa dirección cambia con
los siglos y permitiría fechar las pirámides.

Aquí, para un par de estrellas (A, B) y un año:
1. se calcula el acimut de ambas a lo largo del día sidéreo en Giza;
2. se buscan los instantes en que tienen el mismo acimut cerca del norte (|az| < 3°);
3. ese acimut común es el error de orientación (positivo = este, negativo = oeste).
Hay dos configuraciones por día: A encima de B, o B encima de A.
"""
from __future__ import annotations

import math

import numpy as np

from . import astronomia as astro

# Spence (2000), tabla 1: error del lado oeste (′, + = este) y fecha de acceso al trono según
# von Beckerath (cifras bajas), con el reinado de Esnofru según Stadelmann. Spence supone que la
# orientación se hizo en el año 2 del reinado: aquí se restan 2 años a la fecha a. C. El error de
# fecha es el margen de su tabla, simetrizado.
PIRAMIDES = [
    # nombre, error ('), sigma ('), año a. C. de la orientación, sigma año
    ("Meidum", -20.6, 1.0, 2598, 10),
    ("Acodada", -17.3, 0.2, 2583, 7),
    ("Roja", -8.7, 0.2, 2572, 6),
    ("Keops", -3.4, 0.2, 2552, 2),
    ("Kefrén", -6.0, 0.2, 2520, 2),
    ("Micerino", 12.4, 1.0, 2487, 3),
]
# Pirámides de la V dinastía en la misma tabla (Spence: margen nominal de 10′)
PIRAMIDES_V = [
    ("Sahure", -23.0, 10.0, 2444, 15),
    ("Neferirkare", 30.0, 10.0, 2431, 16),
    ("Unas", 17.1, 1.0, 2315, 20),
]
# Spence obtiene Keops orientada en 2480 ± 5 a. C.: un desfase de −72 a −74 años respecto de esta
# tabla (fechas 74 años más recientes que las de von Beckerath).
ALTURA_MIN = 5.0     # grados: ambas estrellas deben verse por encima del horizonte

LAT = math.radians(astro.LAT_GIZA)


def _altaz(dec, H):
    sd, cd = np.sin(dec), np.cos(dec)
    sh, ch = np.sin(H), np.cos(H)
    alt = np.arcsin(math.sin(LAT) * sd + math.cos(LAT) * cd * ch)
    az = np.arctan2(-cd * sh, sd * math.cos(LAT) - cd * ch * math.sin(LAT))
    return alt, az


def ra_dec_fecha(cat: astro.Catalogo, anio: float):
    """Ascensión recta y declinación de la fecha (rad) para todo el catálogo."""
    dt = anio - 2000.0
    dec = cat.dec + cat.pmde * dt * astro.ARCSEC
    ra = cat.ra + cat.pmra * dt * astro.ARCSEC / np.cos(cat.dec)
    v = np.stack([np.cos(dec) * np.cos(ra), np.cos(dec) * np.sin(ra), np.sin(dec)])
    w = astro._precesion(dt / 100.0) @ v
    return np.arctan2(w[1], w[0]), np.arcsin(np.clip(w[2], -1, 1))


def error_alineacion(raA, decA, raB, decB, n: int = 7200):
    """Acimuts (minutos de arco) de las dos configuraciones de plomada común cerca del norte.

    Devuelve un dict {"A_arriba": az, "B_arriba": az}, o NaN si no existe.
    """
    lst = np.linspace(0, 2 * math.pi, n, endpoint=False)
    altA, azA = _altaz(decA, lst - raA)
    altB, azB = _altaz(decB, lst - raB)
    d = np.angle(np.exp(1j * (azA - azB)))
    out = {"A_arriba": np.nan, "B_arriba": np.nan}
    s = np.where(np.sign(d) != np.sign(np.roll(d, -1)))[0]
    for i in s:
        j = (i + 1) % n
        if abs(d[i] - d[j]) > 1.0:          # salto de ±π, no es un cruce
            continue
        f = d[i] / (d[i] - d[j])
        az = azA[i] + f * np.angle(np.exp(1j * (azA[j] - azA[i])))
        if abs(az) > math.radians(3):
            continue
        if min(altA[i], altB[i]) < math.radians(ALTURA_MIN):
            continue                          # una de las dos estrellas no se ve
        clave = "A_arriba" if altA[i] > altB[i] else "B_arriba"
        out[clave] = math.degrees(az) * 60
    return out


def curva_par(cat: astro.Catalogo, iA: int, iB: int, anios: np.ndarray) -> dict:
    """Error de orientación (′) frente al año para las dos configuraciones del par."""
    res = {"A_arriba": [], "B_arriba": []}
    for a in anios:
        ra, dec = ra_dec_fecha(cat, a)
        e = error_alineacion(ra[iA], dec[iA], ra[iB], dec[iB])
        for k in res:
            res[k].append(e[k])
    return {k: np.array(v) for k, v in res.items()}


def ajustar_par(anios: np.ndarray, curvas: dict, permitir_cambio: bool = False,
                desfases=np.arange(-500, 501, 2.0), piramides=None):
    """Mejor desfase cronológico ΔT (años) y χ² para las pirámides de PIRAMIDES.

    Modelo: error_i = curva(año_i − ΔT). Con `permitir_cambio`, cada pirámide puede usar
    cualquiera de las dos configuraciones (como hizo Spence con Kefrén). La incertidumbre
    del año se convierte en incertidumbre angular con la pendiente local de la curva.
    """
    mejor = (np.inf, None, None)
    for dT in desfases:
        chi = 0.0
        conf = []
        valido = True
        for (nom, e, s, anio_bc, sa) in (piramides or PIRAMIDES):
            t = (1 - anio_bc) - dT                   # año astronómico de la orientación
            opciones = ["A_arriba", "B_arriba"] if permitir_cambio else [None]
            mejores = []
            for k in (opciones if permitir_cambio else ["A_arriba", "B_arriba"]):
                c = curvas[k]
                if np.all(np.isnan(c)):
                    continue
                m = np.interp(t, anios, c, left=np.nan, right=np.nan)
                if not np.isfinite(m):
                    continue
                pend = np.interp(t + 5, anios, c) - np.interp(t - 5, anios, c)
                var = s ** 2 + (pend / 10 * sa) ** 2
                mejores.append(((e - m) ** 2 / var, k))
            if not mejores:
                valido = False
                break
            if permitir_cambio:
                c2, k = min(mejores)
            else:
                c2, k = mejores[0] if len(mejores) == 1 else min(mejores)
            chi += c2
            conf.append(k)
        if not permitir_cambio and valido and len(set(conf)) > 1:
            # sin cambio permitido: obligar a una única configuración para todas
            chi = np.inf
            for k in ("A_arriba", "B_arriba"):
                c = curvas[k]
                tot = 0.0
                for (nom, e, s, anio_bc, sa) in (piramides or PIRAMIDES):
                    t = (1 - anio_bc) - dT
                    m = np.interp(t, anios, c, left=np.nan, right=np.nan)
                    pend = np.interp(t + 5, anios, c) - np.interp(t - 5, anios, c)
                    tot += (e - m) ** 2 / (s ** 2 + (pend / 10 * sa) ** 2)
                if np.isfinite(tot) and tot < chi:
                    chi, conf = tot, [k] * len(piramides or PIRAMIDES)
        if valido and chi < mejor[0]:
            mejor = (chi, dT, conf)
    return mejor
