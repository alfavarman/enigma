# Ecomnigma Application with Django 4, Django REST Framework, and SQLite

This application is a simple e-commerce platform built with Django 4 and Django REST Framework, utilizing SQLite as the database. The platform offers a range of features such as product listing, order placement, and user authentication, catering to both sellers and clients.

## Features:
- **Product Management**: Sellers can add, update, or delete products. Each product has attributes like name, description, price, category, image, and thumbnail.
- **Ordering System**: Clients can view products and place orders. Order details include the customer, delivery address, list of products with their quantities, order date, payment due date, and total price.
- **Authentication**: Built-in authentication system where users can sign up, log in, and have distinct roles (Client or Seller).
- **Product Views**: Display a list of all products with features like pagination, filtering, and sorting.
- **Statistics View**: Sellers can view statistics on the most ordered products.


## Prerequisites

Before you begin, ensure you have the following installed:
- **Python**: The project uses Python 3.10. Ensure it's installed on your system.
- **SQLite**: As the project utilizes SQLite, ensure you have it installed and set up. Usually, it comes pre-installed with Python.


## Installation

You can set up the project in two ways: manually, step by step, or by using the `install.sh` script.

### A. Clone repository

1. **Clone the Repository**
    ```bash
    git clone https://github.com/alfavarman/enigma.git
    cd enigma
    ```

### B. Manual installation

1. **Set Up a Virtual Environment**
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

2. **Install the Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

3. **Migrate the Database**
    ```bash
    python backend/src/manage.py migrate
    ```
4. **Create superuser**
    ```bash
    python backend/src/manage.py createsuperuser --username admin --email admin@example.com
    ```

5. **Run the Development Server**
    ```bash
    python backend/src/manage.py runserver
    ```

### C. Installation Using `install.sh` Script
Note installation scrip, creates new venv, install requirements, createsuperuser admin/admin, groups and permissions.

1. **Clone the Repository**
    ```bash
    git clone https://github.com/alfavarman/enigma.git
    cd enigma
    ```

2. **Run the Script**
    Make sure to provide execute permissions to the script.
    ```bash
    chmod +x install.sh
    ./install.sh
    ```

3. **Run the Development Server**
    After the script has executed, you can run the development server.
    ```bash
    source venv/bin/activate
    python backend/src/manage.py runserver
    ```

With either of the methods, you should now have the project up and running on `http://127.0.0.1:8000/`.


### D. !! SKIP if you used install.sh !! Configure groups:

#### option 1: Use custom command:
This command takes groups from docs/permissions.json and creates groups and add theirs permissions.
1. **Run Django shell**
    ```bash
   python manage.py setup_groups_permissions
    ```

#### option 1: Manually
1. **Run Django shell**
    ```bash
   python backend/src/manage.py shell
    ```

2. **inside shell: NOTE this needs to be sourced from docs/permissions.json **
    ```bash
   from django.contrib.auth.models import Group, Permission
   
   seller_group, created = Group.objects.get_or_create(name='Seller')
   permissions = [
       "change_user", "delete_user", "view_user", "view_order",
       "view_orderproduct", "add_product", "can_view_product_statistics",
       "change_product", "delete_product", "view_product", "add_productcategory",
       "change_productcategory", "delete_productcategory", "view_productcategory"
   ]
   for perm_codename in permissions:
       perm = Permission.objects.get(codename=perm_codename)
       seller_group.permissions.add(perm)
   
   client_group, created = Group.objects.get_or_create(name='Client')
   permissions = [
       "change_user", "delete_user", "view_user", "add_order", "change_order",
       "delete_order", "view_order", "view_product", "view_productcategory"
   ]
   for perm_codename in permissions:
       perm = Permission.objects.get(codename=perm_codename)
       client_group.permissions.add(perm)
   exit() 
   ```
   
## Usage

### Starting the Server

Before interacting with the application, ensure that the Django server is running. Navigate to the `backend/src` directory and start the server using:

```bash
   python backend/src/manage.py shell
```

### Django Admin Panel
To manage the application's data, use Django's built-in admin panel:

1. Visit http://127.0.0.1:8000/admin/.
2. Log in using the superuser credentials (admin/admin).
3. From here, you can manage users, products, orders, and more.

### API Endpoints
#### The application exposes several REST API endpoints:

1. Products:
   - List all products with search, filter, and ordering: GET /products/
   - Retrieve a single product's details: GET /products/<product_id>/
   - Create a new product (Sellers only): POST /products/
   - Update a product (Sellers only): PUT /products/<product_id>/
   - Delete a product (Sellers only): DELETE /products/<product_id>/
2. Orders:
   - Place a new order (Clients only): POST /orders/
   - Update an existing order (Clients only): PUT /orders/<order_id>/
   - Delete an order (Clients only): DELETE /orders/<order_id>/
   - Retrieve details of an order (Clients only): GET /orders/<order_id>/
