from bottle import Bottle, request, response, static_file, template
import subprocess
import os
from socket import gethostname, gethostbyname
import tempfile
import shutil

app = Bottle()

def compress_pdf_file(input_file, output_file, compression_level):
    try:
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
            subprocess.run(['gs', '-q', '-r72', '-dBATCH', '-dNOPAUSE', '-sDEVICE=pdfwrite',
                            '-dCompatibilityLevel=1.5', '-dColorConversionStrategy=/LeaveColorUnchanged',
                            f'-dPDFSETTINGS={quality}', '-dPDFSETTINGS=/printer', '-dEmbedAllFonts=true', '-dSubsetFonts=true',
                            '-dAutoRotatePages=/None', '-dColorImageDownsampleType=/Bicubic',
                            '-dGrayImageDownsampleType=/Bicubic', '-dMonoImageDownsampleType=/Subsample',
                            '-dGrayImageResolution=72', '-dColorImageResolution=72', '-dMonoImageResolution=72',
                            '-sOutputFile=' + output_file, input_file], check=True, stdout=log_file, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as e:
        print(f"Error compressing PDF: {e}")

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
