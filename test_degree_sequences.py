import unittest
from havel_hakimi_algorithm import havel_hakimi_general
from strategies.matching_aware_strategy import MatchingAwareStrategy
from strategies.naive_matching_aware_strategy import NaiveMatchingAwareStrategy

class TestHavelHakimiAlgorithm(unittest.TestCase):
    def test_degree_sequence_k_odd(self):
        for k in range(1, 50, 2):
            degrees = [k] * (k + 1) + [1] * (k * (k + 1))
            self._run_and_compare_strategies(degrees)

    def test_degree_sequence_all_twos(self):
        for n in range(4, 40, 2):
            degrees = [2] * n
            self._run_and_compare_strategies(degrees)

    def test_degree_sequence_d_regular(self):
        for d in range(1, 30):
            for j in range(2 * d + 2, 10 * d, 2):  # Test for j >= 2d+1
                degrees = [d] * j
                self._run_and_compare_strategies(degrees)

    def test_degree_sequence_bipartite(self):
        # degree sequences of the form [n/2] *n
        for k in range(1, 30):
            degrees = [k] * (2 * k)
            self._run_and_compare_strategies(degrees)

    def test_degree_sequence_vanes(self):
        for k in range(3, 50):
            degrees = [k] * 2 + [2] * (2 * k)
            self._run_and_compare_strategies(degrees)

    def _run_and_compare_strategies(self, degrees):
        # Run with MatchingAwareStrategy
        matching_strategy = MatchingAwareStrategy()
        is_graphical_matching, edges_matching = havel_hakimi_general(degrees, strategy=matching_strategy)

        # Run with NaiveMatchingAwareStrategy
        naive_strategy = NaiveMatchingAwareStrategy()
        is_graphical_naive, edges_naive = havel_hakimi_general(degrees, strategy=naive_strategy)

        # Assert both strategies produce graphical sequences
        self.assertTrue(is_graphical_matching, f"MatchingAwareStrategy failed to produce a graphical sequence.")
        self.assertTrue(is_graphical_naive, f"NaiveMatchingAwareStrategy failed to produce a graphical sequence.")

        # Assert MatchingAwareStrategy produces a graph with a perfect matching
        matching_edges = matching_strategy.get_matching_edges()
        self.assertEqual(len(matching_edges), len(degrees) // 2, "MatchingAwareStrategy did not produce a perfect matching.")

        # Optionally compare the edges produced by both strategies
        self.assertEqual(sorted(edges_matching), sorted(edges_naive), "The strategies produced NON identical edges.")

if __name__ == "__main__":
    unittest.main()