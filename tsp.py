import re
import sys

def generate_map(route_string):
    """
    This is a function that takes the route string and generates a dictionary containing the string,
    the individual trips, the length, and a dictionary of the trip indices where each location is present.

    We use this to find the next index without having to loop through the entire list every time.
    :param route_string:
    :return: dictionary
    """
    # Split route into the individual trips (length = stops = no_of_ids)
    trips = route_string.split(" ")

    # Remove any empty elements (i.e. starting/ending whitespace)
    while "" in trips:
        trips.remove("")

    # Convert the trips to arrays of length 2 (starting and stopping point).
    for i in range(len(trips)):
        # This is regex magic to get the numbers on either side of the comma.
        numbers = re.match("\\(([0-9]+),([0-9]+)\\)", trips[i])

        # Replace the string "(A,B)" with an array [(A), B]
        trips[i] = [numbers.group(1), numbers.group(2)]

    def generate_location_indices(route_trips):
        """
        Generate a dictionary:
            keys: locations
            values: the indices for which the location was found

        The purpose of this is to enable the fast lookup of next index
        :param route_trips:
        :return: a dictionary
        """
        locations = {}

        # Generate all the possible locations
        # TODO Can possibly be optimised by flattening the list of lists and uniq'ing?
        for i in list(range(len(route_trips))):
            trip = route_trips[i]
            for location in trip:
                if location in locations:
                    locations[location].append(i)
                else:
                    locations[location] = [i]

        return locations

    # Create a dictionary
    route_dict = {
        "string": route_string,
        "trips": trips,
        "length": len(trips),
        "map": generate_location_indices(trips)
    }

    return route_dict


def calc_route(route):
    """
    This function actually does the calculating.

    Its input is the result of the generate_map function.
    It returns all relevant information about the route.
    :param route: a generated map
    :return: a dictionary of route information.
    """

    # First we define some internal functions:
    def get_next_location(curr_trip, current_location):
        """
        This function calculates where we're going next
        :param curr_trip: the current trip (e.g. [A, B])
        :param current_location:  where we are now (e.g. A or B)
        :return: the next location (i.e. B or A)
        """
        first_or_last = curr_trip.index(current_location)

        if first_or_last == 0:
            next_stop = curr_trip[1]
        else:
            next_stop = curr_trip[0]

        return next_stop

    def get_next_index(possible_next_indices, already_visited):
        """
        This function calculates where to go next based on the possibilities calculated from the map.
        :param possible_next_indices: a list of possible indices to go to
        :param already_visited: a list of indices we've already seen
        :return: the next index or the string "end of tour"
        """
        for possible_next_index in possible_next_indices:
            if possible_next_index not in already_visited:
                return possible_next_index
        return 'end of tour'

    # And now we're getting to the actual work

    # Shorthand some commonly used variables
    route_map = route["map"]
    trips = route["trips"]

    # A record of where we've been
    visited = {
        "locations": [],
        "indices": []
    }

    # Prepare the resulting routes
    resulting_routes = []

    # Start looping over all IDs in our map:
    for location in route_map:

        # Have we already been here?
        if location not in visited["locations"]:

            # The subroute info, initialized
            subroute = {
                "locations": [],
                "indices": [],
                "trips": []
            }

            # Define where we start (the first index for the location)
            next_index = route_map[location][0]
            next_location = location

            ######################################
            #           MAGIC TIMES              #
            ######################################

            # We walk through the route until we reach the end
            while next_index not in visited["indices"]:

                # Just to for the sake of readability:
                curr_index = next_index
                curr_location = next_location
                trip = trips[curr_index]

                # Append our current index and location to the visited dictionary
                visited["indices"].append(curr_index)
                visited["locations"].append(curr_location)

                # Populate the information on the subroute thus far
                subroute["indices"].append(curr_index)
                subroute["locations"].append(curr_location)
                subroute["trips"].append(trip)

                # Calculate where to go next
                next_location = get_next_location(trip, curr_location)
                next_index = get_next_index(route["map"][next_location], visited["indices"])

                # If next_index == 'end of tour' - break out.
                # This happens when there are no unvisited indices for the next location.
                if next_index == 'end of tour':
                    break

            # Append the current subroute to the list of all the subroutes
            resulting_routes.append(subroute)

    # Return all the interesting information
    return {
        "routes": resulting_routes,
        "string": route["string"],
        "length": route["length"]
    }


def print_results(the_results):
    """
    This function just prints out the results nicely.
    :param the_results: the results of a call to calc_route
    :return:
    """
    the_routes = the_results["routes"]
    print(
        "This is the string (length {}) used for analysis:\n\t{}\n".format(the_results["length"], the_results["string"]))
    print("\tThere were a total of {} subroutes found.\n\n".format(len(the_routes)))
    for i in range(len(the_routes)):
        result = the_routes[i]
        locations = result["locations"]
        locations.sort()
        trips = result["trips"]
        trips.sort()
        indices = result["indices"]
        indices.sort()
        print("Showing subroute {}. Length: ".format(i + 1), len(trips))
        print("\tLocations included in this route: {}".format(locations))
        print("\tTrips in this subroute: {}".format(trips))
        print("\tIndices used in this subroute: {}\n".format(indices))


if len(sys.argv) == 1:

    print("Please input the route string in the form of '(A,B) (B,C) ...'.")
    print("Spaces at the beginning and end of the line do not matter.\n")
    print("Enter your input here:")
    route_str = input("> ")
else:
    print("Reading route from first line of passed file")
    route_str = open(sys.argv[1], 'r').readline()


our_map = generate_map(route_str)
results = calc_route(our_map)

print_results(results)
