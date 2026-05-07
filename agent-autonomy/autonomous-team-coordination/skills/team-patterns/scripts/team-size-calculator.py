#!/usr/bin/env python3
"""
Team Size Calculator

Calculates communication overhead using Brooks's formula n(n-1)/2 and provides
qualitative assessments based on organizational theory research.

Usage:
    python team-size-calculator.py 5
    python team-size-calculator.py 5 8 12     # Compare multiple sizes
    python team-size-calculator.py --range 3 15
    python team-size-calculator.py 7 --json

Part of the team-patterns skill for Claude Code agent team design.
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass


@dataclass
class TeamAssessment:
    size: int
    channels: int
    assessment: str
    topology_recommendation: str
    research_notes: list[str]

    def to_dict(self) -> dict:
        return {
            "size": self.size,
            "channels": self.channels,
            "assessment": self.assessment,
            "topology_recommendation": self.topology_recommendation,
            "research_notes": self.research_notes,
        }


def channels(n: int) -> int:
    """Calculate communication channels: n(n-1)/2."""
    return n * (n - 1) // 2


def assess_team_size(n: int) -> TeamAssessment:
    """Provide qualitative assessment for a given team size."""
    ch = channels(n)

    if n < 2:
        return TeamAssessment(
            size=n,
            channels=0,
            assessment="Not a team",
            topology_recommendation="Single agent",
            research_notes=["A single agent requires no coordination topology."],
        )

    if n == 2:
        return TeamAssessment(
            size=n,
            channels=ch,
            assessment="Pair -- optimal for focused collaboration",
            topology_recommendation="Point-to-point (Pair Programming)",
            research_notes=[
                "Ideal for driver-navigator, ping-pong, or strong-style pairing.",
                "Zero coordination overhead beyond the pair itself.",
            ],
        )

    if 3 <= n <= 4:
        return TeamAssessment(
            size=n,
            channels=ch,
            assessment="Small team -- highly efficient",
            topology_recommendation="Mesh (all communicate freely)",
            research_notes=[
                f"{ch} channels is very manageable.",
                "Near Harvard optimal of 4.6 members.",
                "Ideal for tiger teams, focused squads, and pipeline stages.",
            ],
        )

    if n == 5:
        return TeamAssessment(
            size=n,
            channels=ch,
            assessment="Optimal -- closest to Harvard's 4.6 ideal",
            topology_recommendation="Mesh or Hub-and-spoke",
            research_notes=[
                "Harvard Business School research: 4.6 is the optimal team size.",
                f"{ch} channels is comfortable for mesh communication.",
                "Most versatile size: works with any pattern.",
            ],
        )

    if 6 <= n <= 7:
        return TeamAssessment(
            size=n,
            channels=ch,
            assessment="Good -- approaching mesh limit",
            topology_recommendation="Mesh (but consider hub-and-spoke for coordination-heavy work)",
            research_notes=[
                f"{ch} channels is the practical upper limit for mesh topology.",
                "7 is the absolute maximum for full mesh. Beyond this, use hierarchy.",
                "Bain: each member beyond 7 reduces decision effectiveness by ~10%.",
            ],
        )

    if 8 <= n <= 9:
        return TeamAssessment(
            size=n,
            channels=ch,
            assessment="Caution -- hierarchy recommended",
            topology_recommendation="Hub-and-spoke or Tree (sub-teams of 3-4)",
            research_notes=[
                f"{ch} channels exceeds comfortable mesh limit.",
                "Dunbar: beyond 9 close working relationships, invisible sub-teams form.",
                "Split into sub-teams with designated leads.",
                "Brooks's Law: coordination overhead may exceed marginal capability gains.",
            ],
        )

    if 10 <= n <= 15:
        return TeamAssessment(
            size=n,
            channels=ch,
            assessment="Warning -- significant coordination overhead",
            topology_recommendation="Tree with sub-teams of 4-5",
            research_notes=[
                f"{ch} communication channels in full mesh (DO NOT use mesh at this size).",
                "Must use hierarchical topology to manage coordination.",
                f"Recommended structure: 1 lead + {n // 4}-{n // 3} sub-teams of 4-5.",
                "Consider whether all agents are truly needed. Brooks's Law applies.",
            ],
        )

    # n > 15
    return TeamAssessment(
        size=n,
        channels=ch,
        assessment="Critical -- likely too large without deep hierarchy",
        topology_recommendation="Deep tree or Spotify-model tribes",
        research_notes=[
            f"{ch} channels makes flat communication impossible.",
            "Bain: at 17+ members, decisions stall.",
            "Dunbar's number (~150) is the absolute ceiling for any coherent organization.",
            f"Recommended: split into {n // 5}-{n // 4} independent squads of 5-7 with lead coordination.",
            "Seriously reconsider whether this many agents are needed.",
        ],
    )


def format_text(assessment: TeamAssessment) -> str:
    """Format assessment as human-readable text."""
    lines = [
        f"Team Size:      {assessment.size} agents",
        f"Channels:       {assessment.channels} (formula: n(n-1)/2 = {assessment.size}*{assessment.size - 1}/2)",
        f"Assessment:     {assessment.assessment}",
        f"Topology:       {assessment.topology_recommendation}",
        "Research Notes:",
    ]
    for note in assessment.research_notes:
        lines.append(f"  - {note}")
    return "\n".join(lines)


def format_comparison_table(assessments: list[TeamAssessment]) -> str:
    """Format multiple assessments as a comparison table."""
    lines = [
        f"{'Size':>6}  {'Channels':>10}  {'Assessment':<45}  {'Topology'}",
        f"{'----':>6}  {'--------':>10}  {'----------':<45}  {'--------'}",
    ]
    for a in assessments:
        lines.append(
            f"{a.size:>6}  {a.channels:>10}  {a.assessment:<45}  {a.topology_recommendation}"
        )
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Calculate communication overhead and assess team sizes.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s 5                   # Assess a team of 5
  %(prog)s 5 8 12              # Compare multiple sizes
  %(prog)s --range 3 15        # Show all sizes from 3 to 15
  %(prog)s 7 --json            # JSON output
        """,
    )
    parser.add_argument("sizes", nargs="*", type=int, help="Team size(s) to assess")
    parser.add_argument("--range", nargs=2, type=int, metavar=("MIN", "MAX"), help="Range of sizes to assess")
    parser.add_argument("--json", action="store_true", help="Output as JSON")

    args = parser.parse_args()

    sizes: list[int] = []
    if args.range:
        sizes = list(range(args.range[0], args.range[1] + 1))
    elif args.sizes:
        sizes = args.sizes
    else:
        parser.print_help()
        sys.exit(1)

    assessments = [assess_team_size(n) for n in sizes]

    if args.json:
        if len(assessments) == 1:
            print(json.dumps(assessments[0].to_dict(), indent=2))
        else:
            print(json.dumps([a.to_dict() for a in assessments], indent=2))
    elif len(assessments) == 1:
        print(format_text(assessments[0]))
    else:
        print(format_comparison_table(assessments))


if __name__ == "__main__":
    main()
