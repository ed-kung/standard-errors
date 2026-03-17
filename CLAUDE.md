# Standard Errors

Single-page web app that visually demonstrates standard errors in regression analysis. Users adjust parameters, run simulated regressions, and see how coefficient estimates vary across samples.

## Running locally

Serve via any static file server from the project root:

```
python -m http.server
```

Then open http://localhost:8000. First load is slow (~10s) as it downloads Pyodide, numpy, and matplotlib.

## Tech stack

- **PyScript 2024.11.1** — runs Python (via Pyodide/WebAssembly) in the browser
- **numpy** — random sampling and OLS computation
- **matplotlib** — scatter plots and histograms, rendered as images via `pyscript.display()`
- No build step, no bundler, no backend — static files deployed via GitHub Pages

## File structure

| File | Purpose |
|---|---|
| `index.html` | Page structure, CSS, PyScript bootstrap |
| `pyscript.toml` | PyScript config (packages, local file mapping) |
| `simulation.py` | Pure Python simulation logic (numpy only, no DOM) |
| `app.py` | PyScript UI controller, state machine, rendering |

**Key design rule:** `simulation.py` has zero DOM/PyScript imports. It is pure numpy Python that can be read, edited, and tested independently. All browser interaction lives in `app.py`.

## App states

The app is a state machine with three states:

- **Initialization** — controls unlocked, "Run regression for one sample" button
- **Iteration** — controls locked, "Run another", "Repeat for 1000", and "Reset" buttons
- **Completed** — controls unlocked, "Reset" button only

## Simulation model

Y = Xβ + ε, where X ~ Uniform(-1, 1) and ε ~ N(0, σ). OLS slope is computed as Cov(X,Y)/Var(X).
