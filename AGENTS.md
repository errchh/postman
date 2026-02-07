# AGENTS.md

This file contains development guidelines and commands for agentic coding agents working in this repository.

## Project Overview

This is an **OpenSpec** project - a specification-driven development workflow using the experimental artifact-driven approach. The project uses OpenSpec skills for managing changes through a structured workflow.

### Key Project Structure

- `.opencode/` - OpenCode plugin configuration and skills
- `openspec/` - OpenSpec configuration and changes directory
- `openspec/config.yaml` - OpenSpec project configuration
- `openspec/changes/` - Active change directories (created dynamically)

## Build/Lint/Test Commands

This project uses **uv** for Python package management.

### Package Management
```bash
# Add dependencies
uv add <package-name>

# Install dependencies
uv sync

# Run commands
uv run <command>
uv run python <script.py>

# Create virtual environment
uv venv

# Install specific Python version
uv python install 3.14
```

### OpenSpec Commands
```bash
# List available schemas/workflows
openspec schemas --json

# List active changes
openspec list --json

# Create new change (using default schema)
openspec new change "<change-name>"

# Create change with specific schema
openspec new change "<change-name>" --schema <schema-name>

# Check change status
openspec status --change "<change-name>"
openspec status --change "<change-name>" --json

# Get artifact creation instructions
openspec instructions <artifact-id> --change "<change-name>"

# Get implementation instructions
openspec instructions apply --change "<change-name>" --json

# Archive completed change
openspec archive --change "<change-name>"
```

### Testing Individual Changes
Since this is a spec-driven workflow, "testing" typically involves:
1. Verifying change status with `openspec status --change "<name>"`
2. Running implementation with `/opsx-apply <change-name>`
3. Verifying completion with status check

## Code Style Guidelines

### OpenSpec Workflow Conventions

#### Change Naming
- Use **kebab-case** for change names (e.g., `add-user-auth`, `fix-login-bug`)
- Names should be descriptive but concise
- Focus on the action or feature being implemented

#### Schema Usage
- Default to the **spec-driven** schema unless explicitly requested
- The spec-driven workflow follows this artifact sequence:
  1. `proposal` - High-level change description
  2. `specs` - Technical specifications
  3. `design` - Design documents/decisions
  4. `tasks` - Implementation checklist
- Use `--schema` parameter only when user explicitly requests a different workflow

#### Artifact Creation Guidelines
- **Proposals**: Keep under 500 words, always include "Non-goals" section
- **Tasks**: Break into chunks of max 2 hours of work
- **Specs**: Include technical requirements and API contracts
- **Design**: Document architectural decisions and trade-offs

### File Organization
- Changes are organized under `openspec/changes/<change-name>/`
- Each change contains its artifacts as separate files
- Follow the artifact sequence specified by the schema

### Markdown Conventions
- Use standard Markdown formatting
- Include front matter with description for command files
- Use task lists (`- [ ]` and `- [x]`) for tracking progress
- Use code blocks with appropriate language identifiers

### Error Handling and Guardrails
- Always validate change names (kebab-case required)
- Check for existing changes before creating new ones
- Verify artifact dependencies before proceeding
- Pause and ask for clarification when requirements are unclear
- Don't proceed with implementation if prerequisites are missing

### Development Workflow
1. **Exploration**: Use `/opsx-explore` for thinking through requirements
2. **Creation**: Use `/opsx-new` to start structured changes
3. **Continuation**: Use `/opsx-continue` to create subsequent artifacts
4. **Implementation**: Use `/opsx-apply` to execute tasks
5. **Verification**: Use `/opsx-verify` to validate implementation
6. **Archival**: Use `/opsx-archive` to complete changes

### Interactive Guidelines
- Use the **AskUserQuestion tool** for open-ended user input
- Always announce which change is being worked on
- Show progress clearly (e.g., "3/7 tasks complete")
- Provide clear options when pausing due to issues
- Support fluid workflow - can interleave different actions

## Project Configuration

### OpenSpec Context
The `openspec/config.yaml` allows for project-specific context. Currently uses the default schema-driven workflow. Add your tech stack, conventions, and domain knowledge to the context section for AI assistance.

### Dependencies
- `@opencode-ai/plugin` (v1.1.50) - Main plugin functionality
- `@opencode-ai/sdk` (v1.1.50) - SDK integration
- `zod` (v4.1.8) - Schema validation

## Important Notes

- **No Cursor or Copilot rules** found in this repository
- **No traditional build/test commands** - this is a specification-driven project
- **uv** is the preferred package manager
- **OpenSpec skills** provide the primary development workflow
- **Artifact-driven approach** - changes progress through structured artifacts
- **Fluid workflow** - can move between creation and implementation phases
- **Status-driven development** - always check status before proceeding

## Testing Your Changes

After implementing changes:
1. Run `openspec status --change "<name>"` to verify all artifacts are complete
2. Use the implementation verification process with `/opsx-verify`
3. Archive completed changes with `/opsx-archive`

This ensures a clean, tracked development workflow with full traceability from specification to implementation.