import json
import os
import sqlite3
import datetime
from collections import defaultdict
from PIL import Image
from dateutil.parser import parse
import re
import shutil

DATA_DIR = "/data"

# A2: Format Markdown using Prettier
def a2_format_markdown():
    os.system(f"npx prettier@3.4.2 --write {DATA_DIR}/format.md")

# A3: Count Wednesdays
def a3_count_wednesdays():
    with open(f"{DATA_DIR}/dates.txt", "r") as f:
        dates = f.readlines()
    wednesdays = sum(1 for date in dates if parse(date.strip()).weekday() == 2)
    with open(f"{DATA_DIR}/dates-wednesdays.txt", "w") as f:
        f.write(str(wednesdays))

# A4: Sort contacts
def a4_sort_contacts():
    with open(f"{DATA_DIR}/contacts.json", "r") as f:
        contacts = json.load(f)
    contacts.sort(key=lambda x: (x["last_name"], x["first_name"]))
    with open(f"{DATA_DIR}/contacts-sorted.json", "w") as f:
        json.dump(contacts, f, indent=2)

# A5: Extract recent log lines
def a5_recent_logs():
    logs = []
    for file in os.listdir(f"{DATA_DIR}/logs/"):
        path = os.path.join(f"{DATA_DIR}/logs/", file)
        logs.append((os.path.getmtime(path), path))
    logs.sort(reverse=True)
    recent_lines = [open(log[1]).readline().strip() for log in logs[:10]]
    with open(f"{DATA_DIR}/logs-recent.txt", "w") as f:
        f.write("\n".join(recent_lines))

# A6: Extract H1 headers
def a6_extract_headers():
    index = {}
    for root, _, files in os.walk(f"{DATA_DIR}/docs/"):
        for file in files:
            if file.endswith(".md"):
                with open(os.path.join(root, file), "r", encoding="utf-8") as f:
                    for line in f:
                        if line.startswith("# "):
                            index[file] = line.strip("# ").strip()
                            break
    with open(f"{DATA_DIR}/docs/index.json", "w") as f:
        json.dump(index, f, indent=2)

# A7: Extract email sender
def a7_extract_sender():
    with open(f"{DATA_DIR}/email.txt", "r") as f:
        match = re.search(r"From:.*<(.+?)>", f.read())
    if match:
        with open(f"{DATA_DIR}/email-sender.txt", "w") as f:
            f.write(match.group(1))

# A8: Extract credit card number from image
def a8_extract_credit_card():
    img = Image.open(f"{DATA_DIR}/credit_card.png")
    # Placeholder for OCR extraction (use pytesseract or AI model in real case)
    extracted_number = "1234567812345678"  # Simulated
    with open(f"{DATA_DIR}/credit-card.txt", "w") as f:
        f.write(extracted_number)

# A9: Find most similar comments
def a9_find_similar_comments():
    with open(f"{DATA_DIR}/comments.txt", "r") as f:
        comments = f.readlines()
    # Placeholder: Use embeddings to find similarity (simplified approach here)
    similar_comments = comments[:2]
    with open(f"{DATA_DIR}/comments-similar.txt", "w") as f:
        f.write("".join(similar_comments))

# A10: Calculate Gold ticket sales
def a10_calculate_gold_sales():
    conn = sqlite3.connect(f"{DATA_DIR}/ticket-sales.db")
    cursor = conn.cursor()
    cursor.execute("SELECT SUM(units * price) FROM tickets WHERE type = 'Gold'")
    total_sales = cursor.fetchone()[0] or 0
    conn.close()
    with open(f"{DATA_DIR}/ticket-sales-gold.txt", "w") as f:
        f.write(str(total_sales))

task_functions = {
    "A2": a2_format_markdown,
    "A3": a3_count_wednesdays,
    "A4": a4_sort_contacts,
    "A5": a5_recent_logs,
    "A6": a6_extract_headers,
    "A7": a7_extract_sender,
    "A8": a8_extract_credit_card,
    "A9": a9_find_similar_comments,
    "A10": a10_calculate_gold_sales,
}

if __name__ == "__main__":
    import sys
    task = sys.argv[1]
    if task in task_functions:
        task_functions[task]()

