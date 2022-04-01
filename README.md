# "Hello. My name is Tom and I like to ~~quote~~ code!" - Tom

This tool is a training project, aimed to improve the usage
of design principles, the development of guis, the usage of 
integrated hardware, and transcription through an API.  

As a first iteration tkinter was chose for the GUI implementation.
Assembly AIs API was chosen for the transcription.

# Installation
## pyaudio
Portaudio needs to be installed
```bash
brew install portaudio
```
then install pyaudio
```bash
pip install pyaudio
```
We had the problem with the installation of pyaudio, because
portaudio was installed under opt
```bash
python3 -m pip install --global-option='build_ext' --global-option='-I/opt/homebrew/Cellar/portaudio/19.7.0/include' --global-option='-L//opt/homebrew/Cellar/portaudio/19.7.0/lib' pyaudio
```
worked for us, where the version and the place where portaudio is installed
can be found by using 
```bash
brew info portaudio
```
Then for the intermediary conversion from wav to mp3 we used pydub, which additionally
needs ffmpeg or libav which can be installed using brew.
## Remaining dependencies
The remaining dependencies can be installed using the requirements file

# Configuration
The configuration can be performed insinde the conf.yaml under src/conf/. The 
most important step is to replace the API key with your own. It can be found
on the AssemblyAI website under your dashboard.

## PYTHONPATH
Don't forget to add the project to the PYTHONPATH. Run from the project root
```bash
export PYTHONPATH=$PYTHONPATH:$pwd 
```

# Execution
Run the main.py file from from the project root.


