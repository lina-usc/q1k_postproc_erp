## Create the virtual environment
```bash
python3.10 -m venv env
source env/bin/activate
```

## Clone packages into the env and install them
```bash
cd env

git clone https://github.com/mne-tools/mne-icalabel.git
cd mne-icalabel
git checkout maint/0.4
pip install .
cd ..

git clone git@github.com:lina-usc/pylossless.git
cd pylossless
pip install .
cd ../..
```

##Install remaining packages and create the ipykernel
```bash
pip install openneuro-py
pip install EDFLib-Python

pip install ipykernel
python -m ipykernel install --user --name=q1k_postproc_erp
```

## copy pylossless output files from the remote compute cluster..
If this is the first task to be downloaded to the local drive then dowload the entire sub-### folder
```bash
scp -r jdesjard@narval.computecanada.ca:/project/def-emayada/q1k/pilot/q1k-external-pilot/derivatives/pylossless/sub-002 .
```
If the subject has already been downloaded for another task then just get the specific task of interest and then update the *_scans.tsv file
```bash
cd ~/q1k/pilot/q1k-external-pilot/derivatives/pylossless
scp jdesjard@narval.computecanada.ca:/project/def-emayada/q1k/pilot/q1k-external-pilot/derivatives/pylossless/sub-002/ses-01/eeg/*_task-ap_* sub-002/ses-01/eeg/
scp jdesjard@narval.computecanada.ca:/project/def-emayada/q1k/pilot/q1k-external-pilot/derivatives/pylossless/sub-002/ses-01/*_scans.tsv sub-002/ses-01/
```
