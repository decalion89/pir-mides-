import math
import sys
from pathlib import Path

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "simulador"))

from piramide import geometria as g, muones as mu, rampas, obra, granito as gr, vacio as v  # noqa: E402
from piramide.fisica import Parametros, fuerza_arrastre, mu_desde_djehutihotep  # noqa: E402


# --- geometría ------------------------------------------------------------------------
def test_volumen_y_fracciones():
    assert g.VOLUMEN_TOTAL == pytest.approx(g.LADO_BASE ** 2 * g.ALTURA / 3)
    assert 2.55e6 < g.VOLUMEN_TOTAL < 2.62e6
    assert g.altura_para_fraccion(0.5) == pytest.approx(30.24, abs=0.1)
    assert sum(c.volumen for c in g.capas()) == pytest.approx(g.VOLUMEN_TOTAL)
    assert 2.1e6 < sum(c.bloques for c in g.capas()) < 2.5e6
    assert g.ANGULO_CARA == pytest.approx(51.85, abs=0.1)


def test_estructuras_coherentes_con_la_literatura():
    est = {c.nombre: c for c in g.estructuras_conocidas()}
    qc, kc = est["Cámara de la Reina"], est["Cámara del Rey"]
    assert abs(qc.centro[1]) < 2.0                        # la QC está en el eje E-O
    assert kc.centro[2] - kc.tam[2] / 2 == pytest.approx(43.0)
    assert -15 < kc.centro[1] < -8                        # la KC queda al sur del centro
    for c in g.estructuras_conocidas() + g.anomalias_detectadas():
        x, y, z = c.centro
        assert abs(x) < g.lado(z) / 2 and abs(y) < g.lado(z) / 2, c.nombre


def test_rayos_en_piramide_y_cajas():
    d = np.array([[0, 0, 1.0]])
    assert g.longitud_en_piramide(np.zeros(3) + [0, 0, 1e-9], d)[0] == pytest.approx(g.ALTURA)
    assert g.longitud_en_piramide(np.array([0, 0, 1e-9]), d, actual=True)[0] == pytest.approx(138.5)
    # desde fuera: rayo horizontal a z=10 que cruza la pirámide de este a oeste
    o = np.array([200.0, 0, 10.0])
    L = g.longitud_en_piramide(o, np.array([[-1.0, 0, 0]]))[0]
    assert L == pytest.approx(g.lado(10.0), rel=1e-6)
    caja = g.Caja("c", (0, 0, 50), (2, 10, 4))
    assert caja.longitud_en_rayos(np.array([0, -20.0, 50]), np.array([[0, 1.0, 0]]))[0] == pytest.approx(10)
    assert caja.longitud_en_rayos(np.array([0, 0, 0.0]), np.array([[0, 0, 1.0]]))[0] == pytest.approx(4)
    inclinada = g.Caja("i", (0, 0, 50), (2, 10, 4), inclinacion=26.0)
    # un punto 3 m al sur a lo largo del eje está 3·tan26 más alto
    p = np.array([[0, -3 * math.cos(math.radians(26)), 50 + 3 * math.sin(math.radians(26))]])
    assert inclinada.contiene(p)[0]


# --- muones ---------------------------------------------------------------------------
def test_flujo_vertical_conocido():
    # ~70 muones / (m2 s sr) por encima de 1 GeV en vertical
    assert mu.flujo_integral(np.array([1.0]), np.array([1.0]))[0] == pytest.approx(0.0070, rel=0.1)


def test_mas_roca_menos_muones():
    X = np.array([1e3, 1e4, 2e4, 3e4])
    f = mu.flujo_integral(mu.energia_minima(X), np.ones(4))
    assert np.all(np.diff(f) < 0)


def test_reproduce_ordenes_de_magnitud_de_scanpyramids():
    ref = g.estructuras_conocidas()
    det = g.detectores_publicados()["Cámara de la Reina (NE/H)"]
    r = mu.mapa(det, mu.Rejilla.cuadrada(-1, 1, -1, 1, 0.04), ref, [], area_m2=0.45, dias=98)
    assert 0.7 < r.cuentas_ref.sum() / 4.4e6 < 1.6       # Nagoya NE1: 4,4 millones de trazas
    bv = g.anomalias_detectadas()[1]
    pico = v.pico_suavizado(v.firma_qc([bv], dias=98))
    assert 0.05 <= pico <= 0.12                           # KEK: excesos de 5,2 % a 11 %


