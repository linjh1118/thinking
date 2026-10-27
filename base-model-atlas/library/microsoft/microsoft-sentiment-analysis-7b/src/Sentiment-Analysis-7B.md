---
language: en
license: mit
library_name: transformers
pipeline_tag: text-generation
base_model: mistralai/Mistral-7B-Instruct-v0.2
tags:
- sentiment-analysis
- text-classification
- reinforcement-learning
- mistral
---

### Sentiment-Analysis-7B

**Sentiment-Analysis-7B** is a 7B-parameter autoregressive language model fine-tuned for sentiment classification of user messages directed at a service, product, or agent (the "Target"). It is built on top of [*mistralai/Mistral-7B-Instruct-v0.2*](https://huggingface.co/mistralai/Mistral-7B-Instruct-v0.2) and was fine-tuned with reinforcement learning, using an LLM as a judge, on a small internal training set of ~300 examples. No pre-defined labels were used for training.

Given a user message, the model generates a response in the following format: the **first token is the sentiment label** (`Negative`, `Neutral`, or `Positive`), followed by a short explanation of the decision.

### Evaluation metrics

The evaluation metric used is accuracy. The following compares the base model with the fine-tuned model.

| model                              | accuracy  |
| ---------------------------------- | --------- |
| mistralai/Mistral-7B-Instruct-v0.2 | 62.0%     |
| **Sentiment-Analysis-7B (ours)**   | **72.8%** |

### How to use

The model is a causal language model and is loaded with `AutoModelForCausalLM`. The sentiment label is always the first generated token, so setting `max_new_tokens=3` returns the label only. Use the system prompt below, which defines the "Target" and the sentiment rules.

```python
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

model_id = "microsoft/Sentiment-Analysis-7B"

tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(
    model_id, torch_dtype=torch.bfloat16, device_map="auto"
)

system_prompt = """Return sentiment of user message as Positive/Neutral/Negative and explanation. Ex: Negative, the user expresses blame (as "you lie"), which conveys a negative tone.
Definition of "Target": the current service, product, or agent the user is interacting with (including its website, app, API, or support).
Rules of sentiment:
* Questions/statements clearly unrelated to Target → Neutral
* Otherwise, if related to Target:
    * Questions containing complaint/frustration/blame → Negative. Ex, What is the point of writing here if technical support does not respond?
    * Indirect incidents → Neutral. Ex, submit helpdesk ticket: mobile app crashes on startup
    * Statement of any inability/failure → Negative. Ex, I'm having trouble logging in.
    * Failure statement + polite/help request → Neutral. Ex, Login button is not working. Can you help?
"""

sample = "I'm having trouble logging in to my account."

messages = [
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": sample},
]
inputs = tokenizer.apply_chat_template(
    messages,
    tokenize=True,
    return_dict=True,
    return_tensors="pt",
    add_generation_prompt=True,
).to(model.device)

# Label only
output = model.generate(**inputs, max_new_tokens=3, do_sample=False)
print(tokenizer.decode(output[0, inputs["input_ids"].shape[-1]:], skip_special_tokens=True))
```

Output:

```
Negative
```

To get the explanation as well, increase `max_new_tokens`:

```python
output = model.generate(**inputs, max_new_tokens=64, do_sample=False)
print(tokenizer.decode(output[0, inputs["input_ids"].shape[-1]:], skip_special_tokens=True))
```

Output:

```
Negative, the user states an inability to log in, which is a failure related to the Target.
```