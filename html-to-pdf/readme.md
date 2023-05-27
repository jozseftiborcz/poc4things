pip install Jinja2 pdfkit
pip install wkhtmltopdf
python html_to_pdf.py

binaries should be installed on linux from https://wkhtmltopdf.org/downloads.html as Qt is not complied and behaviour (eg. footer) is different.

apt-get install xfonts-75dpi
dpkg -i wkhtmltox_0.12.6-1.focal_amd64.deb
