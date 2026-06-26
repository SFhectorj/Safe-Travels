import unittest
from unittest.mock import patch
import io
import sys
from main import display_history, calculate_route

class TestSafeTravelsCLI(unittest.TestCase):
  @patch('main.get_route_history')
  def test_display_history_empty(self, mock_get_history):
    '''
    TEST 1: Checks happens when the user has no history.
    verifies that when get_route_history() returns an empty list, display_history() prints the expected message.
    '''
    # Mock the database to return an empty list
    mock_get_history.return_value = []
    
    # Capture the terminal output
    captured_output = io.StringIO()
    sys.stdout = captured_output
    
    # Run the function
    display_history(user_id=1)
    
    # Restore normal terminal output
    sys.stdout = sys.__stdout__
    
    # Assert that the CLI told the user there is no history
    self.assertIn("No route history found.", captured_output.getvalue())
    
  @patch('main.get_route_history')
  def test_display_history_with_data(self, mock_get_history):
    '''
    TEST 2: Test for previous saved history.
    verifies that when get_route_history() returns an existing route when available.
    '''
      
    # Mock the database to return a fake past route
    mock_get_history.return_value = [
      {'route_id': 101, 'date': '2026-06-25', 'end_location': 'Dixon Rec Center', 'hazards_avoided': 3}
    ]
      
    captured_output = io.StringIO()
    sys.stdout = captured_output
      
    display_history(user_id=1)
    sys.stdout = sys.__stdout__
    
    # Assert the table formatted correctly and displayed our mock data
    output = captured_output.getvalue()
    self.assertIn("101", output)
    self.assertIn("Dixon Rec Center", output)
    self.assertIn("3", output)
      
  # patch input() to simulate a user typing 'n' to directions and 'n' to saving
  @patch('builtins.input', side_effect=['n', 'n']) 
  @patch('main.find_best_routes')
  @patch('main.get_saved_location')
  def test_calculate_route_output(self, mock_get_location, mock_find_routes, mock_input):
    '''
    TEST 3: Check routing logic formats API data correctly
    test only the logic inside calculate_route() from main.py using mock actions
    '''
    # Mock the database translating aliases
    mock_get_location.side_effect = ["Home", "Library"]
        
    # Mock the API returning safe and quick routes
    mock_find_routes.return_value = {
      "quickest": {"distance_m": 1000, "duration_s": 600, "hazard_score": 5, "directions": ["Turn left"]},
      "safest": {"distance_m": 1200, "duration_s": 800, "hazard_score": 1, "directions": ["Turn right"], "total_incidents": 2}
    }
        
    captured_output = io.StringIO()
    sys.stdout = captured_output
        
    # Run the function
    calculate_route(user_id=1, start_input="Home", end_input="Library")
    sys.stdout = sys.__stdout__
        
    output = captured_output.getvalue()
        
    # Assert the function correctly handled the mock data
    self.assertIn("Planning route from: 'Home, Los Angeles, CA' to 'Library, Los Angeles, CA'", output)
    self.assertIn("Route B (Safest)", output)
    self.assertIn("Route discarded.", output)

if __name__ == '__main__':
    unittest.main()
