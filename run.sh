
if [ ! -d "venv" ]; then
	python3 -m venv venv
	./venv/bin/pip install pygame
fi

./venv/bin/python main.py

