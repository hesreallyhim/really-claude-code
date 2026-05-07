#!/usr/bin/env python3
"""
Pattern Selector for Team Design

Takes situation traits (urgency, complexity, knowledge distribution, risk tolerance)
as CLI arguments and outputs recommended team patterns with topology and reference
file pointers.

Usage:
    python pattern-selector.py --urgency critical --complexity complex-decomposable
    python pattern-selector.py --scenario "production incident"
    python pattern-selector.py --urgency normal --complexity well-defined --json

Part of the team-patterns skill for Claude Code agent team design.
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass, field
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
REFERENCES_DIR = SCRIPT_DIR.parent / "references"
EXAMPLES_DIR = SCRIPT_DIR.parent / "examples"

VALID_URGENCY = ["critical", "high", "normal", "exploratory"]
VALID_COMPLEXITY = ["well-defined", "complex-decomposable", "complex-entangled", "adversarial"]
VALID_KNOWLEDGE = ["concentrated", "distributed", "unknown"]
VALID_RISK = ["zero", "low", "moderate", "high"]


@dataclass
class Recommendation:
    pattern: str
    topology: str
    team_size: str
    reference_file: str
    example_file: str | None = None
    notes: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "pattern": self.pattern,
            "topology": self.topology,
            "team_size": self.team_size,
            "reference_file": self.reference_file,
            "example_file": self.example_file,
            "notes": self.notes,
        }


SCENARIO_SHORTCUTS: dict[str, Recommendation] = {
    "production incident": Recommendation(
        pattern="Incident Command + Fan-Out/Fan-In",
        topology="Hub-and-spoke",
        team_size="4-6",
        reference_file="classic-se-patterns.md (1.1) + multi-agent-patterns.md (2.3)",
        example_file="incident-response-team.md",
        notes=["IC does NOT touch code", "Parallel investigation tracks"],
    ),
    "greenfield": Recommendation(
        pattern="Cross-functional Squad + ARB",
        topology="Mesh + periodic Star",
        team_size="4-7",
        reference_file="scenario-playbooks.md (4.2)",
        example_file="greenfield-fullstack-team.md",
        notes=["ARB at milestones only, not every change", "Risk: over-engineering"],
    ),
    "legacy refactoring": Recommendation(
        pattern="Strangler Fig + Enabling Team",
        topology="Pipeline + Hub-and-spoke",
        team_size="5-7",
        reference_file="scenario-playbooks.md (4.3)",
        example_file="legacy-migration-team.md",
        notes=["Never big-bang rewrite", "Tests before migration", "Feature flags for rollback"],
    ),
    "security audit": Recommendation(
        pattern="Red/Blue/Purple Team",
        topology="Adversarial + bridge",
        team_size="8-15",
        reference_file="classic-se-patterns.md (1.6) + scenario-playbooks.md (4.4)",
        notes=["Verifier agent essential to block collusion", "Purple team bridges findings to improvements"],  # noqa: E501
    ),
    "performance optimization": Recommendation(
        pattern="Tiger Team",
        topology="Mesh",
        team_size="3-5",
        reference_file="classic-se-patterns.md (1.2) + scenario-playbooks.md (4.5)",
        notes=["Profile before AND after each change", "Establish baselines first"],
    ),
    "api design": Recommendation(
        pattern="Design-First Embedded Team + ARB",
        topology="Collaborative Mesh",
        team_size="4-6",
        reference_file="scenario-playbooks.md (4.6)",
        notes=["API contract before implementation", "Embed governance in CI, not review gates"],
    ),
    "data pipeline": Recommendation(
        pattern="Cross-functional DataOps",
        topology="Mesh + Pipeline",
        team_size="4-6",
        reference_file="scenario-playbooks.md (4.7)",
        notes=["Choose orchestration tool early", "Automate data quality validation"],
    ),
    "test suite": Recommendation(
        pattern="Integrated Quality + Testing Pyramid",
        topology="Mesh (shared ownership)",
        team_size="3-5",
        reference_file="scenario-playbooks.md (4.8)",
        notes=["Start with TDD for unit tests", "No separate QA silo"],
    ),
    "documentation": Recommendation(
        pattern="Docs-as-Code + Embedded Writers",
        topology="Mesh + Pipeline",
        team_size="3-5",
        reference_file="scenario-playbooks.md (4.9)",
        notes=["Use Diataxis framework", "Same tools as developers"],
    ),
    "code migration": Recommendation(
        pattern="Strangler Fig + Migration Squad",
        topology="Pipeline + Hub-and-spoke",
        team_size="5-8",
        reference_file="scenario-playbooks.md (4.10)",
        example_file="legacy-migration-team.md",
        notes=["Routing layer in front of legacy", "Migrate one module at a time"],
    ),
}


def select_by_traits(
    urgency: str,
    complexity: str,
    knowledge: str = "distributed",
    risk: str = "moderate",
) -> Recommendation:
    """Select pattern based on situation trait combination.

    Rules are ordered by priority: more specific/urgent rules match first.
    """
    # Rule 1: Critical urgency always maps to Incident Command
    if urgency == "critical":
        return Recommendation(
            pattern="Incident Command",
            topology="Hub-and-spoke",
            team_size="4-6",
            reference_file="classic-se-patterns.md (1.1)",
            example_file="incident-response-team.md",
            notes=["Critical urgency overrides all other traits", "IC does NOT touch code"],
        )

    # Rule 2: Adversarial complexity maps to Red/Blue/Purple
    if complexity == "adversarial":
        return Recommendation(
            pattern="Red/Blue/Purple Team",
            topology="Adversarial + bridge",
            team_size="8-15",
            reference_file="multi-agent-patterns.md (2.4) + classic-se-patterns.md (1.6)",
            notes=["Always include verifier agent", "Purple team bridges red and blue"],
        )

    # Rule 3: High urgency + concentrated knowledge = Tiger Team
    if urgency == "high" and knowledge == "concentrated":
        return Recommendation(
            pattern="Tiger Team",
            topology="Mesh",
            team_size="3-5",
            reference_file="classic-se-patterns.md (1.2)",
            notes=["Handpicked experts", "Full removal from BAU", "Disband after resolution"],
        )

    # Rule 4: High urgency + distributed knowledge = Fan-Out/Fan-In
    if urgency == "high" and knowledge == "distributed":
        return Recommendation(
            pattern="Fan-Out/Fan-In",
            topology="Star",
            team_size="4-7",
            reference_file="multi-agent-patterns.md (2.3)",
            notes=["Workers must be truly independent", "Dispatcher + parallel workers + aggregator"],  # noqa: E501
        )

    # Rule 5: Well-defined complexity = Pipeline
    if complexity == "well-defined" and knowledge == "concentrated":
        return Recommendation(
            pattern="Pipeline",
            topology="Pipeline",
            team_size="3-5",
            reference_file="multi-agent-patterns.md (2.2)",
            notes=["Clear sequential stages", "Each stage independently testable"],
        )

    if complexity == "well-defined" and knowledge == "distributed":
        return Recommendation(
            pattern="Supervisor-Worker",
            topology="Tree",
            team_size="4-7",
            reference_file="multi-agent-patterns.md (2.1)",
            notes=["Keep hierarchy shallow (max 2 levels)", "Most scalable pattern"],
        )

    # Rule 6: Complex-entangled + unknown knowledge = exploration needed
    if complexity == "complex-entangled" and knowledge == "unknown":
        return Recommendation(
            pattern="Mob/Ensemble Programming",
            topology="Hub (coding) + Mesh (discussion)",
            team_size="3-5",
            reference_file="classic-se-patterns.md (1.4)",
            notes=["Rotate driver every 5-15 min", "Ideas must go through another's hands"],
        )

    # Rule 7: Exploratory urgency = small mesh with ARB checkpoints
    if urgency == "exploratory":
        return Recommendation(
            pattern="Small Mesh + ARB Review",
            topology="Mesh + periodic Star",
            team_size="3-5",
            reference_file="classic-se-patterns.md (1.3)",
            example_file="greenfield-fullstack-team.md",
            notes=["Creative freedom with governance checkpoints", "ARB prevents architectural drift"],  # noqa: E501
        )

    # Rule 8: Low risk + complex-decomposable = Strangler Fig
    if risk in ("zero", "low") and complexity == "complex-decomposable":
        return Recommendation(
            pattern="Strangler Fig + Enabling Team",
            topology="Pipeline + Hub-and-spoke",
            team_size="5-7",
            reference_file="scenario-playbooks.md (4.3)",
            example_file="legacy-migration-team.md",
            notes=["Incremental replacement", "Feature flags for rollback", "Tests before migration"],  # noqa [E501
        )

    # Default: Cross-functional Squad
    return Recommendation(
        pattern="Cross-functional Squad",
        topology="Mesh",
        team_size="4-7",
        reference_file="scenario-playbooks.md (4.2)",
        example_file="greenfield-fullstack-team.md",
        notes=[
            "Default pattern for normal urgency + moderate risk",
            "Add ARB review for quality-critical work",
            "Add Reflection Loop for iterative refinement",
        ],
    )


def format_text(rec: Recommendation) -> str:
    """Format recommendation as human-readable text."""
    lines = [
        f"Pattern:        {rec.pattern}",
        f"Topology:       {rec.topology}",
        f"Team Size:      {rec.team_size}",
        f"Reference File: {rec.reference_file}",
    ]
    if rec.example_file:
        lines.append(f"Example File:   {rec.example_file}")
    if rec.notes:
        lines.append("Notes:")
        for note in rec.notes:
            lines.append(f"  - {note}")
    lines.append("")
    lines.append("Overlay recommendation: Consider adding Reflection/Self-Critique (Pattern 12)")
    lines.append("for quality-critical tasks. See multi-agent-patterns.md (2.6).")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Select team patterns based on situation traits or named scenarios.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --urgency critical
  %(prog)s --urgency normal --complexity well-defined --knowledge distributed
  %(prog)s --scenario "production incident"
  %(prog)s --scenario "legacy refactoring" --json
  %(prog)s --list-scenarios
        """,
    )
    parser.add_argument("--urgency", choices=VALID_URGENCY, help="Urgency profile")
    parser.add_argument("--complexity", choices=VALID_COMPLEXITY, help="Problem complexity")
    parser.add_argument("--knowledge", choices=VALID_KNOWLEDGE, default="distributed", help="Knowledge distribution")  # noqa [E501
    parser.add_argument("--risk", choices=VALID_RISK, default="moderate", help="Risk tolerance")
    parser.add_argument("--scenario", help="Named scenario shortcut (e.g., 'production incident')")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument("--list-scenarios", action="store_true", help="List all named scenarios")

    args = parser.parse_args()

    if args.list_scenarios:
        print("Available scenario shortcuts:")
        for name, rec in SCENARIO_SHORTCUTS.items():
            print(f"  {name:25s} -> {rec.pattern}")
        sys.exit(0)

    if args.scenario:
        key = args.scenario.lower().strip()
        if key not in SCENARIO_SHORTCUTS:
            print(f"Unknown scenario: '{args.scenario}'", file=sys.stderr)
            print(f"Available scenarios: {', '.join(SCENARIO_SHORTCUTS.keys())}", file=sys.stderr)
            sys.exit(1)
        rec = SCENARIO_SHORTCUTS[key]
    elif args.urgency:
        rec = select_by_traits(
            urgency=args.urgency,
            complexity=args.complexity or "complex-decomposable",
            knowledge=args.knowledge,
            risk=args.risk,
        )
    else:
        parser.print_help()
        sys.exit(1)

    if args.json:
        print(json.dumps(rec.to_dict(), indent=2))
    else:
        print(format_text(rec))


if __name__ == "__main__":
    main()
