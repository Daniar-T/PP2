import csv
import json
from datetime import datetime
from pathlib import Path

import psycopg2

from connect import connect

PHONE_TYPES = ("home", "work", "mobile")



def load_sql_file(filename):
    path = Path(__file__).with_name(filename)
    sql = path.read_text(encoding="utf-8")

    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute(sql)


def parse_birthday(text):
    """'YYYY-MM-DD' -> date, '' / None -> None. ValueError on bad format."""
    text = (text or "").strip()
    if not text:
        return None
    return datetime.strptime(text, "%Y-%m-%d").date()


def ask_phone_type(default="mobile"):
    text = input(f"Phone type home/work/mobile [{default}]: ").strip().lower()
    return text if text in PHONE_TYPES else default


def get_or_create_group(cur, group_name):
   
    cur.execute(
        """
        INSERT INTO groups (name) """Group id lookup that creates the group when it is missing.

    ON CONFLICT DO UPDATE (not DO NOTHING) guarantees RETURNING id
    also fires when the group already exists.
    """
        VALUES (%s)
        ON CONFLICT (name) DO UPDATE SET name = EXCLUDED.name
        RETURNING id
        """,
        (group_name,)
    )
    return cur.fetchone()[0]


def list_groups():
    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT name FROM groups ORDER BY id")
            return [row[0] for row in cur.fetchall()]


def call_procedure(sql, params):
    
    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, params)
        notices = list(conn.notices)

    for notice in notices:
        print(notice.strip())


def insert_contact_row(cur, name, phone, email, birthday, group):
    
    group_id = get_or_create_group(cur, group) if group else None

    cur.execute(
        """
        INSERT INTO contacts (first_name, phone, email, birthday, group_id)
        VALUES (%s, %s, %s, %s, %s)
        RETURNING id
        """,
        (name, phone, email, birthday, group_id)
    )
    return cur.fetchone()[0]


def insert_phones(cur, contact_id, phones_list):
    
    seen = set()

    for number, phone_type in phones_list:
        if number in seen:
            continue
        seen.add(number)

        cur.execute(
            """
            INSERT INTO phones (contact_id, phone, type)
            VALUES (%s, %s, %s)
            """,
            (contact_id, number, phone_type)
        )



def print_contacts(rows):
    
    if not rows:
        print("No contacts found.")
        return

    for contact_id, name, phone in rows:
        print(f"ID: {contact_id} | Name: {name} | Phone: {phone}")


def print_contacts_detailed(rows):
  
    if not rows:
        print("No contacts found.")
        return

    for contact_id, name, phone, email, group_name, phones in rows:
        print(
            f"ID: {contact_id} | Name: {name} | Phone: {phone} | "
            f"Email: {email or '-'} | Group: {group_name or '-'} | "
            f"Phones: {phones}"
        )



def add_contact(name, phone, email=None, birthday=None, group=None,
                phone_type="mobile"):
    """Task 3.1 — create a contact with the extended fields."""
    with connect() as conn:
        with conn.cursor() as cur:
            contact_id = insert_contact_row(
                cur, name, phone, email, birthday, group
            )
            insert_phones(cur, contact_id, [(phone, phone_type)])


def update_contact(contact_id, first_name=None, phone=None, email=None,
                   birthday=None, group=None):
    fields = []
    values = []

    if first_name:
        fields.append("first_name = %s")
        values.append(first_name)

    if phone:
        fields.append("phone = %s")
        values.append(phone)

    if email:
        fields.append("email = %s")
        values.append(email)

    if birthday:
        fields.append("birthday = %s")
        values.append(birthday)

    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT phone FROM contacts WHERE id = %s",
                (contact_id,)
            )
            row = cur.fetchone()

            if row is None:
                print("Contact not found.")
                return

            old_phone = row[0]

            if group:
                fields.append("group_id = %s")
                values.append(get_or_create_group(cur, group))

            if not fields:
                print("Nothing to update.")
                return

            values.append(contact_id)

            cur.execute(
                f"""
                UPDATE contacts
                SET {", ".join(fields)}
                WHERE id = %s
                """,
                values
            )
            changed = cur.rowcount

            if phone and phone != old_phone:
                cur.execute(
                    """
                    UPDATE phones
                    SET phone = %s
                    WHERE contact_id = %s AND phone = %s
                    """,
                    (phone, contact_id, old_phone)
                )
                if cur.rowcount == 0:
                    cur.execute(
                        """
                        INSERT INTO phones (contact_id, phone, type)
                        VALUES (%s, %s, 'mobile')
                        """,
                        (contact_id, phone)
                    )

    print("Contact updated." if changed else "Contact not found.")


