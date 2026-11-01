---
title: "Rate blindness: physical-limit audits of six high-profile archaeometric claims"
author: "[AUTHOR NAME AND AFFILIATION — to be completed] · Contact: labix7@gmail.com · Code and data: [REPOSITORY URL]"
date: "Draft v3 (revised after an independent adversarial review), 1 November 2026"
---

# Abstract
Archaeological science often moves from a measured quantity to a mechanism without checking whether the mechanism can run at the required *rate*. We call this rate blindness, and we test it on six widely publicised claims. In each case we compute the relevant transport or intake limit from the paper's own geometry and parameters, and propagate uncertainties by Monte Carlo.

**Four claims fail the check:**

1. **Qin Shi Huang tomb** (Zhao et al. 2020). The mercury outflux measured by lidar exceeds the maximum steady diffusive flux from a mercury-saturated chamber, including lateral spreading, by 42× (5.6–520). If the source is the tomb, it must exchange air through open paths, as the authors themselves suggest. This is conditional on the measured excess being real (2.4–3.6σ per scan).
2. **Herculaneum "glass brain"** (Giordano et al. 2025). The ~1000 K s⁻¹ cooling inferred from calorimetry is 600–12,500× faster than conduction allows for material cooling inside a skull, which is where the fragments were found. With the authors' own kinetics, the material would also soften in under a second at the upper burial temperature.
3. **Roman lead and IQ** (McConnell et al. 2025). The air-to-blood regression returns *total* blood lead for US children in 1988–94. It was applied as an *increment* above a separately added baseline, about 35× below its calibration range. An intake budget covering inhalation, cereals, vegetables, cisterns and soil gives +0.7 µg dl⁻¹ and about 1 IQ point, against 2.4 µg dl⁻¹ and 2.5–3 points in the paper (factor 3.4, range 1.5–7.5).
4. **Tikal reservoir mercury** (Lentz et al. 2020). The sediment mercury that led to "seriously compromised" drinking water would give water at ~17% of the WHO guideline, even for the most contaminated samples.

**Two claims are conditional rather than failed:**

5. **Djoser hydraulic lift** (Landreau et al. 2024). It needs ≥5–20 floods per year or near-perennial flow. With episodic desert floods it receives only 7–34% of its demand.
6. **Tikal zeolite filter** (Tankersley et al. 2020). A slow, pathogen-removing filter is feasible (34–200 m²) only if water ponded in front of it.

Each case comes with a falsifiable test.

![Mismatch between each claim and the corresponding physical limit for the four claims that fail (median and 90% Monte Carlo range). The two conditional cases are discussed in the text.](fig1_rate_blindness.png)

# 1. The pattern
Archaeological science often argues from *stocks*: how much mercury is in a tomb, what glass-transition temperature a material shows, how much water a catchment provides, how much lead a sediment holds. But a mechanism also needs a *flux* on the stated time scale, and every flux has a ceiling:

- diffusion is limited by D·ΔC·S, with S the geometric shape factor;
- conductive cooling is limited by k/(ρc·L²);
- a reservoir fed by episodic events is limited by storage between events;
- human uptake is limited by intake rates and partitioning.

The check is cheap. Identify the flux the mechanism requires, compute its ceiling with the paper's own geometry, and report the ratio.

# 2. Qin Shi Huang: a tomb that is probably not sealed
**Claim.** Zhao et al. (Sci. Rep. 10, 10414, 2020) measured atomic mercury above the mound by differential-absorption lidar. They estimated an outflux of ≈5×10⁻⁸ kg s⁻¹ and wrote that mercury "may be escaping through cracks". The chamber ceiling lies ≈30 m below the surrounding ground, under a ≈50 m mound.

**Test.**

- Air in contact with liquid mercury saturates at C_sat ≈ 9.4 mg m⁻³ (15 °C).
- Steady diffusion through 30–80 m of compacted loess uses the Millington–Quirk diffusivity (porosity 0.30–0.45, water saturation 0.3–0.8). Lateral spreading is included through the shape factor of a disk buried in a semi-infinite medium.
- The result is a maximum flux 42× below the measured one (5.6–520). Diffusion suffices in 0.02% of 2×10⁵ draws. Typical emission from the mound soil (~190 ppb) is 9–220× too small.
- An open air path, on the other hand, could suffice. The required exchange is ~460 m³ of saturated air per day.

**Caveats.**

- Barometric pumping supplies this robustly only if much of the 140 × 110 × 30 m underground palace is open space.
- The excess concentration is 2.4–3.6σ per scan and was absent at the windy third site.

