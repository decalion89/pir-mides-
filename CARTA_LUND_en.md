# Draft — request to the Lund lidar team (not sent)

**To:** Prof. Sune Svanberg; Dr. Zheng Duan (Lund University / South China Normal University)
**From:** [NAME, AFFILIATION] — labix7@gmail.com
**Subject:** A falsifiable test of how mercury leaves the Qin Shi Huang tomb, using your 2016 lidar data

Dear Prof. Svanberg, dear Dr. Duan,

Your 2020 *Scientific Reports* paper (Mercury as a geophysical tracer gas: emissions from the Emperor Qin tomb studied by laser radar) estimates an outflux of about 5×10⁻⁸ kg/s from the mound. We compared that number with physical limits, and it has a strong implication.

1. **Diffusion cannot supply it.** If the chamber holds liquid mercury, its air is saturated (≈9 mg/m³ at 15 °C). Steady-state diffusion through 30–80 m of compacted loess cannot deliver your flux: the gap is a factor of 19–2,200 (median 160, Monte Carlo over porosity, moisture, depth, source area and temperature). Even a free-air channel spanning the whole chamber roof falls short in most cases. Typical emission from soils with ~190 ppb Hg also falls short, by a factor of ~10–200.
2. **Advection can.** If the source is the tomb, the underground palace must exchange air with the atmosphere at ~150–1,500 m³/day through cracks. Barometric pumping of the palace volume can supply this, marginally in summer and more easily in winter.

This gives tests that need no excavation. We have pre-registered them (git-timestamped) **before seeing any time-resolved data**:
- Nightly Hg excess (wind-corrected) should correlate positively with a barometric-pumping index we computed from the Jinghe synoptic station (WMO 57131) for 24 July – 12 Aug 2016. On that index, the highest predicted nights are 27–28 July, 1–2 and 12 August; the lowest are 26, 29 and 30 July, 6 and 10 August.
- Winter emission should exceed summer emission.
- Soil-gas Hg should increase with depth.

**Our request:** would you be willing to share the time-stamped DIAL concentration series from the 2016 campaign (date, time, site, range, value) and the mound-top weather-station records? With them, test 1 can be run immediately on existing data. We would of course credit and involve you as you see fit.

The full analysis and code are open: [repository link], docs/34 and PREDICCIONES.md (P15).

With best regards,
[NAME]