def find_contacts(name=None, phone_prefix=None):
    
    conditions = []
    values = []

    if name:
        conditions.append("c.first_name ILIKE %s")
        values.append(f"%{name}%")

    if phone_prefix:
        conditions.append(
            "(c.phone LIKE %s OR EXISTS ("
            "SELECT 1 FROM phones p "
            "WHERE p.contact_id = c.id AND p.phone LIKE %s))"
        )
        values.extend([f"{phone_prefix}%", f"{phone_prefix}%"])

    sql = "SELECT id, first_name, phone FROM contacts c"

    if conditions:
        sql += " WHERE " + " AND ".join(conditions)

    sql += " ORDER BY id"

    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, values)
            rows = cur.fetchall()

    print_contacts(rows)


def delete_contact():
    choice = input("Delete by name or phone? (name/phone): ").strip().lower()

    if choice == "name":
        name = input("Enter exact name: ").strip()
        if not name:
            print("Name cannot be empty.")
            return
        delete_user_sql(name=name)
    elif choice == "phone":
        phone = input("Enter exact phone: ").strip()
        if not phone:
            print("Phone cannot be empty.")
            return
        delete_user_sql(phone=phone)
    else:
        print("Choose name or phone.")
        return

    print("Delete operation completed.")  



def search_contacts_sql(pattern):
    
    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT * FROM search_contacts(%s)",
                (pattern,)
            )
            rows = cur.fetchall()

    print_contacts_detailed(rows)


def insert_user_sql(name, phone):
    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "CALL insert_user(%s, %s)",
                (name, phone)
            )


def insert_many_users_sql(names, phones):
    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "CALL insert_many_users(%s, %s, %s)",
                (names, phones, None)
            )
            result = cur.fetchone()

    return result[0] if result else []


def delete_user_sql(name=None, phone=None):
    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "CALL delete_user(%s, %s)",
                (name, phone)
            )


def fetch_contacts_page(limit, offset):
    if limit <= 0 or offset < 0:
        raise ValueError(
            "Limit must be positive and offset cannot be negative."
        )

    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT * FROM get_contacts_page(%s, %s)",
                (limit, offset)
            )
            return cur.fetchall()


def browse_contacts():
    raw = input("Records per page: ").strip()
    try:
        page_size = int(raw)
    except ValueError:
        print("Please enter a number.")
        return

    if page_size <= 0:
        print("Page size must be positive.")
        return

    page = 0

    while True:
        rows = fetch_contacts_page(page_size, page * page_size)

        print(f"\n--- Page {page + 1} ---")
        print_contacts(rows)

        command = input("next / prev / quit > ").strip().lower()

        if command in ("next", "n"):
            if rows:
                page += 1
            else:
                print("No more records.")
        elif command in ("prev", "p"):
            if page > 0:
                page -= 1
            else:
                print("You are on the first page.")
        elif command in ("quit", "q"):
            break
        else:
            print("Unknown command — use next / prev / quit.")


SORT_ORDERS = {
    "name": "c.first_name",
    "birthday": "c.birthday NULLS LAST",
    "added": "c.created_at",
    "date added": "c.created_at",
}


