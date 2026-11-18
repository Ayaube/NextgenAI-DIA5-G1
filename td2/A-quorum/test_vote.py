"""Offline contract tests for Pair A; no provider calls."""
import itertools
from types import SimpleNamespace
import unittest
from comparaison_quorums import load_vote, proposals_for, MODELS

vote = load_vote()


def panel(values):
    return [SimpleNamespace(provider="test", model_requested=str(i), value=value,
                            verdict="executed" if value is not None else "error")
            for i, value in enumerate(values)]


class VoteTests(unittest.TestCase):
    def test_exhaustive_two_of_three_and_three_of_five(self):
        for n, k in [(3, 2), (5, 3)]:
            for values in itertools.product([None, 0, 100, 120], repeat=n):
                with self.subTest(values=values, k=k):
                    result = vote(panel(values), k)
                    winner = next((v for v in (0, 100, 120) if values.count(v) >= k), None)
                    self.assertEqual(result["consensus"], winner is not None)
                    self.assertEqual(result["value"], winner)
                    self.assertEqual(result["votes"], max(values.count(v) for v in (0, 100, 120)))
                    expected_models = [f"test:{i}" for i, v in enumerate(values) if v == winner] if winner is not None else []
                    self.assertEqual(result["models"], expected_models)

    def test_threshold_and_empty_panel(self):
        for k in (0, 1, 4, 2.0, True):
            with self.assertRaises(ValueError):
                vote(panel([1, 1, 1]), k)
        with self.assertRaises(ValueError):
            vote([], 1)
        with self.assertRaises(ValueError):
            vote(panel([1, 1, 1, 1]), 2)
        self.assertTrue(vote(panel([1, 1, 1, None]), 3)["consensus"])

    def test_duplicate_unavailable_member(self):
        proposals = panel([100, 100, None])
        proposals[2].model_requested = proposals[0].model_requested
        with self.assertRaises(ValueError):
            vote(proposals, 2)

    def test_error_with_residual_value_does_not_vote(self):
        proposals = panel([100, 100, None])
        proposals[1].verdict = "error"
        self.assertFalse(vote(proposals, 2)["consensus"])

    def test_invalid_values(self):
        for value in (100.5, "100", True):
            with self.assertRaises(ValueError):
                vote(panel([value, 100, None]), 2)

    def test_unanimity_and_none(self):
        self.assertFalse(vote(panel([100, 100, None]), 3)["consensus"])
        self.assertEqual(vote(panel([None, None, None]), 2),
                         {"consensus": False, "value": None, "votes": 0, "models": []})

    def test_incorrect_is_still_an_executed_vote(self):
        key = MODELS["A"]
        rows = {(*key, "C01"): {"value": "0", "verdict": "incorrect"}}
        result = vote(proposals_for(rows, "C01", [key]), 1)
        self.assertEqual(result["value"], 0)
        self.assertTrue(result["consensus"])

    def test_missing_trace_is_not_a_provider_error(self):
        with self.assertRaises(ValueError):
            proposals_for({}, "C01", [MODELS["E"]])


if __name__ == "__main__":
    unittest.main(verbosity=2)
