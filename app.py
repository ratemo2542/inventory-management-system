"""Simple local inventory manager backed by SQLite."""
import argparse, sqlite3
from pathlib import Path

DB = Path("inventory.db")
def connect(path=DB):
    db=sqlite3.connect(path)
    db.execute("""CREATE TABLE IF NOT EXISTS products(
        id INTEGER PRIMARY KEY, name TEXT NOT NULL, sku TEXT UNIQUE,
        quantity INTEGER NOT NULL CHECK(quantity >= 0), price REAL NOT NULL CHECK(price >= 0))""")
    return db
def add_product(db,name,sku,quantity,price):
    if quantity < 0 or price < 0: raise ValueError("Quantity and price cannot be negative.")
    db.execute("INSERT INTO products(name,sku,quantity,price) VALUES(?,?,?,?)",(name,sku,quantity,price));db.commit()
def list_products(db):
    return db.execute("SELECT id,name,sku,quantity,price FROM products ORDER BY name").fetchall()
def main():
    parser=argparse.ArgumentParser(description=__doc__);sub=parser.add_subparsers(dest="cmd",required=True)
    a=sub.add_parser("add");a.add_argument("name");a.add_argument("--sku",required=True);a.add_argument("--quantity",type=int,default=0);a.add_argument("--price",type=float,required=True)
    sub.add_parser("list")
    args=parser.parse_args()
    with connect() as db:
        if args.cmd=="add":
            try: add_product(db,args.name,args.sku,args.quantity,args.price);print("Product added.")
            except sqlite3.IntegrityError as exc: parser.error(str(exc))
        else:
            for row in list_products(db): print(f"#{row[0]} {row[1]} | SKU {row[2]} | Qty {row[3]} | {row[4]:.2f}")
if __name__=="__main__":main()
