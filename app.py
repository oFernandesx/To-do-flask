from flask import Flask, render_template, request, redirect, url_for
import csv
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
TASKS_CSV = 'tasks.csv'

def read_tasks():
    tasks = []
    if os.path.exists(TASKS_CSV):
        with open(TASKS_CSV, newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if not row['imagem']:
                    row['imagem'] = 'padrao.png'
                tasks.append(row)
    return tasks

def write_tasks(tasks):
    with open(TASKS_CSV, 'w', newline='', encoding='utf-8') as file:
        fieldnames = ['titulo', 'descricao', 'urgencia', 'imagem']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(tasks)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/listar_tarefas')
def listar_tarefas():
    tasks = read_tasks()
    return render_template('listar_tarefas.html', tasks=tasks)

@app.route('/adicionar_tarefas', methods=['GET', 'POST'])
def adicionar_tarefas():
    if request.method == 'POST':
        titulo = request.form['titulo']
        descricao = request.form['descricao']
        urgencia = request.form['urgencia']
        
        imagem = request.files.get('imagem')
        
        if imagem and imagem.filename != '':
            img_filename = imagem.filename
            img_path = os.path.join(app.config['UPLOAD_FOLDER'], img_filename)
            imagem.save(img_path)
        else:
            img_filename = 'padrao.png'  # imagem padrão se o usuário não enviar nada
        
        tasks = read_tasks()
        tasks.append({'titulo': titulo, 'descricao': descricao, 'urgencia': urgencia, 'imagem': img_filename})
        write_tasks(tasks)
        return redirect(url_for('listar_tarefas'))
        
    return render_template('adicionar_tarefas.html')


@app.route('/editar_tarefas/<int:index>', methods=['GET', 'POST'])
def editar_tarefas(index):
    tasks = read_tasks()
    if request.method == 'POST':
        tasks[index]['titulo'] = request.form['titulo']
        tasks[index]['descricao'] = request.form['descricao']
        tasks[index]['urgencia'] = request.form['urgencia']
        if 'imagem' in request.files:
            imagem = request.files['imagem']
            if imagem.filename:
                img_filename = imagem.filename
                img_path = os.path.join(app.config['UPLOAD_FOLDER'], img_filename)
                imagem.save(img_path)
                tasks[index]['imagem'] = img_filename
        write_tasks(tasks)
        return redirect(url_for('listar_tarefas'))
    return render_template('editar_tarefas.html', task=tasks[index], index=index)

@app.route('/remover_tarefas/<int:index>')
def remover_tarefas(index):
    tasks = read_tasks()
    if 0 <= index < len(tasks):
        del tasks[index]
        write_tasks(tasks)
    return redirect(url_for('listar_tarefas'))

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
