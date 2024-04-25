## Paperweight: Open-Source PDF Compression

**Welcome to Paperweight, a self-hosted open-source PDF compression tool built with Python and Bottle!**

This repository contains the source code for Paperweight, allowing you to easily compress PDF files on your own server without relying on external services. Paperweight utilizes Ghostscript for efficient and customizable compression.

**Features:**

*   **Lossless and Lossy Compression:** Choose between lossless compression for maximum quality or lossy compression for smaller file sizes using different compression levels.
*   **Customizable Settings:** Fine-tune compression parameters to achieve the desired balance between file size and quality through Ghostscript settings.
*   **Self-Hosted:** Maintain complete control over your data and avoid dependence on third-party services.
*   **Easy to Use:** Simple web interface allows you to upload PDFs and select compression levels for quick and easy compression. 
*   **Dockerized:** Easy deployment and setup using Docker.

**Installation:**

**Option 1: Docker**

1.  **Pull the Docker image:** `docker pull chekuhakim/paperweight`
2.  **Run the container:** `docker run -p 8000:8000 chekuhakim/paperweight`
3.  **Access the web interface:** Open your web browser and navigate to `http://localhost:8000/` (or the corresponding IP address and port if running on a server).

**Option 2: Manual Installation**

1.  **Clone the repository:** `git clone https://github.com/your-username/paperweight.git`
2.  **Install dependencies:** 
    *   Ensure you have Python 3.7+ installed.
    *   Install required packages: `pip install bottle ghostscript`
3.  **Run the application:** `python app.py`
4.  **Access the web interface:** Open your web browser and navigate to `http://localhost:1234/` (or the corresponding IP address and port if running on a server).

**Usage:**

1.  **Upload a PDF file:** Use the file upload button on the web interface to select the PDF you want to compress.
2.  **Choose compression level:** Select the desired compression level using the slider or input field. Higher values result in smaller file sizes but may reduce quality.
3.  **Compress:** Click the "Compress" button to start the compression process.
4.  **Download:** Once compression is complete, the compressed PDF file will be automatically downloaded.

**Notes:**

*   The Docker image includes all necessary dependencies, including Python, Bottle, and Ghostscript.
*   You can adjust the port mapping (`-p 8000:8000`) in the `docker run` command if needed. 
*   For manual installation, ensure Ghostscript is installed and accessible on your system. You can adjust the port number and host address in the `paperweight.py` file if needed. 
*   The provided code includes a basic HTML template (`index.html`) for the web interface. You can customize this template to fit your preferences.
