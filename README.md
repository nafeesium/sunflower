# Sunflower.py

A sunflower made entirely out of the words "I love you" in 20 languages.

Run it and a window opens. The words fade in one by one, drifting down from above, and build up a sunflower: first the green stem, then the leaves, then the brown middle, and finally the yellow petals. When it's finished, random words keep twinkling.

No images, no extra libraries. Everything is drawn with text on a Python canvas.

## What you get

- A yellow sunflower with a brown centre, green leaves and a green stem
- About 90 words laid out so they fill the shape edge to edge
- Words in 20 languages, including English, Turkish, Spanish, French, German, Italian, Portuguese, Russian, Korean, Japanese, Chinese, Hindi, Greek, Dutch, Swedish, Polish, Thai, Vietnamese, Indonesian and Ukrainian
- A 10 second build, then a soft shimmer that keeps going until you close the window

## Requirements

- Python 3
- `tkinter` (the window library)

There is nothing to `pip install`. Everything the script imports ships with Python: `math`, `random`, `turtle` and `tkinter`.

`tkinter` comes with the normal Python installers on Windows and macOS. On Linux you may need to add it:

```
sudo apt install python3-tk
```

## How to run

```
python Sunflower.py
```

On Windows you can also use `py Sunflower.py`. In VS Code, press the Run button and make sure the selected Python is one that has tkinter.

Close the window to stop it.

## Make it yours

The settings are the constants at the top of `Sunflower.py`.

| Setting | Default | What it changes |
| --- | --- | --- |
| `DURATION` | `10` | Seconds the flower takes to build |
| `SIZES` | `(9, 10, 11, 12)` | Font sizes used for the words. Smaller sizes fit more words |
| `PETALS` | `14` | Number of petals |
| `PETAL_LEN` / `PETAL_W` | `126` / `40` | How long and how wide each petal is |
| `DISC_R` | `84` | Size of the brown middle |
| `STEM_W` | `36` | How thick the stem is |
| `LEAVES` | two leaves | Position, angle, length and width of each leaf |
| `BG` | `"#060208"` | Background colour |
| `FONT` | `"Arial"` | Font. Pick one that has the scripts you want (Thai, Hindi, Korean and so on) |
| `PHRASES` | 20 phrases | The words that fill the flower. Swap in your own |

The colours are the tuples near the top (`GOLD`, `LEMON`, `BROWN_D`, `LEAF_D` and so on). Each is a set of red, green and blue values from 0 to 1.

The random seed is fixed (`r.Random(11)`), so you get the same flower every time. Change the `11` to any other number for a different arrangement.

## Troubleshooting

**`ModuleNotFoundError: No module named 'tkinter'`**
Your Python was installed without tkinter. Reinstall Python from python.org, or on Linux run the `apt` command above.

**Some words show as empty boxes**
The font you picked doesn't have that script. Change `FONT` to one that does, for example "Segoe UI" on Windows or "Arial Unicode MS" on macOS.

**Gaps or overlapping words**
Text width depends on your system's fonts. Try lowering `SIZES` a little, or raise `GAP` for more room between words.

**The window is cut off on a small screen**
The canvas is 800 by 800. Change the numbers in `s.setup(800, 800)` and scale the shape settings down to match.

## How it works

1. The flower's outline is described by a function (`region_at`) that answers "what is at this point: middle, petal, leaf, stem or nothing?"
2. The canvas is cut into rows, and each row is filled with words that fit the shape.
3. Every word gets a colour based on where it sits, for example gold near the middle of a petal and lemon at the tip.
4. Words are shown in growth order and each one fades in with a little flash as it lands.

## License

MIT. Do whatever you like with it.