def query_contacts_detailed(where="", params=(), order_by="c.first_name"):
    sql = f"""
        SELECT c.id, c.first_name, c.phone, c.email, g.name,
               COALESCE(string_agg(p.type || ': ' || p.phone,
                                   ', ' ORDER BY p.id), '-')
        FROM contacts c
        LEFT JOIN groups g ON g.id = c.group_id
        LEFT JOIN phones p ON p.contact_id = c.id
        {where}
        GROUP BY c.id, g.name
        ORDER BY {order_by}
    """

    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, params)
            rows = cur.fetchall()

    print_contacts_detailed(rows)


def filter_by_group():
    groups = list_groups()
    if not groups:
        print("No groups defined yet.")
        return

    print("Groups: " + ", ".join(groups))
    group = input("Group name (or part of it): ").strip()

    if not group:
        print("Group name cannot be empty.")
        return

    query_contacts_detailed("WHERE g.name ILIKE %s", (f"%{group}%",))


def search_by_email():
    query = input("Email or part of it (e.g. gmail): ").strip()

    if not query:
        print("Search text cannot be empty.")
        return

    query_contacts_detailed("WHERE c.email ILIKE %s", (f"%{query}%",))


def sort_contacts():
    order = input("Sort by name / birthday / added: ").strip().lower()

    if order not in SORT_ORDERS:
        print("Choose name, birthday or added.")
        return

    query_contacts_detailed("", (), SORT_ORDERS[order])


def advanced_menu():
    while True:
        print(
            "\n----- ADVANCED SEARCH & FILTER (task 3.2) -----\n"
            "1. Filter contacts by group\n"
            "2. Search contacts by email\n"
            "3. Sort contacts (name / birthday / date added)\n"
            "0. Back\n"
            "------------------------------------------------"
        )
        choice = input("Choose an option: ").strip()

        if choice == "1":
            filter_by_group()
        elif choice == "2":
            search_by_email()
        elif choice == "3":
            sort_contacts()
        elif choice == "0":
            break
        else:
            print("Unknown option.")



def import_csv(filename="contacts.csv"):
    """Task 3.3.3 — CSV import with email, birthday, group, phone_type."""
    added = skipped = 0

    with open(filename, newline="", encoding="utf-8-sig") as csv_file:
        reader = csv.DictReader(csv_file)

        if not reader.fieldnames or not {
            "first_name", "phone"
        }.issubset(reader.fieldnames):
            raise ValueError(
                "CSV must contain at least first_name and phone columns"
            )

        with connect() as conn:
            with conn.cursor() as cur:
                for row in reader:
                    name = (row.get("first_name") or "").strip()
                    phone = (row.get("phone") or "").strip()

                    if not name or not phone:
                        skipped += 1
                        continue

                    email = (row.get("email") or "").strip() or None
                    group = (row.get("group") or "").strip() or None

                    try:
                        birthday = parse_birthday(row.get("birthday"))
                    except ValueError:
                        print(f"  ! invalid birthday for '{name}' "
                              "— importing without it")
                        birthday = None

                    phone_type = (
                        row.get("phone_type") or "mobile"
                    ).strip().lower()
                    if phone_type not in PHONE_TYPES:
                        if row.get("phone_type"):
                            print(f"  ! invalid phone type for '{name}' "
                                  "— using 'mobile'")
                        phone_type = "mobile"

                    contact_id = insert_contact_row(
                        cur, name, phone, email, birthday, group
                    )
                    insert_phones(cur, contact_id, [(phone, phone_type)])
                    added += 1

    print(f"Added: {added}; skipped: {skipped}")


