# Created by: Sarah Howes

import numpy as np
import matplotlib.pyplot as plt
import librosa
from collections import Counter
import noisereduce as nr
import pandas as pd
from tkinter import messagebox


# Find onsets in an audio signal
def onset_finder(y, sr, hoplen=512, start_time=0, savefig_name=None):
    """
    Detects onsets in an audio signal and corrects them using backtracking.

    :param y: Audio signal.
    :param sr: Sampling rate.
    :param hoplen: Hop length for onset detection.
    :param start_time: Start time for onset detection.
    :param savefig_name: Optional name to save a plot of the onset detection process.
    :return: Corrected onset frames.
    """
    idx = np.arange(len(y))

    # start xx seconds in
    start = librosa.time_to_samples(start_time, sr=sr)  # start 1 second in

    # calculate onset strength envelope
    o_env = librosa.onset.onset_strength(y=y, sr=sr)

    # calculate onset times/frames/samples
    onset_times = librosa.times_like(o_env, sr=sr)
    onset_samples = librosa.time_to_samples(onset_times, sr=sr)
    onset_frames = librosa.onset.onset_detect(onset_envelope=o_env, sr=sr, hop_length=hoplen)

    onstm = librosa.frames_to_time(onset_frames, sr=sr, hop_length=hoplen)
    ons_samples = librosa.time_to_samples(onstm, sr=sr)


    # Use first 2 seconds of recording in order to estimate median noise level
    # and typical variation
    noiseidx = [onset_times < 2.0][0]
    noiseidx = np.array(np.where(noiseidx==True))[0]
    noisemedian = np.percentile(o_env[noiseidx], 50)
    sigma = np.percentile(o_env[noiseidx], 84.1) - noisemedian

    # Set the minimum RMS energy threshold that is needed in order to declare
    # an "onset" event to be equal to 5 sigma above the median
    threshold = noisemedian + 5*sigma
    threshidx = [o_env > threshold][0]
    threshidx = np.array(np.where(threshidx==True))[0]


    # Choose the corrected onset times as only those which meet the RMS energy
    # minimum threshold requirement
    correctedonstm = onstm[[tm in onset_times[threshidx] for tm in onstm]]

    # Print both in units of actual time (seconds) and sample ID number
    corrected_onset_time = correctedonstm+start/sr
    corrected_onset_sample = correctedonstm*sr+start
    corrected_onset_frames = librosa.samples_to_frames(corrected_onset_sample, hop_length=hoplen)
    if len(corrected_onset_frames) != 4:
        print(f'Only {len(corrected_onset_frames)} detected, please try again.')
        return False
    print("Corrected Onset Frames:", corrected_onset_frames)
    corrected_onset_frames = librosa.onset.onset_backtrack(corrected_onset_frames, o_env)
    corrected_onset_sample = librosa.frames_to_samples(corrected_onset_frames, hop_length=hoplen)
    print('Backtracked:', corrected_onset_frames)

    # plot the waveform together with onset times superimposed in red
    if savefig_name is not None:
        fg = plt.figure(figsize=[12, 8])
        ax1 = fg.add_subplot(2,1,1)
        ax2 = fg.add_subplot(2,1,2, sharex=ax1)
        

        ax1.plot(idx+start, y)
        ax2.plot(onset_samples, o_env, marker='.')

        lims1 = ax1.get_ylim()
        lims2 = ax2.get_ylim()

        ax1.vlines(corrected_onset_sample, ymin=lims1[0], ymax=lims1[1], color='r', label='Corrected Onset + Backtrack')
        ax1.vlines(ons_samples, ymin=lims1[0], ymax=lims1[1], color='lime', linestyle='--', label='Initial Onset Detection')
        
        ax2.vlines(ons_samples, ymin=lims2[0], ymax=lims2[1], color='lime', linestyle='--')
        ax2.vlines(corrected_onset_sample, ymin=lims2[0], ymax=lims2[1], color='r')
        ax2.axhline(threshold, linestyle=':', color='k', label='Onset strength threshold')

        ax1.set_ylabel('Amplitude', fontsize=16)
        ax2.set_ylabel("Onset Strength", fontsize=16)
        ax2.set_xlabel("Sample Number", fontsize=16)
        ax1.legend()
        ax2.legend()
        plt.savefig(savefig_name, dpi=300)
        plt.close()

    return corrected_onset_frames



