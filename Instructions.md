
# Deploy Python Application to Red Hat OpenShift Local:

### Step 1: Set Up OpenShift Local and Podman Desktop
    crc start
    crc status

### Step 2: Create a Python Application
Create a directory for your application: 

    mkdir python-app
    cd python-app

Create a simple Python application (app.py):

    refere app.py

Create a frontend page (static/index.html):

    refer static/index.html

Create a requirements.txt file for your application:

    Flask==2.2.3
    Werkzeug==2.3.0

Create a Containerfile:
    
    refer Containerfile

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




