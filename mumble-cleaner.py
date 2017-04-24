import re
import sqlite3


def main():
    with sqlite3.connect('murmur.sqlite') as conn:
        c = conn.cursor()
        c.execute('SELECT channel_id, name FROM channels WHERE parent_id = 0')
        channels = {int(row[0]): row[1] for row in c.fetchall()}

        c.execute("SELECT msg FROM slog WHERE msg LIKE '<%> Moved %:%(%) to %[%]'")
        active_channels = list(set(map(
            lambda y: find_parent_id(conn, y),
            set(map(
                lambda x: int(re.search('\[(\d+)', x[0]).group(1)), c.fetchall()
            ))
        )))

        print(active_channels)

        print(len(list(filter(lambda x: x[0] not in active_channels, channels.items()))))


def find_parent_id(conn, channel_id: int):
    c = conn.cursor()
    c.execute('SELECT parent_id FROM channels WHERE channel_id = ' + str(channel_id))
    parent = c.fetchone()
    if parent is not None:
        parent = parent[0]

    if parent is None or channel_id == 0:
        return channel_id

    find_parent_id(conn, parent)


if __name__ == '__main__':
    main()
