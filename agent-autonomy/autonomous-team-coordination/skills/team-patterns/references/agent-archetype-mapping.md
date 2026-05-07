# Agent Archetype Mapping

Maps abstract team pattern archetypes to actual installed agents in `~/.claude/agents/`. Use this to translate a team design's role requirements into concrete agent assignments.

Last updated: 2026-02-14

---

## Archetype to Agent Mapping

| Archetype | Role in Team Patterns | Installed Agent(s) | Notes |
|-----------|----------------------|-------------------|-------|
| **Coordinator** | Decomposes work, manages flow, acts as IC or supervisor | `project-manager` | Best for orchestration roles. Use as Incident Commander or team lead. |
| **Architect** | Designs systems, defines interfaces, makes technology decisions | `solid-architect` | SOLID principles focus. Good for ARB reviews, system design, migration strategy. |
| **Implementer** | Writes code, builds features, executes tasks | `independent-contributor` (default model) | General-purpose implementer. Follows ticket instructions autonomously. |
| **Implementer (Senior)** | Complex implementation requiring deep reasoning | `independent-contributor-opus` (in `opus/`) | Use for complex migrations, entangled code, critical path work. Higher cost. |
| **Implementer (Fast)** | High-volume implementation work | `independent-contributor-sonnet` (in `sonnet/`) | Use for parallel workers, straightforward implementation. Lower cost. |
| **Critic / Reviewer** | Finds flaws, validates quality, acts as reflection loop | `critical-code-reviewer` | Strict code review focus. Good for review gates and quality checkpoints. |
| **Critic (Complexity)** | Identifies and reduces complexity | `complexity-reducer` | Specialized in finding over-engineered code. Good for legacy analysis. |
| **Critic (Hierarchical)** | Multi-level code review | `hierarchical-code-reviewer` | Layered review process. Use when review needs multiple perspectives. |
| **Investigator** | Explores codebases, gathers context, researches | `research-methodology-expert` | Use for discovery phases, unknown codebases, research tasks. |
| **Specialist (Testing)** | Testing strategy, test generation, quality assurance | `testing-expert` | TDD, testing pyramid, test suite creation. |
| **Specialist (Security)** | Security audit, vulnerability detection | `web-bug-hunter` | Web security focus. Use as Red Team agent or security reviewer. |
| **Specialist (Audio)** | Audio processing domain expertise | `audio-expert` | Narrow domain. Only relevant for audio-related projects. |
| **Specialist (Hooks)** | Claude Code hooks and configuration | `hooks-expert` | Narrow domain. Use when team involves hook configuration. |
| **Specialist (MCP)** | MCP protocol expertise | `mcp-protocol-expert` | Narrow domain. Use when team involves MCP server/client work. |
| **Refactorer** | Improves existing code structure | `refactor-master` | Comprehensive refactoring. Good for legacy modernization roles. |
| **Refactorer (Splitter)** | Breaks large files/modules into smaller ones | `code-refactor-splitter` | Specialized in decomposition. Use in migration pipelines. |
| **Reviser** | Iterative code improvement | `code-reviser` | Good for reflection loops (generator-critic pattern). |
| **Documenter** | Creates and maintains documentation | `document-maintainer` | Docs-as-Code pattern. Technical writing, API docs. |
| **Releaser** | Packaging, versioning, shipping | `release-manager` | Release process management. Use in deployment pipeline stages. |
| **Prompter** | Enhances prompts and agent instructions | `prompt-enhancer` | Meta-role: use when designing new agents, not in task teams. |
| **Agent Designer** | Creates new agent definitions | `sub-agent-architect` / `sub-agent-architect-by-cc` | Meta-role: use when capability gaps are identified. |
| **Marketing** | GitHub marketing, project presentation | `github-marketing-expert` | Non-engineering role. Use for open-source project presentation. |
| **Mentor** | Code quality philosophy, best practices | `guru-uncle-bob` | Advisory role. Clean code principles. |
| **Defender** | Bash command safety review | `bash-defender-agent` | Security role. Use in pipelines where agents execute shell commands. |
| **Scenario Designer** | Personas, hypothetical scenarios, regulatory exploration, test coverage generation | *skill:* `scenario-architect` | Not an agent — a skill loaded by any agent that needs to generate realistic scenarios, personas, or compliance landscapes. Assign to the agent playing the Product Owner, UX Researcher, or QA Lead role. |

---

## Pattern-Specific Agent Assignments

### Incident Command (Hub-and-spoke)
| Role | Agent |
|------|-------|
| Incident Commander | `project-manager` |
| Technical Responders | `independent-contributor-sonnet` (x2-4) |
| Deployment Reviewer | `independent-contributor-opus` |
| Scribe | `document-maintainer` |

### Tiger Team (Mesh)
| Role | Agent |
|------|-------|
| Security Expert | `web-bug-hunter` |
| Architecture Expert | `solid-architect` |
| Code Analyst | `complexity-reducer` |
| Implementer | `independent-contributor-opus` |

### Red/Blue/Purple (Adversarial)
| Role | Agent |
|------|-------|
| Red Team (attackers) | `web-bug-hunter` (x2-3) |
| Blue Team (defenders) | `bash-defender-agent`, `critical-code-reviewer` (x2-3) |
| Purple Team (bridge) | `project-manager` |
| Verifier | `hierarchical-code-reviewer` |

### Strangler Fig Migration (Pipeline)
| Role | Agent |
|------|-------|
| Migration Architect | `solid-architect` |
| Legacy Analyzer | `complexity-reducer` |
| Test Engineer | `testing-expert` |
| Migration Engineer | `independent-contributor-opus` |
| Parity Validator | `critical-code-reviewer` |

### Cross-functional Squad (Mesh)
| Role | Agent |
|------|-------|
| Tech Lead | `solid-architect` |
| Implementers | `independent-contributor` (x2-4) |
| Reviewer | `critical-code-reviewer` |
| Documenter | `document-maintainer` |

---

## Coverage Gaps

These archetypes have **no dedicated agent** currently installed:

| Archetype | Gap Description | Workaround |
|-----------|----------------|------------|
| **DevOps/Infrastructure** | No agent specialized in CI/CD, Kubernetes, cloud infrastructure | Use `independent-contributor` with infrastructure-focused instructions |
| **Data Engineer** | No agent specialized in data pipelines, ETL, database optimization | Use `independent-contributor` with data engineering instructions |
| **Frontend Specialist** | No agent specialized in frontend frameworks (React, Vue, etc.) | Use `independent-contributor` with frontend-focused instructions |
| **Performance Engineer** | No agent specialized in profiling, benchmarking, optimization | Use `independent-contributor-opus` with performance instructions |
| **Product Owner** | No agent for requirements gathering, prioritization, user stories | Use `project-manager` in a product-focused capacity. The `scenario-architect` skill can be loaded to provide structured persona generation, use case exploration, and regulatory landscape analysis. |
