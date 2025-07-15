#!/bin/bash

# Calculator App CI/CD Project Setup Script
# This script helps you set up the project quickly

echo "🧮 Calculator App CI/CD Project Setup"
echo "======================================"

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_header() {
    echo -e "${BLUE}$1${NC}"
}

# Check if Python is installed
check_python() {
    if command -v python3 &> /dev/null; then
        PYTHON_VERSION=$(python3 --version 2>&1 | cut -d' ' -f2)
        print_status "Python $PYTHON_VERSION found"
        return 0
    else
        print_error "Python 3 is not installed. Please install Python 3.9 or higher."
        return 1
    fi
}

# Check if Docker is installed
check_docker() {
    if command -v docker &> /dev/null; then
        DOCKER_VERSION=$(docker --version | cut -d' ' -f3 | cut -d',' -f1)
        print_status "Docker $DOCKER_VERSION found"
        return 0
    else
        print_warning "Docker is not installed. Some features may not work."
        return 1
    fi
}

# Check if Git is installed
check_git() {
    if command -v git &> /dev/null; then
        GIT_VERSION=$(git --version | cut -d' ' -f3)
        print_status "Git $GIT_VERSION found"
        return 0
    else
        print_error "Git is not installed. Please install Git."
        return 1
    fi
}

# Create project directory structure
create_structure() {
    print_header "Creating project structure..."
    
    # Create templates directory
    mkdir -p templates
    print_status "Created templates directory"
    
    # Create static directory (optional)
    mkdir -p static/css static/js
    print_status "Created static directories"
    
    # Create tests directory
    mkdir -p tests
    print_status "Created tests directory"
    
    # Create docs directory
    mkdir -p docs
    print_status "Created docs directory"
}

# Setup Python virtual environment
setup_venv() {
    print_header "Setting up Python virtual environment..."
    
    if [ ! -d "venv" ]; then
        python3 -m venv venv
        print_status "Virtual environment created"
    else
        print_warning "Virtual environment already exists"
    fi
    
    # Activate virtual environment
    source venv/bin/activate
    print_status "Virtual environment activated"
    
    # Upgrade pip
    pip install --upgrade pip
    print_status "pip upgraded"
    
    # Install dependencies
    if [ -f "requirements.txt" ]; then
        pip install -r requirements.txt
        print_status "Dependencies installed"
    else
        print_warning "requirements.txt not found"
    fi
}

# Run tests
run_tests() {
    print_header "Running tests..."
    
    if [ -f "test_calculator.py" ]; then
        python -m pytest test_calculator.py -v
        if [ $? -eq 0 ]; then
            print_status "All tests passed!"
        else
            print_error "Some tests failed"
        fi
    else
        print_warning "test_calculator.py not found"
    fi
}

# Build Docker image
build_docker() {
    print_header "Building Docker image..."
    
    if [ -f "Dockerfile" ]; then
        docker build -t calculator-app .
        if [ $? -eq 0 ]; then
            print_status "Docker image built successfully"
        else
            print_error "Docker build failed"
        fi
    else
        print_warning "Dockerfile not found"
    fi
}

# Main setup function
main() {
    print_header "Starting setup process..."
    
    # Check prerequisites
    check_python || exit 1
    check_git || exit 1
    DOCKER_AVAILABLE=$(check_docker; echo $?)
    
    # Create project structure
    create_structure
    
    # Setup Python environment
    setup_venv
    
    # Run tests
    run_tests
    
    # Build Docker image if available
    if [ $DOCKER_AVAILABLE -eq 0 ]; then
        build_docker
    fi
    
    print_header "Setup complete! 🎉"
    echo ""
    echo "Next steps:"
    echo "1. Activate virtual environment: source venv/bin/activate"
    echo "2. Run the application: python app.py"
    echo "3. Open http://localhost:5000 in your browser"
    echo "4. (Optional) Run with Docker: docker run -p 5000:5000 calculator-app"
    echo ""
    echo "For CI/CD setup:"
    echo "1. Push code to GitLab repository"
    echo "2. Configure GitLab CI/CD variables"
    echo "3. The pipeline will run automatically"
    echo ""
    print_status "Happy coding! 🚀"
}

# Run main function
main "$@"