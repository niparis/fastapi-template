FROM python:3.10.7-bullseye
# Install:
# - git, for git operations (to e.g. push your work). Also required for setting up your configured dotfiles in the workspace.
# - sudo, while not required, is recommended to be installed, since the workspace user (`gitpod`) is non-root and won't be able to install and use `sudo` to install any other tools in a live workspace.
RUN apt-get update && apt-get install -yq \
    git \
    sudo \
    && apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/*

# Create the gitpod user. UID must be 33333.
RUN useradd -l -u 33333 -G sudo -md /home/gitpod -s /bin/bash -p gitpod gitpod

USER gitpod

RUN curl -sSL https://install.python-poetry.org | python3 -
RUN echo "export PATH="/home/gitpod/.local/bin:$PATH"" >> ~/.bashrc