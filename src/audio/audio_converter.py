from pydub import AudioSegment

def convert_audio(input_file, output_file):
  sound = AudioSegment.from_file(input_file, format="wav")
  sound.export(output_file, format="mp3")
