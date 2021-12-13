# Current Implementation
This repository uses Python Flask to setup endpoints, to communicate with frontend application. This backend application is connected to the Blockchain via REST API (currently using default localhost port 8008).


# Setup environment
1. Use Docker (or other methods) to setup sawtooth nodes. It could be multiple nodes or single node for testing. *[link](https://sawtooth.hyperledger.org/docs/core/releases/latest/app_developers_guide/docker_test_network.html)* to hyperledger sawtooth documentation for deploying nodes

2. Run Python SDK on Ubuntu.
    - Ensure that Python3 and pip is installed in Ubuntu
    - "pip install sawtooth-sdk"
    - Install "pkg-config" first if error appears. "sudo apt-get install -y pkg-config".
    - Check if sawtooth_sdk can be imported in Python
    - *[link](https://sawtooth.hyperledger.org/docs/core/releases/latest/app_developers_guide/python_sdk.htmls)* to Python SDK documentation 

3. Refer to Python SDK
    - Hyperledger > sawtooth-sdk-python > examples  > xo_python > sawtooth_xo
    - *[link](https://github.com/hyperledger/sawtooth-sdk-python)* to Python SDK source code

4. Debugging secp256k1 issues
    - .Base cannot be called with secp256k1==0.14.0
    - Try to install secp256k1==0.13.2
    - Not sure why it could not be installed initially, but after a few attempts, it installed.

# Extras
Refer to *[link](https://kba.ai/lets-build-a-hyperledger-sawtooth-application/)* to sample hyperledger sawtooth application. This link provides some useful REST API endpoints to view blockchain.