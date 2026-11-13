"""Unit tests for agent-ui-state-diff-engine."""
import unittest
from agent_ui_state_diff_engine.differ import UIStateDiffEngine

class TestUIDiffEngine(unittest.TestCase):
    def setUp(self):
        self.differ = UIStateDiffEngine(threshold_ratio=0.01)

    def test_no_change(self):
        g = [[0, 0], [0, 0]]
        rep = self.differ.compare_grids(g, g)
        self.assertFalse(rep.changed)
        self.assertEqual(rep.state_type, "NO_CHANGE")

    def test_detect_significant_change(self):
        g1 = [[0] * 10 for _ in range(10)]
        g2 = [[100] * 10 for _ in range(10)]
        rep = self.differ.compare_grids(g1, g2)
        self.assertTrue(rep.changed)
        self.assertEqual(rep.state_type, "MODAL_OR_PAGE_TRANSITION")

if __name__ == "__main__":
    unittest.main()
