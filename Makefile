.PHONY: setup test run lint clean

setup:
	python -m pip install --upgrade pip
	pip install -r requirements.txt
	pip install -r requirements-dev.txt

test:
	pytest tests/

run:
	python scripts/run_pipeline.py

lint:
	flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
	flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics

clean:
	python -c "import shutil, glob; [shutil.rmtree(p, ignore_errors=True) for p in glob.glob('**/__pycache__', recursive=True) + glob.glob('.pytest_cache') + glob.glob('.ipynb_checkpoints')]"