# Find notes in each onset segment
def find_best_notes(y, sr, corrected_onset_frames, savefig_name=None):
    """
    Finds the best note within each onset segment using pitch analysis.

    :param y: Audio signal.
    :param sr: Sampling rate.
    :param corrected_onset_frames: Corrected onset frames.
    :param savefig_name: Optional name to save a plot of the pitch analysis process.
    :return: List of best notes (in Hz) for each onset segment.
    """
    ##find fundamental frequency (f0)
    f0, voiced_flag, voiced_probs = librosa.pyin(y,
                                                fmin=librosa.note_to_hz('C2'),
                                                fmax=librosa.note_to_hz('C7'))
    # times of fundamental frequencies
    f0_times = librosa.times_like(f0)

    # plot CQT spectrogram with notes detected
    if savefig_name is not None:
        # Constant Q Transform (best for finding note names instead of frequencies)
        cqt = np.abs(librosa.cqt(y, sr=sr, hop_length=512))
        corrected_onset_times = librosa.frames_to_time(corrected_onset_frames, sr=sr)

        fig, ax = plt.subplots()
        librosa.display.specshow(librosa.amplitude_to_db(cqt,
                                                        ref=np.max),
                                y_axis='cqt_note', x_axis='time', ax=ax)

        lims = ax.get_ylim()
        ax.vlines(corrected_onset_times, lims[0], lims[1], color='lime', alpha=0.9,
                linewidth=2, label='Onset')
        ax.legend()
        ax.set(title='CQT + Onset markers')
        ax.plot(f0_times, f0, label='f0', color='cyan', linewidth=3)
        plt.savefig(savefig_name, dpi=300)
        plt.close()


    ## add last value of f0 array to the onset frames -- we will be
    ## looking for f0 **between** each of these index values
    corrected_onset_frames = np.append(corrected_onset_frames,len(f0)-1)
    print('onset markers:', corrected_onset_frames)

    last = None
    best_notes = [] # array of best note for each onset segment
    best_hz = []

    ## loop through all the onset indices
    for i in corrected_onset_frames:
        if last is None:
            print('Start')

        else:

            # choose the f0 values within each onset window
            vals = f0[last:i] 

            # instead of looping, choose the mean Hz value, and
            # determine a threshold variance around that note
            # (threshold determined similar to onset strength)

            try:
                avg_val = np.nanmean(vals)
            except:
                print("Error with average values")
                return False
            avg_symbol = librosa.hz_to_note(avg_val)
            hz_median = np.nanpercentile(vals, 50)
            hz_sigma = np.nanpercentile(vals, 84.1) - hz_median
            hz_std = np.nanstd(vals)
            hz_threshold = hz_median + 5*hz_sigma
            
            print('mean note symbol:', avg_symbol)
            print('mean note val:', avg_val)
            print('hz median:', hz_median)
            print('hz sigma:', hz_sigma)
            print('hz std:', hz_std)
            print('hz threshold:', hz_threshold)
            print('============')
            best_notes.append(avg_symbol)
            best_hz.append(avg_val)

        last = i

    print('best notes:', best_notes)
    print('best vals:', best_hz)
    print('=====/////======')
    return best_hz




# Full process of note analysis for password creation
def note_analysis(recording_file, save_rmse_name=None, save_spect_name=None):
    """
    Performs note analysis on an audio recording for password creation.

    :param recording_file: Path to the audio recording.
    :param save_rmse_name: Optional name to save a plot of the RMSE analysis process.
    :param save_spect_name: Optional name to save a plot of the spectrogram analysis process.
    :return: List of best notes (in Hz) for each onset segment.
    """
    # load in file
    y, sr = librosa.load(recording_file)

    # reduce noise
    if y == []:
        print('No audio detected')
        return False
    y = nr.reduce_noise(y, sr)

    # find correct onset index values
    corrected_onset_frames = onset_finder(y, sr, savefig_name=save_rmse_name)
    if type(corrected_onset_frames) == type(False):
        return False

    # find best note within each onset window
    best_notes = find_best_notes(y, sr, corrected_onset_frames, savefig_name=save_spect_name)
    return best_notes

