cd ./test
py.test --cov=./
cd ..
mv ./test/.coverage .coverage
