# QuickBite Food Delivery API

A fast and efficient FastAPI-based food delivery backend for the QuickBite platform.

## Features

- **Menu Management**: Browse, filter, search, and paginate through delicious food items.
- **Cart System**: Add/remove items, update quantities, and prepare for checkout.
- **Order Processing**: Place orders with delivery/pickup options and track order status.
- **Dynamic Billing**: Automatic calculation of totals with delivery charges.

## Tech Stack

- **Framework**: FastAPI
- **Model Validation**: Pydantic
- **Server**: Uvicorn

## Getting Started

### Installation

1. Clone the repository.
2. Navigate to the `Project - Food Delivery App` directory.
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Running the Server

Start the development server:
```bash
python -m uvicorn main:app --reload
```

The API will be available at `http://127.0.0.1:8000`.
Explore the interactive docs at `http://127.0.0.1:8000/docs`.

## API Endpoints

### Menu
- `GET /menu`: List all menu items.
- `POST /menu`: Add a new menu item.
- `GET /menu/{item_id}`: Get item details.
- `PUT /menu/{item_id}`: Update item price/availability.
- `DELETE /menu/{item_id}`: Remove an item.

### Cart
- `GET /cart`: View current cart and grand total.
- `POST /cart/add`: Add an item to the cart.
- `DELETE /cart/{item_id}`: Remove an item from the cart.
- `POST /cart/checkout`: Place orders for all items in the cart.

### Orders
- `GET /orders`: View all placed orders.
- `POST /orders`: Place a single item order.
- `GET /orders/{order_id}`: Get order status.
