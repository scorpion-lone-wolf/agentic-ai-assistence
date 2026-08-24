# from agent import run_agent_loop

# result = run_agent_loop("Can you give me latest news on black hole research paper?")

# print("LLM says Result : \n", result)

from reflection import run_reflection

task = """
Explain dependency injection to a beginner Python developer.

Requirements:
- Explain why dependency injection exists.
- Include one simple example.
- Mention one disadvantage.
- Keep the answer under 250 words.
"""


result = run_reflection(task)


print("\n========== FINAL ANSWER ==========\n")
print(result)
