from flask import Flask, render_template, request, jsonify
import logging

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Calculator:
    """Calculator class with basic arithmetic operations"""
    
    @staticmethod
    def add(a, b):
        """Add two numbers"""
        return a + b
    
    @staticmethod
    def subtract(a, b):
        """Subtract two numbers"""
        return a - b
    
    @staticmethod
    def multiply(a, b):
        """Multiply two numbers"""
        return a * b
    
    @staticmethod
    def divide(a, b):
        """Divide two numbers"""
        if b == 0:
            raise ValueError("Cannot divide by zero")
        return a / b

calculator = Calculator()

@app.route('/')
def index():
    """Render the calculator interface"""
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    """Handle calculation requests"""
    try:
        data = request.get_json()
        
        if not data or 'operation' not in data or 'num1' not in data or 'num2' not in data:
            return jsonify({'error': 'Invalid input data'}), 400
        
        operation = data['operation']
        num1 = float(data['num1'])
        num2 = float(data['num2'])
        
        logger.info(f"Calculating: {num1} {operation} {num2}")
        
        if operation == '+':
            result = calculator.add(num1, num2)
        elif operation == '-':
            result = calculator.subtract(num1, num2)
        elif operation == '*':
            result = calculator.multiply(num1, num2)
        elif operation == '/':
            result = calculator.divide(num1, num2)
        else:
            return jsonify({'error': 'Invalid operation'}), 400
        
        return jsonify({'result': result})
    
    except ValueError as e:
        logger.error(f"Calculation error: {str(e)}")
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return jsonify({'error': 'An unexpected error occurred'}), 500

@app.route('/health')
def health_check():
    """Health check endpoint for monitoring"""
    return jsonify({'status': 'healthy', 'service': 'calculator-app'}), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)