# --- construcción ---------------------------------------------------------------------
def test_djehutihotep_implica_rozamiento_bajo():
    assert 0.06 < mu_desde_djehutihotep(200) < mu_desde_djehutihotep(350) < 0.13


def test_fuerza_arrastre():
    assert fuerza_arrastre(1.0, 0.0, 0.2) == pytest.approx(0.2 * 9810)
    assert fuerza_arrastre(2.6, 0.1, 0.15) > fuerza_arrastre(2.6, 0.0, 0.15)


def test_integral_tramos_coincide_con_numerica():
    s, resta, mn = 0.1, 10.0, 8.0
    zs = np.linspace(0, 140, 200001)
    f = 1 / (s * np.maximum(g.lado(zs) - resta, mn))
    num = np.trapezoid(f, zs)
    assert rampas._integral_tramos(0, 140, s, resta, mn) == pytest.approx(num, rel=1e-4)


def test_rampa_recta_hasta_la_cima_es_inviable_por_volumen():
    assert rampas.RampaRecta().volumen_aux(g.ALTURA) > g.VOLUMEN_TOTAL


def test_con_la_suposicion_inicial_de_giro_un_solo_carril_no_llega():
    p = Parametros()
    assert obra.simular(rampas.Zigzag(), p).anios > 27
    assert obra.simular(rampas.Interna(), p).anios > 27
    assert obra.simular(rampas.Aristas(), p).anios < 20


# --- granito y Gran Vacío -------------------------------------------------------------
def test_contrapeso_crece_con_la_masa_y_cabe_en_un_vacio_como_el_observado():
    a = gr.contrapeso_necesario(25, 0.49, 0.1)
    b = gr.contrapeso_necesario(60, 0.49, 0.1)
    assert b > a > 25
    assert gr.contrapeso_necesario(60, 0.49, 0.1, eficiencia_reenvio=0.7) < gr.capacidad_galeria()


def test_rampa_interna_dentro_de_la_piramide():
    for c in v.rampa_interna_houdin():
        x, y, z = c.centro
        assert max(abs(x), abs(y)) < g.lado(z) / 2


def test_hipotesis_publicadas_reproducen_la_senal_de_2017():
    H = v.hipotesis_base()
    for h in H[:2]:
        assert 0.05 <= v.pico_suavizado(v.firma_qc(h.cajas())) <= 0.12


def test_hibridos_no_duplican_tramos():
    p = Parametros()
    cat = {m.clave: m for m in rampas.catalogo()}
    rz = cat["recta+zigzag"].segmentos(100.0, p)
    assert sum(L for L, s in rz if s > 0) == pytest.approx(100.0 / 0.10)
    rp = cat["recta+palancas"].segmentos(100.0, p)
    assert sum(L for L, s in rp if s > 0) == pytest.approx(45.0 / 0.10)
    assert cat["recta+palancas"].elevaciones(100.0, p) == pytest.approx(55.0 / p.altura_hilada)


# --- fase 2: robustez y huella de las aristas -----------------------------------------
from piramide import robustez as rb, aristas_muones as am  # noqa: E402


def test_chi2_perfilado_absorbe_normalizacion_y_gradiente():
    rng = np.random.default_rng(0)
    tx, ty = rng.uniform(-0.7, 0.7, 500), rng.uniform(-0.7, 0.7, 500)
    M = rng.uniform(5e3, 2e4, 500)
    datos = M * (1.03 + 0.02 * tx - 0.01 * ty)
    assert rb.chi2_perfilado(M, M[None, :], tx, ty)[0] == pytest.approx(0, abs=1e-6)
    chi_perf = rb.chi2_perfilado(datos, M[None, :], tx, ty)[0]
    chi_sin = float(np.sum((datos - M) ** 2 / (M + (0.02 * M) ** 2)))
    assert chi_perf < 0.05 * chi_sin


def test_huella_de_aristas_crece_con_el_deficit_de_densidad():
    z = [am.significacion(dd, dias=30)["Z"] for dd in (-0.02, -0.1)]
    assert z[1] > 3 * z[0] > 0


def test_carriles_dentro_de_la_piramide_actual():
    for c in am.carriles_aristas(-0.1):
        x, y, z = c.centro
        assert max(abs(x), abs(y)) + c.tam[0] / 2 < g.lado(z) / 2 - 0.5 + 1e-9


