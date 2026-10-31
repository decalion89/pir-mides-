---
title: "Khufu's Big Void, ramp logistics and the pyramid alignments: an open reanalysis with pre-registered tests"
author: "[AUTHOR NAME(S) AND AFFILIATION — to be completed before submission] · Proyecto Pirámides, https://github.com/decalion89/pir-mides-"
date: "Preprint draft v2, 31 October 2026"
---

# Abstract

We release an open, reproducible framework (code, digitized data, 28 automated tests) for three long-debated questions about the Great Pyramid of Khufu: what the "Big Void" detected by muography in 2017 is, how 2.3 million blocks were raised, and what the four "star shafts" and the pyramids' orientation to north encode.

**(i) Forward model and validation.** We model muon transmission (Reyna spectrum, continuous energy loss, ray tracing through a reconstructed internal geometry). It reproduces the published ScanPyramids results to within a factor ~2 in significance:

- track counts: 5.3 vs 4.4 million emulsion tracks;
- excess: 8.6 % vs 5.2–11 %;
- significance: 17σ vs 13.7σ inside, 2.8σ vs 5.8σ outside.

**(ii) Reanalysis of the published figures.** We digitize the 679 KEK hodoscope points and the Nagoya emulsion profiles from the 2017 paper. Calibrating only on the simulated Grand Gallery, our geometry recovers the published emulsion positions to within 0.2 m. The void lies close to the Grand Gallery axis, but its height and cross-section depend on the data set:

| Data | Centre height | Cross-section |
|---|---|---|
| Emulsions | 61–62.5 m | ~19–21 m² |
| KEK + emulsions (joint fit) | 56–59 m | ~9–11 m² |

The inclination cannot be determined robustly. The emulsions prefer shallow angles, but this fails a leave-one-slice-out test. KEK prefers inclined geometries, but places the void ~1.7 m east of the axis. Under any tested shape (straight, two-segment, two-level) the two data sets are mutually inconsistent (Δχ² ≈ 78 for ~7 shared parameters), which indicates an unresolved systematic.

**(iii) Simulation study of future measurements.** With one simulated detector in the Queen's Chamber, four candidate void geometries are nearly degenerate (2.3–2.8σ); a loose-fill zone is separable. A Cramér–Rao calculation shows that no analysis of the full 2017 stereo emulsion data could measure the inclination better than ±2.5–3.3°; this is a local, model-dependent lower bound. In blind tests that are optimistic by construction (the injected systematics match the fitted nuisance model), adding a ~1 m² detector in the publicly accessible **King's Chamber** for 60 days identifies the true hypothesis in 96–98.5 % of trials under moderate physics perturbations, and in 82.5 % under a grossly wrong muon spectrum.

**(iv) Ramp logistics.** In a layer-by-layer flow model, corner turns of loaded sledges are the key uncertainty. A mechanical estimate gives 0.8–2.8 min per corner for stop-and-pivot, dominated by an assumed stop/restart overhead, or 0.3 min with a rope-redirecting post at the cost of 1.4–1.9× larger crews. With these values a single cornered ramp is possible but tight (median 20–23 years), while parallel systems leave ample margin. The corner time must be measured; we propose a 2–3-day experiment.

**(v) Shafts and orientation.**

- *Shafts.* With the Yale Bright Star Catalogue and IAU 2006 precession, the two King's Chamber shafts point to their proposed stars (Alnitak, Thuban) at dates 2.4σ apart, and at V ≤ 3.0 the measured angles produce no four-star coincidence while 27 % of random angle sets do. The rational slopes n/11 that the angles fit are not significant after a look-elsewhere correction (p = 16 %).
- *Orientation.* With Spence's (2000) data and only observable star configurations, no star pair explains the Fourth-Dynasty orientation errors without a configuration switch for Khafre. With that switch, Kochab–Mizar is the best pair in a plausible chronology window and reproduces Spence's date (Khufu aligned ~2478 BC). However, a generic linear drift with Khafre reflected fits equally well, and Unas does not fit. The data are compatible with, but do not establish, astronomical dating.

**Self-corrections.** We document four errors in our own earlier analyses and how they were caught:

