#!/usr/bin/env python3
"""
Skill Requirement Analyzer
Automated analysis of task requirements to identify needed skills
"""

import json
from typing import Dict, List, TypedDict
from dataclasses import dataclass
from enum import Enum


class SkillCategory(Enum):
    """Categories of skills based on function"""

    INPUT = "input"
    PROCESSING = "processing"
    OUTPUT = "output"
    QUALITY = "quality"
    SUPPORT = "support"
    ENHANCEMENT = "enhancement"


class GapAnalysisResult(TypedDict):
    missing_critical: List[str]
    missing_important: List[str]
    missing_optional: List[str]
    coverage_percentage: float


@dataclass
class SkillRequirement:
    """Represents a required skill for a task"""

    name: str
    category: SkillCategory
    priority: int  # 1=Critical, 2=Important, 3=Nice-to-have
    exists: bool
    description: str
    dependencies: list[str] = list()

    def __post_init__(self):
        if self.dependencies is None:
            self.dependencies = []


class SkillAnalyzer:
    """Analyzes tasks to identify required skills"""

    def __init__(self):
        self.known_skills = self._load_known_skills()
        self.patterns = self._load_patterns()

    def _load_known_skills(self) -> Dict[str, Dict]:
        """Load database of known skills"""
        return {
            # Document skills
            "docx": {"category": "output", "domain": "documents"},
            "pptx": {"category": "output", "domain": "presentations"},
            "pdf": {"category": "processing", "domain": "documents"},
            "xlsx": {"category": "processing", "domain": "spreadsheets"},
            # Development skills
            "html-builder": {"category": "output", "domain": "web"},
            "react-developer": {"category": "output", "domain": "web"},
            "python-developer": {"category": "processing", "domain": "code"},
            # Data skills
            "csv-processor": {"category": "processing", "domain": "data"},
            "json-handler": {"category": "processing", "domain": "data"},
            "sql-executor": {"category": "processing", "domain": "database"},
            # Quality skills
            "validator": {"category": "quality", "domain": "general"},
            "tester": {"category": "quality", "domain": "code"},
            "accessibility-checker": {"category": "quality", "domain": "web"},
        }

    def _load_patterns(self) -> dict[str, list[str]]:
        """Load task patterns and their typical skill requirements"""
        return {
            "create_document": ["docx", "template-manager", "formatter"],
            "build_website": [
                "html-builder",
                "css-styler",
                "js-developer",
                "accessibility-checker",
            ],
            "analyze_data": ["data-reader", "data-cleaner", "analyzer", "visualizer"],
            "automate_workflow": [
                "scheduler",
                "task-runner",
                "error-handler",
                "notifier",
            ],
            "generate_report": [
                "data-collector",
                "analyzer",
                "report-builder",
                "pdf-creator",
            ],
        }

    def analyze_task(self, task_description: str) -> dict:
        """Analyze a task description to identify required skills"""

        # Extract key indicators from task description
        indicators = self._extract_indicators(task_description)

        # Identify required capabilities
        capabilities = self._identify_capabilities(indicators)

        # Map capabilities to skills
        required_skills = self._map_to_skills(capabilities)

        # Analyze gaps
        gaps = self._analyze_gaps(required_skills)

        # Generate recommendations
        recommendations: list[dict[str, str]] = (
            self._generate_recommendations(required_skills, gaps)
        )

        return {
            "task": task_description,
            "indicators": indicators,
            "capabilities": capabilities,
            "required_skills": required_skills,
            "gaps": gaps,
            "recommendations": recommendations,
            "workflow": self._design_workflow(required_skills),
        }

    def _extract_indicators(self, task: str) -> dict[str, list[str]]:
        """Extract key indicators from task description"""
        task_lower = task.lower()

        indicators: dict[str, list[str]] = {
            "actions": [],
            "inputs": [],
            "outputs": [],
            "domains": [],
            "constraints": [],
        }

        # Action keywords
        action_keywords = {
            "create": ["create", "generate", "build", "make", "construct"],
            "analyze": ["analyze", "examine", "investigate", "study", "review"],
            "transform": ["convert", "transform", "translate", "migrate", "port"],
            "optimize": ["optimize", "improve", "enhance", "speed up", "refine"],
            "automate": ["automate", "schedule", "batch", "recurring", "periodic"],
        }

        for action, keywords in action_keywords.items():
            if any(kw in task_lower for kw in keywords):
                indicators["actions"].append(action)

        # Input/Output formats
        formats = {
            "csv": "data",
            "json": "data",
            "xml": "data",
            "pdf": "document",
            "docx": "document",
            "txt": "document",
            "jpg": "image",
            "png": "image",
            "svg": "image",
            "mp4": "video",
            "avi": "video",
            "html": "web",
            "css": "web",
            "js": "web",
        }

        for fmt, domain in formats.items():
            if fmt in task_lower:
                indicators["inputs"].append(fmt)
                indicators["domains"].append(domain)

        # Quality indicators
        if any(word in task_lower for word in ["accessible", "wcag", "a11y"]):
            indicators["constraints"].append("accessibility")
        if any(word in task_lower for word in ["fast", "performance", "speed"]):
            indicators["constraints"].append("performance")
        if any(word in task_lower for word in ["secure", "security", "safe"]):
            indicators["constraints"].append("security")

        return indicators

    def _identify_capabilities(self, indicators: Dict) -> List[str]:
        """Identify required capabilities based on indicators"""
        capabilities = []

        # Map actions to capabilities
        action_mapping = {
            "create": ["generation", "templating", "formatting"],
            "analyze": ["parsing", "calculation", "interpretation"],
            "transform": ["conversion", "mapping", "validation"],
            "optimize": ["profiling", "tuning", "caching"],
            "automate": ["scheduling", "orchestration", "monitoring"],
        }

        for action in indicators["actions"]:
            capabilities.extend(action_mapping.get(action, []))

        # Add domain-specific capabilities
        if "web" in indicators["domains"]:
            capabilities.extend(["html_generation", "css_styling", "js_interaction"])
        if "data" in indicators["domains"]:
            capabilities.extend(["data_loading", "data_cleaning", "data_analysis"])
        if "document" in indicators["domains"]:
            capabilities.extend(["document_parsing", "document_creation", "formatting"])

        # Add constraint-based capabilities
        if "accessibility" in indicators["constraints"]:
            capabilities.append("accessibility_validation")
        if "performance" in indicators["constraints"]:
            capabilities.append("performance_optimization")
        if "security" in indicators["constraints"]:
            capabilities.append("security_scanning")

        return list(set(capabilities))  # Remove duplicates

    def _map_to_skills(self, capabilities: List[str]) -> List[SkillRequirement]:
        """Map capabilities to specific skills"""
        skill_mapping = {
            "generation": ["generator", "builder", "creator"],
            "templating": ["template-engine", "template-manager"],
            "formatting": ["formatter", "styler", "beautifier"],
            "parsing": ["parser", "reader", "extractor"],
            "calculation": ["calculator", "analyzer", "aggregator"],
            "conversion": ["converter", "transformer", "migrator"],
            "validation": ["validator", "checker", "verifier"],
            "scheduling": ["scheduler", "cron-manager", "task-runner"],
            "monitoring": ["monitor", "watcher", "alerter"],
        }

        required_skills = []

        for capability in capabilities:
            # Direct mapping
            if capability in skill_mapping:
                for skill_suffix in skill_mapping[capability]:
                    skill_name = f"{capability.split('_')[0]}-{skill_suffix}"
                    exists = skill_name in self.known_skills

                    required_skills.append(
                        SkillRequirement(
                            name=skill_name,
                            category=self._categorize_skill(capability),
                            priority=self._prioritize_skill(capability),
                            exists=exists,
                            description=f"Handles {capability}",
                        )
                    )
            else:
                # Generic skill for unmapped capabilities
                skill_name = capability.replace("_", "-")
                required_skills.append(
                    SkillRequirement(
                        name=skill_name,
                        category=SkillCategory.PROCESSING,
                        priority=2,
                        exists=False,
                        description=f"Provides {capability} functionality",
                    )
                )

        return required_skills

    def _categorize_skill(self, capability: str) -> SkillCategory:
        """Categorize a skill based on its capability"""
        if any(word in capability for word in ["load", "read", "import"]):
            return SkillCategory.INPUT
        elif any(word in capability for word in ["generation", "creation", "output"]):
            return SkillCategory.OUTPUT
        elif any(word in capability for word in ["validation", "checking", "testing"]):
            return SkillCategory.QUALITY
        elif any(word in capability for word in ["monitoring", "logging", "alerting"]):
            return SkillCategory.SUPPORT
        elif any(word in capability for word in ["optimization", "enhancement"]):
            return SkillCategory.ENHANCEMENT
        else:
            return SkillCategory.PROCESSING

    def _prioritize_skill(self, capability: str) -> int:
        """Determine priority of a skill (1=Critical, 2=Important, 3=Nice-to-have)"""
        critical = ["generation", "parsing", "validation", "conversion"]
        important = ["formatting", "optimization", "monitoring", "scheduling"]

        if any(word in capability for word in critical):
            return 1
        elif any(word in capability for word in important):
            return 2
        else:
            return 3

    def _analyze_gaps(self, required_skills: List[SkillRequirement]) -> GapAnalysisResult:
        """Analyze gaps in skill availability"""
        gaps: GapAnalysisResult = {
            "missing_critical": [],
            "missing_important": [],
            "missing_optional": [],
            "coverage_percentage": 0.0,
        }

        total_skills = len(required_skills)
        existing_skills = sum(1 for skill in required_skills if skill.exists)

        for skill in required_skills:
            if not skill.exists:
                if skill.priority == 1:
                    gaps["missing_critical"].append(skill.name)
                elif skill.priority == 2:
                    gaps["missing_important"].append(skill.name)
                else:
                    gaps["missing_optional"].append(skill.name)

        if total_skills > 0:
            gaps["coverage_percentage"] = (existing_skills / total_skills) * 100

        return gaps

    def _generate_recommendations(
        self, required_skills: List[SkillRequirement], gaps: GapAnalysisResult
    ) -> list[dict[str, str]]:
        """Generate skill recommendations"""
        recommendations: list[dict[str, str]] = []

        # Critical missing skills
        for skill_name in gaps["missing_critical"]:
            recommendations.append(
                {
                    "skill": skill_name,
                    "priority": "HIGH",
                    "action": "CREATE_IMMEDIATELY",
                    "reason": "Critical for core functionality",
                    "alternative": self._find_alternative(skill_name),
                }
            )

        # Important missing skills
        for skill_name in gaps["missing_important"]:
            recommendations.append(
                {
                    "skill": skill_name,
                    "priority": "MEDIUM",
                    "action": "CREATE_SOON",
                    "reason": "Improves quality and efficiency",
                    "alternative": self._find_alternative(skill_name),
                }
            )

        # Optional enhancements
        for skill_name in gaps["missing_optional"]:
            recommendations.append(
                {
                    "skill": skill_name,
                    "priority": "LOW",
                    "action": "CONSIDER",
                    "reason": "Nice-to-have enhancement",
                    "alternative": "Can work without this",
                }
            )

        return recommendations

    def _find_alternative(self, skill_name: str) -> str:
        """Find alternative approach if skill doesn't exist"""
        alternatives = {
            "validator": "Manual validation steps",
            "scheduler": "Manual execution",
            "monitor": "Periodic manual checks",
            "optimizer": "Standard implementation",
            "formatter": "Basic formatting",
        }

        for key, alt in alternatives.items():
            if key in skill_name:
                return alt

        return "Manual workaround required"

    def _design_workflow(self, required_skills: List[SkillRequirement]) -> List[Dict]:
        """Design optimal workflow using required skills"""
        workflow = []

        # Group skills by category for logical flow
        by_category: dict[SkillCategory, List[SkillRequirement]] = {}
        for skill in required_skills:
            if skill.category not in by_category:
                by_category[skill.category] = []
            by_category[skill.category].append(skill)

        # Build workflow in logical order
        category_order = [
            SkillCategory.INPUT,
            SkillCategory.PROCESSING,
            SkillCategory.QUALITY,
            SkillCategory.ENHANCEMENT,
            SkillCategory.OUTPUT,
            SkillCategory.SUPPORT,
        ]

        step = 1
        for category in category_order:
            if category in by_category:
                for skill in by_category[category]:
                    workflow.append(
                        {
                            "step": step,
                            "skill": skill.name,
                            "exists": skill.exists,
                            "purpose": skill.description,
                            "category": category.value,
                        }
                    )
                    step += 1

        return workflow


def main():
    """Example usage of the SkillAnalyzer"""
    analyzer = SkillAnalyzer()

    # Example task
    task = "Create an accessible website with data visualization from CSV files"

    # Analyze the task
    result = analyzer.analyze_task(task)

    # Output results
    print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":
    main()
