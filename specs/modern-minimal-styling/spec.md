## ADDED Requirements

### Requirement: Minimal border aesthetic
The system SHALL use subtle, low-contrast borders for all form elements.

#### Scenario: Subtle input borders
- **WHEN** form inputs are displayed
- **THEN** inputs have thin borders in muted gray color (#3d3d4a)
- **AND** borders become accent color (#7aa2f7) on focus

### Requirement: Compact input sizing
The system SHALL use single-line height for text inputs.

#### Scenario: Compact input display
- **WHEN** Input widgets are rendered
- **THEN** height is set to 1 line
- **AND** TextArea for description is 4-5 lines maximum
- **AND** all inputs fit within standard terminal height (24 rows)

### Requirement: Clean spacing
The system SHALL use minimal but consistent spacing between elements.

#### Scenario: Minimal margins
- **WHEN** form groups are displayed
- **THEN** vertical margins are minimized (0 or 1)
- **AND** horizontal padding is consistent
- **AND** visual hierarchy is maintained through spacing