def export_contacts_json(filename="contacts.json"):
    
    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT c.id, c.first_name, c.phone, c.email, c.birthday, g.name
                FROM contacts c
                LEFT JOIN groups g ON g.id = c.group_id
                ORDER BY c.id
                """
            )
            contacts = cur.fetchall()

            cur.execute(
                "SELECT contact_id, phone, type FROM phones ORDER BY id"
            )
            phone_rows = cur.fetchall()

    phones_by_contact = {}
    for contact_id, number, phone_type in phone_rows:
        phones_by_contact.setdefault(contact_id, []).append(
            {"phone": number, "type": phone_type}
        )

    data = []
    for contact_id, name, phone, email, birthday, group_name in contacts:
        phones = phones_by_contact.get(contact_id, [])
        if all(item["phone"] != phone for item in phones):
            phones.insert(0, {"phone": phone, "type": "mobile"})

        data.append(
            {
                "first_name": name,
                "phone": phone,
                "email": email,
                "birthday": birthday.isoformat() if birthday else None,
                "group": group_name,
                "phones": phones,
            }
        )

    with open(filename, "w", encoding="utf-8") as json_file:
        json.dump(data, json_file, indent=2, ensure_ascii=False)

    print(f"Exported {len(data)} contacts to {filename}.")


def import_json(filename="contacts.json"):
    
    with open(filename, encoding="utf-8") as json_file:
        data = json.load(json_file)

    if not isinstance(data, list):
        raise ValueError("JSON file must contain a list of contacts")

    added = updated = skipped = 0

    with connect() as conn:
        with conn.cursor() as cur:
            for item in data:
                name = (item.get("first_name") or "").strip()
                phone = (item.get("phone") or "").strip()

                if not name or not phone:
                    skipped += 1
                    continue

                email = (item.get("email") or "").strip() or None
                group = (item.get("group") or "").strip() or None

                try:
                    birthday = parse_birthday(item.get("birthday"))
                except ValueError:
                    print(f"  ! invalid birthday for '{name}' "
                          "— importing without it")
                    birthday = None

                phones_list = []
                for phone_item in item.get("phones") or []:
                    number = (phone_item.get("phone") or "").strip()
                    ptype = (
                        phone_item.get("type") or "mobile"
                    ).strip().lower()
                    if number and ptype in PHONE_TYPES:
                        phones_list.append((number, ptype))

                if all(number != phone for number, _ in phones_list):
                    phones_list.insert(0, (phone, "mobile"))

                cur.execute(
                    "SELECT id FROM contacts WHERE first_name = %s",
                    (name,)
                )
                existing = cur.fetchone()

                if existing is None:
                    contact_id = insert_contact_row(
                        cur, name, phone, email, birthday, group
                    )
                    insert_phones(cur, contact_id, phones_list)
                    added += 1
                else:
                    answer = input(
                        f"Contact '{name}' already exists — "
                        "(s)kip or (o)verwrite? "
                    ).strip().lower()

                    if answer == "o":
                        contact_id = existing[0]
                        group_id = (
                            get_or_create_group(cur, group) if group else None
                        )

                        cur.execute(
                            """
                            UPDATE contacts
                            SET phone = %s, email = %s,
                                birthday = %s, group_id = %s
                            WHERE id = %s
                            """,
                            (phone, email, birthday, group_id, contact_id)
                        )
                        cur.execute(
                            "DELETE FROM phones WHERE contact_id = %s",
                            (contact_id,)
                        )
                        insert_phones(cur, contact_id, phones_list)
                        updated += 1
                    else:
                        skipped += 1

    print(f"Added: {added}; updated: {updated}; skipped: {skipped}")



def add_phone_console():
    name = input("Contact name: ").strip()
    phone = input("Phone number: ").strip()

    if not name or not phone:
        print("Contact name and phone cannot be empty.")
        return

    phone_type = ask_phone_type()

    call_procedure("CALL add_phone(%s, %s, %s)", (name, phone, phone_type))


def move_to_group_console():
    name = input("Contact name: ").strip()
    group = input("Group name: ").strip()

    if not name or not group:
        print("Contact name and group cannot be empty.")
        return

    call_procedure("CALL move_to_group(%s, %s)", (name, group))


def main():
    load_sql_file("schema.sql")      
    load_sql_file("procedures.sql")  

    while True:
        print(
            "\n========== PHONEBOOK ==========\n"
            "1. Add contact (email, birthday, group)\n"
            "2. Import contacts from CSV\n"
            "3. Find contacts (name / phone prefix)\n"
            "4. Update contact\n"
            "5. Delete contact\n"
            "6. Search by pattern (all fields + all phones)\n"
            "7. Insert or update user (SQL procedure)\n"
            "8. Insert many users (SQL procedure)\n"
            "9. Browse contacts page by page (next/prev/quit)\n"
            "10. Advanced search and filter (group / email / sort)\n"
            "11. Add phone to contact (SQL procedure)\n"
            "12. Move contact to group (SQL procedure)\n"
            "13. Export contacts to JSON\n"
            "14. Import contacts from JSON\n"
            "0. Exit\n"
            "================================"
        )

        choice = input("Choose an option: ").strip()

        try:
            if choice == "1":
                name = input("Name: ").strip()
                phone = input("Phone: ").strip()

                if not name or not phone:
                    print("Name and phone cannot be empty.")
                    continue

                email = input("Email (Enter to skip): ").strip() or None
                birthday = parse_birthday(
                    input("Birthday YYYY-MM-DD (Enter to skip): ")
                )
                phone_type = ask_phone_type()
                group = input("Group (Enter to skip): ").strip() or None

                add_contact(name, phone, email, birthday, group, phone_type)
                print("Contact added.")

            elif choice == "2":
                filename = input("CSV file [contacts.csv]: ").strip()
                import_csv(filename or "contacts.csv")

            elif choice == "3":
                name = input(
                    "Name or part of name (Enter to skip): "
                ).strip()
                prefix = input("Phone prefix (Enter to skip): ").strip()
                find_contacts(name or None, prefix or None)

            elif choice == "4":
                contact_id = int(input("Contact ID: "))
                name = input(
                    "New name (Enter to keep current): "
                ).strip()
                phone = input(
                    "New phone (Enter to keep current): "
                ).strip()
                email = input(
                    "New email (Enter to keep current): "
                ).strip()
                birthday = parse_birthday(
                    input("New birthday YYYY-MM-DD (Enter to keep): ")
                )
                group = input(
                    "New group (Enter to keep current): "
                ).strip()

                update_contact(
                    contact_id,
                    name or None,
                    phone or None,
                    email or None,
                    birthday,
                    group or None
                )

            elif choice == "5":
                delete_contact()

            elif choice == "6":
                pattern = input("Enter search pattern: ").strip()
                if pattern:
                    search_contacts_sql(pattern)
                else:
                    print("Pattern cannot be empty.")

            elif choice == "7":
                name = input("Name: ").strip()
                phone = input("Phone: ").strip()
                if name and phone:
                    insert_user_sql(name, phone)
                    print("User inserted or updated.")
                else:
                    print("Name and phone cannot be empty.")

            elif choice == "8":
                count = int(input("Number of users: "))
                if count <= 0:
                    print("Number must be positive.")
                    continue

                names = []
                phones = []

                for i in range(count):
                    print(f"\nUser {i + 1}:")
                    names.append(input("Name: ").strip())
                    phones.append(input("Phone: ").strip())

                incorrect = insert_many_users_sql(names, phones)

                if incorrect:
                    print("\nIncorrect data:")
                    for item in incorrect:
                        print(item)
                else:
                    print("All users processed successfully.")

            elif choice == "9":
                browse_contacts()

            elif choice == "10":
                advanced_menu()

            elif choice == "11":
                add_phone_console()

            elif choice == "12":
                move_to_group_console()

            elif choice == "13":
                filename = input("JSON file [contacts.json]: ").strip()
                export_contacts_json(filename or "contacts.json")

            elif choice == "14":
                filename = input("JSON file [contacts.json]: ").strip()
                import_json(filename or "contacts.json")

            elif choice == "0":
                print("Goodbye!")
                break

            else:
                print("Unknown option.")

        except (ValueError, FileNotFoundError, psycopg2.Error) as error:
            print(f"Error: {error}")


if __name__ == "__main__":
    main()
