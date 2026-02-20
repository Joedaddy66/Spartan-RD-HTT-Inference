import sqlite3
import os

def show_hud():
    if not os.path.exists('nexus.db'):
        print("❌ DATABASE OFFLINE: Run the SQLite setup first.")
        return

    conn = sqlite3.connect('nexus.db')
    c = conn.cursor()
    
    # Get Stats
    c.execute("SELECT COUNT(*) FROM leads")
    total = c.fetchone()[0]
    
    c.execute("SELECT COUNT(*) FROM leads WHERE status='PITCHED'")
    pitched = c.fetchone()[0]

    revenue = pitched * 34450
    goal = 1000000
    progress = min(int((revenue / goal) * 10), 10)
    bar = "█" * progress + "░" * (10 - progress)

    print(f"\n🛡️  OFF-GRID NEXUS: EMPIRE HUD")
    print(f"==============================")
    print(f"Local Leads:   {total}")
    print(f"Pitches Sent:  {pitched}")
    print(f"Revenue (M1): ${revenue:,}")
    print(f"Goal [$1M]:    [{bar}] {int((revenue/goal)*100)}%")
    print(f"==============================\n")

if __name__ == "__main__":
    show_hud()
