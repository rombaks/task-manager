test:
	coverage run -m pytest
	coverage report
	coveralls

poetry_export:
	poetry export -f requirements.txt --output requirements.txt

