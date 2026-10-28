# PROPPR - Task 3 Option B: Python Implementation

## Run

```bash
python3 lead_processor.py
```

The implementation is available in [lead_processor.py](lead_processor.py).

## What the Script Does

1. Stores the four supplied sample leads.
2. Normalizes each phone number and retains its last 10 digits.
3. Groups leads by normalized phone number.
4. Keeps the first record in a cleaned list and places repeated records in a duplicate list.
5. Converts `Cr` and `Lakh` values to numeric INR for priority comparisons.
6. Prints each lead with its priority and duplicate status.

## Expected Output

```text
Cleaned leads: 3
101 | Rahul Sharma | Priority | Unique
102 | Priya Mehta | Normal | Unique
104 | Amit Verma | Priority | Unique

Duplicate records:
103 | Rahul Sharma | 9876543210 | Advertisement
```

## Core Logic

```python
if normalized_phone in seen_phones:
    duplicate_records.append(item)
else:
    cleaned_records.append(item)
    seen_phones.add(normalized_phone)

priority_follow_up = (
    location.lower() == "gurgaon"
    and budget_to_inr(budget) >= 15_000_000
)
```

## Verification

The script is validated with assertions for:

- Canonical records: `101`, `102`, and `104`
- Duplicate record: `103`
- Priority records, including their repeated enquiry status: `101`, `103`, and `104`

Run the script successfully in the workspace with Python 3.
