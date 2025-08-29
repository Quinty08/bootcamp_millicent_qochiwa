# make_dashboard_sketch.py
# Homework 14 – Optional Dashboard Sketch
# Generates a simple PNG file (dashboard_sketch.png) with placeholder metrics.

import matplotlib.pyplot as plt

monitoring = {
    "Data": ["freshness_minutes", "null_rate", "schema_hash"],
    "Model": ["rolling_mae_or_auc", "calibration_error"],
    "System": ["p95_latency_ms", "error_rate"],
    "Business": ["approval_rate", "bad_rate"]
}

def make_dashboard_png():
    fig, axes = plt.subplots(2, 2, figsize=(10, 6))
    fig.suptitle("Conceptual Monitoring Dashboard", fontsize=14, fontweight="bold")

    for ax, (layer, metrics) in zip(axes.flatten(), monitoring.items()):
        ax.set_title(layer)
        ax.barh(range(len(metrics)), [1]*len(metrics))  # fake values (all 1)
        ax.set_yticks(range(len(metrics)))
        ax.set_yticklabels(metrics)
        ax.set_xlim(0, 2)
        ax.set_xticks([])  # hide x-axis since values are fake
        ax.set_xlabel("placeholder")

    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plt.savefig("dashboard_sketch.png")
    print("✅ Saved dashboard sketch to handoff/dashboard_sketch.png")

if __name__ == "__main__":
    make_dashboard_png()
