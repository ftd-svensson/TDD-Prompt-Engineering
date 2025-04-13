"""
Unit tests for the Concert Itinerary Builder.

This file contains unit tests for the ItineraryBuilder class in main.py.
Participants will implement tests based on the system specifications.
"""

import unittest
from main import Concert, ItineraryBuilder
from concerts_data import get_all_concerts

class ItineraryBuilderTest(unittest.TestCase):
    """Test cases for the ItineraryBuilder class."""
    
    def setUp(self):
        """Set up for the tests."""
        self.builder = ItineraryBuilder()
        
        self.all_concerts = get_all_concerts()
    
    # ----- Manual Test Cases -----
    # Participants will implement their manual test cases here. 
    
    def test_manual_1(self):
        """First manually written test case."""
        """Some artists may have no concerts on the list. In that case, that should be indicated in the itinerary"""
        # TODO: Implement this test
        #self.assertListEqual(self.builder.build_itinerary(self.all_concerts), [])
        self.assertIsNotNone(self.builder.findArtist(self.all_concerts, "Adele"))
        self.assertEqual(len(self.builder.findArtist(self.all_concerts, "Miguel Del Santo")), 1)
        
        

    def test_manual_2(self):
        """Second manually written test case."""
        """The itinerary should return a list of concerts sorted in chronological order (by date from earliest to latest)"""
        # TODO: Implement this test
        #self.assertListEqual(self.builder.build_itinerary(self.all_concerts), [])
        self.assertListEqual(self.builder.sortConcerts(self.all_concerts), sorted(self.all_concerts, key= lambda concert: concert.date))
            
        


    def test_manual_3(self):
        """Third manually written test case."""
        """An artist has at most one concert in the itinerary. If an artist has more than one concert in the list, the itinerary should only include the one with the earliest start date."""
        # TODO: Implement this test
        #self.assertListEqual(self.builder.build_itinerary(self.all_concerts), [])
        self.assertLess(len(self.builder.singleDatesOnly(self.all_concerts)), len(self.all_concerts))

        
    
    # ----- AI-Assisted Test Cases -----
    # Participants will implement their AI-assisted test cases here.
    # Please name your test in a way which indicates that these are AI-assisted test cases.
    def test_AI_1(self):
        """
        No two concerts may take place on the same day.
        If multiple concerts are on the same date, only the one closest to the previous concert is included.
        """
        # Assume starting from concert A
        c1 = Concert("A", "2025-07-01", "StartCity", 0.0, 0.0)
        c2 = Concert("B", "2025-07-02", "FarCity", 10.0, 10.0)   # farther
        c3 = Concert("C", "2025-07-02", "NearCity", 1.0, 1.0)    # closer

        itinerary = self.builder.build_itinerary([c1, c2, c3])

        dates = [c.date for c in itinerary]
        self.assertEqual(len(set(dates)), len(dates), "Concert dates must be unique")

        self.assertIn("C", [c.artist for c in itinerary])
        self.assertNotIn("B", [c.artist for c in itinerary])

    def test_AI_2(self):
        """
        The itinerary should return concerts with artist, date, and location.
        """
        concerts = [
            Concert("Taylor Swift", "2025-08-01", "LA", 34.05, -118.25),
            Concert("Drake", "2025-08-02", "NYC", 40.71, -74.01),
        ]

        itinerary = self.builder.build_itinerary(concerts)

        for c in itinerary:
            self.assertIsInstance(c.artist, str)
            self.assertRegex(c.date, r"\d{4}-\d{2}-\d{2}")
            self.assertIsInstance(c.location, str)
            
        


    def test_AI_3(self):
        """
        Artists with only one concert should be prioritized over artists with multiple concerts.
        """
        concerts = [
            Concert("Popular Artist", "2025-08-01", "City 1", 50.0, -70.0),
            Concert("Popular Artist", "2025-08-02", "City 2", 51.0, -71.0),
            Concert("One-time Artist", "2025-08-03", "City 3", 52.0, -72.0),
        ]

        itinerary = self.builder.build_itinerary(concerts)
        artists = [c.artist for c in itinerary]

        # One-time artist should be included
        self.assertIn("One-time Artist", artists)

        # One-time Artist must appear before Popular Artist
        one_time_index = artists.index("One-time Artist")
        popular_indexes = [i for i, a in enumerate(artists) if a == "Popular Artist"]
        self.assertTrue(
            all(one_time_index < i for i in popular_indexes),
            "One-time artists should appear before multi-concert artists"
        )

    

if __name__ == "__main__":
    unittest.main()