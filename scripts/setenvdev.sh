pip install -r requirements.txt


python <<EOF
import os,sys
# select the elements of path list who  contains the word 'site-packages'
site = [x for x in sys.path if 'site-packages' in x]

# take current working directory
cwd = os.getcwd()
print(cwd)
# create a new file named conda.pth in the site-packages directory
with open(os.path.join(site[0], 'conda.pth'), 'w') as f:
    f.write(cwd)
EOF

python -c "from runstep.runstep import runstep"
