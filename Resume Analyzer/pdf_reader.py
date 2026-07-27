import PyPDF2
from PyPDF2.errors import PdfReadError

def extract_text_from_pdf(pdf_file) -> str:
    """
    Extracts text from a PDF file stream.
    Designed to process streamlit uploaded file objects (BytesIO).
    
    Parameters:
        pdf_file: File-like object containing PDF bytes.
        
    Returns:
        str: Extracted and cleaned text from the PDF pages.
        
    Raises:
        ValueError: If the PDF contains no text, or has no pages.
        RuntimeError: If the PDF structure is corrupted or unreadable.
    """
    try:
        # Initialize the PDF reader
        reader = PyPDF2.PdfReader(pdf_file)
        
        # Check if the PDF has pages
        num_pages = len(reader.pages)
        if num_pages == 0:
            raise ValueError("The uploaded PDF file does not contain any pages.")
        
        text_content = []
        for page_idx in range(num_pages):
            page = reader.pages[page_idx]
            page_text = page.extract_text()
            if page_text:
                text_content.append(page_text)
        
        # Combine extracted pages and clean spaces
        full_text = "\n".join(text_content).strip()
        
        if not full_text:
            raise ValueError(
                "Unable to extract text from the PDF. "
                "The file may be image-only (scanned), empty, or password-protected."
            )
            
        return full_text
        
    except PdfReadError as pre:
        raise RuntimeError(f"Corrupted PDF format or parsing failed: {str(pre)}")
    except Exception as e:
        # Preserve ValueError and RuntimeError messages, wrap others
        if isinstance(e, (ValueError, RuntimeError)):
            raise e
        raise RuntimeError(f"Failed to read the PDF document: {str(e)}")
