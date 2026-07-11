# Implementation Plan: operator-contact

## Overview

This plan implements the operator-contact feature through small, incremental changes to four existing files plus the `.env` configuration. Work begins with the pure config parser (the highest-value target for property-based testing), then moves through localization, keyboard verification, and finally the handler that wires everything together. Property-based tests use `hypothesis`; each property from the design is its own sub-task, annotated with its property number and the requirements it validates.

Test dependencies (`pytest`, `hypothesis`) must be available. If they are not already in the project, add them before running tests.

## Tasks

- [x] 1. Configuration: harden admin ID parsing and add the new admin
  - [x] 1.1 Harden the ADMIN_TELEGRAM_IDS parser in `bot/config.py`
    - Extract the inline `ADMIN_TELEGRAM_IDS` list comprehension into a pure function `_parse_admin_ids(raw: str) -> list[int]`
    - Trim surrounding whitespace on each comma-separated entry; skip empty/whitespace-only entries
    - Wrap `int()` conversion in try/except; on `ValueError`, skip the entry and emit `logger.warning` including the offending raw value; continue processing remaining entries
    - Preserve left-to-right order of valid IDs
    - Assign `ADMIN_TELEGRAM_IDS = _parse_admin_ids(os.getenv("ADMIN_TELEGRAM_IDS", ""))` so the module-level list interface is unchanged for consumers
    - _Requirements: 1.1, 1.2, 1.3, 1.4, 1.5, 1.6_

  - [x] 1.2 Append the new admin ID to `.env`
    - Append `8816532579` to the comma-separated `ADMIN_TELEGRAM_IDS` value so it becomes `8536944196,8816532579` (no spaces, no trailing comma)
    - _Requirements: 1.1, 1.2_

  - [ ]* 1.3 Write property test for admin ID order preservation
    - **Property 1: Admin ID parsing preserves all valid IDs in order**
    - Use hypothesis to generate lists of valid integer IDs (length 0–100), join with commas, parse, and assert the result equals the original integer list in order
    - Tag: `# Feature: operator-contact, Property 1: Admin ID parsing preserves all valid IDs in order`
    - **Validates: Requirements 1.2, 1.3**

  - [ ]* 1.4 Write property test for skipping invalid entries
    - **Property 2: Admin ID parsing skips invalid entries without crashing**
    - Use hypothesis to interleave valid integer IDs with blank tokens and non-integer tokens in any order; assert the result is exactly the valid IDs in original relative order, that no exception is raised, and that a warning is emitted for each rejected non-integer token (assert on captured logs)
    - Tag: `# Feature: operator-contact, Property 2: Admin ID parsing skips invalid entries without crashing`
    - **Validates: Requirements 1.4, 1.5**

  - [ ]* 1.5 Write unit tests for parser edge cases
    - Assert `_parse_admin_ids("8536944196,8816532579")` returns `[8536944196, 8816532579]` (both IDs present)
    - Assert `_parse_admin_ids("")` returns `[]`
    - _Requirements: 1.1, 1.6_

- [x] 2. Localization: relabel the button and add operator messages in `bot/localization.py`
  - [x] 2.1 Relabel `btn_support` to the Contact Operator wording for all three languages
    - `uz`: `"📞 Operator bilan bog'lanish"`
    - `ru`: `"📞 Связаться с оператором"`
    - `en`: `"📞 Contact Operator"`
    - Ensure each label is a non-empty string between 1 and 64 characters
    - _Requirements: 2.1, 2.2, 2.3, 2.4_

  - [x] 2.2 Add the `operator_contact` message key for all three languages
    - Include the tappable number `+998 99 058 22 22` in international format (leading `+`, digits after removing spaces) so Telegram renders it as tap-to-call
    - Provide localized uz/ru/en message bodies
    - _Requirements: 3.2, 3.3, 3.4_

  - [x] 2.3 Add the `operator_contact_error` message key for all three languages
    - Localized failure message indicating the operator contact could not be delivered
    - _Requirements: 2.8, 3.7_

  - [ ]* 2.4 Write property test for button label validity and rendering
    - **Property 3: Every supported language has a valid, rendered operator button label**
    - For each supported language (uz, ru, en), assert `get_text("btn_support", lang)` is a non-empty string of length 1–64, and that `get_main_keyboard(lang)` contains that exact label
    - Tag: `# Feature: operator-contact, Property 3: Every supported language has a valid, rendered operator button label`
    - **Validates: Requirements 2.4, 2.5**

  - [ ]* 2.5 Write property test for tap-to-call phone number format
    - **Property 4: The operator phone number is tap-to-call formatted**
    - For each supported language, extract the phone number from `operator_contact`; after removing spaces assert it matches `^\+\d+$`
    - Tag: `# Feature: operator-contact, Property 4: The operator phone number is tap-to-call formatted`
    - **Validates: Requirements 3.2**

  - [ ]* 2.6 Write unit tests for label wording and default-language fallback
    - Assert each language label matches the confirmed wording (2.1–2.3)
    - Assert `get_main_keyboard` built with default language contains the Uzbek label (2.6)
    - _Requirements: 2.1, 2.2, 2.3, 2.6_

