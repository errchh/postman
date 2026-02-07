## ADDED Requirements

### Requirement: Tab navigation
The system SHALL provide tab-based navigation for switching between Event input, Preview output, and History views.

#### Scenario: Tab display on startup
- **WHEN** the application initializes
- **THEN** system displays three tabs: "Event", "Preview", "History"
- **AND** the "Event" tab is active by default

#### Scenario: Tab switching with keyboard
- **WHEN** user presses Tab key
- **THEN** focus moves to the next tab
- **AND** pressing Enter activates the focused tab

#### Scenario: Tab content display
- **WHEN** user activates the "Event" tab
- **THEN** system displays the event input form
- **WHEN** user activates the "Preview" tab
- **THEN** system displays the generated post output

### Requirement: Tab state preservation
The system SHALL preserve form state when switching between tabs.

#### Scenario: State maintained across tabs
- **WHEN** user enters text in Event form
- **AND** switches to Preview tab
- **AND** switches back to Event tab
- **THEN** all form fields retain their previous values
