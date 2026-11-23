# Reduce parcel events to latest state

Implement `latest_parcel_state(events)`. Each event is a tuple `(event_id, parcel_id, occurred_at, state)` with string IDs, integer timestamps and string states. Process only the first occurrence of each event ID in input order across the whole feed. For each parcel, choose the remaining event with the greatest pair `(occurred_at, event_id)`, using lexicographic ID order to break ties. Return a dictionary mapping parcel ID to the chosen state. Do not sort or mutate the input. Aim for one pass.

Example. `latest_parcel_state([("z","P",9,"sent"), ("a","P",9,"packed")])` returns `{"P": "sent"}`.
