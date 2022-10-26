test:
	coverage run -m pytest
	coverage report

poetry_export:
	poetry export -f requirements.txt --output requirements.txt