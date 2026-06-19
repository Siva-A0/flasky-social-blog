import os
import socket
import tempfile
import threading
import time
import unittest
import urllib.request

from selenium import webdriver
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from werkzeug.serving import make_server

from app import create_app, db
from app.models import Role, User


class SeleniumTestCase(unittest.TestCase):
    client = None

    @classmethod
    def setUpClass(cls):
        # Start Chrome.
        options = webdriver.ChromeOptions()
        options.add_argument("--window-size=1400,1200")
        options.add_argument("--headless=new")
        try:
            cls.client = webdriver.Chrome(options=options)
        except WebDriverException:
            cls.client = None

        if not cls.client:
            return

        # Create the testing app.
        cls.app = create_app("testing")

        # Use a temporary database file so the browser and server share the same data.
        cls.db_fd, cls.db_path = tempfile.mkstemp(suffix=".sqlite")
        cls.app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{cls.db_path}"

        cls.app_context = cls.app.app_context()
        cls.app_context.push()

        # Create the database and add one confirmed admin user.
        db.create_all()
        Role.insert_roles()

        admin_role = Role.query.filter_by(name="Administrator").first()
        admin = User(
            email="john@example.com",
            username="john",
            password="cat",
            role=admin_role,
            confirmed=True,
        )
        db.session.add(admin)
        db.session.commit()
        db.session.remove()

        # Run the Flask app in the background for Selenium.
        port = cls.get_free_port()
        cls.base_url = f"http://127.0.0.1:{port}"
        cls.server = make_server("127.0.0.1", port, cls.app)
        cls.server_thread = threading.Thread(target=cls.server.serve_forever)
        cls.server_thread.start()

        cls.wait_for_server()

    @classmethod
    def tearDownClass(cls):
        if not cls.client:
            return

        cls.client.quit()
        cls.server.shutdown()
        cls.server.server_close()
        cls.server_thread.join(timeout=5)

        db.session.remove()
        db.drop_all()
        cls.app_context.pop()

        os.close(cls.db_fd)
        os.unlink(cls.db_path)

    def setUp(self):
        if not self.client:
            self.skipTest("Web browser not available")

    @staticmethod
    def get_free_port():
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.bind(("127.0.0.1", 0))
            return sock.getsockname()[1]

    @classmethod
    def wait_for_server(cls, timeout=10):
        end_time = time.time() + timeout
        while time.time() < end_time:
            try:
                with urllib.request.urlopen(cls.base_url, timeout=1):
                    return
            except Exception:
                time.sleep(0.1)
        raise RuntimeError("The Selenium test server did not start in time.")

    def wait_for_text(self, text, timeout=10):
        try:
            WebDriverWait(self.client, timeout).until(
                lambda driver: text in driver.page_source
            )
        except TimeoutException as exc:
            raise AssertionError(
                f"Could not find text {text!r} on the page.\n{self.client.page_source}"
            ) from exc

    def test_admin_home_page(self):
        # Open the home page.
        self.client.get(f"{self.base_url}/")
        self.wait_for_text("Stranger")

        # Go to login page.
        self.client.find_element(By.LINK_TEXT, "Log In").click()
        self.wait_for_text("Login")

        # Log in as the admin user.
        self.client.find_element(By.NAME, "email").send_keys("john@example.com")
        self.client.find_element(By.NAME, "password").send_keys("cat")
        self.client.find_element(By.NAME, "submit").click()
        self.wait_for_text("john")

        # Open the profile page.
        self.client.find_element(By.LINK_TEXT, "Profile").click()
        self.wait_for_text("Member since")


if __name__ == "__main__":
    unittest.main()
