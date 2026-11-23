# Independent business UAT and stakeholder sign-off protocol

**Status: NOT EXECUTED.** This file defines the independent acceptance process; it is not a completed test report or a sign-off.

## Independence requirements
1. Tester must not be the project author and should have relevant workflow exposure. Record role category and organisation type only where permitted.
2. Tester receives a frozen build identifier, controlled synthetic test data and the UAT scripts. The author may explain the environment but must not coach test execution.
3. Tester records each UAT-01 to UAT-12 result in `data/templates/uat_execution_log_template.csv`.
4. Capture evidence reference for every pass/fail/block. A verbal “looks good” without execution is not a pass.
5. Critical/high defects block acceptance until fixed and retested by the tester.
6. Price-parity scenarios require an approved reference-rate set; synthetic prices cannot be signed off as company parity.
7. Business owner signs only the process areas they are authorised to accept. Technical test completion is not business acceptance.

## Required sign-off fields
- Build/version and test environment
- Tester name or private identity reference (keep private; publish role only with consent)
- Business process owner and authority basis
- UAT case IDs executed, passed, failed, blocked and not run
- Open defects, severity, owners and retest references
- Data scope and privacy/security review
- Explicit acceptance, conditional acceptance or rejection
- Conditions, exclusions and expiry/review date
- Date and retained approval evidence reference

## Decision rule
- **Accept:** all critical workflow cases passed, no open critical/high defect, price parity separately accepted where applicable, and accountable process owner signs.
- **Conditional accept:** only low/medium defects remain with documented workaround, owner and due date; process owner explicitly accepts the residual risk.
- **Reject / defer:** any critical/high defect, missing approval authority, unauthorised access, unresolved pricing integrity issue or absent evidence.

A completed automated test suite cannot substitute for independent UAT. A blank sign-off template cannot be described as stakeholder approval.
