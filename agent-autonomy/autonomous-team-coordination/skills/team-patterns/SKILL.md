---
name: team-patterns
description: Expert knowledge base of team organization patterns for multi-agent AI systems and software engineering. Provides pattern selection guidance for scenarios including incident response, greenfield design, legacy migration, security audits, performance optimization, API design, data pipelines, testing, documentation, and code migration. This skill should be used when designing agent teams, selecting team topologies, choosing communication patterns, sizing teams, or determining optimal team structure for a given situation. Also use when users mention "team pattern", "team topology", "agent coordination", "team design", "swarm configuration", "multi-agent architecture", "how many agents", or "what agents do I need".
---

# Team Patterns - Expert Team Organization Knowledge

Decision-support index for designing optimal team configurations. Start here, then drill into specific reference files as needed.

## Quick Reference: Scenario to Pattern

| Scenario | Primary Pattern | Topology | Size | Key Risk |
|---|---|---|---|---|
| Production incident | Incident Command | Hub-and-spoke | 4-6 | IC bottleneck |
| Greenfield design | Squad + ARB | Mesh + periodic star | 4-7 | Over-engineering |
| Legacy refactoring | Strangler Fig + enabling team | Pipeline + mesh | 5-7 | Stalled migration |
| Security audit | Red/Blue/Purple team | Adversarial + bridge | 8-15 | Collusion |
| Performance optimization | Tiger team | Mesh | 3-5 | Premature scaling |
| API design | Design-first embedded team | Collaborative mesh | 4-6 | Approval bottleneck |
| Data pipeline | Cross-functional DataOps | Mesh + pipeline | 4-6 | Infra vs. insight |
| Test suite creation | Integrated quality + pyramid | Mesh (shared) | 3-5 | QA silo |
| Documentation overhaul | Docs-as-Code + embedded writers | Mesh + pipeline | 3-5 | Doc debt |
| Code migration | Strangler Fig + migration squad | Pipeline + hub-and-spoke | 5-8 | Dual-system stall |

## Decision Matrix: Situation Traits to Pattern

When the scenario does not match the quick reference table above, use this trait-based matrix:

| Urgency | Complexity | Knowledge | Risk | -> Pattern | -> Topology |
|---------|-----------|-----------|------|------------|-------------|
| Critical | Any | Any | Zero | Incident Command | Hub-and-spoke |
| High | Complex-entangled | Concentrated | Low | Tiger Team | Mesh |
| High | Complex-decomposable | Distributed | Low | Fan-Out/Fan-In | Star |
| Normal | Well-defined | Concentrated | Moderate | Pipeline | Pipeline |
| Normal | Well-defined | Distributed | Moderate | Supervisor-Worker | Tree |
| Normal | Complex-decomposable | Distributed | Moderate | Cross-functional Squad | Mesh |
| Normal | Complex-entangled | Distributed | Low | Mob/Ensemble | Hub+Mesh |
| Normal | Adversarial | Distributed | Zero | Red/Blue/Purple | Adversarial |
| Exploratory | Complex-decomposable | Unknown | High | Small Mesh + ARB | Mesh+Star |
| Exploratory | Complex-entangled | Unknown | Moderate | Debate/Adversarial | Point-to-point+Judge |
| Any | Any (quality-critical) | Any | Any | Add Reflection Loop | Bidirectional loop |

**Automated selection:** Run `scripts/pattern-selector.py --urgency <X> --complexity <Y>` for programmatic recommendations.

## Pattern Index

| # | Pattern | Topology | Key Rule |
|---|---------|----------|----------|
| 1 | Incident Command | Hub-and-spoke | IC does NOT touch code |
| 2 | Tiger Team | Mesh | Full removal from BAU; disband after |
| 3 | Architecture Review Board | Star | Embed governance in workflow, not gates |
| 4 | Mob/Ensemble | Hub+Mesh | Ideas must pass through another's hands |
| 5 | Pair Programming | Point-to-point | Driver-Navigator, Ping-Pong, Strong-Style |
| 6 | Red/Blue/Purple | Adversarial | Verifier agent blocks collusion |
| 7 | Strangler Fig | Pipeline+Hub | Never big-bang rewrite |
| 8 | Fan-Out/Fan-In | Star | Workers must be truly independent |
| 9 | Supervisor-Worker | Tree | Max 2 hierarchy levels |
| 10 | Debate/Adversarial | P2P+Judge | Voting improves reasoning 13.2% |
| 11 | Blackboard | Star+shared | Clear read/write protocols |
| 12 | Reflection/Self-Critique | Loop | 78.6% -> 97.1% accuracy with reflection |

