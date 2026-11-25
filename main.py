"""Basic stock control with SQLite."""
import argparse, sqlite3
from pathlib import Path
DB=Path(__file__).with_name("inventory.db")

def db():
    c=sqlite3.connect(DB); c.row_factory=sqlite3.Row
    c.execute("""CREATE TABLE IF NOT EXISTS products(
      sku TEXT PRIMARY KEY, name TEXT NOT NULL, price REAL NOT NULL CHECK(price>=0),
      quantity INTEGER NOT NULL CHECK(quantity>=0), reorder_level INTEGER NOT NULL DEFAULT 0)""")
    return c

def main():
    p=argparse.ArgumentParser(description="Manage product inventory.")
    s=p.add_subparsers(dest="cmd",required=True)
    a=s.add_parser("add"); a.add_argument("--sku",required=True); a.add_argument("--name",required=True)
    a.add_argument("--price",type=float,required=True); a.add_argument("--quantity",type=int,default=0); a.add_argument("--reorder-level",type=int,default=0)
    st=s.add_parser("stock"); st.add_argument("sku"); st.add_argument("--change",type=int,required=True)
    s.add_parser("list")
    x=p.parse_args()
    with db() as c:
        try:
            if x.cmd=="add":
                if x.price<0 or x.quantity<0 or x.reorder_level<0: p.error("price, quantity and reorder level cannot be negative")
                c.execute("INSERT INTO products VALUES(?,?,?,?,?)",(x.sku,x.name,x.price,x.quantity,x.reorder_level))
                print(f"Added {x.name}.")
            elif x.cmd=="stock":
                row=c.execute("SELECT quantity FROM products WHERE sku=?",(x.sku,)).fetchone()
                if not row: print("SKU not found."); return
                new=row["quantity"]+x.change
                if new<0: p.error("stock cannot become negative")
                c.execute("UPDATE products SET quantity=? WHERE sku=?",(new,x.sku))
                print(f"{x.sku}: {new} units.")
            else:
                rows=c.execute("SELECT * FROM products ORDER BY name").fetchall()
                for r in rows:
                    warning="  LOW STOCK" if r["quantity"]<=r["reorder_level"] else ""
                    print(f"{r['sku']:<12} {r['name']:<24} qty={r['quantity']:<5} price={r['price']:.2f}{warning}")
                if not rows: print("No products yet.")
        except sqlite3.IntegrityError as e: p.error(f"Could not save product: {e}")
if __name__=="__main__": main()
