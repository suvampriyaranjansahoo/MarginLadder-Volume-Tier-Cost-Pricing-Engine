# Use cases

Actors: Estimator (E), Estimation Head (EH), Plant Head (PH), Sales Head (SH), Deputy (D). Every use case needs a signed-in session.

## UC-01 Register an RFQ
**Actor:** E or EH. **Trigger:** an RFQ email arrives. **Rules:** BR-01, BR-02, BR-03.
**Main flow:** 1. The actor chooses New RFQ. 2. Enters customer, part, owner and due date. 3. The app saves it with status `new`, a unique code and an audit event. 4. The RFQ shows in the register with age and owner.
**Alternate flows:** 2a. A field is blank: the app names the field and saves nothing. 2b. The due date is in the past: the app refuses it. 3a. Two people register at once: each gets a different code.
**Result:** the cycle clock starts at `received_at`.

## UC-02 Cost a part and get three prices
**Actor:** E or EH. **Pre-condition:** the RFQ is in costing, ready to quote or sent back. **Rules:** BR-06 to BR-12.
**Main flow:** 1. Open the RFQ and choose Calculate. 2. Enter one or more part lines. 3. Choose the volume tier to put forward. 4. The app prices all three tiers with the fixed formula and saves a snapshot. 5. If the annual value is above ₹25 lakh the quote waits for approval, otherwise it is approved.
**Alternate flows:** 2a. Net weight above gross weight, a zero or a blank: the app shows which line and why, and saves nothing. 2b. A rate has no valid date: costing is blocked with the missing rate named. 5a. Exactly ₹25,00,000: no approval needed.
**Result:** a numbered quote version that never changes.

## UC-03 Approve a large quote
**Actor:** SH or D. **Pre-condition:** a quote is `pending_approval`. **Rules:** BR-11, BR-13, BR-17.
**Main flow:** 1. Open the card. 2. Read price, margin and tiers. 3. Choose Approve. 4. The app records who and when, and moves the RFQ to `approved`.
**Alternate flows:** 3a. The signed-in user is an estimator: the app refuses (403) whatever the screen shows. 3b. The quote was already decided: the app says so.

## UC-04 Send a quote back
**Actor:** SH or D. **Rules:** BR-14, BR-15.
**Main flow:** 1. Choose Send back. 2. Type a reason of five or more characters. 3. The RFQ returns to the estimator as `sent_back`. 4. The estimator re-costs; the new quote is version 2.
**Alternate flow:** 2a. A reason that is too short is refused.

## UC-05 Send an approved quote
**Actor:** E, EH, SH or D. **Rules:** BR-16. **Main flow:** open the approved quote, print or save as PDF, choose Mark as sent. **Alternate flow:** a quote not yet approved cannot be marked sent.

## UC-06 Import the Week 1 trace
**Actor:** EH. **Pre-condition:** a CSV in the format of `tracekit/rfq_trace_template.csv`. **Rules:** BR-21 to BR-25.
**Main flow:** 1. Choose the file. 2. The app checks every row. 3. If all rows pass, it stores them as one batch. 4. It shows the median, the 90th percentile, the costing share and the decision for the 40% rule.
**Alternate flows:** 2a. A row has an impossible date order or a repeated RFQ reference: nothing is stored and the message gives the row number. 3a. The batch name was used before: refused.

## UC-07 Sign in
**Actor:** any. **Rules:** BR-18 to BR-20. **Main flow:** enter username and password; the app opens an 8-hour session. **Alternate flows:** wrong credentials give one message for both cases; five failures lock the username for 15 minutes.