**Predictions (pre-registered).**

- Emission rises when barometric pressure falls.
- Soil-gas mercury increases with depth.
- Winter emission exceeds summer emission.
- A night-by-night ranking for the 2016 campaign, built from station pressure data.

# 3. Herculaneum: a cooling rate heat cannot deliver inside a skull
**Claim.** Giordano et al. (Sci. Rep. 15, 5955, 2025) measured calorimetric onsets of 420 °C at 0.42 K s⁻¹ and 510 °C at 1000 K s⁻¹ on glassy fragments "sampled intact, directly from within the skull". They inferred a natural fictive temperature T_f ≈ 510 °C and cooling "at rates comparable with our experimental 1000 K s⁻¹" after a short-lived ash cloud.

**Test.**

- *Cooling.* Transient conduction in a heated head, with convective and radiative loss, gives 0.1–1.7 K s⁻¹ inside the cranium.
- *Fragmentation.* The authors propose fragmentation into "sub-centimetric pieces … favouring the heat exchange". This helps only if the fragments were exposed to open air: free fragments reach 17–720 K s⁻¹, which would imply T_f = 460–506 °C. Enclosed fragments still lose heat through the skull. The paper itself invokes the skull's protection during heating.
- *Fictive temperature.* At in-skull rates, the authors' kinetics (E = 390 kJ mol⁻¹) give T_f ≈ 405–440 °C. This overlaps the 315–465 °C burial deposits, the criterion the authors used to reject 420 °C.
- *Survival.* With the same E, the material softens in 0.4 s at 465 °C and would anneal within minutes to hours at 315–350 °C.
- *Heating.* Drying and heating the brain above 510 °C needs ≥3–40 min of full exposure.

**Prior work.** Morton-Hayward et al. (2020) questioned the temperatures and the survival of fatty acids in the first report; they did not address cooling rates.

**Test proposed.** Upscans after the first one show no events. The natural T_f should therefore be measured from first-scan onsets on fresh fragments at several heating rates, compared with reference tissue glasses of known cooling history.

# 4. Roman lead: a regression's intercept counted as pollution
**Claim.** McConnell et al. (PNAS 122, e2419630121, 2025) model +1.04 ng m⁻³ of air lead over Europe. They apply BLL = exp[1.932 + 0.140 ln(PbA)] from Richmond-Bryant et al. (2014; NHANES III, unadjusted). They obtain a 2.0–5.3 µg dl⁻¹ "enhancement", which they add to a 1 µg dl⁻¹ Neolithic baseline, and hence a deficit of 2.5–3 IQ points.

**Test.**

- *What the regression predicts.* It gives the total blood lead of children exposed to all 1988–94 sources: with almost clean air it already predicts 1.6 µg dl⁻¹.
- *Extrapolation.* Roman air is ~35× below the calibration median (0.036–0.037 µg m⁻³). At 1 ng m⁻³ the implied slope is 355 µg dl⁻¹ per µg m⁻³, whereas Richmond-Bryant et al. report 15.3–16.5 at low air lead.
- *Differencing the regression.* Taking the difference against a natural background gives +1.0 µg dl⁻¹ and 1.4 points, and this is still an extrapolation.
- *Intake budget.* An independent budget gives +0.71 µg dl⁻¹ (0.32–1.6) and 1.0 points (0.5–1.9). It covers inhalation and deposition on cereals (Roman grain yields) and vegetables, cistern rainwater and soil, using the paper's own >500 kt deposited and child slope factors.

The effect is plausible, but 2–3× smaller than claimed for the European average.

# 5. Tikal: sediment mercury is not drinking-water mercury
**Claim.** Lentz et al. (Sci. Rep. 10, 10316, 2020) report sediment mercury above the "toxic effect threshold" of 1 µg g⁻¹, a criterion for benthic organisms. They conclude that the reservoirs were "seriously compromised as sources of drinking water" and that the elite were "fed foods laced with mercury at every meal".

**Test.**

- Mercury reaches the water dissolved (sediment–water partitioning, log K_d = 4.5–6) and on suspended particles (5–100 mg L⁻¹).
- For the most contaminated sediments (10–30 µg g⁻¹), the water carries ~1.0 µg L⁻¹ (0.26–2.4). That is ~17% of the WHO guideline of 6 µg L⁻¹, which no draw exceeds.
- Intake at 3–5 L day⁻¹ is ~3% of the WHO tolerable intake.
- The cyanobacteria evidence in the same paper is independent and not assessed here, nor is methylmercury in fish.

