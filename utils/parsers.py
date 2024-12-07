import os
from typing import Dict, Callable
from docx2txt import process as parse_docx
from utils.config.config import Configuration
import pdfplumber

def parse_pdf(file_path):
     with pdfplumber.open(file_path) as pdf:
         content = []
        
         for page in pdf.pages:
             text = page.extract_text()
             content.append(text)
            
#             tables = page.extract_tables()
#             for table in tables:
#                 content.append("\nТаблица:")
#                 for row in table:
#                     # Заменяем None на пустую строку и преобразуем все элементы в строки
#                     cleaned_row = ["" if cell is None else str(cell) for cell in row]
#                     content.append(" | ".join(cleaned_row))
                
     return "\n".join(content)

def parse_txt(file_path, **kwargs):
    with open(file_path, 'r') as f:
        return f.read()

class UltimateParser:
    
    parsers_mapping: Dict[str, Callable] = {
        '.docx': parse_docx,
        '.txt': parse_txt,
        '.pdf': parse_pdf # AWAITS: parse pdf
    }
    
    def __init__(self, image_dir: str):
        self.image_dir = image_dir
    
    def parse(self, file_path: os.PathLike):
        """
        Parses a file based on its extension and returns its content.

        Parameters:
            file_path (os.PathLike): The path to the file to be parsed.

        Returns:
            The content of the file, as parsed by the appropriate parser function.
        """
        print(f'Extracting content from file: {file_path}...', end='')
        _, ext = os.path.splitext(file_path)
        res = self.parsers_mapping[ext](file_path)
        print('done!')
        return res
        