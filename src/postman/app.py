"""Postman TUI application."""

import pyperclip
from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical, VerticalScroll, VerticalGroup, Grid
from textual.screen import Screen
from textual.widgets import (
    Button,
    Checkbox,
    Footer,
    Header,
    Input,
    Label,
    Static,
    TextArea,
)

from typing import Dict

try:
    from postman.llm import LLMClient, LLMError
    from postman.prompts import Platform, PromptManager

    _HAVE_LLM = True
except ImportError:
    _HAVE_LLM = False

    class LLMClient:
        pass

    class LLMError(Exception):
        pass

    class Platform:
        LINKEDIN = "linkedin"
        FACEBOOK = "facebook"
        TWITTER = "twitter"
        INSTAGRAM = "instagram"

    class PromptManager:
        @staticmethod
        def get_prompt(p):
            return ""

        @staticmethod
        def build_event_context(**kwargs):
            return ""


class PlatformCard(Vertical):
    """Card displaying a single platform's generated content."""

    def __init__(self, platform: str, **kwargs):
        super().__init__(**kwargs)
        self.platform = platform
        self.content = "Generating..."

    def compose(self) -> ComposeResult:
        yield Label(self.platform.title(), classes="platform-title")
        yield Static(
            self.content, id=f"content-{self.platform}", classes="platform-content"
        )
        yield Button("Copy", id=f"copy-{self.platform}", variant="success")

    def update_content(self, content: str) -> None:
        """Update the content display."""
        self.content = content
        try:
            content_widget = self.query_one(f"#content-{self.platform}", Static)
            content_widget.update(content)
        except Exception:
            pass


class PreviewScreen(Screen[None]):
    """Preview screen showing grid of platform posts."""

    BINDINGS = [("escape", "dismiss", "Back"), ("b", "dismiss", "Back")]

    def __init__(self, platforms: list[str], **kwargs):
        super().__init__(**kwargs)
        self.platforms = platforms

    def action_dismiss(self) -> None:
        self.dismiss()

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        with VerticalScroll(classes="scroll-view"):
            # Create grid layout for platform cards
            for i in range(0, len(self.platforms), 2):
                with Horizontal(classes="platform-row"):
                    # First column
                    platform1 = self.platforms[i]
                    yield PlatformCard(platform1, id=f"card-{platform1}")

                    # Second column (if exists)
                    if i + 1 < len(self.platforms):
                        platform2 = self.platforms[i + 1]
                        yield PlatformCard(platform2, id=f"card-{platform2}")
        with Horizontal(classes="button-container"):
            yield Button("Back", id="back", variant="primary")
        yield Footer()

    def on_mount(self) -> None:
        """Update cards with current outputs from app."""
        app = self.app
        if hasattr(app, "platform_outputs"):
            for platform in self.platforms:
                content = app.platform_outputs.get(platform, "Generating...")
                try:
                    card = self.query_one(f"#card-{platform}", PlatformCard)
                    card.update_content(content)
                except Exception:
                    pass

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "back":
            self.dismiss()
        elif event.button.id and event.button.id.startswith("copy-"):
            # Extract platform from button id (copy-{platform})
            platform = event.button.id.replace("copy-", "")
            self.app.action_copy(platform)


