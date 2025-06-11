# Use official Conda base image
FROM continuumio/miniconda3:4.12.0

# Set working directory
WORKDIR /app

# Install essential system tools
RUN apt-get update && \
    apt-get install -y curl bash coreutils && \
    rm -rf /var/lib/apt/lists/*

# Copy Conda environment file
COPY conda.yaml .

# Create the conda environment
RUN conda env create -f conda.yaml

# Install updated libstdc++ into the environment
RUN conda run -n churn_prediction conda install -c conda-forge libstdcxx-ng ncurses

# Set environment variables
ENV PATH=/opt/conda/envs/churn_prediction/bin:$PATH
ENV LD_LIBRARY_PATH=/opt/conda/envs/churn_prediction/lib

# Copy source code
COPY . .

# Add and set permissions for entrypoint script
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Use bash explicitly
SHELL ["/bin/bash", "-c"]

# Expose MLflow port
EXPOSE 5000

# Set entrypoint
ENTRYPOINT ["/entrypoint.sh"]

