"""CLI for agent-ui-state-diff-engine."""
import sys
import argparse
from .differ import UIStateDiffEngine

def main():
    parser = argparse.ArgumentParser(description="Agent UI State Diff Engine CLI")
    parser.add_argument("--demo", action="store_true", help="Run UI state differ demo")
    args = parser.parse_args()

    if args.demo:
        differ = UIStateDiffEngine()
        grid1 = [[10] * 10 for _ in range(10)]
        grid2 = [[10] * 10 for _ in range(10)]
        # Change a small region (button state)
        grid2[4][4] = 90
        grid2[4][5] = 90
        rep = differ.compare_grids(grid1, grid2)
        print(f"[+] Diff report: changed={rep.changed}, ratio={rep.change_ratio}, type={rep.state_type}")
    else:
        parser.print_help()
    sys.exit(0)

if __name__ == "__main__":
    main()
