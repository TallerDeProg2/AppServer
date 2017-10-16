PYTHONPATH=. py.test --cov=./src/main ./src/test
cd ..
mv ./test/.coverage .coverage
