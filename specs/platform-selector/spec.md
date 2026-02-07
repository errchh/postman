## ADDED Requirements

### Requirement: Platform selection widget
The system SHALL provide a RadioSet widget for selecting the target social media platform.

#### Scenario: Display platform options
- **WHEN** the application initializes the input form
- **THEN** system displays a RadioSet with 4 options: LinkedIn, Facebook, Twitter, Instagram
- **AND** LinkedIn is pre-selected by default

#### Scenario: Platform selection
- **WHEN** user clicks on a platform radio button
- **THEN** system selects that platform
- **AND** deselects previously selected platform

#### Scenario: Keyboard navigation
- **WHEN** platform RadioSet has focus
- **AND** user presses Up/Down arrow keys
- **THEN** system moves selection to previous/next platform

### Requirement: Single selection constraint
The system SHALL enforce single-selection behavior for the platform selector.

#### Scenario: Exclusive selection
- **WHEN** user selects a platform
- **THEN** only that platform is selected
- **AND** all other platforms are deselected

### Requirement: Platform value retrieval
The system SHALL provide the selected platform value for post generation.

#### Scenario: Getting selected platform
- **WHEN** generation is requested
- **THEN** system retrieves the currently selected platform from RadioSet
- **AND** maps it to the corresponding Platform enum value
