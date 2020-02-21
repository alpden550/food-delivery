req:
	poetry export -f requirements.txt > requirements.txt --without-hashes

test:
	pytest -s -v
