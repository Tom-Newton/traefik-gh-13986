

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
1. Set env vars to configure the deployment
    ```
    export IMAGE=<some fully qualified image tag pointing to a container registry you can push and pull from>
    export CLUSTER_ISSUER=<>
    ```
