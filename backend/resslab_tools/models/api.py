"""
API Models
"""
import enum
from decimal import Decimal
from typing import List

from pydantic import BaseModel


class OrmModel(BaseModel):
    """
    Parent class for all API models
    """
    class Config:
        orm_mode = True


class ConnectionModel(OrmModel):
    """
    Connection
    """
    id: str
    experimental_program: str
    date: int
    specimen_designation: str
    northridge: str
    specimen_type: str
    slab: bool
    connection_type: str
    section_b: str
    d_b: Decimal
    steel_b: str
    section_c: str
    d_c: Decimal
    t_cf: Decimal
    t_dp: Decimal
    n_dp: int
    lat: Decimal
    lon: Decimal
    t_dp_tot: Decimal


class CountModel(BaseModel):
    """
    Count
    """
    names: List[str]
    value: int


class RangeModel(BaseModel):
    """
    Range
    """
    min: Decimal
    max: Decimal


class DownloadModel(BaseModel):
    """
    DownloadModel
    """
    global_csv: str
    panel_zone_csv: str


ConnectionField = enum.Enum(
    'ConnectionField',
    {key: key
     for key
     in ConnectionModel.__fields__}
)

ConnectionNumberField = enum.Enum(
    'ConnectionNumberField',
    {key: key
     for key, field
     in ConnectionModel.__fields__.items()
     if field.type_ in [int, Decimal]}
)
