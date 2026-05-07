# Skill Creation Templates

## Quick Start Template

Use this template to quickly specify a new skill:

```yaml
---
name: [skill-name-kebab-case]
description: [Action verb] [specific functionality] for [domain/file types]. This skill should be used when [specific triggers/scenarios]. [Key differentiation].
---

# [Skill Name]

## Overview
[One paragraph describing what this skill does and when to use it]

## Quick Start
```[language]
# Minimal working example
[5-10 lines showing immediate value]
```

## Core Functionality
### [Feature 1]
[Instructions and code]

### [Feature 2]
[Instructions and code]

## Troubleshooting
- **Issue**: [Common problem]
  **Solution**: [How to fix]
```

## Specialized Templates by Category

### Document Processing Skill

```yaml
---
name: [format]-processor
description: Processes [format] documents including [key operations]. This skill should be used when users need to [primary use case] with [format] files, especially for [specific scenario].
---

# [Format] Processor

## Overview
This skill handles [format] documents, providing capabilities for reading, writing, and transforming content while preserving formatting and metadata.

## Supported Operations

### Reading [Format] Files
```python
from [format]_processor import read_[format]

# Basic reading
document = read_[format]('path/to/file.[ext]')

# With options
document = read_[format]('path/to/file.[ext]', 
                         extract_images=True,
                         preserve_formatting=True)
```

### Extracting Content
```python
# Text extraction
text = document.extract_text()

# Structured extraction
tables = document.extract_tables()
images = document.extract_images()
metadata = document.get_metadata()
```

### Modifying Documents
```python
# Content modification
document.replace_text('old', 'new')
document.add_page(content)
document.remove_page(page_num)

# Formatting
document.apply_style(style_dict)
document.set_margins(top=1, bottom=1, left=1, right=1)
```

### Writing Output
```python
# Save modified document
document.save('output.[ext]')

# Convert to other formats
document.export_as_pdf('output.pdf')
document.export_as_html('output.html')
```

## Advanced Features

### Batch Processing
```python
from [format]_processor import batch_process

results = batch_process(
    input_dir='./documents',
    output_dir='./processed',
    operation=lambda doc: doc.extract_text(),
    parallel=True
)
```

### Validation
```python
# Validate document structure
is_valid = document.validate()

# Check specific requirements
errors = document.check_accessibility()
warnings = document.check_compatibility('version')
```

## Error Handling
```python
try:
    document = read_[format](file_path)
except FileNotFoundError:
    print(f"File not found: {file_path}")
