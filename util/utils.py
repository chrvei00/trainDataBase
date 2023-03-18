def getPath(conn, start_station, end_station):
    c = conn.cursor()

    query = "SELECT * FROM Delstrekning"
    c.execute(query)

    delstrekninger = c.fetchall()

    path = None
    if (end_station in map(lambda x: x[1], delstrekninger)):
        path = getPath2(start_station, end_station, delstrekninger)
    elif (end_station in map(lambda x: x[0], delstrekninger)):
        path = getPath2(start_station, end_station, list(map(lambda x: (x[1], x[0], x[2], x[3]), delstrekninger)))
    else:
        raise Exception("No path found")

    return path


def getPath2(start_station, end_station, segments):
    start_delstrekning = next(filter(
        lambda x: x[0] == start_station, segments), ("", "", 0, 0))

    path = [start_delstrekning]
    while path[-1][1] != end_station:
        next_delstrekning = next(filter(
            lambda x: x[0] == path[-1][1], segments), ("", "", 0, 0))
        path.append(next_delstrekning)

    return path
