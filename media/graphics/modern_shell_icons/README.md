# ReactOS Fluent shell icons

This directory contains the source generator for the modern ReactOS shell icon
set. The artwork is original and is drawn from geometric primitives by
`generate.py`; it does not contain icons extracted from Microsoft Windows.

The visual direction is inspired by contemporary Fluent interfaces: rounded
silhouettes, restrained depth, blue/cyan accents, and legible shapes at 16 px.
Generated ICO files contain 16, 24, 32, 48, and 64 pixel 32-bit RGBA images.

Run from the repository root:

```text
python3 media/graphics/modern_shell_icons/generate.py
```

The generator requires Python 3 and Pillow.

The script updates the selected high-visibility resources in shell32,
Explorer, Command Prompt, and Applications Manager, and writes `preview.png`
beside the generator.
