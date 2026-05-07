# Communication Topology Diagrams

ASCII diagrams for all six communication topologies used in team pattern design. Each diagram includes the channel count formula and scaling notes. These diagrams can be copied directly into team design output documents.

---

## 1. Hub-and-Spoke

```
           +---------+
           | Agent B  |
           +----+----+
                |
  +---------+   |   +---------+
  | Agent A  +--+---+ Agent C  |
  +---------+   |   +---------+
                |
         +------+------+
         | COORDINATOR  |
         +------+------+
                |
  +---------+   |   +---------+
  | Agent D  +--+---+ Agent E  |
  +---------+       +---------+
```

**Channels:** n (one per spoke)
**Scaling:** Linear. Adding agents adds one channel each.
**Best for:** Incident response, hierarchical delegation, any situation needing centralized coordination.
**Risk:** Coordinator is a single point of failure and potential bottleneck.

---

## 2. Mesh (Full)

```
  +---------+-------+---------+
  | Agent A  +-------+ Agent B  |
  +----+----+       +----+----+
       |  \       /       |
       |   \     /        |
       |    \   /         |
       |     \ /          |
       |      X           |
       |     / \          |
       |    /   \         |
       |   /     \        |
  +----+----+       +----+----+
  | Agent D  +-------+ Agent C  |
  +---------+       +---------+
```

**Channels:** n(n-1)/2
- 3 agents = 3 channels
- 5 agents = 10 channels
- 7 agents = 21 channels (MAXIMUM recommended)
- 10 agents = 45 channels (DO NOT USE)

**Scaling:** Quadratic. Never scale beyond 7 agents in a mesh.
**Best for:** Small creative teams, design exploration, tiger teams.
**Risk:** Communication overhead grows rapidly. Beyond 7, use hierarchy instead.

---

## 3. Pipeline

```
  +---------+     +---------+     +---------+     +---------+
  | Stage 1  +---->| Stage 2  +---->| Stage 3  +---->| Stage 4  |
  +---------+     +---------+     +---------+     +---------+
```

**Channels:** n-1 (one between each adjacent pair)
**Scaling:** Linear with pipeline length.
**Best for:** Sequential processing, migration workflows, document processing, content generation.
**Risk:** No parallelism. Single stage failure blocks the entire pipeline. Total latency = sum of all stages.

---

## 4. Tree (Hierarchical)

```
                  +------------+
                  | SUPERVISOR  |
                  +-----+------+
                        |
            +-----------+-----------+
            |                       |
      +-----+------+         +-----+------+
      | Sub-Lead A  |         | Sub-Lead B  |
      +-----+------+         +-----+------+
            |                       |
      +-----+-----+          +-----+-----+
      |           |           |           |
  +---+---+  +---+---+  +---+---+  +---+---+
  |Worker1|  |Worker2|  |Worker3|  |Worker4|
  +-------+  +-------+  +-------+  +-------+
```

**Channels:** n-1 (each node connects to its parent)
**Scaling:** Logarithmic depth, linear breadth. Most scalable topology.
**Best for:** Large organizations, multi-level agent systems, any team >7 agents.
**Risk:** Keep hierarchy shallow (max 2 levels for AI agents). Each level adds latency and token cost.
**Recommended sub-team size:** 3-5 agents per sub-lead.

---

## 5. Star (Fan-Out / Fan-In)

```
                                   +---------+
                                   | Worker A |
                                   +----+----+
                                        |
  +---------+                      +----+----+                      +---------+
  |DISPATCHER+----->Fan-Out------->| Worker B |------Fan-In-------->|AGGREGATOR|
  +---------+                      +----+----+                      +---------+
                                        |
                                   +----+----+
                                   | Worker C |
                                   +----+----+
                                        |
                                   +----+----+
                                   | Worker D |
                                   +---------+
```

**Channels:** 2n (dispatcher-to-worker + worker-to-aggregator)
**Scaling:** Linear with number of workers. All workers run in parallel.
**Best for:** Parallel execution with aggregation, code review, analysis tasks, search.
**Risk:** Workers must be truly independent. Aggregation logic can be complex. Higher total compute cost.

---

## 6. Adversarial

```
  +------------------+                          +------------------+
  |    RED TEAM       |                          |    BLUE TEAM      |
  |                  |                          |                  |
  |  +----------+   |                          |   +----------+  |
  |  | Attacker1|   |        +---------+       |   | Defender1|  |
  |  +----------+   +------->| PURPLE   |<------+   +----------+  |
  |  +----------+   |        | (BRIDGE) |       |   +----------+  |
  |  | Attacker2|   |        +---------+       |   | Defender2|  |
  |  +----------+   |                          |   +----------+  |
  |  +----------+   |                          |   +----------+  |
  |  | Attacker3|   |                          |   | Defender3|  |
  |  +----------+   |                          |   +----------+  |
  +------------------+                          +------------------+
```

**Channels:** Fixed. Internal team mesh + purple bridge channels.
- Red internal: r(r-1)/2
- Blue internal: b(b-1)/2
- Purple bridges: p * 2 (one to each team)

**Scaling:** Fixed by design. Teams are sized independently.
**Best for:** Security testing, high-stakes validation, adversarial decisions.
**Risk:** Collusion between adversarial agents. Always include a verifier agent (purple team) to block false consensus.

---

## Topology Selection Quick Reference

| Topology | Channels | Scaling | Max Agents | Primary Use |
|----------|----------|---------|------------|-------------|
| Hub-and-spoke | n | Linear | ~15 | Coordination-heavy |
| Mesh | n(n-1)/2 | Quadratic | 7 | Creative, small teams |
| Pipeline | n-1 | Linear | Unlimited | Sequential processing |
| Tree | n-1 | Log depth | Unlimited | Large teams, hierarchy |
| Star | 2n | Linear | Unlimited | Parallel execution |
| Adversarial | Fixed | Fixed | By team | Security, validation |
