"""Pure simulation logic for standard errors demo. No DOM/PyScript imports."""

import numpy as np


def generate_sample(beta, sigma, n, rng=None):
    """Generate one sample: X ~ Uniform(-1,1), Y = X*beta + eps, eps ~ N(0, sigma)."""
    if rng is None:
        rng = np.random.default_rng()
    X = rng.uniform(-1, 1, size=n)
    eps = rng.normal(0, sigma, size=n)
    Y = X * beta + eps
    return X, Y


def ols_slope(X, Y):
    """OLS slope coefficient: Cov(X,Y) / Var(X)."""
    return np.dot(X - X.mean(), Y - Y.mean()) / np.dot(X - X.mean(), X - X.mean())


def run_samples(beta, sigma, n, num_samples, rng=None):
    """Run multiple samples, return list of dicts with X, Y, beta_hat."""
    if rng is None:
        rng = np.random.default_rng()
    results = []
    for _ in range(num_samples):
        X, Y = generate_sample(beta, sigma, n, rng)
        beta_hat = ols_slope(X, Y)
        results.append({"X": X, "Y": Y, "beta_hat": beta_hat})
    return results
