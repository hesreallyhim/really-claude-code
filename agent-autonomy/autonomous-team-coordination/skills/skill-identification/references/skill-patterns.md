# Skill Pattern Reference Guide

## Common Skill Combinations by Domain

### Web Development

#### Frontend Development
```yaml
Essential Skills:
  - html-builder: Structure creation
  - css-framework: Styling system
  - js-components: Interactivity
  - responsive-designer: Mobile optimization

Quality Skills:
  - accessibility-validator: WCAG compliance
  - performance-analyzer: Speed optimization
  - browser-tester: Cross-browser compatibility
  - seo-optimizer: Search visibility

Enhancement Skills:
  - animation-library: Visual effects
  - pwa-converter: Progressive web app
  - i18n-manager: Internationalization
```

#### Full-Stack Application
```yaml
Frontend Layer:
  - react-developer or vue-developer
  - state-manager: Redux/Vuex
  - router: Navigation
  - api-client: Backend communication

Backend Layer:
  - api-builder: REST/GraphQL
  - auth-system: Authentication
  - database-orm: Data management
  - validator: Input validation

Infrastructure Layer:
  - docker-composer: Containerization
  - ci-cd-pipeline: Deployment
  - monitor: Observability
  - logger: Debugging
```

### Data Science & Analytics

#### Data Processing Pipeline
```yaml
Ingestion Stage:
  - csv-reader: Tabular data
  - json-parser: API data
  - sql-connector: Database access
  - web-scraper: Web data

Cleaning Stage:
  - data-cleaner: Missing values, outliers
  - data-validator: Quality checks
  - data-transformer: Format conversion
  - deduplicator: Remove duplicates

Analysis Stage:
  - statistical-analyzer: Descriptive stats
  - ml-modeler: Predictive models
  - time-series-analyzer: Temporal patterns
  - correlation-finder: Relationships

Visualization Stage:
  - chart-generator: Basic plots
  - dashboard-builder: Interactive displays
  - report-creator: PDF/HTML reports
```

#### Machine Learning Project
```yaml
Data Preparation:
  - feature-engineer: Feature creation
  - data-splitter: Train/test/val sets
  - data-augmenter: Synthetic data
  - imbalance-handler: Class balancing

Model Development:
  - model-trainer: Training pipelines
  - hyperparameter-tuner: Optimization
  - cross-validator: Validation
  - ensemble-builder: Model combining

Deployment:
  - model-serializer: Save/load models
  - api-wrapper: Model serving
  - batch-predictor: Bulk inference
  - model-monitor: Drift detection
```

### Content Creation & Management

#### Documentation System
```yaml
Creation Skills:
  - markdown-writer: Technical docs
  - api-doc-generator: API documentation
  - diagram-creator: Visual explanations
  - example-generator: Code samples

Management Skills:
  - version-controller: Change tracking
  - link-checker: Broken link detection
  - search-indexer: Full-text search
  - toc-generator: Navigation

Publishing Skills:
  - static-site-generator: Website creation
  - pdf-exporter: Offline docs
  - epub-creator: E-books
```

#### Blog/CMS Platform
```yaml
Content Skills:
  - post-writer: Article creation
  - image-optimizer: Media handling
  - metadata-manager: SEO tags
  - category-organizer: Taxonomy

Features Skills:
  - comment-system: User engagement
  - rss-generator: Syndication
  - sitemap-creator: Search engines
  - analytics-tracker: Usage metrics
```

### Automation & DevOps

#### CI/CD Pipeline
```yaml
Build Stage:
  - dependency-resolver: Package management
  - compiler: Code compilation
  - bundler: Asset optimization
  - linter: Code quality

Test Stage:
  - unit-tester: Component tests
  - integration-tester: System tests
  - performance-tester: Load testing
  - security-scanner: Vulnerability checks

Deploy Stage:
  - container-builder: Docker images
  - k8s-deployer: Kubernetes
  - secret-manager: Credentials
  - rollback-manager: Recovery
```

#### Infrastructure as Code
```yaml
Provisioning:
  - terraform-writer: Infrastructure definition
  - ansible-playbook: Configuration
  - cloud-cli: Cloud provider APIs

Monitoring:
  - metric-collector: System metrics
  - log-aggregator: Centralized logs
  - alert-manager: Notifications
  - dashboard-creator: Visualization
```

