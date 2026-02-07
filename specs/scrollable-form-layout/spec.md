## ADDED Requirements

### Requirement: Scrollable form container
The system SHALL provide a scrollable container for form content that allows users to access all form fields regardless of terminal size.

#### Scenario: Form content overflows terminal height
- **WHEN** the form content exceeds the available terminal height
- **THEN** the system SHALL display a scrollable container with all form fields accessible
- **AND** scrollbars SHALL appear when content overflows

#### Scenario: Small terminal layout
- **WHEN** the terminal height is below 24 rows
- **THEN** the system SHALL wrap form fields in a VerticalScroll container
- **AND** all form fields SHALL remain accessible through scrolling

### Requirement: Fixed-position action buttons
The system SHALL position action buttons (Generate, Copy, Exit) outside the scrollable area at the bottom of the input panel.

#### Scenario: Buttons remain visible during scrolling
- **WHEN** users scroll through form content
- **THEN** the action buttons SHALL remain fixed at the bottom of the input panel
- **AND** buttons SHALL NOT move or disappear during scrolling

#### Scenario: Button accessibility
- **WHEN** form content is scrolled to any position
- **THEN** all action buttons SHALL remain visible and clickable
- **AND** button functionality SHALL work regardless of scroll position

### Requirement: Independent form field scrolling
The system SHALL allow form fields to scroll independently within the scrollable area while maintaining the overall layout structure.

#### Scenario: Form field navigation
- **WHEN** users navigate through form fields using keyboard or mouse
- **THEN** focus SHALL move correctly between fields within the scrollable container
- **AND** the view SHALL scroll to keep focused fields visible

#### Scenario: Scroll behavior consistency
- **WHEN** users scroll using arrow keys, page up/down, or mouse wheel
- **THEN** scrolling behavior SHALL be consistent and predictable
- **AND** the scrollable area SHALL respond immediately to input

### Requirement: Layout structure updates
The system SHALL update the CSS and component structure to support the new scrollable layout with proper overflow handling.

#### Scenario: CSS styling for scrollable container
- **WHEN** the scrollable form layout is rendered
- **THEN** the system SHALL apply appropriate CSS for overflow handling
- **AND** scrollbars SHALL be styled consistently with the TUI theme

#### Scenario: Component import and structure
- **WHEN** the application starts
- **THEN** the system SHALL import VerticalScroll from textual.containers
- **AND** the compose() method SHALL structure components with scrollable container and fixed buttons
