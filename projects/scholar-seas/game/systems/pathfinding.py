import heapq


def find_shortest_path(graph, start, end):
    distances = {}

    for island in graph:
        distances[island] = float("inf")

    distances[start] = 0

    previous = {}
    places_to_check = [(0, start)]

    while places_to_check:
        current_distance, current_island = heapq.heappop(
            places_to_check
        )

        if current_island == end:
            break

        if current_distance > distances[current_island]:
            continue

        for neighbour, travel_cost in graph[current_island]:
            new_distance = current_distance + travel_cost

            if new_distance < distances[neighbour]:
                distances[neighbour] = new_distance
                previous[neighbour] = current_island

                heapq.heappush(
                    places_to_check,
                    (new_distance, neighbour),
                )

    route = []
    current_island = end

    while current_island in previous:
        route.append(current_island)
        current_island = previous[current_island]

    route.append(start)
    route.reverse()

    if distances[end] == float("inf"):
        return [], None

    return route, distances[end]