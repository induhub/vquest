import os
from flask import Flask
from flask import render_template
from flask import request
import docker
app = Flask(__name__)
@app.route('/')



def index():
    return render_template('index.html')


def start_container(image_name):
    docker_client = docker.Client(base_url='unix://var/run/docker.sock',
                                  version='1.12',
                                  timeout=100)
    docker_client.images(name=image_name)
    container = docker_client.create_container(image=image_name,ports=[(6080, 'tcp'),])
    docker_client.start(container=container['Id'],port_bindings={6080: ('0.0.0.0', 6080)})
    return container['Id']

def stop_container(container_id):
    docker_client = docker.Client(base_url='unix://var/run/docker.sock',
                                  version='1.12',
                                  timeout=100)
    docker_client.stop(container_id)
    
@app.route('/start', methods=['GET'])
def start_process():
    if request.method == 'GET':
       #selected_image=request.form['docker_image']
       x = start_container("vtuquest/c")
       return x

@app.route('/stop/<container_id>', methods=['GET'])
def stop_process(container_id=None):
    if request.method == 'GET':
       stop_container(container_id)
       return "done"


    
if __name__ == '__main__':
    app.run(debug=True)