### Creative & Design

#### Graphic Design
```yaml
Creation Tools:
  - vector-designer: Illustrations
  - raster-editor: Photo editing
  - layout-designer: Compositions
  - color-palette: Color schemes

Asset Management:
  - asset-organizer: File structure
  - version-tracker: Design iterations
  - format-converter: File conversions
  - compressor: Size optimization
```

#### Video/Animation
```yaml
Production:
  - storyboard-creator: Planning
  - animation-engine: Motion graphics
  - video-editor: Cutting/transitions
  - audio-mixer: Sound design

Post-Production:
  - color-grader: Color correction
  - effect-applier: Visual effects
  - subtitle-generator: Captions
  - encoder: Format/compression
```

## Skill Dependency Patterns

### Linear Dependencies
```
A → B → C → D
Example: data-reader → cleaner → analyzer → visualizer
Each skill requires the previous one's output
```

### Parallel Processing
```
    ┌→ B →┐
A →→┤     ├→→ E
    └→ C →┘
Example: data-splitter → (trainer | validator) → ensemble
Multiple skills can work simultaneously
```

### Hub Pattern
```
    B
    ↑
A ← D → C
    ↓
    E
Example: api-gateway connecting multiple services
Central skill coordinates others
```

### Layered Architecture
```
╔══════════════╗
║ Presentation ║
╠══════════════╣
║   Business   ║
╠══════════════╣
║     Data     ║
╚══════════════╝
Each layer has specific skill sets
```

## Skill Anti-Patterns (What to Avoid)

### 1. The Kitchen Sink
**Problem**: One skill tries to do everything
```yaml
bad-skill:
  - Reads 20 file formats
  - Processes data
  - Creates visualizations
  - Deploys to cloud
  - Sends notifications
```
**Solution**: Break into focused skills

### 2. The Dependency Hell
**Problem**: Circular or excessive dependencies
```yaml
skill-a: requires skill-b
skill-b: requires skill-c
skill-c: requires skill-a  # Circular!
```
**Solution**: Design clear dependency hierarchy

### 3. The Overlap Confusion
**Problem**: Multiple skills do the same thing
```yaml
pdf-reader: Extracts text from PDFs
pdf-parser: Parses PDF content
pdf-extractor: Gets data from PDFs
```
**Solution**: One skill per capability

### 4. The Missing Link
**Problem**: Skills that can't connect
```yaml
excel-reader: Outputs proprietary format
chart-creator: Expects different format
# No converter skill exists!
```
**Solution**: Include adapter/converter skills

### 5. The Quality Void
**Problem**: No validation or error handling
```yaml
data-pipeline:
  - reader
  - transformer
  - writer
  # No validator or error-handler!
```
**Solution**: Always include quality skills

## Skill Selection Decision Trees

### For Document Tasks
```
Need to work with documents?
├─ Creating new?
│  ├─ Text only? → markdown-writer
│  ├─ Formatted? → docx-creator
│  └─ Presentation? → pptx-builder
├─ Reading existing?
│  ├─ PDF? → pdf-reader
│  ├─ Office? → office-parser
│  └─ Web? → html-extractor
└─ Converting?
   ├─ To PDF? → pdf-converter
   ├─ To HTML? → html-converter
   └─ To Markdown? → md-converter
```

### For API Development
```
Building an API?
├─ REST or GraphQL?
│  ├─ REST → rest-api-builder
│  └─ GraphQL → graphql-schema
├─ Need authentication?
│  ├─ OAuth? → oauth-provider
│  ├─ JWT? → jwt-handler
│  └─ API Keys? → key-manager
├─ Need documentation?
│  ├─ OpenAPI? → swagger-generator
│  └─ Custom? → doc-builder
└─ Need testing?
   ├─ Unit? → api-unit-tester
   ├─ Integration? → api-integration-tester
   └─ Load? → load-tester
```

### For Data Analysis
```
Analyzing data?
├─ What format?
│  ├─ Structured → sql-analyzer
│  ├─ Semi-structured → json-analyzer
│  └─ Unstructured → text-analyzer
├─ What analysis?
│  ├─ Statistical → stats-calculator
│  ├─ Predictive → ml-predictor
│  └─ Exploratory → eda-tool
└─ Output needed?
   ├─ Report → report-generator
   ├─ Dashboard → dashboard-builder
   └─ API → result-api
```

