from bottle import Bottle, request, response, static_file, template
import subprocess
import os
from socket import gethostname, gethostbyname
import tempfile
import shutil

app = Bottle()

def compress_pdf_file(input_file, output_file, compression_level):
    compression_settings = {
        'screen': '/screen',  # low-resolution output, similar to "Screen Optimized"
        'ebook': '/ebook',    # medium-resolution output, similar to "eBook" setting
        'printer': '/printer',  # high-resolution output, similar to "Print Optimized"
        'prepress': '/prepress',  # very high-resolution, similar to "Prepress Optimized"
        'default': '/default'  # balanced output across a variety of uses
    }
    quality = compression_settings.get(compression_level, '/default')
    try:
        with open('ghostscript.log', 'w') as log_file:
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
        print(f"Error compressing PDF: {str(e)}")

@app.route('/', method='GET')
def index():
    return template('index.html')

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

            response.headers['Content-Disposition'] = f'attachment; filename="{output_filename}"'
            return static_file(output_filename, root=temp_dir, download=output_filename)
        finally:
            shutil.rmtree(temp_dir)

if __name__ == '__main__':
    hostname = gethostname()
    local_ip = gethostbyname(hostname)
    print(f" * Running on http://0.0.0.0:1234/")
    print(f" * Running on http://{local_ip}:1234/")
    print(f" * Running on http://{gethostbyname(gethostname())}:1234/")
    app.run(host='0.0.0.0', port=1234)
