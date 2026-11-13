# Spec delta: add-agents-opening-questions

Capability: `docs/specs/agents-md-entry-point.md`

## ADDED

### Requirement: opening questions

On Standard and Full, the file SHALL tell the agent to open with the UNDERSTAND questions (what,
where, how big), to skip any the user has already answered, and to state the track and why before
offering options or writing code.

#### Scenario: plain feature request

- GIVEN the request "I need to add user authentication to my app"
- WHEN the agent replies
- THEN the reply asks the unanswered questions and names the track
- AND it contains no options and no code

## REMOVED

- The "Known gap at baseline" section.