# Create a password using multiple audio recordings
def password_creation(recording_file_path, recording_file_names, password_df_path, username):
    """
    Creates a password using note analysis on multiple audio recordings.

    :param recording_file_path: Path to the directory containing audio recordings.
    :param recording_file_names: List of audio recording filenames.
    :param password_df_path: Path to save the password DataFrame.
    :param username: Username associated with the password.
    :return: True if password creation is successful.
    """
    # perform note analysis on 5 audio recordings
    full_selection = []
    for name in recording_file_names:
        best_notes = note_analysis(recording_file_path+name) 
        save_spect_name='project3_figures/'+name+'_spect.png'
        print('Best notes for', name, ':', best_notes)
        full_selection.append(best_notes)

    print('================')
    print(full_selection)

    # find average value and stdev for each of the 4 note sections
    avg_vals = []
    sigmas = []
    stds = []
    for idx in range(len(full_selection[0])):
        sec = [item[idx] for item in full_selection]
        avg_val = np.nanmean(sec)
        avg_symbol = librosa.hz_to_note(avg_val)
        hz_median = np.nanpercentile(sec, 50)
        hz_sigma = np.nanpercentile(sec, 84.1) - hz_median
        hz_std = np.nanstd(sec)
        avg_vals.append(avg_val)
        sigmas.append(hz_sigma)
        stds.append(hz_std)

        print('section', idx, ':')
        print('mean note val:', avg_val)
        print('median note:', hz_median)
        print('mean note symbol:', avg_symbol)
        print('section', idx, 'std:', hz_std)
        print('5*sigma:', 5*hz_sigma)
        print('=======')

    # make a dataframe with the avg val and stev for each section
    print("lengths of variables: avg_vals", len(avg_vals), "sigmas: ",len(sigmas), "stds: ",len(stds))
    
    dic = {
        'section_number': list(range(1, len(avg_vals)+1)),
        'average_hz_val': avg_vals,
        'section_sigma': sigmas,
        'section_std': stds 
    }
    print('***Current dic: ', dic)
    df = pd.DataFrame(dic)
    df['user'] = username
    # save to file
    print('     Password_df_path: ', password_df_path)
    print(' Saving to file:', password_df_path)
    df.to_csv(password_df_path, index=False)
    print('Password created!')
    return True

# Attempt to log in by comparing an entry with the stored password
def login_attempt(entry_path, entry, password_df, username):
    """
    Attempts to log in by comparing an entry with the stored password.

    :param entry_path: Path to the directory containing the entry audio.
    :param entry: Filename of the entry audio.
    :param password_df: Path to the stored password DataFrame.
    :param username: Username attempting to log in.
    :return: True if the login attempt is successful.
    """
    # perform note analysis for entry file
    entry_best_notes = note_analysis(entry_path+entry)
    if entry_best_notes == False:
        messagebox.showinfo(message="Not the right number of notes detected, please try again.")
        return False
    print('login attempt best notes:', entry_best_notes)

    # compare to password df
    df_temp = pd.read_csv(password_df)
    try:
        password = df_temp.where(df_temp.user == username)
    except:
        messagebox.showinfo(message="No username detected, please sign up.")
        return False
    if type(entry_best_notes) == type(True):
        messagebox.showinfo(message="Try again please, something went wrong.")
        exit()
    
    pass_counter = 0
    fail_counter = 0
    for entry_idx in range(len(entry_best_notes)):
        password_note = password[password['section_number']==entry_idx+1]['average_hz_val'].values
        password_sigma = password[password['section_number']==entry_idx+1]['section_sigma'].values

        # relax threshold bounds for a correct/incorrect note if the sigma is too low
        if password_sigma*5 < 5.0:
            print('threshold too low, relaxing bounds...')
            note_threshold = 5.0
        else:
            note_threshold = password_sigma*5
        print('section', entry_idx+1, ':')
        print('password note:', password_note)
        print('password threshold:', note_threshold)
        print('entry note:', entry_best_notes[entry_idx])

        # determine if note is within the threshold
        is_within = password_note-note_threshold <= entry_best_notes[entry_idx] <= password_note+note_threshold
        
        # then count the amount of times it passes & fails for each (out of 4) notes
        if is_within == True:
            print(f'Section {entry_idx+1}: PASS')
            pass_counter+=1
        else:
            print(f'Section {entry_idx+1}: FAIL')
            fail_counter+=1
        print('=======')
    print('total pass counter:', pass_counter)
    print('total fail counter:', fail_counter)

    # pass only if all four notes are correct
    if pass_counter == 4:
        return True
    else:
        return False
