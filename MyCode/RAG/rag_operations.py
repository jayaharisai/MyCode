import os
import openai
from PyPDF2 import PdfReader
from docx import Document

class MyCodeOpenaiWrapper:
    def __init__(self, model: str, temperature: float, **kwargs):
        self.model = model
        self.temperature = temperature
        self.extra_args = kwargs

    def start(self, prompt: str, stream: bool = False, **kwargs):
        openai.api_key = os.getenv("mycode_openai_key")

        params = {
            "model": self.model,
            "temperature": self.temperature,
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "stream": stream
        }

        params.update(self.extra_args)
        params.update(kwargs)

        if stream:
            full_content = ""
            response = openai.ChatCompletion.create(**params)
            print("🔁 Streaming response:\n")

            for chunk in response:
                content = chunk["choices"][0].get("delta", {}).get("content", "")
                print(content, end="", flush=True)
                full_content += content

            required_response = {
                "model": self.model,
                "input": prompt,
                "content": full_content,
                "input_tokens": None,
                "completion_tokens": None,
                "total_tokens": None
            }
        else:
            response = openai.ChatCompletion.create(**params)

            required_response = {
                "model": response["model"],
                "input": prompt,
                "content": response["choices"][0]["message"]["content"],
                "input_tokens": response["usage"]["prompt_tokens"],
                "completion_tokens": response["usage"]["completion_tokens"],
                "total_tokens": response["usage"]["total_tokens"],
            }
        return required_response

# Loaders pdf's, docs, csv 
class RagLoaders:
    def __init__(
            self, 
            folder_path: str = None,
            multiple_folder_path: list = None,
            file_path: str = None,
            multiple_file_path: list = None
            ):
        self.folder_path = folder_path
        self.multiple_folder_path = multiple_folder_path
        self.file_path = file_path
        self.multiple_file_path = multiple_file_path

    def folder_loader(self):
        return "Data"
    
    def multiple_folder_loader(self):
        return
    
    def file_loader(self):
        if not self.file_path:
            return None
        file_extension = self.file_path.split('.')[-1].lower()
        
        try:
            if file_extension == 'pdf':
                return self._load_pdf(path = self.file_path)
            elif file_extension == 'txt':
                return self._load_txt()
            elif file_extension == 'docx':
                return self._load_docx()
            else:
                print(f"Unsupported file type: {file_extension}")
                return None
        except Exception as e:
            print(f"Error loading file {self.file_path}: {str(e)}")
            return None
    
    def _load_pdf(self, path: str):
        text = ""
        with open(path, 'rb') as f:
            pdf_reader = PdfReader(f)
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
        return text
    
    def _load_txt(self, path: str):
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    
    def _load_docx(self, path: str):
        
        doc = Document(self.file_path)
        return "\n".join([para.text for para in doc.paragraphs])
    
    def multiple_file_loader(self):
        content = []
        for file in self.multiple_file_path:
            file_extension = file.split('.')[-1].lower()
        
            try:
                if file_extension == 'pdf':
                    content.append(self._load_pdf(file))
                elif file_extension == 'txt':
                    content.append(self._load_txt())
                elif file_extension == 'docx':
                    content.append(self._load_docx())
                else:
                    print(f"Unsupported file type: {file_extension}")
                    pass
            except Exception as e:
                print(f"Error loading file {self.file_path}: {str(e)}")
                pass
        return content
    
    def flatten_list(self, nested_list):
        flat_list = []
        for item in nested_list:
            if isinstance(item, list):
                flat_list.extend(self.flatten_list(item))
            else:
                flat_list.append(item)
        return flat_list

    def start(self):
        content = []
        if self.folder_path:
            self.folder_loader()

        if self.multiple_folder_path:
            self.multiple_folder_loader()

        if self.file_path:
            content.append(self.file_loader())

        if self.multiple_file_path:
            content.append(self.multiple_file_loader())
        flatten_list = self.flatten_list(content)
        return flatten_list



class MyCodeSplitters:
    def __init__(self, text):
        self.text = text

