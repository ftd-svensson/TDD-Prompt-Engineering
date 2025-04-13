"""
Concert Itinerary Builder

This module provides functionality to build an itinerary of upcoming concerts.
"""

import math
from collections import defaultdict

class Concert:
    """
    Represents a concert event.
    
    Attributes:
        artist (str): The name of the artist performing.
        date (str): The date of the concert in 'YYYY-MM-DD' format.
        location (str): The location where the concert will take place.
        latitude (float): Latitude coordinate of the concert location.
        longitude (float): Longitude coordinate of the concert location.
    """
       

    def __init__(self, artist, date, location, latitude, longitude):
        self.artist = artist
        self.date = date
        self.location = location
        self.latitude = latitude
        self.longitude = longitude

class ItineraryBuilder:
    """
    A class to build concert itineraries. 
    """
    # :^)
    def build_itinerary(self, concerts):
        # Step 1: Sort concerts by date
        concerts = sorted(concerts, key=lambda c: c.date)
        
        # Step 2: Group concerts by artist
        artist_counts = defaultdict(int)
        for c in concerts:
            artist_counts[c.artist] += 1
        
        # Separate one-time and multi-concert artists
        one_time_concerts = [c for c in concerts if artist_counts[c.artist] == 1]
        multi_concerts = [c for c in concerts if artist_counts[c.artist] > 1]

        itinerary = []
        used_dates = set()  # Track used dates to avoid duplicates
        prev_concert = None  # Initially there is no previous concert

        # Step 3: Add one-time artists first (priority given to proximity on the same date)
        for c in one_time_concerts:
            if c.date not in used_dates:
                # If the date isn't used, add the concert to the itinerary
                itinerary.append(c)
                used_dates.add(c.date)
                
                if prev_concert == None:
                    prev_concert = c  # Now the previous concert is this one
                else:
                    prev_concert = itinerary[len(itinerary)-2]
            else:
                # If the date is already used, check if it's closer than the current prev_concert
                if prev_concert:
                    distance_to_prev = self._distance(prev_concert.latitude, prev_concert.longitude, c.latitude, c.longitude)
                    # Find last concert on this date
                    last_concert_same_date = next(
                        (x for x in itinerary if x.date == c.date), None)
                    
                    if last_concert_same_date:
                        distance_to_last = self._distance(last_concert_same_date.latitude,
                                                          last_concert_same_date.longitude, c.latitude, c.longitude)
                        # If the current concert is closer to prev_concert, we use it
                        if distance_to_prev < distance_to_last:
                            # Replace the last concert of this date
                            itinerary.remove(last_concert_same_date)
                            itinerary.append(c)
                            used_dates.add(c.date)
                            prev_concert = c
                    else:
                        # Otherwise, just add it as normal
                        itinerary.append(c)
                        used_dates.add(c.date)
                        prev_concert = c

        # Step 4: Add remaining multi-concert artists by closest distance
        remaining = [c for c in multi_concerts if c.date not in used_dates]
        date_groups = defaultdict(list)
        
        for c in remaining:
            date_groups[c.date].append(c)

        # Step 5: Process concerts in each date group
        for date in sorted(date_groups.keys()):
            options = date_groups[date]
            
            if prev_concert:
                # If there are multiple concerts on the same day, choose the closest concert first
                chosen = min(
                    options,
                    key=lambda c: self._distance(
                        prev_concert.latitude, prev_concert.longitude, c.latitude, c.longitude
                    )
                )
            else:
                # If there is no previous concert, pick the first concert
                chosen = options[0]
            
            # After proximity selection, ensure no duplicate dates
            if chosen.date not in used_dates:
                itinerary.append(chosen)
                used_dates.add(chosen.date)
                prev_concert = chosen

        # Step 6: Return the final itinerary
        return itinerary



    def findArtist(self, concerts, artist):
        returnList = []
        for concert in concerts:
            if concert.artist == artist:
                returnList.append(concert)
        if returnList == []:
            returnList.append(Concert(artist, None, None, None, None))
        return returnList
        
    def sortConcerts(self, concerts):
        return sorted(concerts, key = lambda concert : concert.date)
    
    def singleDatesOnly(self, concerts):
        sortedConcerts = self.sortConcerts(concerts)
        returnList = []
        currentArtists = []
        for concert in sortedConcerts:
            if concert.artist not in currentArtists:
                returnList.append(concert)
                currentArtists.append(concert.artist)

        return returnList

    def _distance(self, lat1, lon1, lat2, lon2):
        # Haversine formula to calculate the distance between two points on Earth
        R = 6371  # Earth radius in km
        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)
        a = math.sin(dlat / 2) ** 2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        return R * c  # Returns distance in kilometers

if __name__ == "__main__":
    from concerts_data import get_all_concerts
    
    all_concerts = get_all_concerts()