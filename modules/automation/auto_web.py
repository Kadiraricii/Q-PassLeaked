# TODO
# https://www.zenrows.com/blog/playwright-cloudflare-bypass

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

    ### Action Handlers for Playwright Features ###

    def navigate_action(self, page, current_frame, action):
        page.goto(action['url'])
        return {'action': 'navigate', 'url': action['url']}

    def click_action(self, page, current_frame, action):
        current_frame.click(action['selector'])
        return {'action': 'click', 'selector': action['selector']}

    def type_action(self, page, current_frame, action):
        current_frame.fill(action['selector'], action['value'])
        return {'action': 'type', 'selector': action['selector'], 'value': action['value']}

    def wait_action(self, page, current_frame, action):
        time.sleep(action['delay'])
        return {'action': 'wait', 'delay': action['delay']}

    def select_action(self, page, current_frame, action):
        current_frame.select_option(action['selector'], action['value'])
        return {'action': 'select', 'selector': action['selector'], 'value': action['value']}

    def hover_action(self, page, current_frame, action):
        current_frame.hover(action['selector'])
        return {'action': 'hover', 'selector': action['selector']}

    def scroll_action(self, page, current_frame, action):
        page.evaluate(f"window.scrollTo({action['x']}, {action['y']})")
        return {'action': 'scroll', 'x': action['x'], 'y': action['y']}

    def upload_action(self, page, current_frame, action):
        current_frame.set_input_files(action['selector'], action['files'])
        return {'action': 'upload', 'selector': action['selector'], 'files': action['files']}

    def screenshot_action(self, page, current_frame, action):
        page.screenshot(path=action['path'])
        return {'action': 'screenshot', 'path': action['path']}

    def pdf_action(self, page, current_frame, action):
        page.pdf(path=action['path'])
        return {'action': 'pdf', 'path': action['path']}

    def evaluate_action(self, page, current_frame, action):
        result = current_frame.evaluate(action['script'])
        return {'action': 'evaluate', 'script': action['script'], 'result': result}

    def wait_for_selector_action(self, page, current_frame, action):
        current_frame.wait_for_selector(action['selector'], state=action.get('state', 'visible'))
        return {'action': 'wait_for_selector', 'selector': action['selector'], 'state': action.get('state', 'visible')}

    def wait_for_function_action(self, page, current_frame, action):
        current_frame.wait_for_function(action['script'])
        return {'action': 'wait_for_function', 'script': action['script']}

    def set_cookie_action(self, page, current_frame, action):
        page.context.add_cookies([action['cookie']])
        return {'action': 'set_cookie', 'cookie': action['cookie']}

    def get_cookies_action(self, page, current_frame, action):
        cookies = page.context.cookies()
        return {'action': 'get_cookies', 'cookies': cookies}

    def clear_cookies_action(self, page, current_frame, action):
        page.context.clear_cookies()
        return {'action': 'clear_cookies'}

    def set_local_storage_action(self, page, current_frame, action):
        current_frame.evaluate(f"localStorage.setItem('{action['key']}', '{action['value']}')")
        return {'action': 'set_local_storage', 'key': action['key'], 'value': action['value']}

    def get_local_storage_action(self, page, current_frame, action):
        value = current_frame.evaluate(f"localStorage.getItem('{action['key']}')")
        return {'action': 'get_local_storage', 'key': action['key'], 'value': value}

    def set_viewport_action(self, page, current_frame, action):
        page.set_viewport_size({'width': action['width'], 'height': action['height']})
        return {'action': 'set_viewport', 'width': action['width'], 'height': action['height']}

    def check_action(self, page, current_frame, action):
        current_frame.check(action['selector'])
        return {'action': 'check', 'selector': action['selector']}

    def uncheck_action(self, page, current_frame, action):
        current_frame.uncheck(action['selector'])
        return {'action': 'uncheck', 'selector': action['selector']}

    def press_action(self, page, current_frame, action):
        current_frame.press(action['selector'], action['key'])
        return {'action': 'press', 'selector': action['selector'], 'key': action['key']}

    def get_attribute_action(self, page, current_frame, action):
        element = current_frame.query_selector(action['selector'])
        value = element.get_attribute(action['attribute'])
        return {'action': 'get_attribute', 'selector': action['selector'], 'attribute': action['attribute'], 'value': value}

    def get_text_action(self, page, current_frame, action):
        text = current_frame.inner_text(action['selector'])
        return {'action': 'get_text', 'selector': action['selector'], 'text': text}

    def go_back_action(self, page, current_frame, action):
        page.go_back()
        return {'action': 'go_back'}

    def go_forward_action(self, page, current_frame, action):
        page.go_forward()
        return {'action': 'go_forward'}

    def reload_action(self, page, current_frame, action):
        page.reload()
        return {'action': 'reload'}

    ### Main Automation Method ###

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

        Supported Actions:
            - navigate: {'type': 'navigate', 'url': 'https://example.com'}
            - click: {'type': 'click', 'selector': '#button'}
            - type: {'type': 'type', 'selector': '#input', 'value': 'text'}
            - wait: {'type': 'wait', 'delay': 2}
            - select: {'type': 'select', 'selector': '#dropdown', 'value': 'option'}
            - hover: {'type': 'hover', 'selector': '#element'}
            - scroll: {'type': 'scroll', 'x': 0, 'y': 100}
            - upload: {'type': 'upload', 'selector': '#file', 'files': ['path/to/file']}
            - screenshot: {'type': 'screenshot', 'path': 'screenshot.png'}
            - pdf: {'type': 'pdf', 'path': 'page.pdf'} (Chromium only)
            - evaluate: {'type': 'evaluate', 'script': 'document.title'}
            - wait_for_selector: {'type': 'wait_for_selector', 'selector': '#element', 'state': 'visible'}
            - wait_for_function: {'type': 'wait_for_function', 'script': 'window.status === "complete"'}
            - set_cookie: {'type': 'set_cookie', 'cookie': {'name': 'key', 'value': 'val'}}
            - get_cookies: {'type': 'get_cookies'}
            - clear_cookies: {'type': 'clear_cookies'}
            - set_local_storage: {'type': 'set_local_storage', 'key': 'key', 'value': 'value'}
            - get_local_storage: {'type': 'get_local_storage', 'key': 'key'}
            - set_viewport: {'type': 'set_viewport', 'width': 1280, 'height': 720}
            - check: {'type': 'check', 'selector': '#checkbox'}
            - uncheck: {'type': 'uncheck', 'selector': '#checkbox'}
            - press: {'type': 'press', 'selector': '#input', 'key': 'Enter'}
            - get_attribute: {'type': 'get_attribute', 'selector': '#element', 'attribute': 'href'}
            - get_text: {'type': 'get_text', 'selector': '#element'}
            - go_back: {'type': 'go_back'}
            - go_forward: {'type': 'go_forward'}
            - reload: {'type': 'reload'}
            - switch_to_frame: {'type': 'switch_to_frame', 'frame_selector': 'iframe'}
            - switch_to_default_content: {'type': 'switch_to_default_content'}
        """
        if not actions:
            logger.warning("No actions provided.")
            return {"status": "failure", "message": "No actions provided"}

        # Define action handlers
        action_handlers = {
            'navigate': self.navigate_action,
            'click': self.click_action,
            'type': self.type_action,
            'wait': self.wait_action,
            'select': self.select_action,
            'hover': self.hover_action,
            'scroll': self.scroll_action,
            'upload': self.upload_action,
            'screenshot': self.screenshot_action,
            'pdf': self.pdf_action,
            'evaluate': self.evaluate_action,
            'wait_for_selector': self.wait_for_selector_action,
            'wait_for_function': self.wait_for_function_action,
            'set_cookie': self.set_cookie_action,
            'get_cookies': self.get_cookies_action,
            'clear_cookies': self.clear_cookies_action,
            'set_local_storage': self.set_local_storage_action,
            'get_local_storage': self.get_local_storage_action,
            'set_viewport': self.set_viewport_action,
            'check': self.check_action,
            'uncheck': self.uncheck_action,
            'press': self.press_action,
            'get_attribute': self.get_attribute_action,
            'get_text': self.get_text_action,
            'go_back': self.go_back_action,
            'go_forward': self.go_forward_action,
            'reload': self.reload_action,
        }

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
                current_frame = page  # Start with page as the current frame

                results = []
                for action in actions:
                    action_type = action.get('type')
                    if action_type == 'switch_to_frame':
                        frame_element = current_frame.query_selector(action['frame_selector'])
                        if frame_element:
                            current_frame = frame_element.content_frame()
                            results.append({'action': 'switch_to_frame', 'frame_selector': action['frame_selector']})
                        else:
                            results.append({'action': 'switch_to_frame', 'error': 'Frame not found'})
                    elif action_type == 'switch_to_default_content':
                        current_frame = page
                        results.append({'action': 'switch_to_default_content'})
                    elif action_type in action_handlers:
                        try:
                            result = action_handlers[action_type](page, current_frame, action)
                            results.append(result)
                        except Exception as e:
                            results.append({'action': action_type, 'error': str(e)})
                    else:
                        results.append({'action': action_type, 'error': 'Unknown action type'})

                if use_session:
                    context.storage_state(path=session_file)
                browser.close()
                return {"status": "success", "actions_performed": results}
        except Exception as e:
            logger.error(f"Automation failed: {str(e)}")
            raise RuntimeError(f"Automation failed: {str(e)}")

    ### Existing Methods (Unchanged) ###

    def auto_grok(self, url: str, prompt: str, deeper_search: bool = False,
                  deeper_search_advanced: bool = False, think: bool = False,
                  attachments: Optional[List[str]] = None, output_file: Optional[str] = None,
                  browser_type: str = 'firefox', use_session: bool = True,
                  session_file: str = 'session.json', headless: bool = False) -> Dict:
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
        return self.automate_web(actions, browser_type, use_session, session_file, headless)

    def capture_screenshot(self, url: str, output_file: str, browser_type: str = 'firefox',
                           headless: bool = True) -> Dict:
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
        requests = []
        with sync_playwright() as p:
            browser = getattr(p, browser_type).launch(headless=headless)
            page = browser.new_page()
            page.on("request", lambda req: requests.append({"url": req.url, "method": req.method}))
            page.goto(url)
            page.wait_for_load_state()
            browser.close()
        return requests