## Organizational Theory Constraints

| Principle | Rule | Number |
|-----------|------|--------|
| Communication overhead | n(n-1)/2 channels | 7 agents = 21 channels |
| Optimal team size | Harvard Business School | 4.6 members optimal |
| Mesh ceiling | Never exceed | 7 agents in mesh |
| Dunbar's working limit | Close relationships | 9 max (sub-teams form beyond) |
| Decision degradation | Bain & Company | -10% effectiveness per member beyond 7 |
| Brooks's Law | Adding to late project | Makes it later |
| Conway's Law | Team structure shapes architecture | Use Inverse Conway Maneuver |
| Ringelmann Effect | Agents overlap, not loaf | Clear task boundaries prevent redundancy |

**Calculator:** Run `scripts/team-size-calculator.py <N>` to assess any team size.

## Agent Role Archetypes

| Archetype | Purpose | Example Agents |
|---|---|---|
| Coordinator | Decomposes work, manages flow | project-manager |
| Architect | Designs systems, defines interfaces | solid-architect |
| Implementer | Writes code, builds features | independent-contributor, IC-opus, IC-sonnet |
| Critic | Finds flaws, validates quality | critical-code-reviewer, complexity-reducer |
| Investigator | Explores, gathers context | research-methodology-expert |
| Specialist | Domain expertise | testing-expert, web-bug-hunter, audio-expert |
| Refactorer | Improves existing code | refactor-master, code-refactor-splitter |
| Documenter | Creates/maintains documentation | document-maintainer |
| Releaser | Packages, versions, ships | release-manager |

**Full mapping:** See `references/agent-archetype-mapping.md` for complete agent-to-archetype table with pattern-specific assignments.

**Inventory:** Run `scripts/scan-agents.sh` to list all currently installed agents.

## Communication Topology Reference

| Topology | Channels | Scaling | Max Agents | Primary Use |
|----------|----------|---------|------------|-------------|
| Hub-and-spoke | n | Linear | ~15 | Coordination-heavy |
| Mesh | n(n-1)/2 | Quadratic | 7 | Creative, small teams |
| Pipeline | n-1 | Linear | Unlimited | Sequential processing |
| Tree | n-1 | Log depth | Unlimited | Large teams, hierarchy |
| Star | 2n | Linear | Unlimited | Parallel execution |
| Adversarial | Fixed | Fixed | By team | Security, validation |

**Diagrams:** See `references/topology-diagrams.md` for ASCII diagrams of all 6 topologies.

## Detailed References

Drill into these files only when you need full research for a specific category:

| File | Content | When to Read |
|------|---------|-------------|
| `references/classic-se-patterns.md` | Patterns 1-7: Incident Command, Tiger Team, ARB, Mob, Pair, Spotify, Team Topologies | Designing teams using SE patterns |
| `references/multi-agent-patterns.md` | Patterns 8-12: Supervisor-Worker, Pipeline, Fan-Out, Debate, Voting, Reflection, ToT, Blackboard, MoE, CrewAI, LangGraph | Designing AI agent coordination |
| `references/organizational-theory.md` | Conway's Law, Brooks's Law, Tuckman, Ringelmann, Communication Overhead | Justifying team size and structure decisions |
| `references/scenario-playbooks.md` | Complete playbooks for all 10 scenarios | When the quick reference table matches a scenario |
| `references/topology-diagrams.md` | ASCII diagrams for all 6 topologies with formulas | Including diagrams in team design output |
| `references/agent-archetype-mapping.md` | Maps archetypes to installed agents, pattern-specific assignments | Assigning real agents to team roles |
| `references/sources.md` | 97 source URLs, categorized | Attribution, further reading |

## Example Team Designs

Complete worked examples matching the team-architect output format:

| Example | Pattern | Agents | File |
|---------|---------|--------|------|
| Production API 500 errors | Incident Command + Fan-Out | 4-5 | `examples/incident-response-team.md` |
| Greenfield SaaS application | Squad + ARB | 5-6 | `examples/greenfield-fullstack-team.md` |
| Python 2 to 3 monolith migration | Strangler Fig + Enabling | 5 | `examples/legacy-migration-team.md` |

## Scripts

| Script | Purpose | Usage |
|--------|---------|-------|
| `scripts/pattern-selector.py` | Recommends patterns from traits or scenarios | `python pattern-selector.py --urgency critical` |
| `scripts/team-size-calculator.py` | Communication overhead calculator | `python team-size-calculator.py 5 8 12` |
| `scripts/scan-agents.sh` | Lists installed agents with descriptions | `bash scan-agents.sh` |
