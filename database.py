
import sqlite3
DB="store.db"
def conn():
    return sqlite3.connect(DB)
def init():
    c=conn()
    cur=c.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS transactions(
    id INTEGER PRIMARY KEY,
    item TEXT,action TEXT,qty INTEGER,price REAL,total REAL,
    dt TEXT,tm TEXT)""")
    cur.execute("""CREATE TABLE IF NOT EXISTS stock(
    item TEXT PRIMARY KEY,qty INTEGER)""")
    c.commit();c.close()

def add_tx(item,action,qty,price,dt,tm):
    total=qty*price
    c=conn();cur=c.cursor()
    cur.execute("INSERT INTO transactions(item,action,qty,price,total,dt,tm) VALUES(?,?,?,?,?,?,?)",
                (item,action,qty,price,total,dt,tm))
    q=cur.execute("SELECT qty FROM stock WHERE item=?",(item,)).fetchone()
    current=q[0] if q else 0
    new=current+qty if action=="Purchase" else current-qty
    if q: cur.execute("UPDATE stock SET qty=? WHERE item=?",(new,item))
    else: cur.execute("INSERT INTO stock VALUES(?,?)",(item,max(new,0)))
    c.commit();c.close()

def transactions():
    c=conn()
    rows=c.execute("SELECT * FROM transactions ORDER BY id DESC").fetchall()
    c.close()
    return rows

def stock():
    c=conn()
    rows=c.execute("SELECT * FROM stock").fetchall()
    c.close()
    return rows
