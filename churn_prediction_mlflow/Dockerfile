# Use official continuumio image with Conda and Python 3.8
FROM continuumio/miniconda3:4.12.0

# Set working directory
WORKDIR /app



# Copy environment definition
COPY conda.yaml .

# Create the conda environment
RUN conda env create -f conda.yaml

# Install system dependencies (for libstdc++ version issues)
# ✅ Install updated libstdc++ from conda-forge (fixes GLIBCXX issues)
RUN conda install -n churn_prediction -c conda-forge libstdcxx-ng


# Set environment path
ENV PATH /opt/conda/envs/churn_prediction/bin:$PATH
ENV LD_LIBRARY_PATH /opt/conda/envs/churn_prediction/lib:$LD_LIBRARY_PATH

# Copy rest of the code
COPY . .

# Make entrypoint script executable
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Expose MLflow tracking server port
EXPOSE 5000

# Set entrypoint
ENTRYPOINT ["/entrypoint.sh"]
