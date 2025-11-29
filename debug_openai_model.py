from pydantic_ai.models.openai import OpenAIModel
import inspect

print(inspect.signature(OpenAIModel.__init__))
print(OpenAIModel.__init__.__doc__)
