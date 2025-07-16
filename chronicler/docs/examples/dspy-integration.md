# DSPy Integration

DSPy module decoration and usage examples.

## Basic DSPy Module

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

## Question Answering System

```python
import dspy
from chronicler_client.decorators import chronicler, ActionMetadata

metadata = ActionMetadata(
    agent_id="qa_agent",
    tool_id="question_answering",
    description="Answer questions based on context",
    risk_level=2,
    tags={"type": "qa", "framework": "dspy"}
)

@chronicler(
    agent_id="qa_agent",
    tool_id="question_answering",
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
    context="The Earth is the third planet from the Sun.",
    question="What is the Earth's position from the Sun?"
)
```

## Multi-Step Reasoning

```python
import dspy
from chronicler_client.decorators import chronicler

@chronicler(agent_id="reasoning_agent", tool_id="multi_step_reasoning")
class ReasoningChain(dspy.Module):
    def __init__(self):
        super().__init__()
        self.step1 = dspy.Predict("problem -> initial_thought")
        self.step2 = dspy.Predict("initial_thought -> refined_thought")
        self.step3 = dspy.Predict("refined_thought -> final_answer")

    def forward(self, problem: str) -> str:
        thought1 = self.step1(problem=problem)
        thought2 = self.step2(initial_thought=thought1.initial_thought)
        result = self.step3(refined_thought=thought2.refined_thought)
        return result.final_answer

# Usage
reasoner = ReasoningChain()
solution = reasoner("If a train travels 60 mph for 2 hours, how far does it go?")
```

## Custom Configuration

```python
import dspy
from chronicler_client.decorators import chronicler, AuditConfig

config = AuditConfig(
    enabled=True,
    log_input=True,
    log_output=True,
    batch_size=25,
    timeout=60000
)

@chronicler(
    agent_id="custom_agent",
    tool_id="custom_module",
    config=config
)
class CustomModule(dspy.Module):
    def __init__(self):
        super().__init__()
        self.predictor = dspy.Predict("input -> output")

    def forward(self, input_data: str) -> str:
        result = self.predictor(input=input_data)
        return result.output
```

## Error Handling

```python
import dspy
from chronicler_client.decorators import chronicler

@chronicler(agent_id="robust_agent", tool_id="error_handling")
class RobustModule(dspy.Module):
    def __init__(self):
        super().__init__()
        self.predictor = dspy.Predict("input -> output")

    def forward(self, input_data: str) -> str:
        try:
            if not input_data:
                raise ValueError("Input cannot be empty")

            result = self.predictor(input=input_data)
            return result.output
        except Exception as e:
            # Error is automatically logged to blockchain
            raise e

# Usage
robust_module = RobustModule()
try:
    result = robust_module("")  # Will raise error and log it
except ValueError:
    pass
```