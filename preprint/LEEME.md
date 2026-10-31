# Preprint (borrador en inglés)

- `preprint_en.md`: fuente.
- `preprint_en.pdf`: versión para leer, generada con pandoc y Chromium.
- `preprint_en.tex`: fuente LaTeX para arXiv. Antes de subirla, copia las figuras que cita (`../figuras/*.png`) a la misma carpeta y cambia las rutas a `figuras/...`.

Las figuras llevan las etiquetas en español; para la versión final convendría traducirlas.

Para regenerarlo:
```bash
pandoc preprint_en.md -s --css estilo.css --embed-resources --resource-path=.:.. -o preprint_en.html
pandoc preprint_en.md -s -o preprint_en.tex
node -e "const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();const p=await b.newPage();await p.goto('file://'+process.cwd()+'/preprint_en.html');await p.pdf({path:'preprint_en.pdf',format:'A4'});await b.close();})()"
```
