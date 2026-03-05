import re

def extract_section(full_text, section_name):
    """
    Extracts text from a specific section in the format ### SectionName ...
    """
    pattern = r"### " + re.escape(section_name) + r"\s*\n(.*?)(?=\n###|$)"
    match = re.search(pattern, full_text, re.DOTALL)
    if match:
        return match.group(1).strip()
    return None

def generate_srt(text):
    """
    Converts line-separated text into SRT format with estimated timing.
    """
    if not text:
        return ""
    
    lines = [line.strip() for line in text.strip().split('\n') if line.strip()]
    srt_output = []
    
    current_time = 0.0
    
    for index, line in enumerate(lines, 1):
        # Estimate duration logic:
        # Base pause: 0.5s
        # Reading speed: approx 0.1s per character (adjust as needed)
        duration = 0.5 + (len(line) * 0.1)
        
        start_time = current_time
        end_time = current_time + duration
        
        # Format timestamps: HH:MM:SS,mmm
        def format_time(seconds):
            millis = int((seconds - int(seconds)) * 1000)
            seconds = int(seconds)
            minutes = seconds // 60
            hours = minutes // 60
            minutes %= 60
            seconds %= 60
            return f"{hours:02}:{minutes:02}:{seconds:02},{millis:03}"
            
        srt_output.append(f"{index}")
        srt_output.append(f"{format_time(start_time)} --> {format_time(end_time)}")
        srt_output.append(line)
        srt_output.append("") # Empty line after each block
        
        current_time = end_time
        
    return "\n".join(srt_output)
