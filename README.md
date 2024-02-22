
# Clone repo and navigate to the directory
```bash
git clone git@github.com:lina-usc/q1k_postproc_erp.git
cd q1k_postproc_erp
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