class Postman(App):
    """Main Postman TUI application."""

    theme = "textual-light"

    CSS = """
    .scroll-view {
        width: 100%;
        height: 100%;
        padding: 1;
    }

    .section-label {
        text-style: bold;
        margin-top: 0;
        margin-bottom: 1;
    }

    VerticalGroup {
        margin-bottom: 2;
    }

    Input {
        height: 3;
        margin-bottom: 0;
    }

    TextArea {
        height: 8;
        margin-bottom: 0;
    }

    .platform-row {
        height: auto;
        margin-bottom: 1;
    }

    .datetime-row {
        height: auto;
        margin-bottom: 2;
    }

    .datetime-column {
        width: 50%;
        height: auto;
    }

    .button-container {
        height: auto;
        margin-top: 2;
        margin-bottom: 1;
    }

    Button { margin-right: 1; }

    .platform-title {
        text-style: bold;
        margin-bottom: 1;
    }

    .platform-content {
        width: 100%;
        height: auto;
        min-height: 5;
        padding: 1;
        margin-bottom: 1;
    }

    .banner {
        width: 100%;
        height: auto;
        margin-bottom: 2;
        text-align: left;
    }

    PlatformCard {
        width: 50%;
    }
    """

    BINDINGS = [
        ("q", "quit", "Exit"),
        ("g", "generate", "Generate"),
    ]

    def __init__(self):
        super().__init__()
        self.llm_client = None
        self.platform_outputs: Dict[str, str] = {}
        self.form_state = {}

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        with VerticalScroll(classes="scroll-view"):
            yield Static(
                r"""    
    ___       ___       ___       ___       ___       ___       ___   
   /\  \     /\  \     /\  \     /\  \     /\__\     /\  \     /\__\  
  /::\  \   /::\  \   /::\  \    \:\  \   /::L_L_   /::\  \   /:| _|_ 
 /::\:\__\ /:/\:\__\ /\:\:\__\   /::\__\ /:/L:\__\ /::\:\__\ /::|/\__\
 \/\::/  / \:\/:/  / \:\:\/__/  /:/\/__/ \/_/:/  / \/\::/  / \/|::/  /
    \/__/   \::/  /   \::/  /   \/__/      /:/  /    /:/  /    |:/  / 
             \/__/     \/__/               \/__/     \/__/     \/__/  

[bold]POSTMAN[/bold] [dim]v1.0[/dim]
Social Media Post Agent in .py
                """,
                id="banner",
                classes="banner",
            )
            # Platform
            yield Label("Platform:", classes="section-label")
            with Horizontal(classes="platform-row"):
                yield Checkbox("LinkedIn", id="platform-linkedin", value=True)
                yield Checkbox("Facebook", id="platform-facebook")
                yield Checkbox("Twitter", id="platform-twitter")
                yield Checkbox("Instagram", id="platform-instagram")

            # Title (VerticalGroup has height: auto so container sizes to content)
            with VerticalGroup():
                yield Label("Title:", classes="section-label")
                yield Input(placeholder="Python Workshop", id="title")

            # Date/Time Row
            with Horizontal(classes="datetime-row"):
                with Vertical(classes="datetime-column"):
                    yield Label("Date:")
                    yield Input(placeholder="Mar 15, 2026", id="date")
                with Vertical(classes="datetime-column"):
                    yield Label("Time:")
                    yield Input(placeholder="7:00 PM", id="time")

            # Location (VerticalGroup: height auto)
            with VerticalGroup():
                yield Label("Location:", classes="section-label")
                yield Input(placeholder="Central, Hong Kong", id="location")

            # Description (VerticalGroup: height auto)
            with VerticalGroup():
                yield Label("Description:", classes="section-label")
                yield TextArea(id="description")

            # Buttons
            with Horizontal(classes="button-container"):
                yield Button("Generate", id="generate", variant="primary")
                yield Button("Exit", id="exit", variant="error")

        yield Footer()

    def _get_selected_platforms(self) -> list[str]:
        """Get list of selected platforms from checkboxes."""
        selected = []
        try:
            if self.query_one("#platform-linkedin", Checkbox).value:
                selected.append("linkedin")
            if self.query_one("#platform-facebook", Checkbox).value:
                selected.append("facebook")
            if self.query_one("#platform-twitter", Checkbox).value:
                selected.append("twitter")
            if self.query_one("#platform-instagram", Checkbox).value:
                selected.append("instagram")
        except Exception:
            pass
        return selected if selected else ["linkedin"]

    def save_form_state(self):
        try:
            self.form_state = {
                "title": self.query_one("#title", Input).value,
                "date": self.query_one("#date", Input).value,
                "time": self.query_one("#time", Input).value,
                "location": self.query_one("#location", Input).value,
                "description": self.query_one("#description", TextArea).text,
                "platforms": self._get_selected_platforms(),
            }
        except Exception:
            pass

    def restore_form_state(self):
        if not self.form_state:
            return
        try:
            self.query_one("#title", Input).value = self.form_state.get("title", "")
            self.query_one("#date", Input).value = self.form_state.get("date", "")
            self.query_one("#time", Input).value = self.form_state.get("time", "")
            self.query_one("#location", Input).value = self.form_state.get(
                "location", ""
            )
            self.query_one("#description", TextArea).text = self.form_state.get(
                "description", ""
            )
        except:
            pass

    def action_generate(self) -> None:
        self.save_form_state()
        platforms = self.form_state.get("platforms", ["linkedin"])
        # Initialize outputs with "Generating..." for each platform
        self.platform_outputs = {platform: "Generating..." for platform in platforms}
        self.push_screen(PreviewScreen(platforms))
        self.run_worker(self._run_generation(platforms))

    async def _run_generation(self, platforms: list[str]) -> None:
        """Run LLM generation sequentially for each selected platform."""
        if not _HAVE_LLM:
            for platform in platforms:
                self.platform_outputs[platform] = (
                    "LLM not available. Install postman dependencies and set OPENROUTER_API_KEY."
                )
                self._update_platform_card(platform)
            return

        fs = self.form_state

        # Initialize LLM client once
        if self.llm_client is None:
            try:
                self.llm_client = LLMClient()
            except Exception as e:
                for platform in platforms:
                    self.platform_outputs[platform] = (
                        f"Configuration error: {e}. Set OPENROUTER_API_KEY in .env to generate."
                    )
                    self._update_platform_card(platform)
                return

        # Generate for each platform sequentially
        for platform_name in platforms:
            try:
                platform = Platform(platform_name)
                system_prompt = PromptManager.get_prompt(platform)
                user_input = PromptManager.build_event_context(
                    title=fs.get("title", ""),
                    date=fs.get("date", ""),
                    time=fs.get("time", ""),
                    location=fs.get("location", ""),
                    description=fs.get("description", ""),
                    platform=platform,
                )
                result = await self.llm_client.generate(system_prompt, user_input)
                self.platform_outputs[platform_name] = result
            except LLMError as e:
                self.platform_outputs[platform_name] = f"Generation failed: {e}"
            except Exception as e:
                self.platform_outputs[platform_name] = f"Error: {e}"

            # Update UI after each platform completes
            self._update_platform_card(platform_name)

    def _update_platform_card(self, platform: str) -> None:
        """Update the platform card display."""
        screen = self.screen
        if isinstance(screen, PreviewScreen):
            try:
                card = screen.query_one(f"#card-{platform}", PlatformCard)
                content = self.platform_outputs.get(platform, "")
                card.update_content(content)
            except Exception:
                pass

    def action_copy(self, platform: str = None) -> None:
        """Copy output to clipboard. If platform is specified, copy that platform's content."""
        if platform:
            content = self.platform_outputs.get(platform, "")
            platform_display = platform.title()
        else:
            # Default to first available platform output for backwards compatibility
            content = (
                next(iter(self.platform_outputs.values()), "")
                if self.platform_outputs
                else ""
            )
            platform_display = "content"

        if not content:
            self.notify(f"Nothing to copy for {platform_display}", severity="warning")
            return

        try:
            pyperclip.copy(content)
            self.notify(f"Copied {platform_display} to clipboard!")
        except Exception as e:
            self.notify(f"Failed to copy: {e}", severity="error")

    def on_mount(self):
        self.notify("Postman Ready")

    async def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "generate":
            self.action_generate()
        elif event.button.id == "exit":
            self.exit()


def main():
    """Main entry point for the postman CLI."""
    Postman().run()


if __name__ == "__main__":
    main()