- [x] 3. Verify the main keyboard renders the relabeled button
  - [x] 3.1 Verify `get_main_keyboard` in `bot/keyboards/reply.py` wires the button through `get_text`
    - Confirm `get_main_keyboard(lang)` builds the button via `get_text("btn_support", lang)` and requires no structural change (relabeled translation propagates automatically)
    - Make no code change unless verification reveals the button is not wired through `get_text`
    - _Requirements: 2.5, 2.6_

- [x] 4. Checkpoint - Ensure all tests pass
  - Ensure all tests pass, ask the user if questions arise.

- [x] 5. Handler: retarget and rewrite the operator handler in `bot/handlers/start.py`
  - [x] 5.1 Update the handler filter and rename the handler
    - Change `F.text.in_([...])` from the old support labels to the new labels: `"📞 Operator bilan bog'lanish"`, `"📞 Связаться с оператором"`, `"📞 Contact Operator"`
    - Rename `support` to `contact_operator` for clarity
    - Ensure no other handler in the router collides with the new label strings
    - _Requirements: 2.7_

  - [x] 5.2 Implement registered/unregistered branching and localized send with retry
    - Look up the user via `crud.get_user_by_telegram_id`; if `None`, send `please_register` and return without sending the contact message
    - For a registered user, resolve `lang` (fall back to `uz` when language is missing/None)
    - Send `operator_contact` for `lang` together with `get_main_keyboard(lang)` in a single response
    - Wrap the send in a retry loop of at most 3 attempts (1 initial + 2 retries); catch exceptions, log a warning per failed attempt, and after all attempts fail send `operator_contact_error` with the main keyboard preserved
    - Remove the admin-forwarding logic (the loop over `ADMIN_TELEGRAM_IDS`, admin message, and `forward_message`)
    - _Requirements: 3.1, 3.3, 3.4, 3.5, 3.6, 3.7, 2.8_

  - [ ]* 5.3 Write property test for localized message delivery
    - **Property 5: The operator contact message is localized to the user's language**
    - With a mocked DB session returning a registered user and a mocked `Message`, for each supported language assert the handler sends the `operator_contact` text for that language
    - Tag: `# Feature: operator-contact, Property 5: The operator contact message is localized to the user's language`
    - **Validates: Requirements 3.3**

  - [ ]* 5.4 Write property test for unregistered users
    - **Property 6: Unregistered users never receive the operator contact message**
    - With a mocked DB session returning `None`, assert the handler sends the registration prompt and never sends the `operator_contact` message
    - Tag: `# Feature: operator-contact, Property 6: Unregistered users never receive the operator contact message`
    - **Validates: Requirements 3.6**

  - [ ]* 5.5 Write unit tests for retry behavior, single-response wiring, and default language
    - Mock the send to fail 1×, 2×, and 3×; assert success after retries for the first two cases and an `operator_contact_error` message after 3 failures; assert attempts never exceed 3
    - Assert a single `answer` call carries both the contact text and the main keyboard (3.5)
    - Assert a registered user with unknown/None language receives the Uzbek message (3.4)
    - _Requirements: 2.8, 3.4, 3.5, 3.7_

- [x] 6. Final checkpoint - Ensure all tests pass
  - Ensure all tests pass, ask the user if questions arise.

## Notes

- Tasks marked with `*` are optional test sub-tasks and can be skipped for a faster MVP.
- Each task references specific requirements clauses for traceability.
- Property tests use `hypothesis` (minimum 100 iterations) and are tagged with their design property number.
- The config parser (`_parse_admin_ids`) is factored into a pure function specifically to make Properties 1 and 2 testable in isolation.
- Handler property/unit tests rely on mocking the DB session and the aiogram `Message`/bot rather than a live Telegram connection.
- Requirement 3.1 (3-second latency) is an operational concern and is not covered by automated tests.

## Task Dependency Graph

```json
{
  "waves": [
    { "id": 0, "tasks": ["1.1", "1.2", "2.1", "2.2", "2.3", "3.1"] },
    { "id": 1, "tasks": ["1.3", "1.4", "1.5", "2.4", "2.5", "2.6", "5.1"] },
    { "id": 2, "tasks": ["5.2"] },
    { "id": 3, "tasks": ["5.3", "5.4", "5.5"] }
  ]
}
```
