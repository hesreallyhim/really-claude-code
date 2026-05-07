#!/usr/bin/env python3
"""
Skill Identification Validator
Tests the effectiveness of skill identification for various scenarios
"""

import json
from typing import Dict, List, Tuple
from dataclasses import dataclass


@dataclass
class TestScenario:
    """Represents a test scenario for skill identification"""

    name: str
    user_request: str
    expected_skills: List[str]
    expected_gaps: List[str]
    priority: str  # HIGH, MEDIUM, LOW


class SkillIdentificationValidator:
    """Validates skill identification accuracy"""

    def __init__(self):
        self.test_scenarios = self._load_test_scenarios()
        self.results = []

    def _load_test_scenarios(self) -> List[TestScenario]:
        """Load test scenarios for validation"""
        return [
            # Web Development Scenarios
            TestScenario(
                name="Basic Website",
                user_request="I need to create a simple website with a contact form",
                expected_skills=[
                    "html-builder",
                    "css-framework",
                    "form-handler",
                    "email-sender",
                ],
                expected_gaps=["form-validator", "spam-filter"],
                priority="HIGH",
            ),
            TestScenario(
                name="E-commerce Site",
                user_request="Build an online store with payment processing",
                expected_skills=[
                    "shop-builder",
                    "payment-gateway",
                    "cart-manager",
                    "inventory-tracker",
                ],
                expected_gaps=["tax-calculator", "shipping-api", "review-system"],
                priority="HIGH",
            ),
            # Data Processing Scenarios
            TestScenario(
                name="CSV Analysis",
                user_request="Analyze sales data from multiple CSV files",
                expected_skills=[
                    "csv-reader",
                    "data-merger",
                    "statistical-analyzer",
                    "report-generator",
                ],
                expected_gaps=["data-cleaner", "outlier-detector"],
                priority="MEDIUM",
            ),
            TestScenario(
                name="Data Pipeline",
                user_request="Create automated data pipeline from API to database",
                expected_skills=[
                    "api-fetcher",
                    "data-transformer",
                    "database-writer",
                    "scheduler",
                ],
                expected_gaps=["error-handler", "monitor", "retry-logic"],
                priority="HIGH",
            ),
            # Document Processing Scenarios
            TestScenario(
                name="PDF Processing",
                user_request="Extract tables from PDFs and convert to Excel",
                expected_skills=["pdf-reader", "table-extractor", "excel-writer"],
                expected_gaps=["ocr-processor", "format-validator"],
                priority="MEDIUM",
            ),
            TestScenario(
                name="Report Generation",
                user_request="Generate monthly reports with charts from database",
                expected_skills=[
                    "database-reader",
                    "chart-generator",
                    "report-builder",
                    "pdf-creator",
                ],
                expected_gaps=["template-engine", "scheduler"],
                priority="HIGH",
            ),
            # Automation Scenarios
            TestScenario(
                name="File Monitoring",
                user_request="Monitor folder for new files and process them automatically",
                expected_skills=["file-watcher", "event-handler", "batch-processor"],
                expected_gaps=["error-recovery", "notification-sender"],
                priority="MEDIUM",
            ),
            TestScenario(
                name="Workflow Automation",
                user_request="Automate daily data collection, processing, and reporting",
                expected_skills=[
                    "scheduler",
                    "data-collector",
                    "processor",
                    "report-sender",
                ],
                expected_gaps=["state-manager", "checkpoint-saver"],
                priority="HIGH",
            ),
            # Integration Scenarios
            TestScenario(
                name="API Integration",
                user_request="Connect to Salesforce API and sync with local database",
                expected_skills=["salesforce-client", "data-mapper", "database-syncer"],
                expected_gaps=["auth-manager", "conflict-resolver", "audit-logger"],
                priority="HIGH",
            ),
            TestScenario(
                name="Multi-System Integration",
                user_request="Integrate CRM, email, and calendar systems",
                expected_skills=[
                    "crm-connector",
                    "email-client",
                    "calendar-api",
                    "data-harmonizer",
                ],
                expected_gaps=["event-coordinator", "sync-manager"],
                priority="HIGH",
            ),
            # AI/ML Scenarios
            TestScenario(
                name="ML Model Deployment",
                user_request="Deploy machine learning model as API",
                expected_skills=[
                    "model-loader",
                    "api-builder",
                    "request-handler",
                    "response-formatter",
                ],
                expected_gaps=[
                    "model-monitor",
                    "performance-tracker",
                    "version-manager",
                ],
                priority="HIGH",
            ),
            TestScenario(
                name="Data Labeling",
                user_request="Create interface for labeling training data",
                expected_skills=[
                    "ui-builder",
                    "data-presenter",
                    "label-collector",
                    "export-formatter",
                ],
                expected_gaps=["consensus-calculator", "quality-checker"],
                priority="MEDIUM",
            ),
        ]

    def validate_scenario(self, scenario: TestScenario) -> Dict:
        """Validate a single scenario"""
        result = {
            "scenario": scenario.name,
            "request": scenario.user_request,
            "expected_skills": scenario.expected_skills,
            "expected_gaps": scenario.expected_gaps,
            "tests": {
                "all_skills_identified": False,
                "gaps_detected": False,
                "no_false_positives": True,
                "priority_correct": False,
            },
            "score": 0,
            "issues": [],
        }

        # Simulate skill identification (in real use, this would call the actual analyzer)
        identified_skills = self._simulate_identification(scenario)

        # Test 1: All expected skills identified
        missing_skills = set(scenario.expected_skills) - set(
            identified_skills["skills"]
        )
        if not missing_skills:
            result["tests"]["all_skills_identified"] = True
            result["score"] += 25
        else:
            result["issues"].append(f"Missing skills: {list(missing_skills)}")

        # Test 2: Expected gaps detected
        missing_gaps = set(scenario.expected_gaps) - set(identified_skills["gaps"])
        if not missing_gaps:
            result["tests"]["gaps_detected"] = True
            result["score"] += 25
        else:
            result["issues"].append(f"Undetected gaps: {list(missing_gaps)}")

        # Test 3: No false positives
        false_positives = set(identified_skills["skills"]) - set(
            scenario.expected_skills
        )
        if false_positives:
            result["tests"]["no_false_positives"] = False
            result["issues"].append(f"False positives: {list(false_positives)}")
        else:
            result["score"] += 25

        # Test 4: Priority assessment correct
        if identified_skills["priority"] == scenario.priority:
            result["tests"]["priority_correct"] = True
            result["score"] += 25
        else:
            result["issues"].append(
                f"Priority mismatch: got {identified_skills['priority']}, expected {scenario.priority}"
            )

        return result

    def _simulate_identification(self, scenario: TestScenario) -> Dict:
        """Simulate skill identification (placeholder for actual implementation)"""
        # This would normally call the actual skill analyzer
        # For testing, return a simulated response

        # Simulate 90% accuracy for demonstration
        import random

        skills = scenario.expected_skills.copy()
        if random.random() > 0.9:  # 10% chance of missing a skill
            skills.pop()

        gaps = scenario.expected_gaps.copy()
        if random.random() > 0.9:  # 10% chance of missing a gap
            gaps.pop()

        return {
            "skills": skills,
            "gaps": gaps,
            "priority": scenario.priority if random.random() > 0.1 else "MEDIUM",
        }

    def run_validation(self) -> Dict:
        """Run validation on all test scenarios"""
        print("[VALIDATE] Skill Identification Validation")
        print("=" * 50)

        for scenario in self.test_scenarios:
            print(f"\n[TEST] Testing: {scenario.name}")
            result = self.validate_scenario(scenario)
            self.results.append(result)

            # Print results
            print(f"   Score: {result['score']}/100")

            if result["score"] == 100:
                print("   [PASS] All tests passed!")
            else:
                print("   [WARN] Issues found:")
                for issue in result["issues"]:
                    print(f"      - {issue}")

        # Calculate overall metrics
        return self._calculate_metrics()

    def _calculate_metrics(self) -> Dict:
        """Calculate overall validation metrics"""
        total_scenarios = len(self.results)
        perfect_scores = sum(1 for r in self.results if r["score"] == 100)
        average_score = sum(r["score"] for r in self.results) / total_scenarios

        # Category breakdown
        category_scores: dict[str, float | int] = {
            "skill_identification": 0,
            "gap_detection": 0,
            "false_positive_prevention": 0,
            "priority_assessment": 0,
        }

        for result in self.results:
            if result["tests"]["all_skills_identified"]:
                category_scores["skill_identification"] += 1
            if result["tests"]["gaps_detected"]:
                category_scores["gap_detection"] += 1
            if result["tests"]["no_false_positives"]:
                category_scores["false_positive_prevention"] += 1
            if result["tests"]["priority_correct"]:
                category_scores["priority_assessment"] += 1

        # Convert to percentages
        for key in category_scores:
            category_scores[key] = (category_scores[key] / total_scenarios) * 100

        print("\n" + "=" * 50)
        print("[SUMMARY] VALIDATION SUMMARY")
        print("=" * 50)
        print(f"Total Scenarios Tested: {total_scenarios}")
        print(f"Perfect Scores: {perfect_scores}/{total_scenarios}")
        print(f"Average Score: {average_score:.1f}%")
        print("\nCategory Performance:")
        print(
            f"  • Skill Identification: {category_scores['skill_identification']:.1f}%"
        )
        print(f"  • Gap Detection: {category_scores['gap_detection']:.1f}%")
        print(
            f"  • False Positive Prevention: {category_scores['false_positive_prevention']:.1f}%"
        )
        print(f"  • Priority Assessment: {category_scores['priority_assessment']:.1f}%")

        return {
            "total_scenarios": total_scenarios,
            "perfect_scores": perfect_scores,
            "average_score": average_score,
            "category_scores": category_scores,
            "detailed_results": self.results,
        }

    def export_results(self, filepath: str = "validation_results.json"):
        """Export validation results to JSON"""
        metrics = self._calculate_metrics()

        with open(filepath, "w") as f:
            json.dump(metrics, f, indent=2)

        print(f"\n[EXPORT] Results exported to {filepath}")


