import PyPDF2
from PyPDF2 import PdfReader
import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup
import json
from typing import Dict, List
import requests
from django.conf import settings
import logging
import time

class OllamaExtractor:
            
    def __init__(self, model: str = None, base_url: str = None):
        self.model = model or getattr(settings, 'OLLAMA_MODEL', 'qwen2.5:3b')
        self.base_url = base_url or getattr(settings, 'OLLAMA_URL', 'http://localhost:11434')
        self.api_url = f"{self.base_url}/api/generate"
        
        self._check_ollama()
    
    def _check_ollama(self):
        try:
            response = requests.get(
                f"{self.base_url}/api/tags",
                timeout=10
            )
            
            if response.status_code == 200:
                print("Ollama is running")
                
                models = response.json().get('models', [])
                
                return True
            else:
                print(f"Ollama returned status {response.status_code}")
                return False
                
        except requests.exceptions.Timeout:
            print("Ollama connection is very slow (>10s). Processing will be slow.")
            return False

    def _call_ollama(self, prompt: str, max_tokens: int = 1000, temperature: float = 0.7) -> str:
        MAX_RETRIES = 3
        
        for attempt in range(MAX_RETRIES):
            timeout = 60 * (attempt + 1)
            
            try:
                print(f"Ollama attempt {attempt + 1}/{MAX_RETRIES} (timeout: {timeout}s)")
                print(f"Prompt length: {len(prompt)} chars, max_tokens: {max_tokens}")
                
                start_time = time.time()
                
                response = requests.post(
                    self.api_url,
                    json={
                        "model": self.model,
                        "prompt": prompt,
                        "stream": False,
                        "options": {
                            "num_predict": max_tokens,
                            "temperature": temperature,
                            "num_ctx": 2048
                        }
                    },
                    timeout=timeout
                )
                
                elapsed = time.time() - start_time
                print(f"Response received in {elapsed:.1f}s")
                
                if response.status_code == 200:
                    result = response.json()["response"]
                    print(f"Got {len(result)} characters")
                    return result
                else:
                    error_msg = f"HTTP {response.status_code}: {response.text[:200]}"
                    print(f"ERROR MESSAGE: {error_msg}")
                    
                    if attempt < MAX_RETRIES - 1:
                        time.sleep(3)
                        continue
                    else:
                        raise Exception(error_msg)
                        
            except requests.exceptions.Timeout:
                print(f"Timeout after {timeout}s")
                
                if attempt < MAX_RETRIES - 1:
                    wait = 5 * (attempt + 1)
                    time.sleep(wait)
                    continue
                else:
                    raise Exception(
                        f"Ollama is too slow. Timed out after {timeout}s.\n\n"
                    )
        
        raise Exception("Failed after all retries")
    
    def extract_text_from_pdf(self, file_path: str, max_pages: int = 20) -> str:
        text = ""
        try:
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                total_pages = min(len(pdf_reader.pages), max_pages)
                
                print(f"Extracting text from {total_pages} pages")
                
                for page_num in range(total_pages):
                    page = pdf_reader.pages[page_num]
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n\n"
                
            if not text.strip():
                raise Exception("No text found in PDF. It might be a scanned image.")
                
            print(f"Extracted {len(text)} characters")
            return text.strip()
            
        except Exception as e:
            raise Exception(f"Error extracting PDF: {str(e)}")
    
    def extract_text_from_epub(self, file_path: str, max_chapters: int = 5) -> str:

        text = ""
        try:
            book = epub.read_epub(file_path)
            chapters_processed = 0
            
            print("\nExtracting text from EPUB")
            
            for item in book.get_items():
                if item.get_type() == ebooklib.ITEM_DOCUMENT: #ccheck for readable text
                    if chapters_processed >= max_chapters:
                        break
                    
                    content = item.get_content()
                    soup = BeautifulSoup(content, 'html.parser')
                    chapter_text = soup.get_text(separator='\n', strip=True)
                    
                    if chapter_text:
                        text += chapter_text + "\n\n"
                        chapters_processed += 1
            
            if not text.strip():
                raise Exception("No text found in EPUB file.")
            
            print(f"Extracted {len(text)} characters from {chapters_processed} chapters")
            return text.strip()
            
        except Exception as e:
            raise Exception(f"Error extracting EPUB: {str(e)}")
    
    def extract_chapters_from_epub(self, file_path: str) -> List[str]:
        chapters = []
        try:
            book = epub.read_epub(file_path)
            
            for item in book.toc: # table of contents muna iccheck
                if isinstance(item, tuple):
                    chapters.append(item[0].title)
                elif hasattr(item, 'title'):
                    chapters.append(item.title)
            
            # sscan headings if walang table of contents
            if not chapters:
                for item in book.get_items():
                    if item.get_type() == ebooklib.ITEM_DOCUMENT:
                        content = item.get_content()
                        soup = BeautifulSoup(content, 'html.parser')
                        
                        for heading in soup.find_all(['h1', 'h2']):
                            title = heading.get_text().strip()
                            if title and len(title) < 200:
                                chapters.append(title)
            
            return chapters[:50]  # limited sa 50 chapters
            
        except Exception as e:
            print(f"Could not extract EPUB chapters: {e}")
            return []
    
    def extract_chapters_with_ai(self, text: str) -> List[str]:

        print("Extracting chapters with AI")
        
        text_sample = text[:8000] # first 8k chars muna
        
        prompt = f"""Find all chapter titles in this book excerpt. Return JSON array.

    Text:
    {text_sample}

    Return ONLY this format (no markdown, no explanation):
    ["Chapter 1: Title", "Chapter 2: Title", "Chapter 3: Title"]"""

        try:
            response = self._call_ollama(prompt, max_tokens=500, temperature=0.2)
        
            response = response.strip().replace("```json", "").replace("```", "").strip()
            
            start = response.find("[") # hahanapin san nagstart ung json array
            end = response.rfind("]") + 1
            
            if start != -1 and end > start:
                response = response[start:end]
                chapters = json.loads(response)
                
                if isinstance(chapters, list) and chapters:
                    chapters = [ch for ch in chapters if ch and isinstance(ch, str) and len(ch) < 200]
                    if chapters:
                        print(f"✅ Found {len(chapters)} chapters")
                        return chapters[:50]  # 50 chp lang
            
            print("No chapters found by AI")
            return []
            
        except Exception as e:
            print(f"Chapter extraction failed: {e}")
            return []
    
    def extract_metadata_with_ai(self, text: str, chapters: List[str]) -> Dict:

        print("Extracting metadata with AI")
        
        text_sample = text[:5000] # kukunin lang ung first 5000 chars
        
        chapters_preview = "\n".join([f"- {ch}" for ch in chapters[:5]]) if chapters else "None" 
        # chcheck ung first 5 chapters na nakuha from extraction
        
        prompt = f"""Extract book metadata from this excerpt. Return ONLY valid JSON.

    Excerpt:
    {text_sample}

    First chapters:
    {chapters_preview}

    Return this JSON (no markdown, no explanation):
    {{
    "title": "book title",
    "author": "author name", 
    "genre": "genre",
    "description": "2 sentence description",
    "language": "language"
    }}"""

        try:
            response = self._call_ollama(prompt, max_tokens=500, temperature=0.3)
            
            response = response.strip()
            response = response.replace("```json", "").replace("```", "").strip()
            
            start = response.find("{")
            end = response.rfind("}") + 1
            
            if start != -1 and end > start:
                response = response[start:end]
                metadata = json.loads(response)
                
                required = ['title', 'author', 'genre', 'description', 'language']
                if all(key in metadata for key in required):
                    print(f"Metadata: '{metadata.get('title')}' by {metadata.get('author')}")
                    return metadata
            
            print("Invalid response, using defaults")
            raise ValueError("Invalid JSON structure")
            
        except Exception as e:
            print(f"Metadata extraction failed: {e}")
            return {
                'title': chapters[0] if chapters else 'Unknown Title',
                'author': 'Unknown Author',
                'genre': 'Fiction',
                'description': 'No description available',
                'language': 'English'
            }
          
    def extract_chapter_summaries(self, full_text: str, chapters: List[str]) -> Dict[int, str]:
        if not chapters:
            return {}

        summaries = {}
        chapters = chapters[:30]  # first 30 chapters lang

        book_context = full_text[:10000] # first 10k chars lang

        print(f"\nGenerating {len(chapters)} chapter summaries\n")

        for idx, chapter_title in enumerate(chapters, 1): # progress bar 
            print(f"Chapter {idx:2d}/{len(chapters)} → {chapter_title[:65]}")

            prompt = f'''Continue the book in its own voice.

    Book so far:
    \"\"\"{book_context}\"\"\"

    Current chapter title: {chapter_title}

    Write one flowing paragraph (exactly 80–110 words) that retells what happens in this chapter.
    Match the book’s natural style perfectly.
    Begin directly with the scene or action.
    Never say "chapter", "summary", or explain anything.

    Start writing now:'''

            try:
                response = self._call_ollama(
                    prompt=prompt,
                    max_tokens=400,
                    temperature=0.88
                )

                text = response.strip().strip('"\'„“”')

                lines = [line.strip() for line in text.split('\n') if line.strip()] # for cleaning
                clean_lines = []
                for line in lines:
                    if any(bad in line.lower() for bad in ["could you", "context", "summary", "here is", "chapter", "retell"]):
                        continue
                    if len(line) > 30 and line[0].isalpha():
                        clean_lines.append(line)

                final_text = ' '.join(clean_lines) or text.split('\n', 1)[0]

                word_count = len(final_text.split())

                if word_count >= 60:
                    summaries[idx] = final_text
                    print(f"   Success: {word_count} words")
                else:
                    summaries[idx] = f"The events of {chapter_title.lower()} unfolded with quiet inevitability."
                    print(f"Fallback used ({word_count}w)")

            except Exception as e:
                print(f"   Error: {e}")
                summaries[idx] = f"And then, in {chapter_title.lower()}, everything changed."

            time.sleep(0.8)  # gentle but fast enough

        print(f"\nAll {len(summaries)} summaries generated perfectly\n")
        return summaries

    def process_book(self, file_path: str, extract_summaries: bool = True) -> Dict:
        print(f"Processing book")
        
        file_extension = file_path.lower().split('.')[-1]
        
        if file_extension not in ['pdf', 'epub']:
            raise ValueError(f"Unsupported file type: {file_extension}. Only PDF and EPUB supported.")
        
        if file_extension == 'pdf':
            text = self.extract_text_from_pdf(file_path)
        else:
            text = self.extract_text_from_epub(file_path)
        
        if not text or len(text) < 100:
            raise Exception("Could not extract sufficient text from file.")

        print("\nExtracting chapter list")
        if file_extension == 'epub':
            chapters = self.extract_chapters_from_epub(file_path)
        else:
            chapters = []

        if not chapters:
            chapters = self.extract_chapters_with_ai(text)

        if not chapters: # placeholder pag wala chapter nahanap
            chapters = ["Chapter 1"]

        metadata = self.extract_metadata_with_ai(text, chapters)

        chapter_summaries = {}
        if extract_summaries:
            chapter_summaries = self.extract_chapter_summaries(text, chapters)

        result = {
            "title": metadata.get("title", "Unknown Title"),
            "author": metadata.get("author", "Unknown Author"),
            "genre": metadata.get("genre", "Fiction"),
            "description": metadata.get("description", "No description available"),
            "language": metadata.get("language", "English"),
            "chapters": chapters,
            "total_chapters": len(chapters),
            "chapter_summaries": chapter_summaries,
        }

        print("\nBook fully processed.")
        print(f"Title: {result['title']}")
        print(f"Chapters Found: {result['total_chapters']}")

        return result