import numpy as np
import matplotlib.pyplot as plt
import librosa
from collections import Counter

def audio_note_analysis(audio_file, plot_me=False):
    # load in sample
    y, sr = librosa.load(audio_file, sr=44100)

    # Constant Q Transform (best for finding note names instead of frequencies)
    cqt = np.abs(librosa.cqt(y, sr=sr, hop_length=512))

    # find fundamental frequency (f0)
    f0, voiced_flag, voiced_probs = librosa.pyin(y,
                                                fmin=librosa.note_to_hz('C2'),
                                                fmax=librosa.note_to_hz('C7'))
    # times of fundamental frequencies
    f0_times = librosa.times_like(f0)

    # find the spectral flux onset strength envelope
    # how likely the value is the onset of a new note (????)
    o_env = librosa.onset.onset_strength(y=y, sr=sr)

    # times of onset envelope
    onset_times = librosa.times_like(o_env, sr=sr)

    # index values of each onset frame
    onset_frames = librosa.onset.onset_detect(onset_envelope=o_env, sr=sr)

    # can window the CQT based off the onset frames
    # (need to transpose CQT first so the shapes match, then transpose back)
    # cqt_window = cqt.T[onset_frames[1]:onset_frames[2]].T


    # ====================================
    ## Plot spectrogram and onset strength
    ''' FUTURE: to prevent choosing 'weak' onset values, only select
        onset frames that are greater than a certain strength value?
    '''
    # fig, ax = plt.subplots(nrows=2, sharex=True)
    # librosa.display.specshow(librosa.amplitude_to_db(cqt, ref=np.max),
    #                          x_axis='time', y_axis='cqt_note', ax=ax[0])

    # lims = ax[0].get_ylim()

    # ax[0].vlines(onset_times[onset_frames], lims[0], lims[1], color='lime', alpha=0.9)
    # ax[0].set(title='Power spectrogram')
    # ax[0].label_outer()
    # ax[1].plot(onset_times, o_env, label='Onset strength')
    # ax[1].vlines(onset_times[onset_frames], 0, o_env.max(), color='r', alpha=0.9,
    #         linestyle='--', label='Onsets')
    # ax[1].legend()
    # plt.show()
    # plt.exit()

    # ====================================
    ## Plot full spectrum with onset window lines
    # fig, ax = plt.subplots()
    # librosa.display.specshow(librosa.amplitude_to_db(cqt,
    #                                                  ref=np.max),
    #                          y_axis='cqt_note', x_axis='time', ax=ax)

    # lims = ax.get_ylim()
    # ax.vlines(onset_times[onset_frames], lims[0], lims[1], color='lime', alpha=0.9,
    #            linewidth=2, label='Onset')
    # ax.legend()
    # ax.set(title='CQT + Onset markers')
    # ax.plot(onset_times, f0, label='f0', color='cyan', linewidth=3)
    # plt.savefig('sample_recording_cqt.png', dpi=300)
    # plt.show()
    # plt.close()
    # exit()

    # ====================================
    ## find fundamental frequencies of each window

    # add last index value of full array to onset frames
    # (because we only look at windows between frame lines)
    onset_frames = np.append(onset_frames, len(o_env)-1)

    ind_last = None
    best_notes = []
    for ind in range(len(onset_frames)):
        print('===========')

        if ind_last is None:
            best_notes.append('Start')
        else:
            # constant Q transform windowed segment
            cqt_window = cqt.T[onset_frames[ind_last]:onset_frames[ind]].T
            # inverse CQT to get back to time series
            y_window = librosa.icqt(cqt_window, sr=sr, hop_length=512)


            # find fundamental frequencies of window (array)
            f0, voiced_flag, voiced_probs = librosa.pyin(y_window,
                                                        fmin=librosa.note_to_hz('C2'),
                                                        fmax=librosa.note_to_hz('C7'))
            times = librosa.times_like(f0)

            # calculate average note of array of fundamental frequencies
            notes = []
            for hz in f0:

                # there are some nan values, ignore these
                if np.isnan(hz) == False:

                    # convert frequency to note
                    note = librosa.hz_to_note(hz)
                    notes.append(note)

            # count up each type of detected note
            note_counter = dict(Counter(notes))
            print(note_counter)

            # choose the note that is counted the most in the segment
            if len(note_counter) == 0:
                # sections that don't have any singing in them
                best_notes.append('Pause')
            else:
                best_note = max(note_counter, key=note_counter.get)
                print(note_counter)
                print('The best note in segment:', best_note)

                # append to best note array
                best_notes.append(best_note)
            if plot_me:
                fig, ax = plt.subplots()
                librosa.display.specshow(librosa.amplitude_to_db(cqt_window,
                                                                ref=np.max),
                                        y_axis='cqt_note', x_axis='time', ax=ax)

                lims = ax.get_ylim()
                ax.vlines(onset_times[onset_frames], lims[0], lims[1], color='lime', alpha=0.9,
                        linewidth=2, label='Beats')
                ax.legend()
                ax.set(title='CQT + Beat markers')
                ax.plot(times, f0, label='f0', color='cyan', linewidth=3)
                plt.show()
                plt.close()


        # re-define previous index value
        ind_last = ind


    print('The best note in each interval:', best_notes)


##### Testing

#Past trial audio: 'trial.wav' - #contains 7 notes, dectects 5 - wasnt getting all the 7 notes (changes every execution)
#Past trial audio: 'recording.wav' #contains 5 notes, detects 6 notes (first one is noise)
#Past trial audio: 'trial_nat.wav' #contains 5-6 notes

#audio_note_analysis('trial_nat.wav', plot_me=False)