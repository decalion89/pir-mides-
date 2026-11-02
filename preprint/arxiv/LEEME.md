# Paquete para arXiv

Contenido: `main.tex` (generado desde `../preprint_en.md` con `../a_latex.py`) y `figuras/`.

1. **Rellena el autor**: busca `[AUTHOR NAME(S)` en `main.tex` (y en `../preprint_en.md`) y pon nombre, afiliación ("Independent researcher" si no tienes) y correo.
2. **Verifica que compila** antes de subirlo. No hemos podido compilarlo aquí. La forma más fácil y gratuita es:
   - crear un proyecto en blanco en **Overleaf**;
   - subir `main.tex` y la carpeta `figuras/`;
   - compilar con **pdfLaTeX**.

   Si aparece algún error de carácter Unicode, añade una línea `\newunicodechar{X}{...}` en el preámbulo.
3. **Sube a arXiv** (arxiv.org → Submit): el `.tex` y las figuras, o un `.zip`. Categorías sugeridas: principal *physics.hist-ph*; secundarias *physics.ins-det* y *physics.data-an*. Si es tu primer envío en esa categoría, arXiv puede pedir un aval: ver `../../PLAN_DE_CONTACTO.md`.
