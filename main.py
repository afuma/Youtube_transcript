from youtube_transcript_api import YouTubeTranscriptApi

class YoutubeTranscript:
    def __init__(self, video_id, language='fr'):
        self.video_id = video_id
        self.language = language

    def get_transcript_text(self):
        try:
            transcript = YouTubeTranscriptApi.get_transcript(self.video_id, languages=[self.language])
            text = ''
            for line in transcript:
                text += line['text'] + ' '
            return text
        except Exception as e:
            print(f"Une erreur s'est produite : {e}")
            return None

    def save_transcript_text(self, transcript_text, filename="texte.txt"):
        try:
            with open(filename, 'w') as f:
                f.write(transcript_text)
            print(f"Transcription sauvegardée dans {filename}")
        except Exception as e:
            print(f"Une erreur s'est produite lors de la sauvegarde de la transcription : {e}")

if __name__ == "__main__":
    video_id = input("Entrez l'ID de la video: ")
    yt_transcript = YoutubeTranscript(video_id)
    transcript_text = yt_transcript.get_transcript_text()
    if transcript_text:
        yt_transcript.save_transcript_text(transcript_text)
    else:
        print("Impossible de récupérer la transcription de la vidéo.")
