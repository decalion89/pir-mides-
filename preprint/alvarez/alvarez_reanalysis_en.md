---
title: "Alvarez's Chephren muon data, 56 years on: spatially structured residuals and a data-driven exclusion map"
author: "[AUTHOR NAME(S) AND AFFILIATION — to be completed] · Proyecto Pirámides, https://github.com/decalion89/pir-mides- · Contact: labix7@gmail.com"
date: "Draft, 1 November 2026"
---

## Abstract

In 1969 L. W. Alvarez and collaborators searched for hidden chambers in Khafre's (Chephren's) pyramid with spark chambers in the Belzoni Chamber. They concluded that no chamber of the size of Khufu's King's Chamber exists within a 35° cone around the vertical, "19 percent" of the pyramid's volume. Besides their conclusion, they published the bin-by-bin map of differences between measured and best-fit predicted muon counts (their Fig. 10; χ² = 905 for an effective ≈750 bins). We are not aware of any previous reanalysis of that map.

We transcribe it (801 bins of 3° × 3°) and find:

1. **The residuals are spatially correlated** (nearest-neighbour Moran's I = +0.11; p < 5 × 10⁻⁴ under permutation). Alvarez's excess χ² reflects structured systematics rather than random noise.
2. **No residual cluster is significant** once a null model with the same spatial correlation is used. The most extreme clusters have global p = 0.03–0.04 for individual statistics, below ~2σ after accounting for the six statistics tested.
3. **A data-driven exclusion map.** We predict the residual footprint of a King's-Chamber-sized cavity at every position with a simplified forward model normalised to Alvarez's published predictions. His data exclude such a cavity in **≈22 % of the pyramid's volume at 95 % CL** (12 % at 5σ), including **≈6.5 % of the volume outside the 35° cone** he analysed.
4. **The best-fitting "candidate" cavity is not significant.** It reaches 3.5σ locally but 0.85σ globally (p = 0.40), and it moves when the residual-map alignment is shifted by one bin. It is a fluctuation of the structured residuals.

These results bear on the planned ScIDEP measurements from the same chamber. They show that spatially correlated systematics routinely produce ~3.5σ local "cavities", so global significances must be calibrated with correlated null models.

## 1. Introduction

Alvarez et al. [1] pioneered absorption muography of monuments. Their detector, two 1.8 m × 1.8 m spark chambers with scintillation counters and 1.2 m of iron, sat in the south-east corner of the Belzoni Chamber, the burial chamber cut into the bedrock beneath the centre of Khafre's pyramid. It recorded over a million muons in several months, of which ≈650 000 passed the final selection. Comparing with a simulated pyramid, they could "say with confidence that no chambers with volumes similar to the four known chambers in Cheops's and Sneferu's pyramids exist" in the 35° cone. They also announced plans to look through "the remaining 81 percent", which, as far as we know, were never published.

Two developments make a reanalysis timely:

- Muography of the Giza pyramids has since found the Big Void [2] and the North Face Corridor [3] in Khufu's pyramid.
- The ScIDEP collaboration is preparing new scintillator telescopes for the same Belzoni Chamber and outside Khafre's pyramid [4].

The only previous comparison with Alvarez's data that we know of [5] used a simple model and an azimuthal profile at ~30° zenith. It reported a possible excess at 62°–72° azimuth and a peak near 270°.

## 2. Data

Alvarez et al. (p. 836) print three 30 × 30 matrices in bins of 3° × 3° in the projected angles θ (north–south) and φ (west–east):

- **Fig. 8:** measured counts;
- **Fig. 9:** predicted counts for the best fit;
- **Fig. 10:** their difference in integer standard deviations.

The caption of Fig. 10 gives χ² = 905, and the text an effective number of bins "close to 750".

**Transcription.** We transcribed Fig. 10 visually from the scanned article at 420–900 dpi, because the OCR layer confuses "1" with "3.". The file is `datos/alvarez_1970/fig10_residuos.txt`.

- **Size and alignment.** The matrix has 801 filled bins in 29 rows; its first row is empty. Rows are aligned on the drawn north–south axis, and empty bins occur only at the edges. The absolute row assignment is uncertain by ±1 bin (±3°), which we treat as a systematic.
- **Uncertain values.** Three values have an uncertain sign. All 8 sign combinations were analysed; no conclusion changes.
- **Check against χ².** We obtain Σr² = 1074. Rounding a field of the published variance (905/801) would give ≈973. The ≈10 % difference is consistent with edge bins shown in the figure but excluded from the published χ², and/or isolated transcription errors. Neither could create the spatial correlation found below.

## 3. Spatial structure of the residuals

**Method.**

- **Spatial correlation:** Moran's I for horizontal and vertical neighbours.
- **Cluster search:** the maximum of Σr/√n over all complete windows of 2×2, 3×3 and 4×4 bins, separately for excesses (more muons: a cavity) and deficits (more matter).
- **Two null models:**
  - (i) 2000 permutations of the residuals among the valid bins;
  - (ii) 4000 Gaussian random fields smoothed to reproduce the observed Moran's I (kernel σ = 0.42 bins), with the same variance and rounding.
- **Global p-values:** we compare the observed maximum with the maxima of each simulated map.

| Statistic | Value | p (permutation) | p (correlated null) | Location (θ, φ) |
|---|---|---|---|---|
| Moran's I | +0.11 | < 5 × 10⁻⁴ | — | — |
| Excess 2×2 | 4.0 | 0.44 | 0.74 | (63°, 96°) |
| Excess 3×3 | 4.7 | 0.05 | 0.19 | (110°, 53°) |
| Excess 4×4 | 5.3 | 0.005 | **0.04** | (108°, 54°) |
| Deficit 2×2 | 5.0 | 0.004 | 0.09 | (126°, 69°) |
| Deficit 3×3 | 5.3 | 0.001 | **0.03** | (128°, 71°) |
| Deficit 4×4 | 5.0 | 0.002 | 0.07 | (126°, 72°) |

The residuals are clearly not independent. Under the permutation null, the clusters would look highly significant (p = 0.001–0.005). Under the correlated null, none is: two statistics reach p ≈ 0.03–0.04, and six were tested.

The strongest excess lies ≈38° from the zenith towards the west-south-west (azimuth ≈246°), just outside the 35° cone. The deficit lies on the south-south-west edge of the acceptance.

We also tested the region suggested by [5]: a King's-Chamber-sized cavity at 30° zenith and azimuth 67°, under four possible azimuth conventions. The normalised 3×3 sums are +0.7, +1.0, −0.3 and +2.0. None is notable.

![Fig. 1. Alvarez's Fig. 10 residuals as transcribed, with the most extreme clusters and their global p-values under the correlated null.](fig1_residuals.png)

## 4. What the data exclude

**Forward model.**

- **Geometry:** Khafre's pyramid (side 215.25 m, original height 143.5 m, present height 136.4 m), limestone 2.2 t/m³. Detector at the south-east corner of the Belzoni Chamber, (5, −1.5, −0.5) m relative to the centre of the base.
- **Physics:** Reyna sea-level spectrum and continuous energy loss.
- **Binning:** a fine grid uniform in angle (0.25°), grouped into Alvarez's 3° bins.
- **Acceptance:** vanishes at ≈45° east–west and, fitted to the edge rows of his Fig. 9, at ≈43° north–south.
- **Normalisation:** 1600 counts in a central bin ("in a typical 3- by 3-degree bin there are 1600 events"). The model then predicts ≈605 000 counts in the 801 bins, against ≈650 000 selected events, and reproduces the edge rows of Fig. 9 to within ≈25 %.

**Test statistic.** For a cavity at position v, the footprint in each bin is s = (N_with − N_without)/√N_without, and

  Δχ²_v = [Σ (r − s)² − Σ r²] / κ,

where κ = var(r) = 1.34 inflates the errors for the structured systematics. A cavity is excluded at 95 % CL if Δχ² ≥ 3.84 and at ≈5σ if Δχ² ≥ 25. Only positions where the cavity fits entirely inside the pyramid are counted. The grid is 8 m (4409 positions).

| Cavity | Excluded, 95 % CL | Excluded, 5σ | Inside 35° cone (95 % / 5σ) | Outside cone, 95 % (share of total volume) |
|---|---|---|---|---|
| King's-Chamber size (10.5 × 5.2 × 5.8 m) | **22 %** | 12 % | 95 % / 58 % | **+6.5 %** |
| 8 m cube | 24 % | 19 % | 99.7 % / 92 % | +7.8 % |

**Robustness.** The four variants change the excluded fraction (all positions, King's-Chamber size, 95 % CL) only between 23 % and 26 %. They are: residual alignment shifted ±1 row, and the alternative chamber position of [5] (centre 13.5 m east and 4 m north of the pyramid's centre). Alvarez's statement for the cone holds at 95 % CL but not at 5σ.

![Fig. 2. Where Alvarez's residuals exclude a King's-Chamber-sized cavity.](fig2_exclusion.png)

### The best "candidate"

The minimum Δχ² (data preferring a cavity) is −12.2, at (16, 40, 84) m: 3.5σ local. Shifting the residual alignment by ±1 row or moving the chamber position displaces it to (−24, −16, 36), (40, 40, 68) or (−32, −8, 84) m, with Δχ² between −9.7 and −10.7.

We estimate its global significance by applying the same position scan to 5000 correlated null maps:

| Hypothesis | min Δχ² | local σ | global p | global σ | median null minimum |
|---|---|---|---|---|---|
| King's-Chamber size | −12.2 | 3.5 | 0.40 | 0.85 | −11.3 |
| 8 m cube | −12.1 | 3.5 | 0.23 | 1.2 | −9.4 |

The observed best candidate is typical of what structured noise produces.

## 5. Discussion

- **For Khafre's pyramid.** Alvarez's published residuals contain no evidence of a hidden chamber, consistent with his conclusion. They exclude a King's-Chamber-sized cavity at 95 % CL in about a fifth of the volume, a little more than the 19 % he claimed, and at 5σ in about an eighth.
- **For new measurements.** Correlated residuals of the kind found here make ~3.5σ local "cavities" common. Searches such as ScIDEP's [4] should calibrate global significances with nulls that preserve spatial correlation. The two most extreme regions found here can be checked at no cost by any new exposure covering them: an excess at ≈38° zenith towards azimuth ≈246°, and a deficit at the south-south-west edge.
- **For the method.** Published residual maps from the 1960s–70s can still yield quantitative constraints when combined with a modern forward model and appropriate nulls.

## 6. Limitations

- **Forward model:** simplified, without Geant4. The acceptance agrees with Fig. 9 only to ≈25 % at the edges, which matters most in the 35°–45° band.
- **Alvarez's fit:** we do not refit it. Its free parameters, such as the north–south sensitivity variation he introduced, could have absorbed part of the footprint of a large diffuse cavity. The exclusion is therefore most reliable for compact cavities.
- **Rounding:** the residuals are rounded to integer σ.
- **Transcription:** isolated errors are possible.
- **Next step:** transcribing Figs. 8 and 9 would allow a full refit.

## Data and code

Everything is open at https://github.com/decalion89/pir-mides-:

- `datos/alvarez_1970/fig10_residuos.txt`
- `simulador/reanalisis_alvarez.py`
- `simulador/exclusion_alvarez.py`
- `simulador/significacion_global_alvarez.py`
- results in `resultados/23_*.json` and `resultados/24_*.json`

## References

1. L. W. Alvarez et al., "Search for hidden chambers in the pyramids", *Science* 167, 832–839 (1970).
2. K. Morishima et al., "Discovery of a big void in Khufu's Pyramid by observation of cosmic-ray muons", *Nature* 552, 386–390 (2017).
3. S. Procureur, K. Morishima et al., "Precise characterization of a corridor-shaped structure in Khufu's Pyramid by observation of cosmic-ray muons", *Nat. Commun.* 14, 1144 (2023).
4. M. Gamal, S. Aly, R. Kouzes et al., "The ScIDEP muon radiography project at the Egyptian Pyramid of Khafre", arXiv:2503.21959 (2025).
5. B. Gutowski et al., "The secret chambers in the Chephren Pyramid", arXiv:1712.08590 (2017).
