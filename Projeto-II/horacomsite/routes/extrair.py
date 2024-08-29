import os
import zipfile
#FIZ TESTE LOCAL E DEU CERTO A FUNÇÃO E ZIP DOS ARQUIVOS 

def extrair_e_zipar_documentos(diretorio_documentos, caminho_zip):
    try:
        # Garante que o caminho do arquivo ZIP tenha um nome de arquivo
        if not caminho_zip.endswith('.zip'):
            caminho_zip = os.path.join(caminho_zip, 'documentos.zip')

        # Criação de um arquivo ZIP
        with zipfile.ZipFile(caminho_zip, 'w') as arquivo_zip:
            # Itera sobre os arquivos no diretório de documentos
            for root, dirs, files in os.walk(diretorio_documentos):
                for file in files:
                    caminho_arquivo = os.path.join(root, file)
                    # Adiciona o arquivo ao arquivo ZIP
                    arquivo_zip.write(caminho_arquivo, arcname=os.path.relpath(caminho_arquivo, os.path.dirname(diretorio_documentos)))

        print('Documentos zipados com sucesso.')

    except Exception as e:
        print('Erro ao zipar os documentos:', str(e))

# Substituir local do arquivo dos certificados 
diretorio_documentos = r'C:\Users\Fernanda\Desktop\Certificados'  # Caminho do diretório de documentos
caminho_zip = r'C:\Users\Fernanda\Desktop\documentos.zip'  # Caminho do arquivo ZIP

extrair_e_zipar_documentos(diretorio_documentos, caminho_zip)
