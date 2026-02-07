## ADDED Requirements

### Requirement: Horizontal platform selector
The system SHALL display platform options in a single horizontal row.

#### Scenario: Horizontal layout display
- **WHEN** the application shows the event form
- **THEN** platform options are displayed in one row
- **AND** options are: LinkedIn, Facebook, Twitter, Instagram
- **AND** all four options are visible simultaneously

#### Scenario: Compact platform selection
- **WHEN** user clicks on a platform option
- **THEN** that platform becomes selected
- **AND** the selection is visually indicated
- **AND** only one platform can be selected at a time

### Requirement: Platform selector keyboard navigation
The system SHALL support keyboard navigation for horizontal platform selection.

#### Scenario: Arrow key navigation
- **WHEN** platform selector has focus
- **AND** user presses Left/Right arrow keys
- **THEN** selection moves to previous/next platform
