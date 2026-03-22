from pydantic import BaseModel
import datetime
import .config

class Run(BaseModel):
    id : str # Run Identifier (UUID)
    Timestamp : datetime.datetime
    commit_hash : str
    config : config.Config
