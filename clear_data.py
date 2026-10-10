import mysql.connector

def clear_data():
    try:
        print("Connecting to database...")
        db = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="",
            database="actbayan"
        )
        cur = db.cursor()

        # Disable foreign key checks to make deletion easier across related tables
        cur.execute("SET FOREIGN_KEY_CHECKS=0")

        # 1. Delete ALL reports and related data (comments, votes, if any)
        print("Deleting all reports...")
        cur.execute("DELETE FROM reports")
        
        # 2. Find resident account IDs (role_id = 1)
        print("Finding resident accounts to delete...")
        cur.execute("""
            SELECT DISTINCT c.account_id, ur.user_id, c.contact_id
            FROM user_role ur
            JOIN usercreds uc ON ur.user_id = uc.user_id
            JOIN contacts c ON uc.contact_id = c.contact_id
            WHERE ur.role_id = 1
        """)
        residents = cur.fetchall()
        
        if not residents:
            print("No resident accounts found to delete.")
        else:
            account_ids = list(set([r[0] for r in residents if r[0] is not None]))
            user_ids = list(set([r[1] for r in residents if r[1] is not None]))
            contact_ids = list(set([r[2] for r in residents if r[2] is not None]))

            print(f"Found {len(account_ids)} resident accounts. Wiping their data...")

            # Delete from user_role, credentials, usercreds
            if user_ids:
                format_strings = ','.join(['%s'] * len(user_ids))
                cur.execute(f"DELETE FROM user_role WHERE user_id IN ({format_strings})", tuple(user_ids))
                cur.execute(f"DELETE FROM credentials WHERE user_id IN ({format_strings})", tuple(user_ids))
                cur.execute(f"DELETE FROM usercreds WHERE user_id IN ({format_strings})", tuple(user_ids))

            # Delete from contacts
            if contact_ids:
                format_strings = ','.join(['%s'] * len(contact_ids))
                cur.execute(f"DELETE FROM contacts WHERE contact_id IN ({format_strings})", tuple(contact_ids))

            # Delete from accounts
            if account_ids:
                format_strings = ','.join(['%s'] * len(account_ids))
                cur.execute(f"DELETE FROM accounts WHERE account_id IN ({format_strings})", tuple(account_ids))

            print("Successfully deleted resident accounts!")

        # Re-enable foreign key checks
        cur.execute("SET FOREIGN_KEY_CHECKS=1")
        
        db.commit()
        print("Done! All reports and resident accounts have been cleared. LGU and Admin accounts were kept.")

    except mysql.connector.Error as err:
        print(f"Database Error: {err}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if 'db' in locals() and db.is_connected():
            cur.close()
            db.close()

if __name__ == "__main__":
    clear_data()
