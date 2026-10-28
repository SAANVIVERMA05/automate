#!/usr/bin/env python3

from collections import defaultdict

LEADS = [
    {"lead_id": "101", "name": "Rahul Sharma", "phone": "9876543210", "location": "Gurgaon", "budget": "₹1.5 Cr", "source": "Website"},
    {"lead_id": "102", "name": "Priya Mehta", "phone": "9876543211", "location": "Goa", "budget": "₹90 Lakh", "source": "WhatsApp"},
    {"lead_id": "103", "name": "Rahul Sharma", "phone": "9876543210", "location": "Gurgaon", "budget": "₹1.5 Cr", "source": "Advertisement"},
    {"lead_id": "104", "name": "Amit Verma", "phone": "9876543212", "location": "Gurgaon", "budget": "₹2 Cr", "source": "Website"},
]


def normalize_phone(phone):
    return "".join(character for character in str(phone) if character.isdigit())[-10:]


def budget_in_rupees(value):
    compact = str(value).replace(",", "").lower()
    digits = "".join(character for character in compact if character.isdigit() or character == ".")
    amount = float(digits) if digits else 0
    if "cr" in compact:
        return amount * 100_000_00
    if "lakh" in compact:
        return amount * 100_000
    return amount


def process_leads(leads):
    phone_groups = defaultdict(list)
    cleaned = []
    duplicates = []
    seen_phones = set()

    for lead in leads:
        normalized_phone = normalize_phone(lead["phone"])
        phone_groups[normalized_phone].append(lead)

        item = dict(lead)
        item["normalized_phone"] = normalized_phone
        item["priority_follow_up"] = (
            lead["location"].strip().lower() == "gurgaon"
            and budget_in_rupees(lead["budget"]) >= 1.5 * 100_000_00
        )

        if normalized_phone in seen_phones:
            item["is_duplicate"] = True
            duplicates.append(item)
        else:
            item["is_duplicate"] = False
            cleaned.append(item)
            seen_phones.add(normalized_phone)

    return cleaned, duplicates


def main():
    cleaned, duplicates = process_leads(LEADS)

    print("Cleaned leads:", len(cleaned))
    for lead in cleaned:
        status = "Priority" if lead["priority_follow_up"] else "Normal"
        duplicate_status = "Duplicate" if lead["is_duplicate"] else "Unique"
        print(f"{lead['lead_id']} | {lead['name']} | {status} | {duplicate_status}")

    print("\nDuplicate records:")
    for lead in duplicates:
        print(f"{lead['lead_id']} | {lead['name']} | {lead['phone']} | {lead['source']}")


if __name__ == "__main__":
    main()
