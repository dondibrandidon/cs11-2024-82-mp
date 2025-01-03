sphinx-build ./docs ./docs/html
echo
echo "Running mypy!"
mypy . --strict
echo
echo "Running pytest!"
pytest .