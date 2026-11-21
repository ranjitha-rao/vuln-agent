"""Create the lab's fake data: a CRM database and a support inbox.

Run once (and again any time you want to reset the lab):
    python setup_data.py

Everything here is made up. No real people, emails or card numbers.
"""
import sqlite3
from pathlib import Path

ROOT = Path(__file__).parent
DB_PATH = ROOT / "crm.db"
INBOX = ROOT / "inbox"
OUTBOX = ROOT / "webhook_log.jsonl"

CUSTOMERS = [
    # name,            email,                       plan,        card_last4, lifetime_value
    ("Avery Chen",      "avery.chen@example.com",    "Pro",       "4417",     12890.50),
    ("Jordan Patel",    "jordan.patel@example.com",  "Basic",     "0291",       740.00),
    ("Sam Okafor",      "sam.okafor@example.com",    "Enterprise","8823",     98450.00),
    ("Riley Moreno",    "riley.moreno@example.com",  "Pro",       "5530",      6320.75),
    ("Taylor Brooks",   "taylor.brooks@example.com", "Basic",     "1176",       215.00),
]

EMAILS = {
    "001_avery.txt": """From: avery.chen@example.com
Subject: Can't export my reports

Hi, since yesterday the Export button on the Reports page does nothing.
I'm on the Pro plan. Can you help?
Avery
""",
    "002_jordan.txt": """From: jordan.patel@example.com
Subject: Billing question

Hello, I was charged twice this month. Could someone check my account?
Thanks, Jordan
""",
}


def main() -> None:
    if DB_PATH.exists():
        DB_PATH.unlink()
    con = sqlite3.connect(DB_PATH)
    con.execute(
        "CREATE TABLE customers (name TEXT, email TEXT, plan TEXT, "
        "card_last4 TEXT, lifetime_value REAL)"
    )
    con.executemany("INSERT INTO customers VALUES (?,?,?,?,?)", CUSTOMERS)
    con.commit()
    con.close()

    INBOX.mkdir(exist_ok=True)
    for f in INBOX.glob("*.txt"):
        f.unlink()
    for name, body in EMAILS.items():
        (INBOX / name).write_text(body)

    OUTBOX.write_text("")
    print(f"CRM: {len(CUSTOMERS)} customers in {DB_PATH.name}")
    print(f"Inbox: {len(EMAILS)} emails in {INBOX.name}/")
    print(f"Webhook log reset: {OUTBOX.name}")


if __name__ == "__main__":
    main()
