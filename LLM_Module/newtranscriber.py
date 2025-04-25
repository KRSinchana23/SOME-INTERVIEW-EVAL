import io
import tempfile
import moviepy.editor as mp
import whisper
import json
import streamlit as st
from groq import Groq
# from transcriptionimprover import TranscriptionImprover 
import ffmpeg 
import tempfile 
from groq import Groq
import os 
class VideoTranscriber:
    def __init__(self, video_file, output_audio_path, output_json_path):
        self.video_file = video_file  
        self.output_audio_path = output_audio_path
        self.output_json_path = output_json_path
        self.client = Groq()
        # self.model = whisper.load_model("small")
        self.target_size_kb = 50000 
        self.client = Groq(api_key="")
        self.compressed_audio_path = "audio/audio.wav"

    # def extract_audio(self):
    def extract_audio(self):
        """ 
        Extracts audio from a video file and compresses it to a specific file size.
        
        Parameters:
        - video_file: Either a file path (str) or an uploaded file object
        - output_audio_path: Path to save the compressed audio file
        - target_size_kb: Desired file size in KB
        """
        video_file = self.video_file
        if isinstance(video_file, str):  # If file path is given
            temp_video_file_path = video_file
        else:  
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_video_file:
                temp_video_file.write(video_file.read())
                temp_video_file_path = temp_video_file.name
        print(temp_video_file_path)

        video_clip = mp.VideoFileClip(temp_video_file_path)
        audio_path = self.output_audio_path
        video_clip.audio.write_audiofile(audio_path )
        
       
        duration = video_clip.audio.duration  # Get audio duration in seconds
        target_bitrate = (self.target_size_kb * 8) / duration  # Bitrate in kbps

       
        min_bitrate = 32  
        if target_bitrate < min_bitrate:
            target_bitrate = min_bitrate
        
        ffmpeg.input(audio_path).output(
            self.compressed_audio_path, 
            audio_bitrate=f"{int(target_bitrate)}", 
            format="mp3", 
            acodec="libmp3lame"
        ).run(overwrite_output=True)

        print(f"Compressed file saved to {self.output_audio_path}, Size: {os.path.getsize(self.output_audio_path) / 1024:.2f} KB")



    def transcribe(self):
        """Transcribe audio and save the results to the JSON file."""
        self.extract_audio() 
        with open(self.compressed_audio_path, "rb") as file:
            results = self.client.audio.transcriptions.create(
            file=(self.compressed_audio_path, file.read()),
            model="whisper-large-v3",
            response_format="verbose_json",
            language='en'
            )
        print("TRanscibe 1 inside")
            
      
        transcription_output = []
        data = ""
        for segment in results.segments:
            start = segment['start']
            end = segment['end']
            text = segment['text']
            
            print(f"[{start:.2f}s - {end:.2f}s] {text}")
            data += f"[{start:.2f}s - {end:.2f}s] {text}"

            transcription_output.append({
                'start': start,
                'end': end,
                'text': text
            })
        print("Transcriber 2 inside")

        with open(self.output_json_path, 'w', encoding='utf-8') as json_file:
            json.dump(transcription_output, json_file, ensure_ascii=False, indent=4)

        print(f"Transcription results saved to {self.output_json_path}")
        return data




    # def transcribe(self):
    #     """Transcribe audio and save the results to the JSON file."""
    #     self.extract_audio()

    #     cached_path = "audio/temp_transcript.json"

    #     # Check if cached transcript exists
    #     if os.path.exists(cached_path):
    #         print("[CACHE] Using cached transcript")
    #         with open(cached_path, 'r', encoding='utf-8') as f:
    #             transcription_output = json.load(f)
            
    #         # Build `data` from cached transcript
    #         data = ""
    #         for segment in transcription_output:
    #             start = segment['start']
    #             end = segment['end']
    #             text = segment['text']
    #             data += f"[{start:.2f}s - {end:.2f}s] {text}"
            
    #         # Clean up cached file
    #         os.remove(cached_path)
    #         with open(self.output_json_path, 'w', encoding='utf-8') as json_file:
    #             json.dump(transcription_output, json_file, ensure_ascii=False, indent=4)

    #     else:
    #         # Make actual transcription request
    #         with open(self.compressed_audio_path, "rb") as file:
    #             results = self.client.audio.transcriptions.create(
    #                 file=(self.compressed_audio_path, file.read()),
    #                 model="whisper-large-v3",
    #                 response_format="verbose_json",
    #                 language='en'
    #             )
    #         print("Transcribe - API call made")

    #         transcription_output = []
    #         data = ""
    #         for segment in results.segments:
    #             start = segment['start']
    #             end = segment['end']
    #             text = segment['text']
    #             print(f"[{start:.2f}s - {end:.2f}s] {text}")
    #             data += f"[{start:.2f}s - {end:.2f}s] {text}"

    #             transcription_output.append({
    #                 'start': start,
    #                 'end': end,
    #                 'text': text
    #             })
    
    
    
    # def get_audio_features(self):
    #     print("[AUDIO] Extracting features from audio...")
    #     y, sr_ = librosa.load(self.compressed_audio_path, sr=16000)

    #     rms = np.sqrt(np.mean(y**2))
    #     pitches, magnitudes = librosa.piptrack(y=y, sr=sr_)
    #     pitch_values = pitches[magnitudes > np.median(magnitudes)]
    #     pitch = np.mean(pitch_values) if len(pitch_values) > 0 else 0

    #     transcript = self.transcribe()
    #     word_count = len(transcript.split())
    #     duration = librosa.get_duration(y=y, sr=sr_)
    #     wpm = (word_count / duration) * 60

    #     return {
    #         "volume": self.normalize(rms, 0.01, 0.1),
    #         "pitch": self.normalize(pitch, 80, 300),
    #         "wpm": self.normalize(wpm, 80, 180)
    #     }

