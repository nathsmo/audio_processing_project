# Welcome Page Application

## Overview

The Welcome Page Application is a simple Tkinter-based graphical user interface (GUI) for user login and signup functionalities. It includes features for recording and analyzing audio passwords to enhance security.

## Features

- **User Login:**
  - Enter a username and press the "Login" button.
  - Verify the username against the recorded audio passwords.
  - If successful, a welcome message is displayed, and the user is redirected to the Dashboard.

- **User Signup:**
  - Enter a chosen username and confirm it.
  - Record three different audio passwords for added security.
  - Verify that the usernames match and save the audio passwords.
  - Display a success message upon successful signup.

- **Audio Recording:**
  - Users are prompted to wait for 1 second after pressing the recording button.
  - Audio recording lasts for 5 seconds.
  - Recorded audio files are saved in the "audio_input" folder.

- **Dashboard:**
  - Upon successful login, a Dashboard window is opened.
  - The Dashboard welcomes the user with a simple message.

## Prerequisites

- Python 3.x
- Required Python libraries: `tkinter`, `pandas`

## Usage

1. Clone the repository:

   ```bash
   git clone https://github.com/nathsmo/audio_processing_project.git
   ```

2. Navigate to the project directory:

   ```bash
   cd welcome-page-app
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Run the application:

   ```bash
   python login_page.py
   ```

5. Follow the on-screen instructions for login and signup.

## File Structure

- `login_page.py`: Main application script.
- `code_audio.py`: Module containing functions for audio password verification and creation.
- `gui_audio_input.py`: Module containing functions for user audio input.

## Data Storage

- User audio passwords are stored in a CSV file named `section_outputs.csv`.

## Known Issues

- Delete audio files after signup is done
- Delete original login page after dashboard page gets open

## Future Enhancements

- Improve user interface design.
