import subprocess
import logging
import json
from typing import Dict, List, Optional
import os
import time
import random
import pyperclip
from playwright.sync_api import sync_playwright, Playwright

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class AutoWeb:
    def __init__(self):
        """Initialize AutoWeb and verify Playwright installation."""
        self.check_requirements()

    def check_requirements(self) -> None:
        """Verify that at least one supported browser is installed."""
        supported_browsers = ['chromium', 'firefox', 'webkit']
        installed_browsers = []
        missing_browsers = []

        with sync_playwright() as p:
            for browser_type in supported_browsers:
                try:
                    getattr(p, browser_type).launch()
                    installed_browsers.append(browser_type)
                except Exception:
                    missing_browsers.append(browser_type)

        if not installed_browsers:
            logger.error(
                f"No supported browsers installed. Please install at least one of: {', '.join(supported_browsers)}")
            raise EnvironmentError("No supported browsers found.")
        logger.info(f"Installed browsers: {', '.join(installed_browsers)}")
        if missing_browsers:
            logger.warning(f"Missing browsers: {', '.join(missing_browsers)}")

    def move_and_click(self, page, selector: str) -> bool:
        """Move mouse naturally to element and click."""
        try:
            element = page.query_selector(selector)
            if element:
                box = element.bounding_box()
                page.mouse.move(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2)
                time.sleep(random.uniform(0.1, 0.3))
                page.mouse.click(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2)
                logger.info(f"Clicked on element with selector: {selector}")
                return True
            logger.warning(f"No element found for selector: {selector}")
            return False
        except Exception as e:
            logger.error(f"Error in move_and_click with selector {selector}: {str(e)}")
            return False

    def automate_web(self, actions: List[Dict], browser_type: str = 'firefox',
                     use_session: bool = False, session_file: str = 'session.json',
                     headless: bool = True, timeout: int = 30) -> Dict:
        """
        Automate web interactions based on a list of actions.

        Args:
            actions: List of action dictionaries (e.g., {'type': 'click', 'selector': 'button'}).
            browser_type: Browser to use ('chromium', 'firefox', 'webkit').
            use_session: Load session if available (default: False).
            session_file: Path to session file (default: 'session.json').
            headless: Run browser in headless mode (default: True).
            timeout: Maximum time in seconds for each action (default: 30).

        Returns:
            Dict with status and results of actions.
        """
        if not actions:
            logger.warning("No actions provided.")
            return {"status": "failure", "message": "No actions provided"}

        try:
            with sync_playwright() as p:
                browser_launcher = getattr(p, browser_type, None)
                if not browser_launcher:
                    raise ValueError(f"Unsupported browser: {browser_type}")
                browser = browser_launcher.launch(headless=headless)
                context = (browser.new_context(storage_state=session_file)
                           if use_session and os.path.exists(session_file)
                           else browser.new_context())
                page = context.new_page()
                page.set_default_timeout(timeout * 1000)  # Convert to milliseconds

                results = []
                for action in actions:
                    action_type = action.get('type')
                    if action_type == 'navigate':
                        page.goto(action['url'])
                        results.append(f"Navigated to {action['url']}")
                    elif action_type == 'click':
                        page.click(action['selector'])
                        results.append(f"Clicked {action['selector']}")
                    elif action_type == 'type':
                        page.fill(action['selector'], action['value'])
                        results.append(f"Typed '{action['value']}' into {action['selector']}")
                    elif action_type == 'wait':
                        time.sleep(action['delay'])
                        results.append(f"Waited {action['delay']} seconds")
                    else:
                        raise ValueError(f"Unknown action type: {action_type}")

                if use_session:
                    context.storage_state(path=session_file)
                browser.close()
                return {"status": "success", "actions_performed": results}
        except Exception as e:
            logger.error(f"Automation failed: {str(e)}")
            raise RuntimeError(f"Automation failed: {str(e)}")

    def auto_grok(self, url: str, prompt: str, deeper_search: bool = False,
                  deeper_search_advanced: bool = False, think: bool = False,
                  attachments: Optional[List[str]] = None, output_file: Optional[str] = None,
                  browser_type: str = 'firefox', use_session: bool = True,
                  session_file: str = 'session.json', headless: bool = False) -> Dict:
        """
        Automate interactions on a Grok-like interface.

        Args:
            url: URL to navigate to.
            prompt: Text to input.
            deeper_search: Enable DeeperSearch feature.
            deeper_search_advanced: Enable advanced DeeperSearch.
            think: Enable Think feature.
            attachments: List of file paths to attach.
            output_file: File to save response.
            browser_type: Browser to use.
            use_session: Load session if available.
            session_file: Path to session file.
            headless: Run in headless mode.

        Returns:
            Dict with automation results.
        """
        if sum([deeper_search, deeper_search_advanced, think]) > 1:
            raise ValueError("Only one feature toggle can be enabled.")

        if attachments:
            for file_path in attachments:
                if not os.path.exists(file_path):
                    raise ValueError(f"Attachment file not found: {file_path}")

        actions = [{'type': 'navigate', 'url': url}]
        if deeper_search:
            actions.append({'type': 'click', 'selector': '#deeper_search'})
        elif deeper_search_advanced:
            actions.append({'type': 'click', 'selector': '#deeper_search_advanced'})
        elif think:
            actions.append({'type': 'click', 'selector': '#think'})
        actions.append({'type': 'type', 'selector': 'textarea#prompt', 'value': prompt})
        # Note: Attachment and submission logic could be expanded here if UI specifics are provided.

        return self.automate_web(actions, browser_type, use_session, session_file, headless)

    def capture_screenshot(self, url: str, output_file: str, browser_type: str = 'firefox',
                           headless: bool = True) -> Dict:
        """Capture a screenshot of a webpage and save it to a file."""
        try:
            with sync_playwright() as p:
                browser = getattr(p, browser_type).launch(headless=headless)
                page = browser.new_page()
                page.goto(url)
                page.screenshot(path=output_file)
                browser.close()
                return {"status": "success", "file": output_file}
        except Exception as e:
            logger.error(f"Screenshot capture failed: {str(e)}")
            raise RuntimeError(f"Screenshot capture failed: {str(e)}")

    def intercept_network(self, url: str, browser_type: str = 'firefox', headless: bool = True) -> List[Dict]:
        """Intercept and log network requests on a webpage."""
        requests = []
        with sync_playwright() as p:
            browser = getattr(p, browser_type).launch(headless=headless)
            page = browser.new_page()
            page.on("request", lambda req: requests.append({"url": req.url, "method": req.method}))
            page.goto(url)
            page.wait_for_load_state()
            browser.close()
        return requests