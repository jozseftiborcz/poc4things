import pdfkit
from jinja2 import Environment, FileSystemLoader

def generate_html_from_template(template_file, output_file, data):
    # Load the Jinja2 template environment
    env = Environment(loader=FileSystemLoader('.'))
    template = env.get_template(template_file)

    # Render the template with the provided data
    rendered_html = template.render(data)

    # Write the rendered HTML to a file
    with open(output_file, 'w') as file:
        file.write(rendered_html)

def convert_html_to_pdf(html_file, pdf_file):
    options = {
        'footer-center': '[page]',
        'footer-font-size': '8',
    }
    pdfkit.from_file(html_file, pdf_file, options=options)

# Example usage
template_file = 'template.html'
output_html_file = 'output.html'
output_pdf_file = 'output.pdf'

# Data to populate the template
template_data = {
    'title': 'My HTML Page',
    'content': 'This is the content of my HTML page.'
}

# Generate the HTML page from the template
generate_html_from_template(template_file, output_html_file, template_data)

# Convert the HTML page to PDF
convert_html_to_pdf(output_html_file, output_pdf_file)

