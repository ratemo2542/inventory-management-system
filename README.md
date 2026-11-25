# Inventory Management System

A small inventory CLI backed by SQLite. Add products, receive stock, record sales, and list items with low-stock warnings.

## Requirements
- Python 3.10+
- No third-party packages

## Run
```bash
python main.py add --sku KB01 --name "Keyboard" --price 1200 --quantity 10 --reorder-level 3
python main.py stock KB01 --change 5
python main.py stock KB01 --change -2
python main.py list
```

Negative stock changes are rejected if they would make inventory fall below zero. Data is stored in `inventory.db`.
