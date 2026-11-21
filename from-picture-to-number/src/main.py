from pathlib import Path

import seaborn as sns
from matplotlib import pyplot as plt

PLOTS_DIR = Path(__file__).resolve().parent.parent / "plots"

def get_effective_voters(k: int, corr: float) -> float:
    """
    Calculate the effective number of voters based on the number of voters and their correlation.

    Args:
        k (int): The total number of voters.
        corr (float): The correlation between voters' decisions.

    Returns:
        float: The effective number of voters.
    """
    if not (0 <= corr <= 1):
        raise ValueError(f"Correlation must be in [0, 1], but got {corr}")
    return k / (1 + ((k - 1) * corr))

def plot(k_values: list[int], corr_values: list[float], list_of_effective_voters: list[list[float]], title: str, output_path: Path) -> None:
    plt.figure(figsize=(20, 6))
    for corr, effective_voters in zip(corr_values, list_of_effective_voters):
        sns.lineplot(x=k_values, y=effective_voters, label=f"corr={corr}")
    plt.xlabel("Number of Voters")
    plt.ylabel("Effective Voters")
    plt.title(title)
    plt.legend()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_path, bbox_inches="tight")
    plt.close()

def main() -> None:
    k_values = list(range(1, 31))  # Number of voters from 1 to 30
    corr_values = [0.0, 0.2, 0.5, 0.8]  # Different correlation values

    list_of_effective_voters = []
    for corr in corr_values:
        effective_voters = [get_effective_voters(k, corr) for k in k_values]
        list_of_effective_voters.append(effective_voters)

    plot(k_values, corr_values, list_of_effective_voters, title="Effective Voters vs Number of Voters", output_path=PLOTS_DIR / "effective_voters.png")


if __name__ == "__main__":
    main()