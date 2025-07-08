{
  "cells": [
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "view-in-github",
        "colab_type": "text"
      },
      "source": [
        "<a href=\"https://colab.research.google.com/github/HWAN-OH/H2-Ammonia-Simulator/blob/main/config_loader.py\" target=\"_parent\"><img src=\"https://colab.research.google.com/assets/colab-badge.svg\" alt=\"Open In Colab\"/></a>"
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "import yaml\n",
        "\n",
        "def load_config(path='config.yml'):\n",
        "    \"\"\"\n",
        "    Loads the configuration from a YAML file.\n",
        "    YAML 파일을 로드하여 설정을 불러옵니다.\n",
        "    \"\"\"\n",
        "    try:\n",
        "        with open(path, 'r', encoding='utf-8') as f:\n",
        "            return yaml.safe_load(f)\n",
        "    except FileNotFoundError:\n",
        "        st.error(f\"Error: The configuration file '{path}' was not found.\")\n",
        "        return None\n",
        "    except Exception as e:\n",
        "        st.error(f\"Error loading or parsing the configuration file: {e}\")\n",
        "        return None"
      ],
      "outputs": [],
      "execution_count": null,
      "metadata": {
        "id": "UeeeRPdeM3YA"
      }
    }
  ],
  "metadata": {
    "colab": {
      "provenance": [],
      "include_colab_link": true
    },
    "kernelspec": {
      "display_name": "Python 3",
      "name": "python3"
    }
  },
  "nbformat": 4,
  "nbformat_minor": 0
}