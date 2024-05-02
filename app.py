from bottle import Bottle, request, response, static_file, template
import subprocess
import os
import tempfile
import shutil

app = Bottle()

def compress_pdf_file(input_file, output_file, compression_level):
    compression_settings = {
        10: '/screen',
        20: '/ebook',
        30: '/printer',
        40: '/prepress',
        50: '/default',
        60: '/printer',
        70: '/prepress',
        80: '/ebook',
        90: '/screen'
    }
    quality = compression_settings.get(int(compression_level), '/default')
    with open('ghostscript.log', 'w') as log_file:
        try:
            subprocess.run([
                'gs', '-q', '-dBATCH', '-dNOPAUSE', '-sDEVICE=pdfwrite',
                '-dCompatibilityLevel=1.5', '-dColorConversionStrategy=/LeaveColorUnchanged',
                f'-dPDFSETTINGS={quality}', '-dEmbedAllFonts=true', '-dSubsetFonts=true',
                '-dAutoRotatePages=/None', '-dColorImageDownsampleType=/Bicubic',
                '-dGrayImageDownsampleType=/Bicubic', '-dMonoImageDownsampleType=/Subsample',
                '-dGrayImageResolution=72', '-dColorImageResolution=72', '-dMonoImageResolution=72',
                '-sOutputFile=' + output_file, input_file
            ], check=True, stdout=log_file, stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError as e:
            print(f"Error compressing PDF: {e}")

@app.route('/', method='GET')
def show_form():
    return template('index.html', message="Please upload a file and select a compression level.")

@app.route('/', method='POST')
def compress_pdf():
    file = request.files.get('file')
    compression_level = request.forms.get('compression-level')
    if file and compression_level:
        filename = file.filename
        temp_dir = tempfile.mkdtemp()
        try:
            input_path = os.path.join(temp_dir, filename)
            with open(input_path, 'wb') as f:
                f.write(file.file.read())

            output_filename = f"{filename}_compressed.pdf"
            output_path = os.path.join(temp_dir, output_filename)

            compress_pdf_file(input_path, output_path, compression_level)

            original_size = os.path.getsize(input_path)
            compressed_size = os.path.getsize(output_path)
            size_reduction = 100 * (1 - (compressed_size / original_size))

            response.content_type = 'application/pdf'
            response.headers['Content-Disposition'] = f'attachment; filename="{output_filename}"'
            message = f"File compressed successfully. Size reduced by {size_reduction:.2f}%."
            return template('index.html', message=message, download_link=f'/download/{filename}')
        finally:
            shutil.rmtree(temp_dir)
    else:
        return template('index.html', message="Please upload a file and select a compression level.")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=1434)
