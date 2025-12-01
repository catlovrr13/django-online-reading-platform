import requests
import io
from PIL import Image
from typing import Dict, Optional, Tuple
from django.conf import settings
from django.core.files.base import ContentFile
import urllib.parse
import time


class PollinationsGenerator:
    
    def __init__(self, ollama_url: str = None, ollama_model: str = None):
        self.ollama_url = ollama_url or getattr(settings, 'OLLAMA_URL', 'http://localhost:11434')
        self.ollama_model = ollama_model or getattr(settings, 'OLLAMA_MODEL', 'qwen2.5:3b')
        self.ollama_api = f"{self.ollama_url}/api/generate"
        
        self.pollinations_url = "https://image.pollinations.ai/prompt/"
        
        print("Image Generator initialized")
    
    def _call_ollama(self, prompt: str, max_tokens: int = 200) -> str:
        try:
            response = requests.post(
                self.ollama_api,
                json={
                    "model": self.ollama_model,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "num_predict": max_tokens,
                        "temperature": 0.8,  # More creative for image descriptions
                    }
                },
                timeout=60
            )
            
            if response.status_code == 200:
                return response.json()["response"].strip()
            else:
                print(f"Ollama error: {response.status_code}")
                return ""
                
        except Exception as e:
            print(f"Could not call Ollama for prompt: {e}")
            return ""

    def generate_cover_prompt(self, book_metadata: Dict) -> str:
        print(f"Creating cover prompt for '{book_metadata.get('title')}'")
        
        ollama_prompt = f"""Create a visual description for an AI image generator to make a book cover.

    Book: {book_metadata.get('title', 'Unknown')}
    Author: {book_metadata.get('author', 'Unknown')}
    Genre: {book_metadata.get('genre', 'Fiction')}
    Summary: {book_metadata.get('description', '')[:200]}

    Write ONLY a visual description (2-3 sentences) for the image. Do NOT include:
    - Instructions like "Insert" or "Create"
    - The book title or author name (no text in image)
    - Any bracketed notes or explanations
    - Phrases like "I hope this meets your requirements"

    Just describe what should be visible in the image.

    Example good response: "A misty forest at twilight with ancient oak trees and ethereal fog, mysterious shadows dancing between moonlit branches, dark fantasy atmosphere with Gothic elements, professional book cover art style"

    Your visual description:"""

        try:
            ai_prompt = self._call_ollama(ollama_prompt, max_tokens=200)
            
            ai_prompt = ai_prompt.strip()
            
            if ai_prompt.startswith('['):
                start = ai_prompt.find(']')
                if start != -1:
                    ai_prompt = ai_prompt[start+1:].strip()
            
            unwanted_phrases = [
                "I hope this prompts meet your requirements",
                "I hope this meets your requirements",
                "Here is the prompt:",
                "Here's the description:",
                "The book title",
                "is prominently displayed",
                "Insert ",
                "Create ",
                "[",
                "]"
            ]
            
            for phrase in unwanted_phrases:
                ai_prompt = ai_prompt.replace(phrase, "")
            
            ai_prompt = ai_prompt.replace('"', '').replace("'", "")
            
            ai_prompt = ' '.join(ai_prompt.split())
            
            if 20 < len(ai_prompt) < 1000:
                final_prompt = f"{ai_prompt}"
                print(f"AI prompt (cleaned): {final_prompt[:100]}")
                return final_prompt
            else:
                print(f"AI prompt too short/long ({len(ai_prompt)} chars), using fallback")
                
        except Exception as e:
            print(f"Ollama failed: {e}")
        
        genre = book_metadata.get('genre', 'Fiction')
        title = book_metadata.get('title', 'Book')
        description = book_metadata.get('description', '')[:150]
        
        genre_styles = {
            'fiction': 'literary novel cover with artistic composition, emotional depth, modern design',
            'non_fiction': 'professional non-fiction book cover, clean typography space, authoritative design',
            'mystery': 'dark mysterious atmosphere with noir elements, shadows and intrigue, detective thriller style',
            'science_fiction': 'futuristic sci-fi landscape with cosmic elements, advanced technology, space atmosphere',
            'fantasy': 'epic fantasy scene with magical elements, mystical creatures, enchanted forest or castle',
            'romance': 'romantic atmosphere with warm lighting, emotional connection, soft dreamy aesthetic',
            'thriller': 'intense dramatic composition with high contrast, suspenseful mood, dark thriller aesthetic',
            'biography': 'historical portrait style with period details, documentary aesthetic, realistic composition',
            'self_help': 'uplifting inspirational design with positive energy, modern minimalist aesthetic, bright colors',
            'history': 'historical accuracy with period appropriate details, vintage photograph style, documentary feel',
            'horror': 'dark horror atmosphere with eerie Gothic elements, supernatural mood, scary aesthetic',
            'other': 'professional artistic book cover, compelling visual narrative, high quality design'
        }
        
        style = genre_styles.get(genre.lower(), genre_styles['other'])
        
        theme_hint = ""
        if description:
            keywords = []
            theme_words = ['witch', 'magic', 'forest', 'castle', 'dragon', 'vampire', 'detective', 
                        'murder', 'love', 'war', 'space', 'robot', 'alien', 'ghost', 'zombie',
                        'princess', 'knight', 'pirate', 'ocean', 'mountain', 'city', 'desert']
            
            desc_lower = description.lower()
            for word in theme_words:
                if word in desc_lower:
                    keywords.append(word)
            
            if keywords:
                theme_hint = f"featuring {', '.join(keywords[:3])}, "
        
        fallback_prompt = (
            f"Professional book cover for {genre} genre, "
            f"{theme_hint}"
            f"{style}, "
            f"cinematic composition, atmospheric lighting, "
            f"detailed artwork, compelling visual storytelling, "
            f"no text or words, symbolic imagery"
        )
        
        print(f"Using fallback prompt")
        return fallback_prompt

    def generate_chapter_prompt(self, chapter_data: Dict, book_context: Dict) -> str:
        chapter_num = chapter_data.get('chapter_number', 1)
        chapter_title = chapter_data.get('title', 'Chapter')
        chapter_summary = chapter_data.get('summary', '')
        
        print(f"Creating illustration prompt for Chapter {chapter_num}")
        
        if chapter_summary and len(chapter_summary) > 15:
            genre = book_context.get('genre', 'Fiction')
            
            genre_styles = {
                'fiction': 'artistic book illustration, literary narrative style',
                'non_fiction': 'documentary illustration, informative visual style',
                'mystery': 'noir illustration with mysterious shadows and atmosphere',
                'science_fiction': 'sci-fi concept art, futuristic detailed scene',
                'fantasy': 'fantasy art with magical atmosphere, epic composition',
                'romance': 'romantic illustration, emotional soft lighting',
                'thriller': 'dramatic intense illustration, high contrast suspense',
                'biography': 'historical illustration, realistic portrait style',
                'self_help': 'modern uplifting illustration, positive clean design',
                'history': 'period-accurate historical illustration',
                'horror': 'dark horror art, eerie Gothic atmosphere',
                'other': 'professional book illustration'
            }
            
            style = genre_styles.get(genre.lower(), 'professional book illustration')
            
            clean_summary = chapter_summary.strip(' "\'[]')
            
            prompt = (
                f"{clean_summary}, "
                f"{style}, "
                f"detailed scene, cinematic composition, "
                f"professional artwork, no text or words"
            )
            
            print(f"Using summary: {prompt[:80]}")
            return prompt
        
        genre = book_context.get('genre', 'Fiction')
        
        genre_styles = {
            'fiction': 'artistic book illustration',
            'mystery': 'noir detective scene',
            'science_fiction': 'futuristic sci-fi scene',
            'fantasy': 'epic fantasy illustration',
            'romance': 'romantic scene',
            'thriller': 'intense dramatic scene',
            'horror': 'dark horror scene',
            'biography': 'historical scene',
            'history': 'period historical scene',
            'self_help': 'uplifting inspirational scene',
            'other': 'book illustration'
        }
        
        style = genre_styles.get(genre.lower(), 'book illustration')
        
        title_clean = chapter_title.lower()
        for remove in ['chapter', str(chapter_num), ':', '-', '.']:
            title_clean = title_clean.replace(remove, ' ')
        title_clean = ' '.join(title_clean.split()).strip()
        
        if title_clean:
            fallback_prompt = (
                f"{title_clean}, "
                f"{style}, "
                f"atmospheric scene, detailed composition, "
                f"professional artwork, no text"
            )
        else:
            fallback_prompt = (
                f"Chapter {chapter_num} scene, "
                f"{style}, "
                f"compelling visual narrative, "
                f"professional artwork"
            )
        
        print(f"Using title-based prompt")
        return fallback_prompt
    
    def generate_image_pollinations( self,  prompt: str,  width: int = 512,  height: int = 768, model: str = "flux", retries: int = 2) -> Optional[bytes]:

        encoded_prompt = urllib.parse.quote(prompt)
        
        image_url = (
            f"{self.pollinations_url}{encoded_prompt}"
            f"?width={width}&height={height}&model={model}&nologo=true&enhance=true"
        )
        
        print("Generating image with Pollinations.ai")
        
        for attempt in range(retries):
            try:
                response = requests.get(image_url, timeout=30)
                
                if response.status_code == 200:
                    content_type = response.headers.get('content-type', '')
                    
                    if 'image' in content_type:
                        print(f"Image generated successfully ({len(response.content)} bytes)")
                        return response.content
                    else:
                        print(f"Response was not an image: {content_type}")
                else:
                    print(f"HTTP {response.status_code}")
                
                if attempt < retries - 1:
                    wait_time = (attempt + 1) * 2
                    print(f"Retrying in {wait_time} seconds")
                    time.sleep(wait_time)
                    
            except requests.exceptions.Timeout:
                print(f"Request timed out (attempt {attempt + 1}/{retries})")
                if attempt < retries - 1:
                    time.sleep(3)
            except Exception as e:
                print(f"Error: {e}")
                if attempt < retries - 1:
                    time.sleep(2)
        
        print("Failed to generate image after all retries")
        return None
    
    def process_and_save_image(self, image_bytes: bytes, target_size: Tuple[int, int]) -> ContentFile:
        print(f"Processing image to size {target_size}")
        
        try:
            image = Image.open(io.BytesIO(image_bytes))
            
            print(f"Original size: {image.size}, mode: {image.mode}")
            
            if image.mode in ('RGBA', 'LA', 'P'):
                print(f"Converting {image.mode} to RGB")
                background = Image.new('RGB', image.size, (255, 255, 255))
                
                if image.mode == 'P':
                    image = image.convert('RGBA')
                
                if image.mode == 'RGBA':
                    background.paste(image, mask=image.split()[-1])
                else:
                    background.paste(image)
                
                image = background
            
            image.thumbnail(target_size, Image.Resampling.LANCZOS)
            print(f"Resized to: {image.size}")
            
            buffer = io.BytesIO()
            image.save(buffer, format='JPEG', quality=90, optimize=True)
            buffer.seek(0)
            
            file_size = len(buffer.getvalue())
            print(f"Image processed: {file_size} bytes")
            
            return ContentFile(buffer.read())
            
        except Exception as e:
            raise Exception(f"Error processing image: {str(e)}")
    
    def generate_book_cover(self, book_metadata: Dict) -> Tuple[Optional[ContentFile], str]:
        print("GENERATING BOOK COVER")
        
        prompt = self.generate_cover_prompt(book_metadata)
        
        if not prompt:
            return None, "Failed to generate prompt"
        
        image_bytes = self.generate_image_pollinations(
            prompt,
            width=512,
            height=768,
            model="flux"
        )
        
        if not image_bytes:
            return None, prompt
        
        try:
            cover_size = getattr(settings, 'BOOK_COVER_SIZE', (800, 1200))
            processed_image = self.process_and_save_image(image_bytes, cover_size)
            
            print("COVER GENERATION COMPLETE")
            
            return processed_image, prompt
            
        except Exception as e:
            print(f"Error processing cover: {e}")
            return None, prompt
    
    def generate_chapter_illustration(self, chapter_data: Dict, book_context: Dict) -> Tuple[Optional[ContentFile], str]:
        
        chapter_num = chapter_data.get('chapter_number', '?')

        print(f"Generating Chapter {chapter_num} Illustration")

        prompt = self.generate_chapter_prompt(chapter_data, book_context)
        
        if not prompt:
            return None, "Failed to generate prompt"
        
        image_bytes = self.generate_image_pollinations(
            prompt,
            width=512,
            height=512,
            model="turbo"
        )
        
        if not image_bytes:
            return None, prompt
        
        try:
            chapter_size = getattr(settings, 'CHAPTER_IMAGE_SIZE', (1024, 1024))
            processed_image = self.process_and_save_image(image_bytes, chapter_size)
        
            print(f"Chapter {chapter_num} illustration complete")

            return processed_image, prompt
            
        except Exception as e:
            print(f"Error processing chapter image: {e}")
            return None, prompt

    def generate_all_images(self, book_metadata: Dict, chapters: list,max_chapters: int = 20) -> Dict:
        print("BATCH IMAGE GENERATION")
        
        results = {
            'cover': None,
            'chapters': {}
        }
        
        print("\nBook Cover")
        results['cover'] = self.generate_book_cover(book_metadata)
        
        print("\nChapter Illustrations")
        chapters_to_process = chapters[:max_chapters]
        
        for i, chapter in enumerate(chapters_to_process, 1):
            print(f"\n[{i}/{len(chapters_to_process)}]")
            
            chapter_result = self.generate_chapter_illustration(
                chapter,
                {
                    'title': book_metadata.get('title'),
                    'genre': book_metadata.get('genre')
                }
            )
            
            chapter_num = chapter.get('chapter_number', i)
            results['chapters'][chapter_num] = chapter_result
            
            if i < len(chapters_to_process):
                time.sleep(1)
        
        print("BATCH GENERATION COMPLETE")
        print(f"Cover: {'✓' if results['cover'][0] else '✗'}")
        print(f"Chapters: {len([c for c in results['chapters'].values() if c[0]])}/{len(chapters_to_process)}")
        
        return results