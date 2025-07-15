import pytest
import json
from app import app, Calculator

@pytest.fixture
def client():
    """Create a test client for the Flask app"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@pytest.fixture
def calculator():
    """Create a calculator instance for testing"""
    return Calculator()

class TestCalculator:
    """Test class for Calculator operations"""
    
    def test_add(self, calculator):
        """Test addition operation"""
        result = calculator.add(5, 3)
        assert result == 8
        
        result = calculator.add(-5, 3)
        assert result == -2
        
        result = calculator.add(0, 0)
        assert result == 0
        
        result = calculator.add(1.5, 2.5)
        assert result == 4.0
    
    def test_subtract(self, calculator):
        """Test subtraction operation"""
        result = calculator.subtract(5, 3)
        assert result == 2
        
        result = calculator.subtract(-5, 3)
        assert result == -8
        
        result = calculator.subtract(0, 0)
        assert result == 0
        
        result = calculator.subtract(10.5, 2.5)
        assert result == 8.0
    
    def test_multiply(self, calculator):
        """Test multiplication operation"""
        result = calculator.multiply(5, 3)
        assert result == 15
        
        result = calculator.multiply(-5, 3)
        assert result == -15
        
        result = calculator.multiply(0, 10)
        assert result == 0
        
        result = calculator.multiply(2.5, 4)
        assert result == 10.0
    
    def test_divide(self, calculator):
        """Test division operation"""
        result = calculator.divide(10, 2)
        assert result == 5
        
        result = calculator.divide(-10, 2)
        assert result == -5
        
        result = calculator.divide(7, 2)
        assert result == 3.5
        
        result = calculator.divide(0, 5)
        assert result == 0
    
    def test_divide_by_zero(self, calculator):
        """Test division by zero raises ValueError"""
        with pytest.raises(ValueError, match="Cannot divide by zero"):
            calculator.divide(10, 0)
        
        with pytest.raises(ValueError, match="Cannot divide by zero"):
            calculator.divide(-5, 0)

class TestFlaskRoutes:
    """Test class for Flask routes"""
    
    def test_index_route(self, client):
        """Test the main index route"""
        response = client.get('/')
        assert response.status_code == 200
        assert b'Calculator' in response.data
        assert b'calculator | CI/CD Project' in response.data
    
    def test_health_check(self, client):
        """Test the health check endpoint"""
        response = client.get('/health')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert data['status'] == 'healthy'
        assert data['service'] == 'calculator-app'
    
    def test_calculate_addition(self, client):
        """Test addition via API"""
        response = client.post('/calculate', 
                              json={'operation': '+', 'num1': 5, 'num2': 3})
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert data['result'] == 8
    
    def test_calculate_subtraction(self, client):
        """Test subtraction via API"""
        response = client.post('/calculate', 
                              json={'operation': '-', 'num1': 10, 'num2': 4})
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert data['result'] == 6
    
    def test_calculate_multiplication(self, client):
        """Test multiplication via API"""
        response = client.post('/calculate', 
                              json={'operation': '*', 'num1': 6, 'num2': 7})
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert data['result'] == 42
    
    def test_calculate_division(self, client):
        """Test division via API"""
        response = client.post('/calculate', 
                              json={'operation': '/', 'num1': 15, 'num2': 3})
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert data['result'] == 5
    
    def test_calculate_division_by_zero(self, client):
        """Test division by zero via API"""
        response = client.post('/calculate', 
                              json={'operation': '/', 'num1': 10, 'num2': 0})
        assert response.status_code == 400
        
        data = json.loads(response.data)
        assert 'error' in data
        assert 'Cannot divide by zero' in data['error']
    
    def test_calculate_invalid_operation(self, client):
        """Test invalid operation via API"""
        response = client.post('/calculate', 
                              json={'operation': '%', 'num1': 10, 'num2': 3})
        assert response.status_code == 400
        
        data = json.loads(response.data)
        assert 'error' in data
        assert 'Invalid operation' in data['error']
    
    def test_calculate_missing_data(self, client):
        """Test missing data in API request"""
        response = client.post('/calculate', json={'operation': '+'})
        assert response.status_code == 400
        
        data = json.loads(response.data)
        assert 'error' in data
        assert 'Invalid input data' in data['error']
    
    def test_calculate_invalid_numbers(self, client):
        """Test invalid number inputs via API"""
        response = client.post('/calculate', 
                              json={'operation': '+', 'num1': 'abc', 'num2': 3})
        assert response.status_code == 400
        
        data = json.loads(response.data)
        assert 'error' in data

class TestEdgeCases:
    """Test edge cases and boundary conditions"""
    
    def test_large_numbers(self, calculator):
        """Test with large numbers"""
        result = calculator.add(999999999, 1)
        assert result == 1000000000
        
        result = calculator.multiply(1000000, 1000000)
        assert result == 1000000000000
    
    def test_small_numbers(self, calculator):
        """Test with very small numbers"""
        result = calculator.add(0.000001, 0.000001)
        assert abs(result - 0.000002) < 1e-10
        
        result = calculator.multiply(0.1, 0.1)
        assert abs(result - 0.01) < 1e-10
    
    def test_negative_numbers(self, calculator):
        """Test with negative numbers"""
        result = calculator.add(-5, -3)
        assert result == -8
        
        result = calculator.subtract(-5, -3)
        assert result == -2
        
        result = calculator.multiply(-5, -3)
        assert result == 15
        
        result = calculator.divide(-10, -2)
        assert result == 5

if __name__ == '__main__':
    pytest.main(['-v', __file__])