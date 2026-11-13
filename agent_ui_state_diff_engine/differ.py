"""Perceptual and component-level UI state change detection."""
from typing import Dict, List, Optional, Tuple, Any

class UIDiffReport:
    def __init__(self, changed: bool, change_ratio: float, state_type: str, altered_regions: List[Tuple[int, int, int, int]]):
        self.changed = changed
        self.change_ratio = change_ratio
        self.state_type = state_type  # NO_CHANGE, SPINNER, MODAL, CONTENT_UPDATE
        self.altered_regions = altered_regions

class UIStateDiffEngine:
    """Detects visual transitions between pre- and post-interaction states."""

    def __init__(self, threshold_ratio: float = 0.005):
        self.threshold_ratio = threshold_ratio

    def compare_grids(self, grid_before: List[List[int]], grid_after: List[List[int]]) -> UIDiffReport:
        """Compares two 2D luminance grids (e.g. downsampled grayscale frames)."""
        rows = len(grid_before)
        cols = len(grid_before[0]) if rows > 0 else 0
        total_cells = rows * cols
        if total_cells == 0:
            return UIDiffReport(False, 0.0, "NO_CHANGE", [])

        diff_count = 0
        min_r, min_c = rows, cols
        max_r, max_c = -1, -1

        for r in range(rows):
            for c in range(cols):
                if abs(grid_before[r][c] - grid_after[r][c]) > 20:  # Noise threshold
                    diff_count += 1
                    min_r = min(min_r, r)
                    min_c = min(min_c, c)
                    max_r = max(max_r, r)
                    max_c = max(max_c, c)

        ratio = diff_count / total_cells
        if ratio < self.threshold_ratio:
            return UIDiffReport(False, ratio, "NO_CHANGE", [])

        state_type = "CONTENT_UPDATE"
        if ratio > 0.4:
            state_type = "MODAL_OR_PAGE_TRANSITION"
        elif 0.01 <= ratio <= 0.08:
            state_type = "BUTTON_OR_SPINNER"

        regions = [(min_c, min_r, max_c - min_c + 1, max_r - min_r + 1)] if diff_count > 0 else []
        return UIDiffReport(True, round(ratio, 4), state_type, regions)
