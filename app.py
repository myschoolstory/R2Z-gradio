import aspose.zip as az
from io import BytesIO
import tempfile
import os
import gradio as gr

def rar_to_zip(rar_file_path):
    # Create a temporary ZIP file
    temp_zip = tempfile.NamedTemporaryFile(suffix='.zip', delete=False)
    temp_zip_path = temp_zip.name
    temp_zip.close()

    # Create ZIP archive
    with az.Archive() as zip_archive:
        # Load RAR file
        with az.rar.RarArchive(rar_file_path) as rar_archive:
            # Loop through entries and add to ZIP
            for i in range(rar_archive.entries.length):
                if not rar_archive.entries[i].is_directory:
                    ms = BytesIO()
                    rar_archive.entries[i].extract(ms)
                    zip_archive.create_entry(rar_archive.entries[i].name, ms)
        # Save ZIP archive
        zip_archive.save(temp_zip_path)

    return temp_zip_path

def convert_rar_to_zip(rar_file):
    if rar_file is None:
        return None
    zip_path = rar_to_zip(rar_file)
    return zip_path

with gr.Blocks() as demo:
    gr.Markdown("## RAR to ZIP Converter")
    file_input = gr.File(label="Upload RAR File", file_types=[".rar"])
    file_output = gr.File(label="Download ZIP File")
    convert_button = gr.Button("Convert")
    convert_button.click(
        convert_rar_to_zip,
        inputs=file_input,
        outputs=file_output
    )

demo.launch()