# PROPPR - Task 4: Team Communication

## What the Automation Does

When a customer submits an enquiry through the website, WhatsApp, or an advertisement, the automation collects the name, phone number, location, budget, source, and enquiry date. It checks for an existing phone number, creates or updates the CRM record, writes the result to Google Sheets, assigns a team owner, and marks high-value Gurgaon enquiries for priority follow-up.

## How the Team Uses It

1. Open the CRM and review leads assigned to your location or team.
2. Contact priority leads first where practical.
3. Change the status from `New` to:
   - `Contacted` after reaching the customer
   - `Qualified` when there is a clear property requirement and possibility to proceed
   - `Closed` after the sale opportunity is won or lost
4. Review incomplete records in the designated review queue.
5. Treat a repeated enquiry as an additional conversation attached to the existing customer, not as a separate customer record.

## What Happens When Something Goes Wrong

The automation first retries automatically. If a service remains unavailable or a record cannot be processed, the enquiry is kept in a retry/error queue and operations receives an alert. The team can then recover the enquiry from the queue and process it again without creating a duplicate lead.

## Important Limitations

- A phone number is useful for deduplication, but a shared family or workplace number can produce a false match.
- Customers may provide different numbers for separate household members or enquiries.
- Unverified budget or location values may need review.
- Sales status updates remain dependent on team compliance.
- A no-code workflow still requires monitoring, access control, API credentials, and ownership.

## Recommended Improvements

- Add a consent and source-policy review for marketing enquiries.
- Use CRM-managed duplicate warnings for manual review.
- Add a merge-and-history process for confirmed duplicate records.
- Add follow-up deadline reminders and SLA alerts.
- Track automation failures and lead response time on a small operations dashboard.
- Use CRM database-level unique constraints or a third-party deduplication tool when volume grows.