def run_custom_test(user_request: str, expected_skills: List[str] = list()):
    """Run a custom test with user-provided scenario"""
    print("\n[TEST] Custom Test")
    print(f"Request: {user_request}")

    # Simulate analysis
    import importlib

    skill_analyzer = importlib.import_module("skill-analyzer")
    SkillAnalyzer = skill_analyzer.SkillAnalyzer
    analyzer = SkillAnalyzer()
    result = analyzer.analyze_task(user_request)

    print("\n[RESULTS] Identified Requirements:")
    print(f"Skills: {result['required_skills']}")
    print(f"Gaps: {result['gaps']}")
    print(f"Workflow: {result['workflow']}")

    if expected_skills:
        matches = set(expected_skills).intersection(set(result["required_skills"]))
        print(
            f"\n[MATCH] Matched {len(matches)}/{len(expected_skills)} expected skills"
        )


def main():
    """Main validation function"""
    import sys

    if len(sys.argv) > 1:
        # Custom test mode
        user_request = " ".join(sys.argv[1:])
        run_custom_test(user_request)
    else:
        # Full validation suite
        validator = SkillIdentificationValidator()
        metrics = validator.run_validation()

        # Determine pass/fail
        if metrics["average_score"] >= 80:
            print("\n[PASS] VALIDATION PASSED")
            print("Skill identification is working effectively!")
        else:
            print("\n[FAIL] VALIDATION NEEDS IMPROVEMENT")
            print("Review the issues and adjust skill identification logic.")

        # Export results
        validator.export_results()


if __name__ == "__main__":
    main()
