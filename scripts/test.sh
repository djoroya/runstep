if [ -d ".conda" ]; then
  rm -r .conda
fi

conda create -p .conda 
conda activate .conda

pip install git+https://github.com/djoroya/runstep.git

cd .. 

python -c "from runstep.runstep import runstep"
