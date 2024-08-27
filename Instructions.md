
# Deploy Python Application to Red Hat OpenShift Local:

### Step 1: Set Up OpenShift Local and Podman Desktop
    crc start
    crc status

### Step 2: Create a Python Application
Create a directory for your application: 

    mkdir python-app
    cd python-app

Create a simple Python application (app.py):

    from flask import Flask
    app = Flask(__name__)

    @app.route('/')
    def hello():
        return "Hello, OpenShift!"

    if __name__ == '__main__':
        app.run(host='0.0.0.0', port=8080)

Create a requirements.txt file for your application:

    Flask==2.0.1
    Werkzeug==2.0.1

Create a Containerfile:

    # Use OpenShift Python Builder image as base
    FROM registry.access.redhat.com/ubi8/python-38

    # Set working directory
    WORKDIR /app

    # Install dependencies
    COPY requirements.txt .
    RUN pip install -r requirements.txt

    # Copy the rest of the application code
    COPY . .

    # Set the command to run the application
    CMD ["python", "app.py"]

    # Expose the port your application runs on
    EXPOSE 8080

### Step3: Configure Podman to trust the certificate

Extract and save the openshift router Certificate:

    oc get secret router-certs-default -n openshift-ingress -o jsonpath='{.data.tls\.crt}' | base64 --decode > openshift-router.crt

Add the Certificate to the macOS System Keychain:

    sudo security add-trusted-cert -d -r trustRoot -k /Library/Keychains/System.keychain openshift-router.crt

### Step 4: Build the application Image

Build the Podman Image:

    podman build -t python-app:latest .
    podman images

Push the Image to OpenShift Internal Registry:

    podman login -u kubeadmin -p $(oc whoami -t) default-route-openshift-image-registry.apps-crc.testing --tls-verify=false 

    podman tag python-app:latest default-route-openshift-image-registry.apps-crc.testing/demo/python-app
 
    podman push default-route-openshift-image-registry.apps-crc.testing/demo/python-app




