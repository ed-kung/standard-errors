"""PyScript UI controller for the standard errors demo."""

from enum import Enum

import matplotlib
matplotlib.use("agg")
import matplotlib.pyplot as plt
from pyscript import document, display, when

import numpy as np
from simulation import run_samples


class State(Enum):
    INITIALIZATION = "initialization"
    ITERATION = "iteration"
    COMPLETED = "completed"


class App:
    def __init__(self):
        self.state = State.INITIALIZATION
        self.estimates = []
        self.last_4 = []  # list of {X, Y, beta_hat} dicts, most recent last
        self._update_ui()

    def _get_params(self):
        beta = float(document.getElementById("beta-slider").value)
        sigma = float(document.getElementById("sigma-slider").value)
        n = int(document.getElementById("n-slider").value)
        return beta, sigma, n

    def _lock_controls(self, locked):
        for sid in ("beta-slider", "sigma-slider", "n-slider"):
            document.getElementById(sid).disabled = locked

    def _show_button(self, btn_id, visible):
        document.getElementById(btn_id).style.display = "block" if visible else "none"

    def _update_buttons(self):
        if self.state == State.INITIALIZATION:
            self._show_button("btn-run-one", True)
            self._show_button("btn-run-another", False)
            self._show_button("btn-run-1000", False)
            self._show_button("btn-reset", False)
        elif self.state == State.ITERATION:
            self._show_button("btn-run-one", False)
            self._show_button("btn-run-another", True)
            self._show_button("btn-run-1000", True)
            self._show_button("btn-reset", True)
        elif self.state == State.COMPLETED:
            self._show_button("btn-run-one", False)
            self._show_button("btn-run-another", False)
            self._show_button("btn-run-1000", False)
            self._show_button("btn-reset", True)

    def render_scatter_plots(self):
        for i in range(4):
            target = f"scatter-{i}"
            el = document.getElementById(target)
            el.innerHTML = ""
            if i < len(self.last_4):
                sample = self.last_4[i]
                fig, ax = plt.subplots(figsize=(2.8, 2.4))
                ax.scatter(sample["X"], sample["Y"], s=10, alpha=0.6, color="steelblue")
                x_line = np.array([-1, 1])
                y_line = x_line * sample["beta_hat"]
                ax.plot(x_line, y_line, color="red", linewidth=1.5)
                ax.set_xlim(-1, 1)
                ax.set_ylim(-3, 3)
                ax.set_title(f"β̂ = {sample['beta_hat']:.3f}", fontsize=10)
                ax.tick_params(labelsize=7)
                fig.tight_layout()
                display(fig, target=target)
                plt.close(fig)

    def render_histogram(self):
        target = "histogram-container"
        el = document.getElementById(target)
        el.innerHTML = ""
        if self.estimates:
            fig, ax = plt.subplots(figsize=(4, 3.5))
            bin_edges = np.linspace(-2, 2, 81)  # 80 bins, width 0.05
            counts, _ = np.histogram(self.estimates, bins=bin_edges)
            ax.bar(bin_edges[:-1], counts, width=0.05, align="edge",
                   color="steelblue", edgecolor="white", alpha=0.8)
            # Invisible points at edges to anchor the axis range
            ax.plot([-2, 2], [0, 0], alpha=0)
            ax.set_xlabel("β̂ estimate", fontsize=10)
            ax.set_ylabel("Count", fontsize=10)
            ax.tick_params(labelsize=8)
            fig.tight_layout()
            display(fig, target=target)
            plt.close(fig)
        n = len(self.estimates)
        count_el = document.getElementById("estimate-count")
        mean_el = document.getElementById("estimate-mean")
        std_el = document.getElementById("estimate-std")
        if n > 0:
            count_el.innerText = f"{n} estimate{'s' if n != 1 else ''} from {n} different sample{'s' if n != 1 else ''}"
            mean_el.innerText = f"Mean = {np.mean(self.estimates):.4f}"
            std_el.innerText = f"Standard Deviation = {np.std(self.estimates):.4f}"
        else:
            count_el.innerText = ""
            mean_el.innerText = ""
            std_el.innerText = ""

    def _update_ui(self):
        self._lock_controls(self.state == State.ITERATION)
        self._update_buttons()
        self.render_scatter_plots()
        self.render_histogram()

    def add_samples(self, results):
        for r in results:
            self.estimates.append(r["beta_hat"])
            self.last_4.append(r)
            if len(self.last_4) > 4:
                self.last_4.pop(0)

    def run_one(self):
        beta, sigma, n = self._get_params()
        results = run_samples(beta, sigma, n, 1)
        self.add_samples(results)
        self.state = State.ITERATION
        self._update_ui()

    def run_1000(self):
        beta, sigma, n = self._get_params()
        results = run_samples(beta, sigma, n, 1000)
        self.add_samples(results)
        self.state = State.COMPLETED
        self._update_ui()

    def reset(self):
        self.estimates = []
        self.last_4 = []
        self.state = State.INITIALIZATION
        self._update_ui()


# --- Initialize app ---
app = App()


# --- Button handlers ---
@when("click", "#btn-run-one")
def on_run_one(event):
    app.run_one()


@when("click", "#btn-run-another")
def on_run_another(event):
    app.run_one()


@when("click", "#btn-run-1000")
def on_run_1000(event):
    app.run_1000()


@when("click", "#btn-reset")
def on_reset(event):
    app.reset()


# --- Slider display handlers ---
@when("input", "#beta-slider")
def on_beta_change(event):
    document.getElementById("beta-value").innerText = f"{float(event.target.value):.2f}"


@when("input", "#sigma-slider")
def on_sigma_change(event):
    document.getElementById("sigma-value").innerText = f"{float(event.target.value):.2f}"


@when("input", "#n-slider")
def on_n_change(event):
    document.getElementById("n-value").innerText = event.target.value
