from pydantic import BaseSettings


class Settings(BaseSettings):
    # The absolute path to the FastText model
    fasttext_model_path: str = "UNSET"

    class Config:
        env_file = "isamples_metadata.env"
