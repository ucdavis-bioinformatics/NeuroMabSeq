# NeuroMabSeq

Welcome to the NeuroMabSeq project repository. This project is structured across multiple branches to organize different components of the project. Below you will find installation and setup instructions for the main branches: `website_2.0` and `pipeline`.

## Getting Started

To get started with the NeuroMabSeq project, you first need to clone the repository to your local machine.

1. Open a terminal or command prompt.
2. Clone the repository by running:

    ```
    git clone https://github.com/ucdavis-bioinformatics/NeuroMabSeq.git
    ```
3. Navigate into the cloned repository directory:

    ```
    cd NeuroMabSeq
    ```

Now, you're ready to set up the environments for different branches as per your needs.

## Branches

### `website_2.0`

This branch contains the necessary files and configuration for setting up the project's website environment.

#### Installation

To set up your environment to run or develop the website, follow these steps:

1. Switch to the `website_2.0` branch by running:

    ```
    git checkout website_2.0
    ```

2. Navigate to the directory containing the `environment.yml` file.
3. Create the Conda environment by running:

    ```
    conda env create -f environment.yml
    ```

4. Activate the new environment:

    ```
    conda activate <env_name>
    ```

Replace `<env_name>` with the name of the environment specified in the `environment.yml` file. This name is usually found at the top of the `environment.yml` file under the `name` field.

### `pipeline`

The `pipeline` branch is designed for processing and analysis tasks within the project.

#### Installation

*Specific installation instructions for the `pipeline` branch will be provided shortly. Stay tuned for updates.*

## Contributing

We welcome contributions! If you would like to contribute, please follow the standard GitHub fork and pull request workflow.

## License

This project is licensed under the [MIT License](LICENSE) - see the LICENSE file for details.

## Acknowledgments

* List any acknowledgments and credits here.

