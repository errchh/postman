## ADDED Requirements

### Requirement: Two-column field layout
The system SHALL arrange Date and Time fields side-by-side in a two-column layout.

#### Scenario: Side-by-side display
- **WHEN** the event form is displayed
- **THEN** Date field appears on the left
- **AND** Time field appears on the right
- **AND** both fields share the same row

#### Scenario: Responsive fallback
- **WHEN** terminal width is less than 60 columns
- **THEN** Date and Time fields stack vertically
- **AND** each field takes full width
