pip install --upgrade pip

if [ -f requirements.txt ]; then
    echo "Installing requirements..."
    pip install -r requirements.txt
fi

if [ -f requirements-dev.txt ]; then
    echo "Installing development requirements..."
    pip install -r requirements-dev.txt
fi
