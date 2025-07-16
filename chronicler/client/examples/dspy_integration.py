"""
DSPy integration example for Chronicler decorator
"""

import os
from typing import Any, Dict

import dspy
from chronicler_client.decorators import ActionMetadata, AuditConfig, chronicler
from dspy import Predict, Signature


# Example 1: DSPy Predict with Chronicler decorator
@chronicler(
    agent_id="dspy_agent_001",
    tool_id="text_generator",
    metadata=ActionMetadata(
        agent_id="dspy_agent_001",
        tool_id="text_generator",
        description="Generate text using DSPy",
        risk_level=2,
        tags={"framework": "dspy", "type": "generation"},
    ),
)
class TextGenerator(dspy.Module):
    """Generate text based on a prompt"""

    def __init__(self):
        super().__init__()
        self.predictor = Predict("context -> generated_text")

    def forward(self, context: str) -> str:
        """Generate text from context"""
        result = self.predictor(context=context)
        return result.generated_text


# Example 2: DSPy Signature with Chronicler decorator
@chronicler(
    agent_id="dspy_agent_002",
    tool_id="qa_system",
    config=AuditConfig(enabled=True, log_input=True, log_output=True, batch_size=25),
    metadata=ActionMetadata(
        agent_id="dspy_agent_002",
        tool_id="qa_system",
        description="Question answering system",
        risk_level=1,
        tags={"framework": "dspy", "type": "qa"},
    ),
)
class QASystem(dspy.Module):
    """Question answering system"""

    def __init__(self):
        super().__init__()
        self.predictor = Predict(
            Signature(
                "context, question -> answer",
                "Answer the question based on the given context.",
            )
        )

    def forward(self, context: str, question: str) -> str:
        """Answer question based on context"""
        result = self.predictor(context=context, question=question)
        return result.answer


# Example 3: DSPy Chain with Chronicler decorator
@chronicler(
    agent_id="dspy_agent_003",
    tool_id="text_analyzer",
    metadata=ActionMetadata(
        agent_id="dspy_agent_003",
        tool_id="text_analyzer",
        description="Analyze and summarize text",
        risk_level=2,
        tags={"framework": "dspy", "type": "analysis"},
    ),
)
class TextAnalyzer(dspy.Module):
    """Analyze and summarize text"""

    def __init__(self):
        super().__init__()
        self.summarizer = Predict("text -> summary")
        self.sentiment_analyzer = Predict("text -> sentiment")

    def forward(self, text: str) -> Dict[str, Any]:
        """Analyze text and return summary and sentiment"""
        summary = self.summarizer(text=text).summary
        sentiment = self.sentiment_analyzer(text=text).sentiment

        return {
            "original_text": text,
            "summary": summary,
            "sentiment": sentiment,
            "word_count": len(text.split()),
        }


def run_dspy_examples():
    """Run all DSPy integration examples"""
    print("=== Chronicler DSPy Integration Examples ===\n")

    # Configure DSPy (simplified for demo)
    dspy.settings.configure(lm=None)  # In real usage, configure with actual LM

    # Example 1: Text Generator
    print("1. Text Generator:")
    try:
        generator = TextGenerator()
        # Note: This won't actually work without a configured LM
        # result = generator("Generate a story about a robot")
        # print(f"   Result: {result}")
        print("   (LM not configured - would generate text in real usage)")
        print("   Audit info would be attached to the result")
    except Exception as e:
        print(f"   Error: {e}")
    print()

    # Example 2: QA System
    print("2. QA System:")
    try:
        qa_system = QASystem()
        # Note: This won't actually work without a configured LM
        # result = qa_system("The sky is blue", "What color is the sky?")
        # print(f"   Result: {result}")
        print("   (LM not configured - would answer questions in real usage)")
        print("   Audit info would be attached to the result")
    except Exception as e:
        print(f"   Error: {e}")
    print()

    # Example 3: Text Analyzer
    print("3. Text Analyzer:")
    try:
        analyzer = TextAnalyzer()
        # Note: This won't actually work without a configured LM
        # result = analyzer("This is a sample text for analysis.")
        # print(f"   Result: {result}")
        print("   (LM not configured - would analyze text in real usage)")
        print("   Audit info would be attached to the result")
    except Exception as e:
        print(f"   Error: {e}")
    print()


def demonstrate_decorator_usage():
    """Demonstrate how the decorator works with DSPy"""
    print("=== Decorator Usage Demonstration ===\n")

    # Show how the decorator wraps DSPy modules
    print("The @chronicler decorator wraps DSPy modules to:")
    print("1. Capture input/output data")
    print("2. Log actions to blockchain")
    print("3. Attach audit information to results")
    print("4. Handle errors and failures")
    print()

    print("Example usage:")
    print("@chronicler(")
    print("    agent_id='my_agent',")
    print("    tool_id='my_tool',")
    print("    metadata=ActionMetadata(...)")
    print(")")
    print("class MyDSPyModule(dspy.Module):")
    print("    def forward(self, ...):")
    print("        # Your DSPy logic here")
    print("        return result")
    print()


if __name__ == "__main__":
    # Set up environment variables for testing
    os.environ["REGISTRY_ADDRESS"] = "0x1234567890123456789012345678901234567890"
    os.environ["AUDIT_LOG_ADDRESS"] = "0x2345678901234567890123456789012345678901"
    os.environ["ACCESS_CONTROL_ADDRESS"] = "0x3456789012345678901234567890123456789012"

    run_dspy_examples()
    demonstrate_decorator_usage()