except Invalid[Format]Error as e:
    print(f"Invalid [format]: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

## Resources
- `scripts/[format]_reader.py` - Core reading functionality
- `scripts/[format]_writer.py` - Writing and modification
- `references/[format]_spec.md` - Format specification
- `assets/templates/` - Document templates
```

### Data Transformation Skill

```yaml
---
name: [source]-to-[target]-converter
description: Converts data from [source format] to [target format] with validation and mapping capabilities. This skill should be used when migrating data between [source system] and [target system] or transforming [data type] for [purpose].
---

# [Source] to [Target] Converter

## Overview
Seamlessly transform data from [source format] to [target format] while handling schema differences, data validation, and custom mappings.

## Quick Conversion
```python
from converter import convert

# Simple conversion
result = convert('input.[source_ext]', 'output.[target_ext]')

# With configuration
result = convert(
    source='input.[source_ext]',
    target='output.[target_ext]',
    config={
        'encoding': 'utf-8',
        'validate': True,
        'preserve_types': True
    }
)
```

## Custom Mapping
```python
# Define field mappings
mapping = {
    'source_field': 'target_field',
    'nested.field': 'flat_field',
    'calculated': lambda row: row['field1'] + row['field2']
}

result = convert(source, target, mapping=mapping)
```

## Data Transformation
```python
# Transform during conversion
def transform_row(row):
    row['date'] = parse_date(row['date_string'])
    row['amount'] = float(row['amount_text'].replace('$', ''))
    return row

result = convert(
    source,
    target,
    transform=transform_row,
    validate=True
)
```

## Validation Rules
```python
# Define validation schema
schema = {
    'required_fields': ['id', 'name', 'date'],
    'field_types': {
        'id': int,
        'name': str,
        'date': datetime,
        'amount': float
    },
    'constraints': {
        'amount': lambda x: x >= 0,
        'date': lambda x: x <= datetime.now()
    }
}

result = convert(source, target, schema=schema)
```

## Batch Processing
```python
# Convert multiple files
from converter import batch_convert

results = batch_convert(
    source_pattern='data/*.csv',
    target_dir='converted/',
    target_format='json',
    parallel=True,
    on_error='skip'  # or 'stop', 'log'
)
```

## Error Recovery
```python
# Conversion with error handling
result = convert(
    source,
    target,
    on_error={
        'missing_field': 'use_default',
        'type_mismatch': 'coerce',
        'validation_fail': 'log_and_skip'
    },
    defaults={
        'status': 'pending',
        'created_at': datetime.now()
    }
)

# Check conversion report
print(f"Converted: {result.success_count}")
print(f"Skipped: {result.skip_count}")
print(f"Errors: {result.errors}")
```

## Performance Optimization
```python
# Streaming for large files
from converter import stream_convert

stream_convert(
    source='huge_file.csv',
    target='output.json',
    chunk_size=10000,
    memory_limit='1GB'
)
```

## Resources
- `scripts/converter.py` - Main conversion engine
- `scripts/validators.py` - Validation rules
- `scripts/mappers/` - Format-specific mappers
- `references/format_specs.md` - Format specifications
```

### Automation Skill

```yaml
---
name: [task]-automator
description: Automates [task type] including [key features]. This skill should be used when users need to [use case] automatically, especially for [scenario] or recurring [activity].
---

# [Task] Automator

## Overview
Automate [task description] with scheduling, monitoring, and error recovery capabilities.

## Quick Setup
```python
from automator import Automator

# Create automation
auto = Automator('[task_name]')

# Define workflow
auto.add_step('fetch_data', fetch_function)
auto.add_step('process', process_function)
auto.add_step('notify', notify_function)

# Run once
result = auto.run()

# Schedule recurring
auto.schedule('daily', time='09:00')
```

## Workflow Definition
```python
# Complex workflow with conditions
workflow = {
    'steps': [
        {
            'name': 'check_conditions',
            'action': check_function,
            'on_success': 'process_data',
            'on_failure': 'send_alert'
        },
        {
            'name': 'process_data',
            'action': process_function,
            'retry': 3,
            'timeout': 300
        },
        {
            'name': 'send_alert',
            'action': alert_function,
            'critical': True
        }
    ]
}

auto.load_workflow(workflow)
```

## Event Triggers
```python
# Trigger on events
auto.on_event('file_created', path='/data/incoming/')
auto.on_event('api_webhook', endpoint='/webhook')
auto.on_event('time', schedule='*/15 * * * *')  # Every 15 minutes
auto.on_event('threshold', metric='cpu_usage', value=80)
```

## Monitoring & Alerts
```python
# Add monitoring
auto.add_monitor('execution_time', threshold=60)
auto.add_monitor('error_rate', threshold=0.05)
auto.add_monitor('output_validation', validator=check_output)

# Configure alerts
auto.set_alerts({
    'email': 'admin@example.com',
    'slack': '#automation-alerts',
    'sms': '+1234567890'
})
```

## State Management
```python
# Persistent state across runs
auto.set_state('last_run', datetime.now())
auto.set_state('processed_count', 0)

def process_with_state(context):
    count = context.get_state('processed_count', 0)
    # Process items...
    context.set_state('processed_count', count + processed)
    
auto.add_step('process', process_with_state)
```

## Error Handling & Recovery
```python
# Configure error handling
auto.configure({
    'max_retries': 3,
    'retry_delay': 60,  # seconds
    'failure_mode': 'continue',  # or 'stop', 'rollback'
    'save_checkpoint': True
})

# Custom error handlers
@auto.on_error('DataError')
def handle_data_error(error, context):
    # Clean up bad data
    cleanup_data()
    # Retry with cleaned data
    return 'retry'

@auto.on_error('CriticalError') 
def handle_critical(error, context):
    # Alert immediately
    send_urgent_alert(error)
    # Stop automation
    return 'stop'
```

## Logging & Audit
```python
# Configure logging
auto.set_logging({
    'level': 'INFO',
    'file': 'automation.log',
    'rotation': 'daily',
    'retention': 30  # days
})

# Audit trail
auto.enable_audit(
    store='database',
    include=['inputs', 'outputs', 'errors', 'state_changes']
)
```

## Resources
- `scripts/automator.py` - Core automation engine
- `scripts/schedulers/` - Scheduling backends
- `scripts/monitors/` - Monitoring plugins
- `references/automation_patterns.md` - Best practices
```

### API Integration Skill

```yaml
---
name: [service]-api-client
description: Integrates with [service] API for [operations]. This skill should be used when users need to [use case] with [service], handling authentication, rate limiting, and error recovery.
---

# [Service] API Client

## Overview
Complete integration with [service] API, providing simple methods for common operations and advanced features for complex workflows.

## Quick Start
```python
from [service]_client import Client

# Initialize client
client = Client(api_key='your_api_key')

# Basic operations
data = client.get_[resource]()
result = client.create_[resource](data)
updated = client.update_[resource](id, changes)
client.delete_[resource](id)
```

## Authentication
```python
# API Key
client = Client(api_key='key')

# OAuth2
client = Client(
    client_id='id',
    client_secret='secret',
    redirect_uri='http://localhost:8080/callback'
)
token = client.authorize()

# Custom auth
client = Client(
    auth_handler=custom_auth_function
)
```

## Resource Operations
```python
# Listing with pagination
items = client.list_[resources](
    page=1,
    per_page=100,
    filters={'status': 'active'},
    sort='created_at:desc'
)

# Bulk operations
results = client.bulk_create([item1, item2, item3])
client.bulk_update(updates)
client.bulk_delete(ids)

# Search
results = client.search(
    query='search terms',
    resource_type='[resource]',
    fields=['field1', 'field2']
)
```

## Advanced Queries
```python
# Complex filtering
results = client.query()
    .filter(status='active')
    .filter(created_after='2024-01-01')
    .sort_by('priority', 'desc')
    .limit(50)
    .include(['related1', 'related2'])
    .execute()

# Aggregations
stats = client.aggregate()
    .group_by('category')
    .sum('amount')
    .avg('rating')
    .count()
    .execute()
```

## Rate Limiting & Retry
```python
# Automatic rate limit handling
client.configure(
    rate_limit=100,  # requests per minute
    burst_limit=10,  # burst capacity
    retry_on_rate_limit=True
)

# Custom retry logic
@client.retry(
    max_attempts=3,
    backoff='exponential',
    on_errors=[429, 500, 502, 503, 504]
)
def api_operation():
    return client.critical_operation()
```

## Webhooks
```python
# Register webhook
webhook = client.create_webhook(
    url='https://your-app.com/webhook',
    events=['resource.created', 'resource.updated'],
    secret='webhook_secret'
)

# Handle webhook
from [service]_client import verify_webhook

@app.route('/webhook', methods=['POST'])
def handle_webhook():
    if not verify_webhook(request, 'webhook_secret'):
        return 'Invalid signature', 401
    
    event = request.json
    if event['type'] == 'resource.created':
        handle_new_resource(event['data'])
    
    return 'OK', 200
```

## Caching
```python
# Enable caching
client.enable_cache(
    backend='redis',
    ttl=300,  # seconds
    key_prefix='[service]_api'
)

# Custom cache rules
client.cache_rule(
    resource='[static_resource]',
    ttl=3600
)
client.cache_rule(
    resource='[dynamic_resource]',
    ttl=60
)
```

## Error Handling
```python
from [service]_client import APIError, RateLimitError, AuthError

try:
    result = client.operation()
except AuthError:
    # Refresh token or re-authenticate
    client.refresh_auth()
    result = client.operation()
except RateLimitError as e:
    # Wait and retry
    time.sleep(e.retry_after)
    result = client.operation()
except APIError as e:
    print(f"API error: {e.code} - {e.message}")
```

## Resources
- `scripts/[service]_client.py` - API client implementation
- `scripts/models/` - Resource models
- `references/api_docs.md` - API documentation
- `assets/examples/` - Usage examples
```

## Skill Creation Checklist

Before creating your skill, ensure you have:

### Planning
- [ ] Defined clear, specific scope
- [ ] Listed trigger phrases users will say
- [ ] Identified what the skill does NOT do
- [ ] Checked for existing similar skills
- [ ] Determined skill category and pattern

### Description
- [ ] Started with strong action verb
- [ ] Specified target domain/file types
- [ ] Included "This skill should be used when..."
- [ ] Differentiated from similar skills
- [ ] Kept under 3 sentences

### Documentation
- [ ] Provided immediate value example
- [ ] Organized with clear headers
- [ ] Included practical code examples
- [ ] Added troubleshooting section
- [ ] Used progressive complexity

### Resources
- [ ] Created necessary scripts
- [ ] Added reference documentation
- [ ] Included template files
- [ ] Used correct directory structure
- [ ] Made paths relative, not absolute

### Quality
- [ ] Tested core functionality
- [ ] Handled common errors
- [ ] Validated with edge cases
- [ ] Checked integration points
- [ ] Provided debug mode

### User Experience
- [ ] Made trigger phrases obvious
- [ ] Provided helpful error messages
- [ ] Included sensible defaults
- [ ] Offered customization options
- [ ] Documented all parameters

## Quick Decision Helper

```
What type of skill are you creating?

Is it primarily about...
├─ Creating/generating content?
│  └─ Use Builder Pattern template
├─ Processing/transforming data?
│  └─ Use Data Transformation template
├─ Integrating with external service?
│  └─ Use API Integration template
├─ Automating workflows?
│  └─ Use Automation template
├─ Working with specific file format?
│  └─ Use Document Processing template
└─ Providing knowledge/reference?
   └─ Use Knowledge Base pattern from guide
```
