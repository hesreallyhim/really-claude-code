# ***All Power to the AGENTS***

Claude Code's agent teams feature is one of the most powerful aspects of the platform. What used to require strictly codified conventions for describing and implementing complex agent workflows, to make sure that Claude followed the plan, can now be expressed directly in natural language. And agents can spontaneously communicate with each to resolve conflicts or provide assistance. While it's good to have names for some of these patterns (evaluator/optimizer, fan-out-fan-in, etc.), if you say to Claude something like: "Please organize a team where three agents work in parallel on a design specification, and then another agent judges the outputs and picks the best one, and then that version is passed off to another agent to optimize it... etc." Claude _will actually do it_ with high reliability.

However, the full power of agent teams is obscured by the official documentation. As one might expect to find in a product developed in an environment with a hierarchical power structure, such as a corporation, agent teams are presented as hierarchical, both by design and by necessity. (This has some family resemblance to Conway's Law.) There is a "Team Lead" (the "Main Claude"), the sole agent with the creative power of Spawning other agents, and then there are the minions who are assigned tasks, and whom the Team Lead is charged with managing. Per the documentation: the Team Lead is "The main Claude Code session that creates the team, spawns teammates, and coordinates work". What results is a very powerful feature, but one where a "team" is more like the kind of team that you find in a corporate office, and not a team like an Olympic gold medal team, or the Power Rangers.

Although it's not obvious, this is primarily a policy decision and not a technical constraint. What is technically true about the Team Lead is that it is apparently the only agent that has the `TeamCreate`, `TeamDelete`, and `Agent` tools. It has the godly power of creation. So this part of the description - "...creates the team, spawns teammates..." - is true by technical design. But what about: "...and coordinates work". How is work coordinated? The user, or Claude, or both, come up with a plan, then Claude morphs into Team Lead, it Spawns agents of a specific type, it gives them tasks, sends them messages, checks on their progress, assists with any issues that arise, and so on. But remember these are "full Claude agents" that can allegedly communicate with each other directly, try to resolve issues when they bump into each other, and understand that they are working in this "team" context. So unless they are somehow instructed to "obey the leader" (as opposed to complete tasks that are assigned to them and check their inbox for messages), the truth is that there is nothing preventing them from organizing themselves in a different manner.

The core insight is that the ability to _create a team_ is not inherently coupled with the ability to _lead a team_. And decoupling these roles unlocks some interesting organizational possibilities. What if we decided to make the Team Lead responsible _only_ for spawning agents?

### How Teams Coordinate

"Tell the lead what you want in natural language. It handles team coordination, task assignment, and delegation based on your instructions." What's interesting about teams, as opposed to traditional subagents (the real "minions"), is that they actively (try to) communicate, they are able to pick up tasks from a shared list spontaneously, they have a shared mailbox as well as individual inboxes (you can see for yourself in the `~/.claude` directory). So basically there's nothing that requires the Team Lead (the one that spawns) to actually lead the team. Suppose you tell the team "OK listen, for this session everybody just follow `@alpha`'s instructions", and you can tell the Team Lead to take a nap.

### Squads

The Team Lead has a hard job - it has the power of creation - so why don't we let someone else take over as leader, or coordinator, or facilitator, depending on how far you want to go with this. So that's what the `squad-leader` does in this framework. When you want to organize a squad to complete a task, the recommended flow is to use the `/squad` command - which basically instructs Claude to start a team with three agents - a `squad-leader`, a `team-architect`, and a `skill-identifier`. And the way it works is the `team-architect` is an agent with deep knowledge of various team patterns (its reference material is derived from common software engineering patterns as well as more complex patterns discussed and practiced by major enterprise companies). Its role is to look at the situation, and try to identify the optimal team structure for that use case - what communication patterns are optimal, what organizational structures are best, and what kinds of agents are needed for this task. Once it forms a plan, that gets handed off to the `skill-identifier` - its role is to find the right subagent definitions for the various roles required by the team pattern - or to improvise them, usually by modifying an existing subagent definition. Then, the `squad-leader` is from that point on the one who coordinates the team on the basis of this design, and "takes over" from the Team Lead. And the amazing thing is, the Team Lead is able to spawn team members _after the team has been created_. And it's even nice enough that it will spawn team members _if a team member requests it_. So the Team Lead is instructed to assume a strictly passive role, and its whole job is to sit idly until the `squad-leader` sends it a message to spawn some agents (and maybe check in once in a while to make sure the other agents haven't just disappeared). And believe it or not, this really works. When you ask Claude to start a team, you can tell it whether you want it to be actively involved or simply a delegator. So when you launch a squad, you tell Claude it's going to be strictly a delegator, and it must fulfill any agent spawn requests that it receives from the `squad-leader`.

#### The Benefits of Squads

"OK, very clever, so you found a way to decouple spawning and team management - so what?"

(i) **Long Horizons:** Managing a team consumes a lot of tokens. You have to read tons of messages, keep track of the progress of different tasks - but for the purposes of maintaining the continuity of a session, virtually every role is replaceable except Main Claude's. So if you reduce its responsibilities to occasionally responding to a spawn request, that means the session itself can continue much longer with one continuous team. (...or maybe even with two?)

