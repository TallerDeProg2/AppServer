PYTHONPATH=. py.test --cov=./src/main ./src/test
cd ..
mv ./src/test/.coverage .coverage
