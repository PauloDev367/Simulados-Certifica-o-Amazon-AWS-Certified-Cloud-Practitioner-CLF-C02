import json
import os
from flask import Flask, render_template, abort

app = Flask(__name__)

# --- CONFIGURAÇÃO DOS QUIZZES ---
# Adicione seus quizzes aqui. O 'filename' deve corresponder ao arquivo na pasta /quizes.
QUIZES = [
    {
        "name": "Simulado 01 - Certificação Amazon AWS Certified Cloud Practitioner CLF-C02",
        "filename": "quiz_output.json"
    },
    {
        "name": "Simulado 02 - Certificação Amazon AWS Certified Cloud Practitioner CLF-C02",
        "filename": "quiz2_output.json"
    },
]

def load_quiz_data(filename):
    """Carrega os dados de um arquivo JSON específico da pasta /quizes."""
    # Validação para evitar que usuários tentem acessar arquivos indesejados
    if filename not in [q['filename'] for q in QUIZES]:
        abort(404) # Retorna "Not Found" se o arquivo não estiver na lista
        
    filepath = os.path.join('quizes', filename)
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        # Se o arquivo está na lista mas não existe fisicamente, retorna um erro
        abort(404)
    except json.JSONDecodeError:
        # Se o JSON for inválido
        abort(500, description="Erro ao decodificar o arquivo JSON do quiz.")


@app.route('/')
def home():
    """Renderiza a página inicial que lista todos os quizzes disponíveis."""
    return render_template('home.html', quizzes=QUIZES)

@app.route('/quiz/<filename>')
def choice(filename):
    """Página para escolher entre o Modo Quiz e o Modo Visualização."""
    # Encontra o nome do quiz para exibir na página
    quiz_info = next((q for q in QUIZES if q['filename'] == filename), None)
    if not quiz_info:
        abort(404)
        
    return render_template('choice.html', quiz=quiz_info)

@app.route('/viewer/<filename>')
def viewer(filename):
    """Renderiza o modo de visualização para um quiz específico."""
    quiz_info = next((q for q in QUIZES if q['filename'] == filename), None)
    questions_data = load_quiz_data(filename)
    return render_template('viewer.html', questions=questions_data, quiz=quiz_info)

@app.route('/quiz_mode/<filename>')
def quiz_mode(filename):
    """Renderiza o modo de quiz interativo para um quiz específico."""
    quiz_info = next((q for q in QUIZES if q['filename'] == filename), None)
    questions_data = load_quiz_data(filename)
    return render_template('quiz.html', questions=questions_data, quiz=quiz_info)


if __name__ == '__main__':
    app.run(debug=True)