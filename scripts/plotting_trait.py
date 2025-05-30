import re
from collections import Counter

# Loading the trait file
with open("data/trait_ofgr8dev.txt", "r", encoding="utf-8") as f:
    text = f.read().lower()

# list of key traits
traits = [
    "problem solving", "passionate", "communication", "debugging", "ownership", "domain knowledge",
    "resilience", "teamwork", "consistency", "fast thinker", "documentation",
    "business understanding", "asking questions", "design decisions",'learning'
    "not giving up", "adaptability", "deep thinking" , "articulate", "fast thinkers", "logical"
]

# Count occurrences
counts = Counter()
for trait in traits:
    counts[trait] = len(re.findall(trait, text))

# Filterin traits with at least 1 count
filtered = {k: v for k, v in counts.items() if v > 0}

# Plotting
import matplotlib.pyplot as plt

plt.figure(figsize=(12, 6))
plt.bar(filtered.keys(), filtered.values(), color="skyblue")
plt.xticks(rotation=45, ha="right")
plt.title("Most Mentioned Traits of Great Developers")
plt.xlabel("Trait")
plt.ylabel("Mentions")
plt.tight_layout()
plt.show()