# 6. Conditional cases
**Djoser** (Landreau et al., PLOS ONE 19, e0306690, 2024). We ran a daily water balance with the authors' storage elements, demand, evaporation and infiltration. The lift receives 7–34% of its demand with ≤2 floods per year. It receives ~80–100% with frequent floods or near-perennial flow, which the authors propose. O. Siegel had objected qualitatively that the basin "could not have held enough water from occasional rains". Our result makes that objection quantitative and shows it depends on the flood regime. *Test:* do 3rd-Dynasty sediments in the Abusir wadi show frequent or continuous flow, or isolated floods separated by aeolian layers?

**Tikal filter** (Tankersley et al., Sci. Rep. 10, 18021, 2020). Passing the reservoir volume (58,000 m³ yr⁻¹) through a slow filter needs ~550–2,300 m² if storm water arrives directly. It needs only ~34–200 m² if water ponds behind the dry-laid walls of the authors' own scheme. Seasonal drying of the biological layer remains a qualitative concern.

# 7. Discussion
In four of six claims, the step from measurement to mechanism fails a simple rate or intake check by factors of 3 to over 1,000. In two it reveals a hidden condition that the papers do not state.

We do not claim this is the typical rate. The cases were chosen because they looked vulnerable. Five further claims we screened passed or could not be decided with public data:

- the ScanPyramids Big Void;
- Teotihuacan muography;
- Mt Echia muography;
- the Hierapolis Plutonion;
- X-ray dating of the Turin Shroud.

What the exercise shows is that the check is cheap, and that it changes conclusions often enough in prominent papers to be worth making routine.

Our own drafts illustrate the point. An independent adversarial review of this work found:

- a one-dimensional diffusion bound that understated lateral flux by 3–6×;
- a filter target set at all runoff rather than the reservoir volume;
- a flood regime that excluded the authors' own scenario;
- a misattributed citation.

All of these are corrected here. Rate checks need the same scrutiny as the claims they test.

# Data and code
All calculations, Monte Carlo inputs and figures are open:

- Qin: `simulador/qin_mercurio.py`, `simulador/qin_presion_prerregistro.py`;
- Herculaneum: `simulador/herculano_vidrio.py`;
- Djoser: `simulador/saqqara_balance_hidrico.py`;
- Roman lead: `simulador/plomo_romano.py`;
- Tikal: `simulador/tikal_filtro.py`, `simulador/tikal_mercurio.py`;
- results: `resultados/42–48_*.json`.

The pre-registered predictions are P15 and P16 in `PREDICCIONES.md`.

# References
- Giordano, G. et al. Unique formation of organic glass from a human brain in the Vesuvius eruption of 79 CE. *Sci. Rep.* 15, 5955 (2025).
- Landreau, X. et al. On the possible use of hydraulic force to assist with building the step pyramid of Saqqara. *PLOS ONE* 19, e0306690 (2024).
- Lentz, D. L. et al. Molecular genetic and geochemical assays reveal severe contamination of drinking water reservoirs at the ancient Maya city of Tikal. *Sci. Rep.* 10, 10316 (2020).
- McConnell, J. R. et al. Pan-European atmospheric lead pollution, enhanced blood lead levels, and cognitive decline from Roman-era mining and smelting. *PNAS* 122, e2419630121 (2025).
- Millington, R. J. & Quirk, J. P. Permeability of porous solids. *Trans. Faraday Soc.* 57, 1200–1207 (1961).
- Morton-Hayward, A. L. et al. A conscious rethink: why is brain tissue commonly preserved in the archaeological record? *STAR* 6, 87–95 (2020).
- Moynihan, C. T. et al. Dependence of the fictive temperature of glass on cooling rate. *J. Am. Ceram. Soc.* 59, 12–16 (1976).
- Richmond-Bryant, J. et al. The influence of declining air lead levels on blood lead–air lead slope factors in children. *Environ. Health Perspect.* 122, 754–760 (2014).
- Bower, B. Was Egypt's first pyramid built with hydraulics? *Science News*, 5 August 2024 (O. Siegel quoted).
- Tankersley, K. B. et al. Zeolite water purification at Tikal, an ancient Maya city in Guatemala. *Sci. Rep.* 10, 18021 (2020).
- WHO. Mercury in drinking-water (chemical fact sheet, 2022).
- Zhao, G. et al. Mercury as a geophysical tracer gas — emissions from the emperor Qin tomb in Xi'an studied by laser radar. *Sci. Rep.* 10, 10414 (2020).
