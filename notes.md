# Installation of pyaudio

In order to install pyaudio, portaudio has to be installed on the system. But
brew installs portaudio by default under opt/homebrew/Cellar/portaudio/19.7.0/
Therefore installing it with pip in a virtual environment requires the following
command:
``` bash
python3 -m pip install --global-option='build_ext' --global-option='-I/opt/homebrew/Cellar/portaudio/19.7.0/include' --global-option='-L//opt/homebrew/Cellar/portaudio/19.7.0/lib' pyaudio
```

# pyaudio paInt16
I am not completely sure what the purpose of this is, it seems to be a constant
set to 8. But what does it represent?

# Stuff missing from PythonPath
Add by using
```	bash
export PYTHONPATH=$PYTHONPATH:$pwd 
```

# Hydra usage
First create a configuration folder and in it a configuration yaml file. In this
yaml file group the configuration parameters. To use these configurations in
a function import hydra and add the hydra decorator to the function. The decorator
receives the path to the configuration folder and the name of the configuration file.
``` python
@hydra.main(config_path="../src/conf/", config_name="conf")
```
The configuration is then passed as an argument to the function. In order to be
able to specify the type of the parameter, add an config.py to your project
with multiple dataclasses that represent your parameter structure. This class structure
has to be passed to the script that the configuration is being used in. For this
```python
from hydra.core.config_store import ConfigStore
cs = ConfigStore.instance()
cs.store(name="recording_config", node=RecordingConfig)
```
Now you can give the paramter of the function the proper type.

# Asynchronous programming
There is the problem, that if we want to enable a variable recording length
depending whether a button has been pressed or not, we need to put the recording
on another subroutine. I thought we could do that by using asynchronous programming
but the problem then is, that the function isn't idle and continues to run.
The future is therefore never resolved. The solution might be to either use
a thread, a callback or subroutine.  

Copilot says we should use a callback in that case  
And Copilot was right

# Alternative to Hydra
Hydra might not be the optimal package for the problem at hand.
I think it is better suited for a purely data science oriented problem
setting. An alternative might be pyenv