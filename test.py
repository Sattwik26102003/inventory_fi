import requests
import random
import string

BASE_URL = "http://localhost:8080/api" 


def print_result(test_name, passed, expected=None, got=None, request_data=None, response_body=None):
    """
    Prints a formatted test result.
    If the test passed, it prints a simple success message.
    If it failed, it provides detailed information about the request and response.
    """
    if passed:
        print(f"✅ {test_name}: PASSED")
    else:
        print(f"❌ {test_name}: FAILED")
        if request_data:
            print(f"   Request Data: {request_data}")
        if expected is not None and got is not None:
            print(f"   Expected: {expected}, Got: {got}")
        if response_body:
            response_text = str(response_body)
            if len(response_text) > 300:
                response_text = response_text[:300] + "..."
            print(f"   Response Body: {response_text}")
    print("-" * 40)


def generate_random_string(length=8):
    """Generates a random string to ensure usernames are unique for each test run."""
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))


def test_register_user(username, password):
    """Tests the user registration endpoint."""
    print("Running: User Registration Test")
    payload = {"username": username, "password": password}
    res = requests.post(f"{BASE_URL}/auth/register", json=payload)
    passed = res.status_code in [201, 400]
    print_result("User Registration", passed, "201 (Created) or 400 (Conflict)", res.status_code, payload, res.text)
    return passed


def test_login(username, password):
    """
    Tests the login endpoint.
    On success, it expects a 200 status and an 'access_token' in the JSON response.
    Returns the token to be used in subsequent authenticated requests.
    """
    print("Running: Login Test")
    payload = {"username": username, "password": password}
    res = requests.post(f"{BASE_URL}/auth/login", json=payload)
    
    token = None
    passed = False
    if res.status_code == 200:
        try:
            token = res.json().get("access_token")
            passed = token is not None
        except Exception:
            passed = False
            
    print_result("Login Test", passed, "Status 200 and a valid JWT token", f"Status {res.status_code}", payload, res.text)
    return token


def test_add_product(token):
    """
    Tests adding a new product.
    Must include the Authorization header with the Bearer token.
    Returns the new product's ID on success.
    """
    print("Running: Add Product Test")
    payload = {
        "name": "Gaming Mouse",
        "type": "Electronics",
        "sku": f"GM-{generate_random_string(6).upper()}", 
        "image_url": "https://example.com/mouse.jpg",
        "description": "A high-performance gaming mouse.",
        "quantity": 50,
        "price": 79.99
    }
    headers = {"Authorization": f"Bearer {token}"}
    res = requests.post(f"{BASE_URL}/products", json=payload, headers=headers)
    
    product_id = None
    passed = res.status_code == 201
    if passed:
        try:
            product_id = res.json().get("product_id")
        except Exception:
            passed = False
            
    print_result("Add Product", passed, "Status 201 and a product_id", f"Status {res.status_code}", payload, res.text)
    return product_id


def test_update_quantity(token, product_id, new_quantity):
    """Tests updating the quantity for a specific product."""
    print(f"Running: Update Product Quantity Test (New Quantity: {new_quantity})")
    payload = {"quantity": new_quantity}
    headers = {"Authorization": f"Bearer {token}"}
    res = requests.put(f"{BASE_URL}/products/{product_id}/quantity", json=payload, headers=headers)

    passed = res.status_code == 200
    if passed:
        try:
            updated_qty = res.json().get("quantity")
            if updated_qty != new_quantity:
                passed = False 
        except Exception:
            passed = False

    print_result("Update Quantity", passed, f"Status 200 and quantity updated to {new_quantity}", f"Status {res.status_code}", payload, res.text)


def test_get_products(token, expected_quantity):
    """
    Tests fetching the list of products.
    Checks if the previously added product exists and has the correct quantity.
    """
    print("Running: Get Products Test")
    headers = {"Authorization": f"Bearer {token}"}
    res = requests.get(f"{BASE_URL}/products", headers=headers)

    if res.status_code != 200:
        print_result("Get Products", False, 200, res.status_code, None, res.text)
        return

    try:
        products = res.json()
        test_product = next((p for p in products if p.get("name") == "Gaming Mouse"), None)
        
        if not test_product:
            print_result("Get Products", False, "Product 'Gaming Mouse' to be in the list", "Product not found", None, products)
            return

        final_quantity = test_product.get("quantity")
        if final_quantity == expected_quantity:
            print_result("Get Products", True)
        else:
            print_result("Get Products", False, f"Quantity to be {expected_quantity}", f"Got {final_quantity}", None, products)

    except Exception as e:
        print_result("Get Products", False, "A valid JSON list of products", f"An error occurred: {e}", None, res.text)


def run_all_tests():
    """Runs all API tests in sequence."""
    print("--- Starting Inventory Management API Test Suite ---")
    
    test_username = f"testuser_{generate_random_string()}"
    test_password = "password123"

    if not test_register_user(test_username, test_password):
        print("\nRegistration failed. Aborting tests.")
        return

    token = test_login(test_username, test_password)
    if not token:
        print("\nLogin failed. Aborting further tests.")
        return

    product_id = test_add_product(token)
    if not product_id:
        print("\nProduct creation failed. Aborting further tests.")
        return

    new_quantity = 125
    test_update_quantity(token, product_id, new_quantity)
    
    test_get_products(token, expected_quantity=new_quantity)
    
    print("--- Test Suite Finished ---")


if __name__ == "__main__":
    run_all_tests()




