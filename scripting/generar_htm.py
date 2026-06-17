import sys
import base64
import os
import pdf_splitter

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.environ.get('PORTABLE_ROOT', os.path.dirname(SCRIPT_DIR) if os.path.basename(SCRIPT_DIR) == 'scripting' else SCRIPT_DIR)

def generate_single_normal_htm(template_content, pdf_base64, filename, output_path):
    html = template_content
    # Nombre del archivo para mostrar en la UI
    old_logic = """        const urlParams = new URLSearchParams(window.location.search);
        const fileName = urlParams.get('file');
        
        if (!fileName) {
            document.body.innerHTML = "<h1>Error: No se especificó un archivo PDF</h1>";
        } else {
            document.getElementById('filename').textContent = fileName;
            document.title = fileName;
        }"""
    
    new_logic = f"""        const fileName = "{filename}";
        document.getElementById('filename').textContent = fileName;
        document.title = fileName;"""
    
    if old_logic in html:
        html = html.replace(old_logic, new_logic)
    
    # Reemplazar la llamada a getDocument(fileName) por la versión con data
    html = html.replace("pdfjsLib.getDocument(fileName)", "pdfjsLib.getDocument({data: pdfData})")

    # Inyectar la variable pdfData con el contenido Base64
    data_injection = f'\n        const pdfData = atob("{pdf_base64}");\n'
    
    insertion_point = "pdfjsLib.GlobalWorkerOptions.workerSrc = workerUrl;"
    if insertion_point in html:
        html = html.replace(insertion_point, insertion_point + data_injection)
    else:
        html = html.replace("<script>\n        // Setup worker", "<script>\n" + data_injection + "        // Setup worker")

    # Escribir el archivo final
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"HTM generado con éxito: {output_path}")

def main():
    if len(sys.argv) < 3:
        print("Usage: python3 generar_htm.py <pdf_path> <output_path> [pdf_js_path] [worker_js_path]")
        sys.exit(1)

    pdf_path = sys.argv[1]
    output_path = sys.argv[2]
    
    template_path = f"{PROJECT_ROOT}/scripting/htm.htm"
    if not os.path.exists(template_path):
        print(f"Error: Template {template_path} no encontrado.")
        sys.exit(1)
        
    with open(template_path, 'r', encoding='utf-8') as f:
        template_content = f.read()

    # Get total pages and check if split is needed (with empty audios)
    total_pages = pdf_splitter.get_total_pages(pdf_path)
    parts = pdf_splitter.partition_pdf(pdf_path, "", total_pages, {})
    
    if len(parts) > 1:
        print(f"[!] PDF es masivo. Dividiendo en {len(parts)} partes...")
        pdf_splitter.cleanup_old_parts(pdf_path)
        
        output_dir = os.path.dirname(output_path)
        output_base, _ = os.path.splitext(os.path.basename(output_path))
        
        for idx, (start, end) in enumerate(parts, 1):
            part_pdf_path, part_suffix = pdf_splitter.split_pdf_file(pdf_path, start, end, idx, len(parts))
            if not part_pdf_path:
                continue
            
            with open(part_pdf_path, 'rb') as f:
                part_pdf_bytes = f.read()
            part_pdf_base64 = base64.b64encode(part_pdf_bytes).decode('utf-8')
            
            part_output_name = f"{output_base}{part_suffix}.htm"
            part_output_path = os.path.join(output_dir, part_output_name)
            part_filename = os.path.basename(part_pdf_path)
            
            generate_single_normal_htm(template_content, part_pdf_base64, part_filename, part_output_path)
    else:
        # Convencional
        with open(pdf_path, 'rb') as f:
            pdf_bytes = f.read()
        pdf_base64 = base64.b64encode(pdf_bytes).decode('utf-8')
        filename = os.path.basename(pdf_path)
        generate_single_normal_htm(template_content, pdf_base64, filename, output_path)

if __name__ == "__main__":
    main()
