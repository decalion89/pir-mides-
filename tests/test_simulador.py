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


def test_un_solo_carril_con_giros_no_llega_a_tiempo():
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
