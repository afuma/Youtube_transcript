import yt_dlp
from typing import Dict, Optional, Tuple
import re
from youtube_transcript_api import YouTubeTranscriptApi

class YoutubeTranscript:
    def __init__(self, language: str = 'fr'):
        """
        Initialise le service YouTube avec la langue spécifiée.
        
        Args:
            language (str): Code de langue pour les transcriptions (par défaut: 'fr')
        """
        self.language = language

    def to_snake_case(self, text: str) -> str:
        """
        Convertit un texte en format snake_case.
        
        Args:
            text (str): Texte à convertir
            
        Returns:
            str: Texte converti en snake_case
        """
        text = re.sub(r'[^\w\s-]', ' ', text)
        text = text.lower()
        text = re.sub(r'[-\s]+', '_', text)
        return text.strip('_')

    def get_video_info(self, video_url: str) -> Dict:
        """
        Récupère les informations d'une vidéo YouTube.
        
        Args:
            video_url (str): URL de la vidéo YouTube
            
        Returns:
            Dict: Informations de la vidéo
        """
        ydl_opts = {'quiet': True, 'extract_flat': True}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
        return {
            "url": info.get("webpage_url"),
            "title": info.get("title"),
            "channel": info.get("uploader"),
            "upload_date": info.get("upload_date"),
            "description": info.get("description")
        }

    def get_video_details(self, video_id: str) -> Tuple[Optional[str], Optional[str]]:
        """
        Récupère les détails de la vidéo (titre, description, nom de la chaîne).
        
        Args:
            video_id (str): ID de la vidéo YouTube
            
        Returns:
            Tuple[Optional[str], Optional[str]]: Tuple contenant le nom de la chaîne et le titre de la vidéo
        """
        try:
            video_url = f"https://www.youtube.com/watch?v={video_id}"
            video_info = self.get_video_info(video_url)
            
            channel_name = self.to_snake_case(video_info['channel'])
            video_title = self.to_snake_case(video_info['title'])
            
            return channel_name, video_title

        except Exception as e:
            print(f"Erreur lors de la récupération des détails de la vidéo: {e}")
            return None, None

    def extract_video_id(self, url: str) -> str:
        """
        Extrait l'ID de la vidéo à partir de l'URL YouTube.
        
        Args:
            url (str): URL YouTube
            
        Returns:
            str: ID de la vidéo
        """
        patterns = [
            r'(?:youtube\.com\/watch\?v=|youtu\.be\/)([A-Za-z0-9_-]+)',
            r'youtube\.com\/watch\?.*v=([A-Za-z0-9_-]+)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        return url

    def get_transcript_text(self, video_id: str) -> Optional[str]:
        """
        Récupère la transcription d'une vidéo YouTube.
        
        Args:
            video_id (str): ID de la vidéo YouTube
            
        Returns:
            Optional[str]: Texte de la transcription ou None si erreur
        """
        try:
            transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=[self.language])
            text = ''
            for line in transcript:
                text += line['text'] + ' '
            return text
        except Exception as e:
            print(f"Une erreur s'est produite pour la vidéo {video_id}: {e}")
            return None

    def save_transcript_text(self, transcript_text: str, video_id: str) -> None:
        """
        Sauvegarde la transcription dans un fichier avec le format channel_name-video_title.
        
        Args:
            transcript_text (str): Texte de la transcription
            video_id (str): ID de la vidéo YouTube
        """
        try:
            channel_name, video_title = self.get_video_details(video_id)
            
            if channel_name and video_title:
                filename = f"transcripts/{channel_name}-{video_title}.txt"
            else:
                filename = f"transcripts/transcript_{video_id}.txt"
            
            with open(filename, 'w', encoding='utf-8') as f:
                if channel_name and video_title:
                    f.write(f"Chaîne: {channel_name}\n")
                    f.write(f"Titre: {video_title}\n")
                    f.write(f"ID de la vidéo: {video_id}\n")
                    f.write("\n--- Transcription ---\n\n")
                f.write(transcript_text)
            
            print(f"Transcription sauvegardée dans {filename}")
            
        except Exception as e:
            print(f"Une erreur s'est produite lors de la sauvegarde de la transcription : {e}")

    def download_audio(self, video_id: str) -> bool:
        """
        Télécharge l'audio d'une vidéo YouTube en MP3.
        
        Args:
            video_id (str): ID de la vidéo YouTube
            
        Returns:
            bool: True si le téléchargement a réussi, False sinon
        """
        try:
            video_url = f"https://www.youtube.com/watch?v={video_id}"
            channel_name, video_title = self.get_video_details(video_id)
            
            if not (channel_name and video_title):
                print("Impossible de récupérer les détails de la vidéo")
                return False
            
            output_filename = f"audio/{channel_name}-{video_title}.%(ext)s"
            
            ydl_opts = {
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
                'outtmpl': output_filename,
                'quiet': True
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([video_url])
                
            print(f"Audio sauvegardé dans audio/{channel_name}-{video_title}.mp3")
            return True
            
        except Exception as e:
            print(f"Une erreur s'est produite lors du téléchargement de l'audio: {e}")
            return False

    def download_video(self, video_id: str, quality: str = '720p') -> bool:
        """
        Télécharge une vidéo YouTube complète.
        
        Args:
            video_id (str): ID de la vidéo YouTube
            quality (str): Qualité de la vidéo ('720p', '480p', '360p', etc.)
            
        Returns:
            bool: True si le téléchargement a réussi, False sinon
        """
        try:
            video_url = f"https://www.youtube.com/watch?v={video_id}"
            channel_name, video_title = self.get_video_details(video_id)
            
            if not (channel_name and video_title):
                print("Impossible de récupérer les détails de la vidéo")
                return False
            
            output_filename = f"video/{channel_name}-{video_title}.%(ext)s"
            
            # Convertir la qualité en hauteur de pixels
            height_map = {
                '720p': 720,
                '480p': 480,
                '360p': 360,
                '240p': 240
            }
            max_height = height_map.get(quality, 720)
            
            ydl_opts = {
                'format': f'bestvideo[height<={max_height}]+bestaudio/best[height<={max_height}]',
                'outtmpl': output_filename,
                'merge_output_format': 'mp4',
                'postprocessor_args': [
                    '-c:v', 'libx264',
                    '-crf', '23',  # Qualité vidéo (18-28, plus bas = meilleure qualité)
                ],
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([video_url])
                
            print(f"Vidéo sauvegardée dans video/{channel_name}-{video_title}.mp4")
            return True
            
        except Exception as e:
            print(f"Une erreur s'est produite lors du téléchargement de la vidéo: {e}")
            return False

    def download_video_clip(self, video_id: str, start_time: int, end_time: int, quality: str = '720p') -> bool:
        """
        Télécharge un extrait d'une vidéo YouTube.
        
        Args:
            video_id (str): ID de la vidéo YouTube
            start_time (int): Temps de début en secondes
            end_time (int): Temps de fin en secondes
            quality (str): Qualité de la vidéo ('720p', '480p', '360p', etc.)
            
        Returns:
            bool: True si le téléchargement a réussi, False sinon
        """
        try:
            video_url = f"https://www.youtube.com/watch?v={video_id}"
            channel_name, video_title = self.get_video_details(video_id)
            
            if not (channel_name and video_title):
                print("Impossible de récupérer les détails de la vidéo")
                return False
            
            output_filename = f"video/{channel_name}-{video_title}_clip.%(ext)s"
            
            # Convertir la qualité en hauteur de pixels
            height_map = {
                '720p': 720,
                '480p': 480,
                '360p': 360,
                '240p': 240
            }
            max_height = height_map.get(quality, 720)
            
            ydl_opts = {
                'format': f'bestvideo[height<={max_height}]+bestaudio/best[height<={max_height}]',
                'outtmpl': output_filename,
                'merge_output_format': 'mp4',
                'postprocessor_args': [
                    '-ss', str(start_time),
                    '-to', str(end_time),
                    '-c:v', 'libx264',
                    '-crf', '23',
                ],
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([video_url])
                
            print(f"Extrait vidéo sauvegardé dans video/{channel_name}-{video_title}_clip.mp4")
            return True
            
        except Exception as e:
            print(f"Une erreur s'est produite lors du téléchargement de l'extrait vidéo: {e}")
            return False

    def process_url_file(self, filename: str) -> None:
        """
        Traite toutes les URLs contenues dans un fichier.
        
        Args:
            filename (str): Nom du fichier contenant les URLs
        """
        try:
            with open(filename, 'r') as f:
                urls = f.readlines()
            
            for url in urls:
                url = url.strip()
                if url:
                    print(f"\nTraitement de l'URL: {url}")
                    video_id = self.extract_video_id(url)
                    if video_id:
                        transcript_text = self.get_transcript_text(video_id)
                        if transcript_text:
                            self.save_transcript_text(transcript_text, video_id)
                    else:
                        print(f"URL invalide: {url}")
            
        except FileNotFoundError:
            print(f"Le fichier {filename} n'a pas été trouvé.")
        except Exception as e:
            print(f"Une erreur s'est produite lors de la lecture du fichier: {e}")
