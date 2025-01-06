import numpy as np
import pandas as pd
import pylossless as ll
import mne
import mne_bids

def apply_ll(bids_path, ll_state, eeg_ll_raw):

    ##load the lossless state...
    #ll_state = ll.LosslessPipeline()
    #ll_state = ll_state.load_ll_derivative(bids_path)
    bids_path_str=str(bids_path)

    # Merge marks down to bads (aka manual)
    #ll_qcr = ll_state.raw.copy()
    manual = []
    for flag_type in ll_state.flags['ch']:
        manual.extend(ll_state.flags['ch'][flag_type])
    print(ll_state.flags['ch'])
    eeg_ll_raw.info['bads'].extend(manual)
    eeg_ll_raw.info['bads'] = list(set(eeg_ll_raw.info['bads']))

    fig = eeg_ll_raw.plot_sensors(show_names=True)

    # Read the ICLabel info from file and add to exclude
    df = pd.read_csv(bids_path_str.replace('_eeg.edf', '_iclabels.tsv'), sep='\t')
    ll_state.ica2.exclude = list(df[df['ic_type'].str.match('eog|muscle|ch_noise|ecg')].index)

    # Load the data and apply the ICA
    eeg_ll_raw.load_data()
    ll_state.ica2.apply(eeg_ll_raw)
    eeg_ll_raw = eeg_ll_raw.filter(l_freq=1.0, h_freq=50.0, picks='eeg')
    eeg_ll_raw = eeg_ll_raw.interpolate_bads()
    eeg_ll_raw = eeg_ll_raw.set_eeg_reference(ref_channels="average")

    ##experiment with purging...
    #rejection_policy = ll_state.RejectionPolicy()
    #cleaned_raw = rejection_policy.apply(eeg_ll_raw)
    
    return eeg_ll_raw


def eeg_et_combine(eeg_raw, et_raw, eeg_times, et_times, eeg_events, eeg_event_dict, et_events, et_event_dict):

    eeg_raw.load_data()
    et_raw.load_data()

    # Align the data
    mne.preprocessing.realign_raw(eeg_raw, et_raw, eeg_times, et_times, verbose="error")

    # Add EEG channels to the eye-tracking raw object
    eeg_raw.add_channels([et_raw], force_update_info=True)

    ## update the annotations...
    #eeg_event_dict_r = {value: key for key, value in eeg_event_dict.items()}
    #eeg_annots = mne.annotations_from_events(
    #    events=eeg_events,
    #    event_desc=eeg_event_dict_r,
    #    sfreq=eeg_raw.info["sfreq"],
    #    orig_time=eeg_raw.info["meas_date"],
    #)
    #eeg_raw.set_annotations(eeg_annots)

    # Reset orig_time for et_raw annotations
    eeg_annot = mne.Annotations(
        onset=eeg_raw.annotations.onset - eeg_raw.first_samp/1000,
        duration=eeg_raw.annotations.duration,
        description=eeg_raw.annotations.description,
        orig_time=None  # Ignore orig_time
    )

    et_annot = mne.Annotations(
        onset=et_raw.annotations.onset,
        duration=et_raw.annotations.duration,
        description=et_raw.annotations.description,
        orig_time=None  # Ignore orig_time
    )
    #eeg_annot = eeg_raw.annotations
    #et_annot = et_raw.annotations
    combined_annotations = eeg_annot + et_annot
    eeg_raw.set_annotations(combined_annotations)

    #eeg_annot = eeg_raw.annotations
    #et_annot = et_raw.annotations
    #eeg_raw.set_annotations(eeg_annot + et_annot)
    
    return eeg_raw, et_raw


def write_eeg(eeg_raw, eeg_event_dict, eeg_events, subject_id_out, session_id, task_id_out, project_path, device_info):
    # write the BIDS output files
    # specify power line frequency as required by BIDS
    #eeg_raw.info["line_freq"] = 60
    #eeg_raw.info['device_info']=device_info
    #eeg_raw.info['device_info']['type'] = eeg_raw.info['device_info']['type'].replace(' ', '-')

    #THIS SHOULD BE MOVED TO QIT.FILLNA if it is needed...
    def fillna(raw, fill_val=0):
        return mne.io.RawArray(np.nan_to_num(raw.get_data(), nan=fill_val), raw.info)
    eeg_raw=fillna(eeg_raw,fill_val=0)

    eeg_bids_path = mne_bids.BIDSPath(
        subject=subject_id_out, session=session_id, task=task_id_out, run="1", datatype="eeg", root=project_path
    )

    print(eeg_bids_path)
    mne_bids.write_raw_bids(
        raw=eeg_raw,
        bids_path=eeg_bids_path,
        events=eeg_events,
        event_id=eeg_event_dict,
        format = "EDF",
        overwrite=True,
        allow_preload=True,
    )
    
    return eeg_bids_path

