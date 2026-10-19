# DSP Tasks GUI

## Structure

```text
dsp_project/
├── main.py                 # GUI only: widgets, layout, navigation, callbacks
├── style.css               # central CSS-like palette reference
├── style.py                # applies the palette to Tkinter/ttk
├── signal_operations.py    # copy your existing file here unchanged
└── tasks/
    ├── __init__.py
    ├── task1_operations.py # loading, display, add/subtract/multiply/shift/fold
    └── task2_operations.py # sine/cosine generation and plotting
```

## Run
1. Place your existing `signal_operations.py` in the same folder as `main.py`.
2. Install Matplotlib if needed: `pip install matplotlib`
3. Run `python main.py`.

**Note:** Tkinter cannot read CSS natively. `style.css` is the central visual reference;
`style.py` applies the matching colors and ttk styles to the actual Tkinter widgets.
