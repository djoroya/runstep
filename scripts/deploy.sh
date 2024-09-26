if [ -d "dist" ]; then
  rm -r dist
fi

if [ -d "build" ]; then
  rm -r build
fi

rm -r *.egg-info

python setup.py sdist
python setup.py bdist_wheel