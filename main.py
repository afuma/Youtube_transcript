from youtube_service import YoutubeTranscript

if __name__ == "__main__":
    yt_transcript = YoutubeTranscript()
    
    while True:
        print("\nChoisissez une option:")
        print("1. Traiter une seule URL YouTube")
        print("2. Traiter un fichier contenant des URLs")
        print("3. Télécharger l'audio d'une vidéo YouTube")
        print("4. Télécharger une vidéo YouTube complète")
        print("5. Télécharger un extrait de vidéo YouTube")
        print("6. Quitter")
        
        choice = input("Votre choix (1-6): ")
        
        if choice == "1":
            url = input("Entrez l'URL de la vidéo YouTube: ")
            video_id = yt_transcript.extract_video_id(url)
            if video_id:
                transcript_text = yt_transcript.get_transcript_text(video_id)
                if transcript_text:
                    yt_transcript.save_transcript_text(transcript_text, video_id)
        
        elif choice == "2":
            filename = input("Entrez le nom du fichier contenant les URLs: ")
            yt_transcript.process_url_file(filename)
        
        elif choice == "3":
            url = input("Entrez l'URL de la vidéo YouTube: ")
            video_id = yt_transcript.extract_video_id(url)
            if video_id:
                yt_transcript.download_audio(video_id)
        
        elif choice == "4":
            url = input("Entrez l'URL de la vidéo YouTube: ")
            quality = input("Choisissez la qualité (720p, 480p, 360p, 240p) [720p]: ").lower() or "720p"
            video_id = yt_transcript.extract_video_id(url)
            if video_id:
                yt_transcript.download_video(video_id, quality)

        elif choice == "5":
            url = input("Entrez l'URL de la vidéo YouTube: ")
            quality = input("Choisissez la qualité (720p, 480p, 360p, 240p) [720p]: ").lower() or "720p"
            try:
                start = input("Temps de début (en secondes): ")
                end = input("Temps de fin (en secondes): ")
                start_time = int(start)
                end_time = int(end)
                video_id = yt_transcript.extract_video_id(url)
                if video_id:
                    yt_transcript.download_video_clip(video_id, start_time, end_time, quality)
            except ValueError:
                print("Erreur: Les temps doivent être des nombres entiers en secondes")

        elif choice == "6":
            print("Au revoir!")
            break
        
        else:
            print("Option invalide. Veuillez choisir 1, 2, 3, 4, 5 ou 6.")