## Skill Ecosystem Examples

### E-commerce Platform
```yaml
Frontend:
  - product-catalog: Display products
  - shopping-cart: Order management
  - checkout-flow: Payment process
  - user-account: Customer portal

Backend:
  - inventory-manager: Stock tracking
  - order-processor: Order fulfillment
  - payment-gateway: Transactions
  - shipping-calculator: Delivery

Support:
  - email-sender: Notifications
  - invoice-generator: Billing
  - analytics-tracker: Metrics
  - review-system: Feedback

Admin:
  - admin-dashboard: Management
  - report-builder: Analytics
  - bulk-updater: Mass changes
  - backup-manager: Data safety
```

### Educational Platform
```yaml
Content:
  - course-builder: Course creation
  - lesson-organizer: Structure
  - quiz-generator: Assessments
  - video-handler: Media

Learning:
  - progress-tracker: Student progress
  - grade-calculator: Scoring
  - certificate-generator: Completion
  - recommendation-engine: Suggestions

Interaction:
  - forum-system: Discussions
  - chat-system: Real-time help
  - assignment-submitter: Homework
  - peer-reviewer: Collaboration

Analytics:
  - engagement-analyzer: Usage patterns
  - performance-reporter: Success metrics
  - dropout-predictor: Risk detection
  - improvement-suggester: Optimization
```

### Healthcare System
```yaml
Patient Management:
  - patient-registry: Records
  - appointment-scheduler: Bookings
  - medical-history: Documentation
  - prescription-manager: Medications

Clinical:
  - diagnosis-assistant: Decision support
  - lab-result-processor: Test results
  - imaging-viewer: Scans/X-rays
  - treatment-planner: Care plans

Compliance:
  - hipaa-validator: Privacy
  - audit-logger: Compliance tracking
  - consent-manager: Permissions
  - data-anonymizer: De-identification

Billing:
  - insurance-verifier: Coverage
  - claim-processor: Billing
  - payment-handler: Transactions
  - statement-generator: Patient bills
```

## Skill Quality Metrics

### Performance Indicators
```yaml
Efficiency:
  - Execution time < threshold
  - Memory usage optimal
  - CPU utilization reasonable
  - I/O operations minimized

Reliability:
  - Error rate < 1%
  - Recovery from failures
  - Consistent outputs
  - Predictable behavior

Usability:
  - Clear error messages
  - Intuitive parameters
  - Good documentation
  - Examples provided

Maintainability:
  - Modular design
  - Version compatibility
  - Update path clear
  - Debug mode available
```

### Success Criteria
```yaml
Adoption:
  - Used in >80% of relevant cases
  - Positive user feedback
  - Reduces task time by >30%
  - Fewer support requests

Integration:
  - Works with related skills
  - Standard data formats
  - Clear interfaces
  - No breaking changes

Evolution:
  - Regular updates
  - Feature additions
  - Bug fixes prompt
  - Community contributions
```

## Skill Creation Triggers

### User Phrases That Indicate Skill Needs

#### Document Processing
- "Convert this PDF to..." → pdf-converter
- "Extract tables from..." → table-extractor
- "Merge these documents..." → document-merger
- "Fill out this form..." → form-filler

#### Data Operations
- "Clean this dataset..." → data-cleaner
- "Find patterns in..." → pattern-analyzer
- "Predict future..." → forecaster
- "Visualize trends..." → trend-visualizer

#### Automation
- "Do this every day..." → scheduler
- "When X happens, do Y..." → event-handler
- "Process all files in..." → batch-processor
- "Monitor and alert..." → monitor-alerter

#### Quality Assurance
- "Check for errors..." → error-checker
- "Validate against..." → validator
- "Test performance..." → performance-tester
- "Ensure accessibility..." → accessibility-checker

## Conclusion

This reference guide provides patterns and combinations for effective skill ecosystems. Remember:

1. **Start Simple**: Begin with core skills, add enhancements later
2. **Think Modular**: Each skill should do one thing well
3. **Plan Integration**: Skills should work together seamlessly
4. **Include Quality**: Always have validation and error handling
5. **Document Well**: Clear descriptions enable discovery
6. **Test Thoroughly**: Verify skills work as intended
7. **Iterate Often**: Improve based on usage patterns
