import os

dirs = [
    "MediDrishtiAI",
    "MediDrishtiAI/assets",
    "MediDrishtiAI/frontend",
    "MediDrishtiAI/backend",
    "MediDrishtiAI/utils",
    "MediDrishtiAI/tests",
]

for d in dirs:
    os.makedirs(d, exist_ok=True)
    print(f"Created: {d}")

print("All directories created.")
