# install requirements if they arent already
pip install -r requirements.txt
# make main have no console
mv src/main.py src/main.pyw
# build with pyinstaller to single file exectuable
pyinstaller -F src/main.pyw
# restore main.py
mv src/main.pyw src/main.py
# remove intermediate files used by pyinstaller
rm -r build/