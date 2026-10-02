

## Running locally
1. Create a clean python venv
    ```
    python3 -m venv ~/venvs/traefik-reproduce
    source ~/venvs/traefik-reproduce/bin/activate
    ```
2. Install the dependency
    ```
    pip install -r requirements.txt
    ```
3. Start the server
    ```
    python3 server.py
    ```
4. In another terminal run the client
    ```
    source ~/venvs/traefik-reproduce/bin/activate
    python3 client.py
    ```
The client should raise an exception mentioning "deliberate failure on the server". This is the expected working behaviour.


## Running with a traefik ingress controller
1. Create a k3d cluster and install traefik as per the traefik docs https://doc.traefik.io/traefik/setup/kubernetes/. We can skip TLS and the use the default values except for disabling the read timeout.
    ```
    k3d cluster create traefik \
        --port 80:80@loadbalancer \
        --port 443:443@loadbalancer \
        --port 8000:8000@loadbalancer \
        --k3s-arg "--disable=traefik@server:0"

    helm repo add traefik https://traefik.github.io/charts
    helm repo update
    kubectl create namespace traefik
    helm install traefik traefik/traefik --namespace traefik --set ports.web.transport.respondingTimeouts.readTimeout=0
    ```
2. Build the test server's image and import it to `k3d`
    ```
    docker build -t test-grpc:local .
    k3d image import test-grpc:local -c traefik
    ```
3. Run the server in `k3d`
    ```
    kubectl apply -f deployment.yaml
    ```
4. Run the client against the server running in `k3d`
    ```
    K3D=true python3 client.py
    ```
The client will get one response and then hang. If you left the `ports.web.transport.respondingTimeouts.readTimeout`
enabled then the error will propagate when that timeout expires.


## Testing an older version of traefik
1. Uninstall the traefik version we installed before
    ```
    helm uninstall traefik
    ```
2. Install a version that works
    ```
    helm install traefik traefik/traefik --namespace traefik --set image.tag=3.7.6 --set ports.web.transport.respondingTimeouts.readTimeout=0
    ```
3. Run the client against the server running in `k3d`
    ```
    K3D=true python3 client.py
    ```
Now the error is propagated straight away