1. a digitization artefact that produced a spurious "18° inclination at 4–6σ";
2. an untested corner-time assumption that had produced "single ramps are impossible";
3. wrong chronology inputs and unobservable stars in a first orientation study;
4. outdated void dimensions.

Predictions are registered in git before any new measurement.

# 1. Introduction

ScanPyramids reported a void of length ≥30 m above the Grand Gallery, with a cross-section "comparable to the Grand Gallery" (Morishima et al. 2017). Its orientation, horizontal or inclined, was left open, and so was its function. Proposals include a structural relieving space and a construction gallery for counterweights (Houdin).

Equally debated are the method used to raise the blocks (straight, zigzag, spiral, internal or edge-integrated ramps; levers), the purpose of the shafts (Trimble 1964; Badawy 1964; Bauval 1993), and whether the pyramids' orientation errors can date them (Spence 2000; Belmonte 2001).

We treat these questions quantitatively, test our own claims adversarially, and release everything.

# 2. Methods (summary; full details in docs/06–16 of the repository)

**Geometry.** The pyramid is a convex solid (base 230.33 m, original height 146.6 m). The current truncated shape is used for muography. Chambers and passages are oriented boxes reconstructed from Petrie (1883) and Maragioglio & Rinaldi (±1–2 m).

**Muon model.**

