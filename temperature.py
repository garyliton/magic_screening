from csv import reader


class Temperature:
    def __init__(self, filename):
        self.temperatures = {}
        self.parse_file(filename)

    def parse_file(self, filename):
        """
        When class is instantiated, this function is called to parse the csv file
        and store it in a dictionary where the key is the station_id
        and the value is a list of list containing date and temperature data

        @param filename:  (string) csv file path
        """
        with open(filename, 'r') as file:
            r = reader(file)
            next(r, None)
            for row in r:
                station_id, date, temp = row
                if station_id not in self.temperatures:
                    self.temperatures[station_id] = []

                self.temperatures[station_id].append([float(date), float(temp)])

    def get_lowest_temp(self):
        """
        Retrieves the lowest_temp recorded from temperatures dict

        @return: (tuple) containing station_id and date of the lowest temperature recorded
        """
        lowest_temp = float("inf")
        lowest_temp_station_id = None
        lowest_temp_date = None

        # loop through each key (station_id), value pair in the temperatures dict
        for stn_id, data in self.temperatures.items():
            # loop through each date, temp data for the current station_id
            for date, temp in data:
                if temp < lowest_temp:
                    lowest_temp = temp
                    lowest_temp_station_id = stn_id
                    lowest_temp_date = date

        #  if csv file is empty
        if lowest_temp_date is None:
            return (None, None)

        return (lowest_temp_station_id, str(lowest_temp_date))

    def get_most_fluctuation(self):
        """
        retrieves the station_id that experienced the most amount of temperature fluctuation
         across all dates that it reported temperatures for

        @return: (String) station_id that experienced the most amount of temperature fluctuation
        """
        max_fluctuation = float("-inf")
        station_id = None

        for stn_id, data in self.temperatures.items():
            fluctuation = self.calculate_fluctuation(data)

            if fluctuation > max_fluctuation:
                max_fluctuation = fluctuation
                station_id = stn_id

        return station_id if station_id else None

    def get_most_fluctuation_range(self, start_date, end_date):
        """
        Retrieves the station_id that experienced the most amount of temperature fluctuation
        for any given range of dates

        @param start_date: (String) start date
        @param end_date: (String) end date
        @return: (String) station_id
        """
        max_fluctuation = float("-inf")
        station_id = None

        for stn_id, data in self.temperatures.items():
            date_range_data = []
            for item in data[1:]:
                date = item[0]
                if date >= float(start_date) and date <= float(end_date):
                    date_range_data.append(item)

            if date_range_data:
                fluctuation = self.calculate_fluctuation(date_range_data)
            else:
                continue

            if fluctuation > max_fluctuation:
                max_fluctuation = fluctuation
                station_id = stn_id

        return station_id if station_id else None

    def calculate_fluctuation(self, data):
        """
        Helper function to calculate fluctutation over a given set of data

        @param data: (List of List) containing data and temps
        @return: (Int) Total Fluctuation
        """
        fluctuation = 0
        prev_temp = data[0][-1]
        for date, temp in data[1:]:
            fluctuation += abs(prev_temp - temp)
            prev_temp = temp

        return fluctuation