3. Product Statistics (For Sellers):
    - View statistics of the most ordered products within a specific date range and limit: GET /product-statistics/?date_from=<start_date>&date_to=<end_date>&number_of_products=<limit>

#### Client and Seller Permissions
As outlined in the post-installation steps, the application supports two primary user roles: Client and Seller.

- Clients can place orders, view products, and manage their user profiles.

- Sellers have permissions to add, edit, and delete products. They can also view product statistics, manage users, and oversee orders.

Ensure that users are assigned to the appropriate group (either Client or Seller) to utilize the respective functionalities.

## Database Schema

The core e-commerce functionality of the application relies on a few primary data models. Here's a brief overview of these models:

### 1. ProductCategory
Represents a category for products. It helps in categorizing the products for better accessibility and organization.

- **Fields:**
  - `name`: A unique name for the category (e.g., Electronics, Clothing).

### 2. Product
Represents an item/product that can be listed and purchased in the e-commerce application.

- **Fields:**
  - `name`: Name of the product.
  - `description`: A brief description of the product.
  - `price`: Price of the product.
  - `category`: A foreign key to the ProductCategory model, allowing each product to be associated with a category.
  - `image`: An image representing the product.
  - `thumbnail`: A smaller, thumbnail-sized image generated from the main product image.

- **Permissions:**
  - `can_view_product_statistics`: Allows the viewing of product statistics.

### 3. Order
Represents a purchase made by a user. It contains details about the order, the customer, products in the order, and the total price.

- **Fields:**
  - `customer`: A foreign key to the Django User model, denoting who made the purchase.
  - `delivery_address`: Address where the order needs to be delivered.
  - `order_date`: The date and time when the order was placed.
  - `total_price`: The total price of all products in the order.
  - `payment_due_date`: The date by which the payment for the order should be made.
  - `products`: A many-to-many field linking to the Product model, representing products in the order. This relationship utilizes the `OrderProduct` model to capture the quantity of each product in the order.

### 4. OrderProduct
Captures the quantity of a product in a given order. Acts as a through model for the many-to-many relationship between `Order` and `Product`.

- **Fields:**
  - `order`: A foreign key to the Order model.
  - `product`: A foreign key to the Product model.
  - `quantity`: The number of units of the product in the order.

Each `OrderProduct` instance represents a specific product's quantity in a particular order, ensuring each product's accurate representation in various orders.

## Authentication & Authorization

### Built-in Authentication System:
Our application leverages Django's built-in authentication system, ensuring secure user registration, login, and session management. Users can sign up, log in, and manage their profiles seamlessly.

### User Groups and Permissions:

The application primarily distinguishes between two user groups: `Client` and `Seller`. Here's a detailed breakdown of their respective permissions:
Ref: docs/permissions.json

#### **Seller**:
- **User Management**:
  - `change_user`: Can update user information.
  - `delete_user`: Can delete users.
  - `view_user`: Can view user details.
  
- **Product Management**:
  - `add_product`: Can add new products.
  - `change_product`: Can update existing products.
  - `delete_product`: Can delete products.
  - `view_product`: Can view products.
  - `can_view_product_statistics`: Can view statistics related to products.
  
- **Product Category Management**:
  - `add_productcategory`: Can add new product categories.
  - `change_productcategory`: Can update existing product categories.
  - `delete_productcategory`: Can delete product categories.
  - `view_productcategory`: Can view product categories.

- **Order Management**:
  - `view_order`: Can view orders.
  - `view_orderproduct`: Can view products within orders.

#### **Client**:
- **User Management**:
  - `change_user`: Can update their own user information.
  - `delete_user`: Can delete their account.
  - `view_user`: Can view their own user details.

- **Product Browsing**:
  - `view_product`: Can view products.
  - `view_productcategory`: Can view product categories.

- **Order Management**:
  - `add_order`: Can place new orders.
  - `change_order`: Can update their orders (if allowed by business logic).
  - `delete_order`: Can cancel their orders.
  - `view_order`: Can view their orders.

## Tests

Ensuring the robustness and reliability of our application, we've incorporated a suite of tests. These tests cover the main components of our e-commerce application, ensuring everything from model validations to view functionalities works as intended.

### Running the Tests:

1. **Activate Your Virtual Environment**: 
   If you're not already in your virtual environment, activate it with the following command (replace 'venv' if you've named your virtual environment differently):

    ```bash
   source venv/bin/activate
    ```
2. **Run the Tests:**
Execute the following command to run all the tests:
    ```bash
   python manage.py test
   ```

### Test Reports:
After running the tests, you'll receive a report in the terminal detailing the number of tests run, any errors or failures, and more. Ensure all tests pass before making changes to the production environment or pushing updates.

If you encounter failing tests, the report will provide information on which test failed and why, assisting in debugging and rectifying the issue.

### PyCharm - if you run test via pycharm without django support
django.core.exceptions.ImproperlyConfigured: Requested setting INSTALLED_APPS:
import test_init for initialize django app during test


## License
This project is open-source and available under the MIT License. The details can be found in the LICENSE file in the repository.

