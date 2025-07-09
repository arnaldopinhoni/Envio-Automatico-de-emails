import streamlit as st
import pandas as pd
from fpdf import FPDF
import tempfile
import os
import zipfile

def gerar_pdf(cliente, reajuste, data, temp_dir):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    texto = f"""
Ribeirão Preto, {data}

{cliente}

Prezado(a) cliente,

Gostaríamos de começar esta carta expressando nossa sincera gratidão por sua confiança e parceria contínua com a Medicar.

Ao longo dos anos, nos empenhamos diariamente para oferecer serviços de alta qualidade, visando sempre a segurança e o bem-estar de nossos clientes.

Por isso, a fim de manter o nível de excelência que você já conhece e espera de nós, precisamos realizar um reajuste nos valores dos nossos serviços.

Esse ajuste é necessário para repor os aumentos nos custos de materiais e insumos que enfrentamos ao longo do último ano.

Além disso, ele é fundamental para garantir a manutenção da qualidade dos nossos equipamentos, a atualização da nossa frota de veículos e o contínuo treinamento dos nossos profissionais.

Sabemos que qualquer mudança nos valores pode causar impacto, mas asseguramos que essa medida é imprescindível para continuarmos oferecendo serviços de alta qualidade, com a segurança e a eficiência que você merece.

O índice de reajuste será de {reajuste}.

Reiteramos nosso compromisso com a transparência e a qualidade e estamos à disposição para esclarecer qualquer dúvida que possa surgir.

Agradecemos, mais uma vez, pela confiança depositada em nossos serviços.

Atenciosamente,
Equipe Medicar Soluções em Saúde
0800 940 0590
    """

    for linha in texto.strip().split('\n'):
        pdf.multi_cell(0, 10, linha.strip())

    pdf_path = os.path.join(temp_dir, f"{cliente}.pdf")
    pdf.output(pdf_path)
    return pdf_path

# Interface do app
st.title("Gerador de PDFs Personalizados - Reajuste Medicar")

uploaded_excel = st.file_uploader("📄 Upload da planilha Excel (.xlsx)", type=["xlsx"])

if uploaded_excel:
    df = pd.read_excel(uploaded_excel)

    if st.button("📄 Gerar PDFs e Baixar .zip"):
        with tempfile.TemporaryDirectory() as temp_dir:
            pdf_paths = []

            for _, row in df.iterrows():
                cliente = str(row['Cliente'])
                reajuste = str(row['Reajuste'])
                data = str(row['Data'])

                pdf_path = gerar_pdf(cliente, reajuste, data, temp_dir)
                pdf_paths.append(pdf_path)

            # Criar ZIP com os PDFs
            zip_path = os.path.join(temp_dir, "pdfs_reajuste.zip")
            with zipfile.ZipFile(zip_path, 'w') as zipf:
                for pdf in pdf_paths:
                    zipf.write(pdf, arcname=os.path.basename(pdf))

            with open(zip_path, "rb") as f:
                st.download_button(
                    label="📥 Baixar todos os PDFs (.zip)",
                    data=f,
                    file_name="pdfs_reajuste.zip",
                    mime="application/zip"
                )
