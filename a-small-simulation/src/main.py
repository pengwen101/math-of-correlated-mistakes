from pathlib import Path

import seaborn as sns
from matplotlib import pyplot as plt
from scipy.stats import bernoulli

PLOTS_DIR = Path(__file__).resolve().parent.parent / "plots"


class Panel:
    def __init__(self, n_models: int, n_questions: int, p_correct: float, delta_p: float = 0.0) -> None:
        if p_correct - delta_p < 0 or p_correct + delta_p > 1:
            raise ValueError(f"p_correct ± delta_p must be in [0, 1], but got p_correct={p_correct} and delta_p={delta_p}")
        self.n_models = n_models
        self.n_questions = n_questions
        self.p_correct = p_correct
        self.delta_p = delta_p
        self._set_hard_indexes()

    def _set_hard_indexes(self) -> None:
        if self.delta_p:
            self.hard_indexes = range(self.n_questions // 2)
        else:
            self.hard_indexes = []

    def _get_p_correct_updated(self, question: int) -> float:
        if question in self.hard_indexes:
            return self.p_correct - self.delta_p
        return self.p_correct + self.delta_p

    def simulate(self) -> list[list[int]]:
        results = []
        for _ in range(self.n_models):
            verdicts = []
            for question in range(self.n_questions):
                p_correct_updated = self._get_p_correct_updated(question)
                verdict = int(bernoulli.rvs(p=p_correct_updated))
                verdicts.append(verdict)
            results.append(verdicts)
        return results


def plot(results: list[list[int]], title: str, output_path: Path) -> None:
    plt.figure(figsize=(20, 6))
    sns.heatmap(results, cmap="RdYlGn", cbar=True)
    plt.xlabel("Questions")
    plt.ylabel("Models")
    plt.title(title)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_path, bbox_inches="tight")
    plt.close()


def main() -> None:
    panel_1 = Panel(n_models=5, n_questions=40, p_correct=0.7, delta_p=0.0)
    panel_2 = Panel(n_models=5, n_questions=40, p_correct=0.7, delta_p=0.2)

    results_1 = panel_1.simulate()
    results_2 = panel_2.simulate()

    plot(results_1, title="Panel with no harder questions", output_path=PLOTS_DIR / "panel_1.png")
    plot(results_2, title="Panel with harder questions", output_path=PLOTS_DIR / "panel_2.png")


if __name__ == "__main__":
    main()