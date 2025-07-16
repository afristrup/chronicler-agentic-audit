# Chronicler Decorator: Complete Guide

## Overview

The `@chronicler` decorator is the core integration point for adding blockchain audit logging to your AI agent functions. It automatically captures function inputs, outputs, execution metadata, and logs everything to the blockchain for complete transparency and accountability.

## Table of Contents

- [Basic Usage](#basic-usage)
- [How It Works](#how-it-works)
- [Parameters](#parameters)
- [Configuration Options](#configuration-options)
- [Metadata](#metadata)
- [DSPy Integration](#dspy-integration)
- [Error Handling](#error-handling)
- [Best Practices](#best-practices)
- [Advanced Examples](#advanced-examples)
- [Troubleshooting](#troubleshooting)

## Basic Usage

### Simple Function Decoration

```python
from chronicler_client.decorators import chronicler

@chronicler(agent_id="financial_advisor", tool_id="portfolio_analysis")
def analyze_portfolio(portfolio_data: dict) -> dict:
    # Your AI agent logic here
    risk_score = calculate_risk(portfolio_data)
    recommendations = generate_recommendations(portfolio_data)

    return {
        "risk_score": risk_score,
        "recommendations": recommendations,
        "timestamp": time.time()
    }

# Use the function
result = analyze_portfolio({
    "stocks": ["AAPL", "GOOGL", "MSFT"],
    "amounts": [10000, 15000, 8000]
})
```

### What Gets Logged

When you call the decorated function, the following information is automatically captured and logged to the blockchain:

- **Action ID**: Unique identifier (UUID) for this specific execution
- **Agent ID**: `"financial_advisor"` - identifies which AI agent performed the action
- **Tool ID**: `"portfolio_analysis"` - identifies which specific tool/function was used
- **Input Data**: The arguments passed to the function
- **Output Data**: The result returned by the function
- **Execution Time**: How long the function took to execute
- **Timestamp**: When the action occurred
- **Transaction Hash**: Blockchain transaction identifier
- **Status**: Success or failure status

## How It Works

### The Decorator Pattern

The `@chronicler` decorator uses Python's decorator pattern to wrap your function with audit logging capabilities:

```python
def chronicler(
    agent_id: str,
    tool_id: str,
    config: Optional[AuditConfig] = None,
    metadata: Optional[ActionMetadata] = None,
):
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # 1. Initialize configuration
            # 2. Generate unique action ID
            # 3. Capture input data
            # 4. Execute the function
            # 5. Capture output data
            # 6. Log to blockchain
            # 7. Add audit info to result
            # 8. Return result
        return wrapper
    return decorator
```

### Step-by-Step Process

1. **Configuration Setup**: Initialize audit configuration and metadata
2. **Action ID Generation**: Create a unique UUID for this execution
3. **Input Capture**: Record function arguments if `log_input=True`
4. **Function Execution**: Run your actual AI logic and measure execution time
5. **Output Capture**: Record function result if `log_output=True`
6. **Blockchain Logging**: Hash the data and send to smart contracts
7. **Audit Info Attachment**: Add audit metadata to the result object
8. **Return Result**: Return the original function result with audit info

### Data Flow

```
Function Call → Decorator Wrapper → Input Capture → Function Execution →
Output Capture → Blockchain Logging → Audit Info Attachment → Return Result
```

## Parameters

### Required Parameters

#### `agent_id` (str)
Unique identifier for the AI agent performing the action.

```python
@chronicler(agent_id="trading_bot_v1", tool_id="market_analysis")
def analyze_market(data: dict) -> dict:
    # Trading bot logic
    pass
```

**Best Practices:**
- Use descriptive, meaningful names
- Include version information (e.g., `"trading_bot_v1"`)
- Be consistent across related functions
- Avoid generic names like `"agent"` or `"bot"`

#### `tool_id` (str)
Unique identifier for the specific tool or function being used.

```python
@chronicler(agent_id="medical_ai", tool_id="xray_diagnosis")
def diagnose_xray(image_data: bytes) -> dict:
    # Medical diagnosis logic
    pass
```

**Best Practices:**
- Use specific, descriptive names
- Include the type of operation (e.g., `"risk_assessment"`, `"fraud_detection"`)
- Be consistent with naming conventions
- Avoid generic names like `"process"` or `"analyze"`

### Optional Parameters

#### `config` (AuditConfig)
Configuration object that controls audit logging behavior.

```python
from chronicler_client.decorators import AuditConfig

config = AuditConfig(
    enabled=True,           # Enable/disable audit logging
    log_input=True,         # Log function inputs
    log_output=True,        # Log function outputs
    log_metadata=True,      # Log additional metadata
    batch_size=100,         # Batch size for logging
    ipfs_gateway="https://ipfs.io",  # IPFS gateway for data storage
    timeout=30000,          # Timeout in milliseconds
    retry_attempts=3        # Number of retry attempts
)
```

#### `metadata` (ActionMetadata)
Additional metadata about the action being performed.

```python
from chronicler_client.decorators import ActionMetadata

metadata = ActionMetadata(
    agent_id="financial_advisor",
    tool_id="portfolio_analysis",
    category_id="investment_management",
    risk_level=3,  # 1=Low, 2=Medium, 3=High, 4=Critical
    description="Analyze investment portfolio risk and generate recommendations",
    tags={
        "domain": "finance",
        "type": "analysis",
        "framework": "custom"
    },
    custom_data={
        "regulatory_requirements": ["SOX", "GDPR"],
        "data_sensitivity": "high"
    }
)
```

## Configuration Options

### AuditConfig Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `enabled` | bool | `True` | Enable or disable audit logging |
| `log_input` | bool | `True` | Log function input arguments |
| `log_output` | bool | `True` | Log function output results |
| `log_metadata` | bool | `True` | Log additional metadata |
| `batch_size` | int | `100` | Number of actions to batch before logging |
| `ipfs_gateway` | str | `"https://ipfs.io"` | IPFS gateway for data storage |
| `timeout` | int | `30000` | Timeout in milliseconds |
| `retry_attempts` | int | `3` | Number of retry attempts on failure |

### Configuration Examples

#### Minimal Configuration
```python
@chronicler(
    agent_id="simple_agent",
    tool_id="basic_function"
)
def simple_function(data: str) -> str:
    return data.upper()
```

#### Full Configuration
```python
config = AuditConfig(
    enabled=True,
    log_input=True,
    log_output=True,
    log_metadata=True,
    batch_size=50,
    ipfs_gateway="https://gateway.pinata.cloud",
    timeout=60000,
    retry_attempts=5
)

@chronicler(
    agent_id="enterprise_agent",
    tool_id="critical_analysis",
    config=config
)
def critical_function(data: dict) -> dict:
    # Critical business logic
    pass
```

#### Disabled Audit Logging
```python
config = AuditConfig(enabled=False)

@chronicler(
    agent_id="test_agent",
    tool_id="test_function",
    config=config
)
def test_function(data: str) -> str:
    # Function runs without audit logging
    return data
```

## Metadata

### ActionMetadata Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `agent_id` | str | Yes | Unique agent identifier |
| `tool_id` | str | Yes | Unique tool identifier |
| `category_id` | str | No | Category for grouping related actions |
| `risk_level` | int | No | Risk level (1-4: Low, Medium, High, Critical) |
| `description` | str | No | Human-readable description |
| `tags` | Dict[str, Any] | No | Key-value tags for categorization |
| `custom_data` | Dict[str, Any] | No | Additional custom data |

### Metadata Examples

#### Basic Metadata
```python
metadata = ActionMetadata(
    agent_id="customer_service_bot",
    tool_id="ticket_classification",
    description="Classify customer support tickets by priority and category"
)
```

#### Detailed Metadata
```python
metadata = ActionMetadata(
    agent_id="fraud_detection_system",
    tool_id="transaction_analysis",
    category_id="security",
    risk_level=4,  # Critical
    description="Analyze financial transactions for potential fraud patterns",
    tags={
        "domain": "finance",
        "type": "security",
        "framework": "ml",
        "model_version": "v2.1"
    },
    custom_data={
        "regulatory_compliance": ["PCI-DSS", "SOX"],
        "data_retention_days": 2555,
        "approval_required": True
    }
)
```

#### Industry-Specific Metadata
```python
# Healthcare
healthcare_metadata = ActionMetadata(
    agent_id="diagnostic_ai",
    tool_id="medical_imaging_analysis",
    category_id="healthcare",
    risk_level=4,
    description="Analyze medical images for diagnostic purposes",
    tags={"domain": "healthcare", "type": "diagnostic"},
    custom_data={
        "hipaa_compliant": True,
        "fda_approved": True,
        "medical_specialty": "radiology"
    }
)

# Financial Services
finance_metadata = ActionMetadata(
    agent_id="risk_assessment_engine",
    tool_id="credit_scoring",
    category_id="risk_management",
    risk_level=3,
    description="Calculate credit scores for loan applications",
    tags={"domain": "finance", "type": "risk_assessment"},
    custom_data={
        "regulatory_framework": ["FCRA", "ECOA"],
        "score_range": "300-850",
        "model_accuracy": 0.89
    }
)
```

## DSPy Integration

### Basic DSPy Module

```python
import dspy
from chronicler_client.decorators import chronicler

@chronicler(agent_id="dspy_agent", tool_id="text_generator")
class TextGenerator(dspy.Module):
    def __init__(self):
        super().__init__()
        self.predictor = dspy.Predict("context -> generated_text")

    def forward(self, context: str) -> str:
        result = self.predictor(context=context)
        return result.generated_text

# Usage
generator = TextGenerator()
result = generator("Generate a story about a robot")
```

### Advanced DSPy Module with Configuration

```python
import dspy
from chronicler_client.decorators import chronicler, AuditConfig, ActionMetadata

config = AuditConfig(
    enabled=True,
    log_input=True,
    log_output=True,
    batch_size=25
)

metadata = ActionMetadata(
    agent_id="qa_system",
    tool_id="question_answering",
    description="Answer questions based on provided context",
    risk_level=2,
    tags={"framework": "dspy", "type": "qa"}
)

@chronicler(
    agent_id="qa_system",
    tool_id="question_answering",
    config=config,
    metadata=metadata
)
class QASystem(dspy.Module):
    def __init__(self):
        super().__init__()
        self.predictor = dspy.Predict("context, question -> answer")

    def forward(self, context: str, question: str) -> str:
        result = self.predictor(context=context, question=question)
        return result.answer

# Usage
qa_system = QASystem()
answer = qa_system(
    context="The capital of France is Paris.",
    question="What is the capital of France?"
)
```

### DSPy Chain with Multiple Decorated Modules

```python
import dspy
from chronicler_client.decorators import chronicler

@chronicler(agent_id="document_processor", tool_id="text_extractor")
class TextExtractor(dspy.Module):
    def __init__(self):
        super().__init__()
        self.predictor = dspy.Predict("document -> extracted_text")

    def forward(self, document: str) -> str:
        result = self.predictor(document=document)
        return result.extracted_text

@chronicler(agent_id="document_processor", tool_id="summary_generator")
class SummaryGenerator(dspy.Module):
    def __init__(self):
        super().__init__()
        self.predictor = dspy.Predict("text -> summary")

    def forward(self, text: str) -> str:
        result = self.predictor(text=text)
        return result.summary

@chronicler(agent_id="document_processor", tool_id="document_chain")
class DocumentProcessor(dspy.Module):
    def __init__(self):
        super().__init__()
        self.extractor = TextExtractor()
        self.summarizer = SummaryGenerator()

    def forward(self, document: str) -> str:
        extracted_text = self.extractor(document)
        summary = self.summarizer(extracted_text)
        return summary

# Usage
processor = DocumentProcessor()
summary = processor("Long document text here...")
```

## Error Handling

### Automatic Error Logging

The decorator automatically captures and logs both successful and failed operations:

```python
@chronicler(agent_id="calculator", tool_id="math_operations")
def safe_divide(a: float, b: float) -> float:
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b

# Both success and failure are logged to blockchain
try:
    result = safe_divide(10, 2)  # Success - logged
    print(f"Result: {result}")

    result = safe_divide(10, 0)  # Failure - logged with error details
except ValueError as e:
    print(f"Error: {e}")
```

### Error Information Captured

When an error occurs, the following information is logged:

- **Action ID**: Unique identifier for the failed execution
- **Agent ID**: Which agent was involved
- **Tool ID**: Which tool failed
- **Input Data**: The arguments that caused the failure
- **Error Message**: The exception message
- **Error Type**: The type of exception
- **Timestamp**: When the error occurred
- **Status**: `"failed"`

### Custom Error Handling

```python
@chronicler(agent_id="data_processor", tool_id="validation")
def validate_data(data: dict) -> dict:
    try:
        # Validation logic
        if not data.get("required_field"):
            raise ValueError("Missing required field")

        return {"status": "valid", "data": data}

    except Exception as e:
        # Custom error handling
        error_result = {
            "status": "invalid",
            "error": str(e),
            "error_type": type(e).__name__,
            "timestamp": time.time()
        }

        # The decorator will log this error result
        raise e
```

## Best Practices

### 1. Meaningful Identifiers

**Good:**
```python
@chronicler(agent_id="fraud_detection_v2", tool_id="transaction_risk_assessment")
def assess_transaction_risk(transaction: dict) -> dict:
    pass
```

**Bad:**
```python
@chronicler(agent_id="agent", tool_id="process")
def process(data: dict) -> dict:
    pass
```

### 2. Consistent Naming

Use consistent naming conventions across your application:

```python
# Consistent agent naming
@chronicler(agent_id="customer_service_bot_v1", tool_id="ticket_classification")
def classify_ticket(ticket: dict) -> dict:
    pass

@chronicler(agent_id="customer_service_bot_v1", tool_id="response_generation")
def generate_response(context: dict) -> str:
    pass

@chronicler(agent_id="customer_service_bot_v1", tool_id="escalation_detection")
def detect_escalation(ticket: dict) -> bool:
    pass
```

### 3. Appropriate Risk Levels

Set risk levels based on the potential impact of the action:

```python
# Low risk - simple data processing
@chronicler(
    agent_id="data_processor",
    tool_id="text_normalization",
    metadata=ActionMetadata(risk_level=1)
)
def normalize_text(text: str) -> str:
    return text.lower().strip()

# Medium risk - business logic
@chronicler(
    agent_id="recommendation_engine",
    tool_id="product_recommendations",
    metadata=ActionMetadata(risk_level=2)
)
def recommend_products(user_data: dict) -> list:
    pass

# High risk - financial decisions
@chronicler(
    agent_id="trading_algorithm",
    tool_id="trade_execution",
    metadata=ActionMetadata(risk_level=3)
)
def execute_trade(trade_params: dict) -> dict:
    pass

# Critical risk - medical diagnosis
@chronicler(
    agent_id="medical_ai",
    tool_id="diagnosis_generation",
    metadata=ActionMetadata(risk_level=4)
)
def generate_diagnosis(patient_data: dict) -> dict:
    pass
```

### 4. Sensitive Data Handling

Be careful with sensitive data in audit logs:

```python
# Good - hash sensitive data
@chronicler(agent_id="auth_system", tool_id="password_validation")
def validate_password(password: str) -> bool:
    # Hash password before logging
    hashed_password = hashlib.sha256(password.encode()).hexdigest()

    # The decorator will log the hashed version
    return check_password(password)

# Good - exclude sensitive fields
@chronicler(
    agent_id="user_processor",
    tool_id="profile_update",
    config=AuditConfig(log_input=False)  # Don't log input data
)
def update_user_profile(user_data: dict) -> dict:
    pass
```

### 5. Performance Considerations

```python
# Use batching for high-frequency operations
@chronicler(
    agent_id="high_freq_processor",
    tool_id="data_analysis",
    config=AuditConfig(batch_size=1000)  # Batch 1000 actions
)
def process_data_batch(data_list: list) -> list:
    pass

# Disable logging for performance-critical functions
@chronicler(
    agent_id="performance_critical",
    tool_id="real_time_processing",
    config=AuditConfig(enabled=False)
)
def real_time_function(data: dict) -> dict:
    pass
```

## Advanced Examples

### 1. Financial Services Example

```python
from chronicler_client.decorators import chronicler, AuditConfig, ActionMetadata
import time

# High-risk financial analysis
financial_config = AuditConfig(
    enabled=True,
    log_input=True,
    log_output=True,
    batch_size=10,  # Small batch size for critical operations
    retry_attempts=5
)

financial_metadata = ActionMetadata(
    agent_id="risk_management_system_v2",
    tool_id="portfolio_risk_assessment",
    category_id="risk_management",
    risk_level=4,  # Critical
    description="Assess portfolio risk and generate risk metrics",
    tags={
        "domain": "finance",
        "type": "risk_assessment",
        "regulatory": ["SOX", "Basel III"],
        "model_version": "v2.1.3"
    },
    custom_data={
        "approval_required": True,
        "data_retention_years": 7,
        "audit_trail_required": True
    }
)

@chronicler(
    agent_id="risk_management_system_v2",
    tool_id="portfolio_risk_assessment",
    config=financial_config,
    metadata=financial_metadata
)
def assess_portfolio_risk(portfolio_data: dict) -> dict:
    """
    Assess the risk of an investment portfolio.

    Args:
        portfolio_data: Dictionary containing portfolio information
            - positions: List of investment positions
            - market_data: Current market data
            - risk_parameters: Risk assessment parameters

    Returns:
        Dictionary containing risk assessment results
    """
    start_time = time.time()

    try:
        # Extract portfolio components
        positions = portfolio_data.get("positions", [])
        market_data = portfolio_data.get("market_data", {})
        risk_params = portfolio_data.get("risk_parameters", {})

        # Calculate risk metrics
        var_95 = calculate_value_at_risk(positions, market_data, 0.95)
        var_99 = calculate_value_at_risk(positions, market_data, 0.99)
        expected_shortfall = calculate_expected_shortfall(positions, market_data)
        sharpe_ratio = calculate_sharpe_ratio(positions, market_data)

        # Generate risk assessment
        risk_assessment = {
            "portfolio_id": portfolio_data.get("portfolio_id"),
            "assessment_timestamp": time.time(),
            "risk_metrics": {
                "var_95": var_95,
                "var_99": var_99,
                "expected_shortfall": expected_shortfall,
                "sharpe_ratio": sharpe_ratio
            },
            "risk_level": determine_risk_level(var_95, risk_params),
            "recommendations": generate_risk_recommendations(var_95, risk_params),
            "execution_time": time.time() - start_time
        }

        return risk_assessment

    except Exception as e:
        # Log detailed error information
        error_info = {
            "error_type": type(e).__name__,
            "error_message": str(e),
            "portfolio_id": portfolio_data.get("portfolio_id"),
            "execution_time": time.time() - start_time
        }
        raise e

# Usage
portfolio_data = {
    "portfolio_id": "PORT-001",
    "positions": [
        {"symbol": "AAPL", "quantity": 100, "price": 150.0},
        {"symbol": "GOOGL", "quantity": 50, "price": 2800.0}
    ],
    "market_data": {
        "risk_free_rate": 0.02,
        "market_volatility": 0.15
    },
    "risk_parameters": {
        "max_var": 100000,
        "risk_tolerance": "moderate"
    }
}

try:
    risk_result = assess_portfolio_risk(portfolio_data)
    print(f"Risk Assessment: {risk_result}")
except Exception as e:
    print(f"Risk assessment failed: {e}")
```

### 2. Healthcare Example

```python
from chronicler_client.decorators import chronicler, AuditConfig, ActionMetadata
import hashlib

# Healthcare-specific configuration
healthcare_config = AuditConfig(
    enabled=True,
    log_input=False,  # Don't log patient data directly
    log_output=True,
    batch_size=1,  # Process one at a time for patient safety
    retry_attempts=3
)

healthcare_metadata = ActionMetadata(
    agent_id="diagnostic_ai_system_v3",
    tool_id="medical_imaging_diagnosis",
    category_id="healthcare",
    risk_level=4,  # Critical - medical diagnosis
    description="Analyze medical images for diagnostic purposes",
    tags={
        "domain": "healthcare",
        "type": "diagnostic",
        "specialty": "radiology",
        "model_version": "v3.2.1"
    },
    custom_data={
        "hipaa_compliant": True,
        "fda_approved": True,
        "medical_specialty": "radiology",
        "confidence_threshold": 0.85
    }
)

@chronicler(
    agent_id="diagnostic_ai_system_v3",
    tool_id="medical_imaging_diagnosis",
    config=healthcare_config,
    metadata=healthcare_metadata
)
def diagnose_medical_image(image_data: bytes, patient_metadata: dict) -> dict:
    """
    Analyze medical images for diagnostic purposes.

    Args:
        image_data: Raw medical image data
        patient_metadata: Patient information (anonymized)

    Returns:
        Dictionary containing diagnostic results
    """
    try:
        # Hash patient data for audit trail (HIPAA compliant)
        patient_hash = hashlib.sha256(
            json.dumps(patient_metadata, sort_keys=True).encode()
        ).hexdigest()

        # Analyze the medical image
        analysis_result = analyze_image(image_data)

        # Generate diagnosis
        diagnosis = {
            "patient_hash": patient_hash,  # Anonymized patient identifier
            "image_hash": hashlib.sha256(image_data).hexdigest(),
            "diagnosis": analysis_result.get("diagnosis"),
            "confidence": analysis_result.get("confidence"),
            "findings": analysis_result.get("findings"),
            "recommendations": analysis_result.get("recommendations"),
            "timestamp": time.time(),
            "model_version": "v3.2.1"
        }

        return diagnosis

    except Exception as e:
        # Log error without exposing patient data
        error_info = {
            "error_type": type(e).__name__,
            "error_message": str(e),
            "patient_hash": patient_hash if 'patient_hash' in locals() else None,
            "timestamp": time.time()
        }
        raise e

# Usage
image_data = b"medical_image_data_here"
patient_metadata = {
    "age_group": "adult",
    "gender": "female",
    "exam_type": "chest_xray"
}

try:
    diagnosis_result = diagnose_medical_image(image_data, patient_metadata)
    print(f"Diagnosis: {diagnosis_result}")
except Exception as e:
    print(f"Diagnosis failed: {e}")
```

### 3. E-commerce Recommendation System

```python
from chronicler_client.decorators import chronicler, AuditConfig, ActionMetadata

# E-commerce configuration
ecommerce_config = AuditConfig(
    enabled=True,
    log_input=True,
    log_output=True,
    batch_size=100
)

ecommerce_metadata = ActionMetadata(
    agent_id="recommendation_engine_v1",
    tool_id="product_recommendations",
    category_id="ecommerce",
    risk_level=2,  # Medium risk
    description="Generate personalized product recommendations",
    tags={
        "domain": "ecommerce",
        "type": "recommendation",
        "personalization": True
    },
    custom_data={
        "algorithm": "collaborative_filtering",
        "model_accuracy": 0.78,
        "update_frequency": "daily"
    }
)

@chronicler(
    agent_id="recommendation_engine_v1",
    tool_id="product_recommendations",
    config=ecommerce_config,
    metadata=ecommerce_metadata
)
def generate_recommendations(user_data: dict, product_catalog: dict) -> dict:
    """
    Generate personalized product recommendations.

    Args:
        user_data: User preferences and history
        product_catalog: Available products

    Returns:
        Dictionary containing recommendations
    """
    try:
        # Extract user preferences
        user_id = user_data.get("user_id")
        preferences = user_data.get("preferences", {})
        purchase_history = user_data.get("purchase_history", [])

        # Generate recommendations
        recommendations = []
        for product_id, product_info in product_catalog.items():
            score = calculate_recommendation_score(
                product_info, preferences, purchase_history
            )
            if score > 0.5:  # Threshold for recommendation
                recommendations.append({
                    "product_id": product_id,
                    "score": score,
                    "reason": generate_recommendation_reason(product_info, preferences)
                })

        # Sort by score and limit results
        recommendations.sort(key=lambda x: x["score"], reverse=True)
        top_recommendations = recommendations[:10]

        result = {
            "user_id": user_id,
            "recommendations": top_recommendations,
            "total_products_considered": len(product_catalog),
            "recommendations_generated": len(top_recommendations),
            "timestamp": time.time()
        }

        return result

    except Exception as e:
        error_info = {
            "error_type": type(e).__name__,
            "error_message": str(e),
            "user_id": user_data.get("user_id") if 'user_data' in locals() else None,
            "timestamp": time.time()
        }
        raise e

# Usage
user_data = {
    "user_id": "user_12345",
    "preferences": {
        "category": "electronics",
        "price_range": "100-500",
        "brands": ["Apple", "Samsung"]
    },
    "purchase_history": [
        {"product_id": "phone_001", "rating": 5},
        {"product_id": "laptop_002", "rating": 4}
    ]
}

product_catalog = {
    "phone_001": {"name": "iPhone 15", "category": "electronics", "price": 799},
    "laptop_002": {"name": "MacBook Pro", "category": "electronics", "price": 1299},
    "tablet_003": {"name": "iPad Pro", "category": "electronics", "price": 899}
}

try:
    recommendations = generate_recommendations(user_data, product_catalog)
    print(f"Recommendations: {recommendations}")
except Exception as e:
    print(f"Recommendation generation failed: {e}")
```

## Troubleshooting

### Common Issues

#### 1. Configuration Errors

**Problem**: Decorator not working as expected
```python
# Incorrect
@chronicler(agent_id="my_agent")  # Missing tool_id
def my_function():
    pass
```

**Solution**: Always provide both required parameters
```python
# Correct
@chronicler(agent_id="my_agent", tool_id="my_function")
def my_function():
    pass
```

#### 2. Import Errors

**Problem**: Cannot import decorator
```python
# Incorrect import path
from chronicler import chronicler
```

**Solution**: Use correct import path
```python
# Correct import path
from chronicler_client.decorators import chronicler
```

#### 3. Performance Issues

**Problem**: Slow execution due to audit logging
```python
# High-frequency function with default settings
@chronicler(agent_id="fast_processor", tool_id="data_processing")
def process_data(data: dict) -> dict:
    # Called thousands of times per second
    pass
```

**Solution**: Optimize configuration
```python
# Optimized for high frequency
@chronicler(
    agent_id="fast_processor",
    tool_id="data_processing",
    config=AuditConfig(
        batch_size=1000,  # Larger batch size
        log_input=False,  # Don't log inputs for performance
        log_output=False  # Don't log outputs for performance
    )
)
def process_data(data: dict) -> dict:
    pass
```

#### 4. Memory Issues

**Problem**: Large data causing memory problems
```python
# Large data being logged
@chronicler(agent_id="data_processor", tool_id="large_data_processing")
def process_large_data(large_dataset: list) -> dict:
    # Large dataset being logged to blockchain
    pass
```

**Solution**: Handle large data appropriately
```python
# Hash large data instead of logging it directly
@chronicler(
    agent_id="data_processor",
    tool_id="large_data_processing",
    config=AuditConfig(log_input=False)  # Don't log large inputs
)
def process_large_data(large_dataset: list) -> dict:
    # Hash the dataset for audit trail
    dataset_hash = hashlib.sha256(
        json.dumps(large_dataset, sort_keys=True).encode()
    ).hexdigest()

    result = process_data(large_dataset)
    result["dataset_hash"] = dataset_hash  # Include hash in output

    return result
```

### Debugging Tips

#### 1. Enable Debug Logging

```python
import logging

# Enable debug logging
logging.basicConfig(level=logging.DEBUG)

@chronicler(agent_id="debug_agent", tool_id="debug_function")
def debug_function(data: dict) -> dict:
    logging.debug(f"Processing data: {data}")
    return {"processed": True}
```

#### 2. Check Audit Results

```python
@chronicler(agent_id="test_agent", tool_id="test_function")
def test_function(data: str) -> str:
    result = data.upper()

    # Check if audit info was attached
    if hasattr(result, '_audit_info'):
        print(f"Audit info: {result._audit_info}")

    return result
```

#### 3. Verify Blockchain Logging

```python
@chronicler(agent_id="verification_agent", tool_id="verification_function")
def verification_function(data: dict) -> dict:
    result = {"status": "success", "data": data}

    # The decorator will add audit info
    # You can verify this was logged to blockchain using the transaction hash
    if hasattr(result, '_audit_info'):
        tx_hash = result._audit_info.get('audit_result', {}).get('tx_hash')
        print(f"Transaction hash: {tx_hash}")

    return result
```

## Conclusion

The `@chronicler` decorator provides a powerful and flexible way to add blockchain audit logging to your AI agent functions. By following the best practices outlined in this guide, you can ensure that your AI systems are transparent, accountable, and compliant with regulatory requirements.

Key takeaways:

1. **Always provide meaningful agent_id and tool_id values**
2. **Use appropriate risk levels and metadata for your use case**
3. **Configure audit logging based on your performance and security requirements**
4. **Handle sensitive data appropriately**
5. **Monitor and debug audit logging to ensure it's working correctly**

For more information, see the [API Reference](../api/client/decorators.md) and [Examples](../examples/).