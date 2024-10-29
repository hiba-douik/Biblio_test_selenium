from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import unittest
import random
import string

class AuthenticationTests(unittest.TestCase):
    def setUp(self):
        # Initialize the Chrome WebDriver
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(10)
        self.base_url = "http://localhost:3000"  # Adjust this to your React app's URL
        
    def tearDown(self):
        # Close the browser
        if self.driver:
            self.driver.quit()
            
    def generate_random_email(self):
        # Generate a random email for testing
        random_string = ''.join(random.choices(string.ascii_lowercase, k=8))
        return f"test_{random_string}@example.com"
    
    def fill_registration_form(self, email, password, confirm_password):
        """Helper method to fill registration form"""
        self.driver.find_element(By.ID, "email").send_keys(email)
        self.driver.find_element(By.ID, "password").send_keys(password)
        self.driver.find_element(By.ID, "confirm_password").send_keys(confirm_password)  # Updated ID
        
    def fill_login_form(self, email, password):
        """Helper method to fill login form"""
        self.driver.find_element(By.ID, "email").send_keys(email)
        self.driver.find_element(By.ID, "password").send_keys(password)
    
    def test_01_successful_registration(self):
        """Test successful user registration"""
        self.driver.get(f"{self.base_url}/register")
        
        # Generate random test data
        test_email = self.generate_random_email()
        test_password = "Test123!"
        
        # Fill in the registration form
        self.fill_registration_form(test_email, test_password, test_password)
        
        # Submit the form
        self.driver.find_element(By.TAG_NAME, "form").submit()
        
        # Wait for redirect to login page or success message
        try:
            WebDriverWait(self.driver, 10).until(
                lambda driver: driver.current_url == f"{self.base_url}/login"
            )
            self.assertEqual(self.driver.current_url, f"{self.base_url}/login")
        except TimeoutException:
            self.fail("Registration failed - redirect to login page did not occur")
    
    def test_02_password_mismatch_registration(self):
        """Test registration with mismatched passwords"""
        self.driver.get(f"{self.base_url}/register")
        
        # Generate test data
        test_email = self.generate_random_email()
        test_password = "Test123!"
        different_password = "Different123!"
        
        # Fill in the registration form
        self.fill_registration_form(test_email, test_password, different_password)
        
        # Submit the form
        self.driver.find_element(By.TAG_NAME, "form").submit()
        
        # Wait for error message
        try:
            error_message = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "alert-danger"))
            )
            self.assertIn("Passwords do not match", error_message.text)
        except TimeoutException:
            self.fail("Error message for password mismatch not displayed")
            
    def test_03_duplicate_email_registration(self):
        """Test registration with an existing email"""
        self.driver.get(f"{self.base_url}/register")
        
        # Use a known existing email
        existing_email = "existing@example.com"
        test_password = "Test123!"
        
        # Fill in the registration form
        self.fill_registration_form(existing_email, test_password, test_password)
        
        # Submit the form
        self.driver.find_element(By.TAG_NAME, "form").submit()
        
        # Wait for error message
        try:
            error_message = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "alert-danger"))
            )
            self.assertIn("Email is already in use", error_message.text)
        except TimeoutException:
            self.fail("Error message for duplicate email not displayed")
            
    def test_04_successful_login(self):
        """Test successful login"""
        self.driver.get(f"{self.base_url}/login")
        
        # Use valid credentials
        valid_email = "test@example.com"
        valid_password = "Test123!"
        
        # Fill in the login form
        self.fill_login_form(valid_email, valid_password)
        
        # Submit the form
        self.driver.find_element(By.TAG_NAME, "form").submit()
        
        # Wait for redirect to contact page
        try:
            WebDriverWait(self.driver, 10).until(
                lambda driver: driver.current_url == f"{self.base_url}/contact"
            )
            self.assertEqual(self.driver.current_url, f"{self.base_url}/contact")
        except TimeoutException:
            self.fail("Login failed - redirect to contact page did not occur")
            
    def test_05_invalid_login(self):
        """Test login with invalid credentials"""
        self.driver.get(f"{self.base_url}/login")
        
        # Use invalid credentials
        invalid_email = "nonexistent@example.com"
        invalid_password = "WrongPassword123!"
        
        # Fill in the login form
        self.fill_login_form(invalid_email, invalid_password)
        
        # Submit the form
        self.driver.find_element(By.TAG_NAME, "form").submit()
        
        # Wait for error message
        try:
            error_message = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "alert-danger"))
            )
            self.assertIn("Incorrect username or password", error_message.text)
        except TimeoutException:
            self.fail("Error message for invalid credentials not displayed")

if __name__ == "__main__":
    unittest.main()