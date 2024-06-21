import sqlite3
connection = sqlite3.connect("creds.db")

cursor = connection.cursor()

#cursor.execute("DROP TABLE credentials")
cursor.execute("CREATE TABLE IF NOT EXISTS credentials (userid INTEGER, firstName TEXT, lastName TEXT, username TEXT, password TEXT)")
cursor.execute("INSERT INTO credentials VALUES (1, 'alice', 'kim', 'akim001', 'aSVUism209')")
cursor.execute("INSERT INTO credentials VALUES (2, 'bob', 'mcdaniels', 'mcdanielsbob', 'FS80VJlsj@#')")
cursor.execute("INSERT INTO credentials VALUES (3, 'steve', 'burton', 'steven.burton', 's*S0-afjvSU')")

cursor.execute("CREATE TABLE IF NOT EXISTS permissions (userid INTEGER, permissionid INTEGER)")
cursor.execute("INSERT INTO permissions VALUES (1, 1)")
cursor.execute("INSERT INTO permissions VALUES (1, 2)")
cursor.execute("INSERT INTO permissions VALUES (1, 3)")
cursor.execute("INSERT INTO permissions VALUES (2, 1)")

cursor.execute("CREATE TABLE IF NOT EXISTS permission_labels (permissionid INTEGER, rolename TEXT)")
cursor.execute("INSERT INTO permission_labels VALUES (1, 'read_access')")
cursor.execute("INSERT INTO permission_labels VALUES (2, 'write_access')")
cursor.execute("INSERT INTO permission_labels VALUES (3, 'admin_access')")

connection.commit()

cursor.execute("SELECT * FROM credentials")
rows = cursor.fetchall()
for row in rows:
    print(row)
cursor.close()

print(connection.total_changes)

connection.close()