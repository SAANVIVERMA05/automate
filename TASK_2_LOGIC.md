# PROPPR - Task 2: Automation Logic

## 1. Potential Duplicates

**Leads 101 and 103 are potential duplicates.** Both use normalized phone number `9876543210` and the same name and location. Lead 103 is a second enquiry from a different source, so it is an additional activity rather than a separate customer record by default.

## 2. Preventing Duplicate CRM Records

Before creating a CRM contact, normalize the phone number and search for an existing contact or lead using that value.

If a match exists:

- Update the existing record.
- Add the latest enquiry date and source as an activity.
- Link or preserve the source history.
- Do not create a new CRM lead.

CRM duplicate rules, a unique database constraint, or an idempotent CRM upsert should also enforce this rule. In the sample, 103 should be attached to 101 instead of becoming a second CRM lead.

## 3. Priority Follow-up Logic

Convert budget values to numeric INR before comparison:

```text
IF location equals Gurgaon
AND budget >= 15000000 INR
THEN Priority Follow-up = Yes
ELSE Priority Follow-up = No
```

For ₹1.5 Cr, the numeric amount is ₹15,000,000.

- Lead 101: Priority because Gurgaon and ₹1.5 Cr.
- Lead 103: Priority because Gurgaon and ₹1.5 Cr.
- Lead 104: Priority because Gurgaon and ₹2 Cr.

In a CRM deduplicated view, 101 and 104 are the two resulting lead records. The enquiry from 103 remains linked as an activity to 101. The priority flag should remain visible on both canonical CRM records.

## 4. CRM Unavailable

When the CRM is unavailable, the workflow should:

1. Return an acknowledgement to the source where appropriate.
2. Save the complete event and its ID in a durable queue.
3. Retry with exponential backoff.
4. Alert the operations owner when the configured retry limit is reached.
5. Reconcile the record once service is restored, rather than accepting incoming duplicates as new records.

## 5. Preventing Repeated Processing

Use two protections:

1. **Event idempotency:** Store every unique `event_id` in a processing table before side effects. Mark it `Processing`, then `Completed`. The workflow only creates or updates records when the event is new or resumable.
2. **Business-key uniqueness:** Use normalized phone number as a CRM uniqueness key. A repeated lead can update an existing record instead of creating another one.

If a failure happens after the CRM write but before the Sheet write or completion marker, reconciliation should resume from the missing step instead of rerunning the full workflow.

## Pseudocode

```python
event_id = normalize_event_id(incoming_event.id)
phone = normalize_phone(incoming_event.phone)

if event_already_completed(event_id):
    return "Already processed"

if not claim_event(event_id):
    return "Processing by another execution"

try:
    existing = crm.find_by_phone(phone)

    if existing:
        crm.add_activity(existing.id, incoming_event)
        crm.update(existing.id, latest_details_from(incoming_event))
        lead = existing
    else:
        lead = crm.create_lead(incoming_event)

    lead.priority_follow_up = (
        incoming_event.location.lower() == "gurgaon"
        and budget_to_inr(incoming_event.budget) >= 15_000_000
    )

    sheets.upsert("CRM Lead ID", lead.id, incoming_event)
    mark_event_completed(event_id)
except TemporaryFailure:
    mark_event_for_retry(event_id)
except PermanentFailure:
    mark_event_failed(event_id)
    notify_operations(event_id)
```