# --- fase 3: reanálisis de los datos publicados de 2017 -------------------------------
from piramide import reanalisis as ra, reanalisis_emulsiones as rem  # noqa: E402


def test_datos_kek_extraidos():
    d = ra.cargar()
    assert d["val"].size == 679
    assert set(d["det"]) == {"H1", "H2"}
    assert np.allclose(d["dx"], np.round(d["dx"]), atol=0.15)      # canales casi enteros: calibración correcta
    assert 1.05 < d["val"].max() < 1.2


def test_la_galeria_calibra_las_emulsiones_como_scanpyramids():
    x1, x2, _ = rem.calibrar(xs1=np.arange(12.0, 14.01, 0.5), xs2=np.arange(2.2, 3.81, 0.4))
    assert abs((x1 - g.X_PASAJES) - 5.8) < 0.8      # publicado: NE1 5,8 m al este del eje
    assert abs((g.X_PASAJES - x2) - 4.5) < 0.8      # publicado: NE2 4,5 m al oeste


def test_reanalisis_kek_pide_un_vacio():
    r = ra.Reanalisis()
    con = r.chi2(ra.Corredor(8.9, 21.0, 52.0, 45.0, 2.7, ancho=3.6, inclinacion=18))
    assert con < r.chi2_sin_vacio() - 500


# --- fase 4: física del giro ----------------------------------------------------------
from piramide import giro  # noqa: E402


def test_fisica_del_giro():
    c = giro.comparar()
    assert 0.5 < c["pivote_min"] < 3.0
    assert c["poste_ocupacion_min"] < 0.5
    assert 1.3 < c["poste_factor_equipo_mu02"] < c["poste_factor_equipo_mu04"] < 2.0


def test_con_giros_fisicos_una_rampa_unica_va_justa_pero_es_posible():
    cat = {m.clave: m for m in rampas.catalogo()}
    p = Parametros()
    p.tecnica_giro = "pivote"
    a = obra.simular(cat["zigzag"], p).anios
    assert 12 < a < 27


# --- fase 5: cota de Cramér–Rao -------------------------------------------------------
from piramide import cota_informacion as ci  # noqa: E402


def test_la_camara_del_rey_mejora_la_cota_de_inclinacion():
    P = rb.puestos_estandar(dias_kc=60.0)
    v0 = (17.0, 63.0, 32.0, 6.0, 2.0, 13.0)
    F_qc = ci.fisher(P["QC"], v0)
    F_kc = ci.fisher(P["KC"], v0)
    assert np.all(np.linalg.eigvalsh(F_qc) > 0)
    s_qc = np.sqrt(np.linalg.inv(ci.combinar(F_qc))[5, 5])
    s_ambos = np.sqrt(np.linalg.inv(ci.combinar(F_qc, F_kc))[5, 5])
    assert s_ambos < 0.6 * s_qc


# --- fase 6: astronomía de los canales ------------------------------------------------
from piramide import astronomia as astro  # noqa: E402


def test_thuban_era_la_estrella_polar_hacia_2800_aC():
    cat = astro.cargar(vmax=4.0)
    j = [i for i, n in enumerate(cat.nombre) if "Alp Dra" in n][0]
    assert astro.declinacion(cat, -2799)[j] > 89.7
    assert abs(astro.declinacion(cat, 2000)[j] - 64.38) < 0.02


def test_declinacion_objetivo_canal_sur_del_rey():
    assert abs(astro.declinacion_objetivo(45.0, "S") - (-15.04)) < 0.05


from piramide import orientacion as orient  # noqa: E402


def test_reproduce_la_correccion_de_spence_con_kochab_y_mizar():
    cat = astro.cargar(vmax=3.5)
    i = lambda s: [j for j, n in enumerate(cat.nombre) if s in n][0]
    anios = np.arange(-3000, -1999, 5.0)
    c = orient.curva_par(cat, i("Bet UMi"), i("Zet UMa"), anios)
    chi, dT, _ = orient.ajustar_par(anios, c, False)
    assert -130 < dT < -60          # Spence: Keops ~2467-2480 a. C., unos 100 años más tarde


from piramide import luna  # noqa: E402


def test_presupuesto_energetico_de_la_gran_piramide():
    p = luna.gran_piramide()
    E_GWh = p.energia_total_J() / luna.KWH / 1e6
    assert 2.0 < E_GWh < 3.0
    assert p.energia_arrastre_J() > 3 * p.energia_elevar_J()
