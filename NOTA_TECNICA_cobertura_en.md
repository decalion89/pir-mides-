# How much of Khufu's Pyramid has muography actually searched? A sensitivity map from the published campaigns, and the case for the Subterranean Chamber

*Technical note for muography groups (Nagoya, CEA/IRFU, KEK, EGP). Draft of 1 November 2026. Code and data are open: https://github.com/decalion89/pir-mides- (docs/17, `simulador/piramide/cobertura.py`).*

## Summary
We model the 14 published muography campaigns at Khufu's Pyramid (2016–2020), with the positions, areas and exposures given in their Methods sections. The model is calibrated to reproduce the published Big Void significances. For every 4 m voxel, we ask whether an additional air cube of side 2–12 m would have produced a ≥ 5σ signal in the combined data.

- **An extra 8 m cubic void (512 m³, larger than the King's Chamber) would have gone undetected in 59–66 % of the pyramid's volume.** The range spans zenith cuts of 70°–85°. For a 5 m cube the figure is 72–73 %.
- **The lowest 20 m are the least explored.** There, an 8 m void would have gone undetected in ≥ 94 % of the volume. No interior detector has ever had this region in its field of view. Only the 2017 exterior telescopes graze it, at near-horizontal angles through 100–200 m of rock.
- **A single emulsion detector in the Subterranean Chamber** (about 30 m below the base) is by far the most effective accessible position. With 1 m² for 100 days, analysed with |tanθ| ≤ 1, the explored fraction for 8 m voids rises from **34 % to 53 %**. With 4 m² for one year, the explored fraction for 5 m voids rises from 27 % to 43 %. Upper positions (King's Chamber, Campbell's Chamber, top of the Grand Gallery) add almost nothing for this purpose.

We know of no published muon measurement from Khufu's Subterranean Chamber. The approach is the one Alvarez et al. (1970) used from the Belzoni Chamber at the base of Khafre's Pyramid.

## Method (short)
- **Forward model:** Reyna/Gaisser spectrum; continuous energy loss in standard rock; limestone at 2.2 t/m³, bedrock at 2.3 t/m³; granite around the King's Chamber.
- **Binning and errors:** angular bins of 0.02 in tanθ; 2 % uncorrelated systematic per bin; about 20 mrad smearing.
- **Sub-ray sampling:** adaptive, up to 6 × 6 rays per bin, so that voids narrower than a bin at large distance are not missed.
- **Reference structures:** the known structures, plus the NFC and the Big Void (horizontal model).
- **Significance:** χ² of the count difference, summed in quadrature over campaigns.
- **Calibration per detector family**, to the published Big Void significances:
  - Nagoya NE1/NE2 (13.7σ and 12.7σ): ×0.44;
  - CEA G1+G2 combined (5.8σ): ×2.6.

  KEK and the 2019 campaigns take their family's factor.

**Validation:**

| Quantity | Model | Published |
|---|---|---|
| CEA G1 / G2 separately | 4.3σ / 3.7σ | 5.0σ / 3.7σ |
| NFC from the 2019 descending-corridor emulsions | 40–84σ | "well over 10σ" |
| NFC from the 2017 exterior telescopes | ~2.7σ | not reported in 2017 |

**Robustness** (8 m grid). The fraction moves by ≤ 3 points under any of these changes:
- no calibration;
- a 1 % or 3 % systematic per bin;
- random detector displacements of 2 m.

The zenith cut is the dominant assumption: 66 % at 70° and 59 % at 85°.

## What the Subterranean Chamber would see (prediction P12, registered 1 Nov 2026)
For 1 m² × 100 d, the model predicts these in-situ calibration targets (calibrated model, factor of ~2 margin):
- the King's Chamber granite mass as a muon deficit at ~23σ;
- the Grand Gallery at ~7σ;
- the Queen's Chamber at ~4σ;
- the King's Chamber at ~4σ.

The descending corridor and the NFC are outside the field of view. The newly explored region lies between ~6 and ~58 m in height, within ~75 m of the axis.

**Robustness of the gain:**
- moving the detector 8 m horizontally, or down to −30 m: ≤ 2 points;
- bedrock at 2.6 t/m³ instead of 2.3: about −3 points.

## Limitations
- This is a simplified model, not Geant4.
- Internal geometry is uncertain by ±1–2 m. The 2019 detector positions are approximate, because the papers give no coordinates.
- The model does not include correlated large-angle systematics. These matter most for heterogeneous bedrock directly above the chamber.
- Unpublished data may already cover more of the pyramid. The map refers to the published record only.
- The map does **not** suggest that hidden chambers exist. It states where their absence has not yet been established, and which measurement would establish it.

## Request
1. **Feedback on the campaign parameters**, especially the 2019 detector positions and the analysed acceptances.
2. **Interest in a Subterranean Chamber emulsion run.** Its access is the descending corridor, where Nagoya films were already installed in 2019.

Contact: [AUTHOR NAME] · labix7@gmail.com

## References
- Alvarez, L. W. et al. (1970). *Search for hidden chambers in the pyramids*. Science 167, 832–839.
- Bross, A. et al. (2022). *Tomographic muon imaging of the Great Pyramid of Giza*. arXiv:2202.08184 (feasibility study).
- Morishima, K. et al. (2017). *Discovery of a big void in Khufu's Pyramid by observation of cosmic-ray muons*. Nature 552, 386–390.
- Procureur, S., Morishima, K. et al. (2023). *Precise characterization of a corridor-shaped structure in Khufu's Pyramid by observation of cosmic-ray muons*. Nat. Commun. 14, 1144.