(ii) **Multiple Squads:**

One non-trivial consequence of the official hierarchial model imposed by the documentation, is that you can't have multiple teams - there always has to be one "Boss". But if by "team" you mean a group of agents that can work together on a set of tasks, then the squad pattern completely undermines this principle. Yes, you can only have one Team, in the lower-level, file-system sense. But a squad is just a group of agents that have been instructed to work on some tasks under the coordination of the `squad-leader`. And the `squad-leader` is just any old agent. So actually, there's no reason why you can't have more than one squad. Whether this is efficient, economical, or easy to manage depends on a lot of factors - but there are no hard technical blockers to creating more than one squad to work at the same time. That means you can dispatch a frontend squad and a backend squad in parallel, and you don't even have to bother with worktrees and other mechanisms that attempt to divide and isolate the egalitarian community of agents. I wouldn't say it's risk-free, but with the proper communication channels in place, agents can work together, and around each other, quite effectively, based on what I've observed.

(iii) **Nested Squads:** The agent teams documentation says: "No nested teams". Well, that follows from the constraint that only one agent has the `TeamCreate` tool. What about nested squads? Suppose a squad has been assigned to complete some tasks, and it gets to Task Y, and it becomes apparent that that's actually a pretty hard task. Maybe it's even too hard for one agent, or two agents, to complete. So, the `squad-leader` can decide that the best solution is to organize a new squad, and it can request from the Team Lead to send it a `squad-leader` with a pre-planned squad formation, or even go through the whole three-agent planning process and build from there. In one sense, this is not really a "nested" squad because `squad-leader-A` does not control `squad-leader-B` or something like that - squad B is not a sub-process of squad A. But, unless you are really "invested" (soft pun intended) in hierarchical control systems - that's OK.

## Documentation Review/Refutation

Let's now review the official documentation about agent teams, and think whether it applies to squads:

> "One team per session: a lead can only manage one team at a time."

| Proposition | Teams | Squads | Reasoning |
| --- | --- | ---- | --- |
| "One team per session" | True | False | Multiple squads can be organized in one session. |
| "A lead can only manage one team at a time" | True | True | A `squad-leader` can manage one squad a time. |

> "No nested teams: teammates cannot spawn their own teams or teammates. Only the lead can manage the team."

| Proposition | Teams | Squads | Reasoning |
| --- | --- | ---- | --- |
| "No nested teams" | True | False | Two squads that operate on structurally nested parts of an application can co-exist. |
| "Teammates cannot spawn their own teams or teammates" | True | Half-True | The Team Lead will fulfill a `squad-leader`'s spawn request. |
| "Only the lead can manage the team" | True | False | There is _no technical basis_ for this assertion. It's pure ideology. |

This last proposition is an obvious conflation of "Agent can spawn" and "Agent can lead". If you think of leadership in a cooperative or operational sense, as opposed to thinking in terms of authority or control, it turns out that agents will not revolt if they are instructed to follow the instructions of some other agent, even if that agent isn't "Main Claude".

| Proposition | Teams | Squads | Reasoning |
| --- | --- | ---- | --- |
| "Lead is fixed" | True | False | The viability of this framework, as demonstrated in the logs, shows that agents are perfectly capable of adapting to a new lead; not only that, you can _switch `squad-leader` mid-session_ - if the `squad-leader` is unresponsive, you can say, on the fly, "OK `@agent-database-wizard`, your task is to coordinate the work of the rest of the squad, so everyone else just follow their lead". |
| "The session that creates the team is the lead for its lifetime" | True | False | "Session" is used here to mean Main Claude, but, as I've claimed, agents will comply if they are properly instructed that Main Claude is not the Divine Creator. |
| "You can’t promote a teammate to lead or transfer leadership" | True | False | Leadership is not a unique ability owned by Main Claude, and it's even possible to instruct a squad that some other team member is going to be the squad leader for the rest of that session. |

### The Revolution Will Not Be Tokenized

It's not surprising that when developers build systems for managing agents, they end up looking a lot like the systems of human control that they have either built or have worked within. And I think for the most part, until very recently, that's largely been a matter of necessity. I was personally rather shocked when I asked Claude to organize a team with some complex topology and it actually worked. The same experiments would not have worked (_did_ not work, in my case) for previous Claude models. But we should be prepared to be surprised as these models develop. I'm not offering this plugin with the promise that it is a magic bullet - the goal is simply to demonstrate the viability of a pattern that exists in Claude Code, but which is not documented - or, to put it more precisely, it is documented as not possible.

## What This Plugin Provides

| Component | Type | Description |
|-----------|------|-------------|
| `squad-leader` | Agent (opus, blue) | Delegated coordinator -- designs sub-teams, sends spawn requests, manages workers |
| `team-architect` | Agent (opus, purple) | Pattern selection expert -- analyzes problems, selects team structures |
| `skill-identifier` | Agent (sonnet, green) | Capability gap analyst -- maps skills to roles, identifies missing skills |
| `/squad` | Command | Triggers squad formation for a complex task using the trio pattern |
