
# Clone repo and navigate to the directory
```bash
git clone git@github.com:jadesjardins/acar-q1k-pilot-seg.git
cd acar-q1k-pilot-seg
```

# Create and source the Python virtual environment
```bash
python3 -m venv env
source env/bin/activate
```

# Install the required packages
```bash
pip install pylossless
pip install pyqt5==5.12.0
pip install mne-qt-browser
pip install plotly
pip install ipykernel
```

# Create the kernel to use for the notebook.
```bash
python -m ipykernel install --user --name=q1k_postproc
```
