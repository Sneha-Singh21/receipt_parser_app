import os

def is_valid_filetype(filename):
    allowed_extensions = ['.jpg', '.png', '.pdf', '.txt']
    ext = os.path.splitext(filename)[1].lower()
    return ext in allowed_extensions