- Spectrum: Reyna (2006), joined to Gaisser (1990) above 2 TeV.
- Energy loss: E_min(X) = E₀ + (a/b)(e^{bX} − 1), with standard-rock a and b. This approximation neglects the rise of ionization loss and calcite-specific constants.
- χ²: includes a 2 % per-bin systematic and angular smearing. In the robustness studies it also profiles normalization, two angular gradients and two spectral terms. Directions more than 70° from the zenith are excluded.
- Realism factor: a factor of 0.5 is applied to model significances. It is calibrated on one published number (Queen's Chamber), and the outside-detector comparison suggests the model is instead ~2× pessimistic there.

**Digitization.**

- KEK Extended Data Fig. 4: PDF vector graphics, axes calibrated from major ticks. The recovered Δx values are integers to within 0.15.
- Nagoya Extended Data Fig. 2: raster image. Data crosses are found as intersections of horizontal and vertical colour runs. Where a bin has two candidates (data cross and overlaid fitted curve), the candidate with the longer error bar is kept.

**Construction model.** Layer by layer (210 courses), the daily rate is the minimum of three capacities:

- lane capacity (sledge spacing and corner occupancy);
- placement area;
- labour (Little's law).

A Monte Carlo runs over 22 uncertain parameters. Friction is calibrated on the Djehutihotep painting (μ ≈ 0.06–0.11 for 200–350 N per man).

**Astronomy.**

- Catalogue: Yale BSC5 (Hoffleit & Warren 1991), with proper motions.
- Precession: IAU 2006 (Capitaine et al. 2003).
- Refraction: Bennett.
- Site: meridian transit at Giza (φ = 29.979°).
- Orientation fits: for each star pair, the azimuth at which both stars share a plumb line near north, with both at least 5° above the horizon.

# 3. Validation against published results

| Quantity | Model | Published |
|---|---|---|
| Emulsion NE1 tracks (98 d, 0.45 m²) | 5.3 × 10⁶ (square \|tanθx,y\| < 1) | 4.4 × 10⁶ (acceptance to \|tanθ\| ≈ 1.3) |
| Big Void excess, Queen's Chamber | 8.6 % (smoothed) | 5.2–11 % (KEK slices) |
| Big Void significance, Queen's Chamber | 17σ (with ×0.5 factor) | 13.7σ (NE1) |
| Big Void significance, outside the north face | 2.8σ (with ×0.5 factor) | 5.8σ (CEA) |
| Emulsion E–W offsets from the Grand Gallery axis, recovered from the simulated Gallery alone | NE1 +5.7 m, NE2 −4.3 m | +5.8 m, −4.5 m |

# 4. Reanalysis of the published 2017 data

The void lies close to the Grand Gallery axis:

- emulsions: x = 7.5 m (axis 7.3 m);
- KEK alone: ~1.7 m east;
- joint fit: 7.1–7.3 m.

Its centre height and cross-section depend on the data set: emulsions 61–62.5 m and ~19–21 m²; joint fit 56–59 m and ~9–11 m²; KEK alone 52–54 m.

Inclination profile (σ against each angle, errors rescaled by χ²/ndf):

| Data | 0° | 10° | 20° | 26° | 35° |
|---|---|---|---|---|---|
| Emulsions (nominal) | 0.4 | 0.9 | 2.2 | 2.8 | 3.9 |
| Emulsions, without the southern slice | 1.6 | 0.5 | 0.1 | 0.4 | 1.0 |
| Emulsions, Grand Gallery residual free | 2.4 | 0.3 | 1.4 | 2.4 | 3.8 |
| KEK alone (detector position free; best at the +1 m grid edge) | 4.3 | 2.5 | 1.0 (18°) | 0.0 | 1.8 |
| Joint fit | 4.0 | 1.3 | 0.0 (18°) | 0.7 | 4.0 |

The joint fit is not trusted: the two data sets are inconsistent under a common straight corridor (χ² 807 vs ≈ 729 for the separate minima, ~7 shared parameters), and the tension is unchanged for two-segment and two-level shapes. We attribute it to an unresolved systematic, most plausibly the KEK normalization to the authors' own simulation of known structures or the hodoscope geometry. Only the original maps can resolve it.

**Our own error.** A first version reported an 18° inclination at 4–6σ, robust to five variations. A leave-one-slice-out test removed it. We traced it to 26 of 396 bins in which the overlaid fitted curve had been digitized instead of the data cross.

# 5. Simulation study: what a new measurement could decide

**Hypotheses.** H1 is a horizontal corridor; H2 a corridor inclined at 26°; H3 a 26° counterweight gallery joined to the relieving chambers; H4 a loose-fill zone; H5 stacked low chambers.

**Fitting.** Each hypothesis is fitted to mimic the expected Queen's Chamber view of a simulated reference void (a 1.6 × 8 m box at z = 63 m, H1). It is *not* fitted to the 2017 data. Two exclusions are therefore relative to this simulation:

- a relieving void hugging the Grand Gallery roof (29σ);
- an open internal spiral ramp of Houdin's type, which would produce an expected 17–32σ ring in the Queen's Chamber acceptance.

**Results.** With one simulated Queen's Chamber detector, H1, H2, H3 and H5 are within 2.3–2.8σ of each other, while H4 is separable at 11σ.

**Joint fit and blind tests.** The joint fit covers the Queen's Chamber plus a new position, with 225 variants per hypothesis (±3 m, cross-section ×0.75–1.25) and profiled systematics. The blind trials perturb the physics (flux ±10 % and index ±0.05; limestone 2.35 g/cm³; known chambers displaced by 1 m), but they remain **optimistic by construction**:

- the injected systematics have the same form as those profiled in the fit;
- the true geometries are drawn inside the library range and only from H1–H5.

Within these limits, 60 days with 1 m² in the King's Chamber (25 % effective exposure) identify the true hypothesis in 96–98.5 % of trials, and in 82.5 % with a grossly wrong spectrum (Gaisser outside its validity). The counterweight interpretation (H3) is the most sensitive to flux mismodelling. We pre-register four conditions before H3 may be claimed:

1. ≥5σ against H2;
2. open-sky flux calibration;
3. laser-scan geometry;
4. confirmation from a second position.

Quoted "margins" are √(median Δχ²) between non-nested hypotheses, not Gaussian significances.

**Cramér–Rao lower bound.**

| True void (z = 63 m, 6 × 2 m) | 2017 stereo (NE1 + NE2) | + King's Chamber 60 d |
|---|---|---|
| Horizontal | σ(incl.) ≥ 2.5° | ≥ 1.1° |
| Inclined 13° | ≥ 3.3° | ≥ 1.6° |
| Inclined 26° | ≥ 3.0° | ≥ 1.9° |

The bound is local and model-dependent: x and the density contrast are fixed, the nuisances carry Gaussian priors, and the 2 %/bin systematic is optimistic compared with the real χ²/ndf. Blind tests with the stereo configuration give 92 % accuracy with ~3σ median margins for 2017 alone, and 98.5 % when King's Chamber data are added. This is a forecast for the *full* 2017 maps, which our figure-based reanalysis (Section 4) does not reach.

**Campbell's Chamber** adds no information for a horizontal void: the void lies at the detector's height, in directions removed by the zenith cut. The King's Chamber is therefore the robust choice.

# 6. Ramp logistics and the corner bottleneck

Rotating a 2.6 t sledge needs ~2.4 kN·m. The pivot itself takes seconds; the 0.8–2.8 min per corner is dominated by an *assumed* 30–150 s stop/restart overhead. A rope-redirecting post would reduce corner occupancy to ~0.3 min, at a capstan cost of e^{μ_c π/2} = 1.4–1.9 on crew size. The Khufu-era Hatnub ramp shows posts used for hauling on a *straight* ramp; posts at corners are an extrapolation.

| Model | Median years | Share finishing in ≤ 27 years |
|---|---|---|
| Single cornered ramp (zigzag, spiral or internal) | 20–23 | 74–85 % |
| Four edge ramps | 6 | 100 % |
| Straight ramp to 45 m + zigzag | 12–13 | 100 % |
| Straight ramp to 45 m + levers | 8 | 100 % |

An earlier version assumed 2–15 min per corner and concluded that single ramps were impossible; we withdraw it. Under that broad prior, corner time dominated the variance (rank correlation 0.97), which is why it must be measured.

Proposed test: a 2.5 t sledge on wet tafla, with a 90° corner on a 4 m platform. The pre-registered thresholds are:

- stop-and-pivot ≤ 2.1 min per corner, or
- post friction μ_c ≤ 0.4,

either of which implies a single ramp could finish within the reign.

# 7. The "star shafts"

| Shaft | Measured (Gantenbrink) | Proposed star | Date it culminated along the shaft |
|---|---|---|---|
| King's south | 45.0° ± 0.2 | Alnitak | 2497 ± 41 BC |
| King's north | 32.47–32.6° (± 0.3) | Thuban | 2338 ± 53 BC (or 3257 BC) |
| Queen's south | 39.61° (± 1, Gantenbrink quotes ± 2) | Sirius | 2369 ± 333 BC |
| Queen's north | ~39.1° (upper part unmeasured) | Kochab | 2369 ± 446 BC |

**Dates.** Sirius and Kochab are compatible with Khufu's reign (~2589–2566 BC) because their angles are poorly constrained; Alnilam also fits the King's south shaft within the reign. The real tension is between the two King's Chamber shafts (2.4σ), which rests on the adopted 0.3° uncertainty.

**Chance.** At V ≤ 3.0, the measured angles produce no simultaneous four-star coincidence, while 27 % of random angle sets do. At V ≤ 3.7 (needed to include Thuban), 59 % of random sets do.

**Rational slopes.** The angles fit slopes n/11 (11/11, 7/11, 9/11; the face is 14/11), but after look-elsewhere over denominators 5–16 the chance probability is 16 %. The result also depends on the adopted σ of the Queen's south shaft, and 9/11 corresponds to an unusual seked (8 4/9 palms). We therefore make no claim that either explanation is preferred.

A ±0.2° laser survey would discriminate: Kochab at Khufu's reign needs 39.8–39.9°, while 9/11 gives 39.29°.

# 8. Orientation to north

**Data.** Spence (2000), Table 1: Meidum −20.6′, Bent −17.3′, Red −8.7′, Khufu −3.4′, Khafre −6.0′, Menkaure +12.4′. Dates follow von Beckerath, with Sneferu after Stadelmann, and the alignment is taken in regnal year 2.

**Pairs.** We consider 219 observable star pairs (V ≤ 3.5, both stars at least 5° up) and fit a chronology shift ΔT between −500 and +500 years.

| Model | χ² (6 pyramids) | ΔT |
|---|---|---|
| No drift | 3320 | — |
| Any pair or a line, same configuration for all | ≥ 199 | — |
| η UMa + Kochab, with switch | 11.8 | +472 yr (excluded by radiocarbon) |
| **Kochab + Mizar, with switch (Spence)** | **12.3** | **−74 yr (Khufu aligned ~2478 BC)** |
| β UMa + η Dra, with switch | 22.2 | −2 yr |
| Line with Khafre reflected | 11.4 | — |

**Retrodiction for the Fifth Dynasty.** With Kochab–Mizar and the switch:

- Sahure: predicted ±29′, measured −23′ ± 10: consistent;
- Neferirkare: predicted ±33′, measured +30′ ± 10: consistent;
- Unas: predicted ±68′, measured +17.1′: inconsistent.

The orientations support a stellar method and are compatible with Spence's pair and date, but a generic drift fits as well. Astronomical dating therefore remains conditional on the configuration-switch rule and on the chronology window.

# 9. Pre-registered predictions (full list in PREDICCIONES.md, dated in git)

1. A ~1 m² detector in the King's Chamber separates the hypotheses in ≤ 2 months.
2. A stereo analysis of the full 2017 NE1 + NE2 maps prefers the true shape at ~2–3σ and constrains the void height to ≲ 1 m.
3. A new measurement finds the void centre within ±2 m of the Grand Gallery's vertical plane, at 52–63 m height, with a cross-section of 9–21 m².
4. If edge-integrated ramps were used and back-filled ≥ 0.1 t/m³ (~4.5 %) lighter than the core, an external 1 m² detector sees helical bands at 5σ in ~300 days; at ≥ 0.2 t/m³, in ~30 days.
5. A precise survey of the upper Queen's north shaft gives 39.29° ± 0.3° (9/11) rather than 39.8–39.9° (Kochab at Khufu's reign).

# 10. Limitations

- No full transport simulation (Geant4); multiple scattering is approximated by a fitted angular smearing.
- Approximate internal geometry (±1–2 m).
- The reanalysis uses digitized figures, not raw data.
- The blind tests are optimistic by construction (Section 5).
- The construction model is a mean-flow model with an assumed corner overhead.
- Shaft angle uncertainties are partly assumed.
- The orientation conclusions depend on Spence's tabulated values and dates.

# 11. Conclusion

The public data establish that the Big Void exists close to the Grand Gallery axis, at roughly 52–63 m height. They do not fix its shape, and the two published data sets disagree for reasons we cannot resolve from the figures.

We identify measurements that would decide:

- a stereo reanalysis of the original 2017 maps;
- a King's Chamber muography campaign;
- a sledge-turning experiment;
- a laser survey of the Queen's Chamber shafts.

Each comes with predictions registered in advance, so that its result can prove us wrong.

# References

- Badawy, A. *Mitteilungen des Instituts für Orientforschung* 10, 189 (1964).
- Bauval, R. *Discussions in Egyptology* 26 (1993).
- Belmonte, J. A. *Journal for the History of Astronomy, Archaeoastronomy Supplement* 26, S1 (2001).
- Capitaine, N., Wallace, P. T. & Chapront, J. *Astron. Astrophys.* 412, 567 (2003).
- Dash, G. *Journal of Ancient Egyptian Architecture* 2 (2017).
- Fall, A. et al. *Phys. Rev. Lett.* 112, 175502 (2014).
- Gaisser, T. K. *Cosmic Rays and Particle Physics* (Cambridge, 1990).
- Gantenbrink, R. Upuaut Project survey data (1993–1999).
- Hoffleit, D. & Warren, W. H. *The Bright Star Catalogue*, 5th ed. (Yale, 1991).
- Houdin, J.-P. *Khufu: The Secrets Behind the Building of the Great Pyramid* (2006).
- Lehner, M. *The Complete Pyramids* (Thames & Hudson, 1997).
- Magli, G. arXiv:physics/0407108 (2004).
- Maragioglio, V. & Rinaldi, C. *L'architettura delle piramidi menfite* IV (1965).
- Morishima, K. et al. *Nature* 552, 386–390 (2017); arXiv:1711.01576.
- Petrie, W. M. F. *The Pyramids and Temples of Gizeh* (1883).
- Procureur, S. et al. *Nat. Commun.* 14, 1144 (2023).
- Rawlins, D. & Pickering, K. *Nature* 412, 699 (2001).
- Reyna, D. hep-ph/0604145 (2006).
- Rosell Roig, V. L. arXiv:2511.06112 (2025).
- Spence, K. *Nature* 408, 320–324 (2000).
- Tallet, P. *Les papyrus de la mer Rouge I*, MIFAO 136 (2017).
- Trimble, V. *Mitteilungen des Instituts für Orientforschung* 10, 183 (1964).

*Bibliographic details of some references (volume and page numbers) should be verified against the original publications before submission.*
