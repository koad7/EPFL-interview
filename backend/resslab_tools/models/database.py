"""
Databse Models
"""
from resslab_tools.services.database import Base
from sqlalchemy import (BigInteger, Boolean, Column, ForeignKey, Numeric,
                        SmallInteger, String)
from sqlalchemy.orm import column_property


class Connection(Base):
    """
    Connection
    """
    __tablename__ = 'connection'

    id = Column(String, primary_key=True)
    experimental_program = Column(String, nullable=False)
    date = Column(SmallInteger, nullable=False)
    specimen_designation = Column(String, nullable=False)
    northridge = Column(String(4), nullable=False)
    specimen_type = Column(String, nullable=False)
    slab = Column(Boolean, nullable=False)
    connection_type = Column(String, nullable=False)
    section_b = Column(String, nullable=False)
    d_b = Column(Numeric(8, 4))
    steel_b = Column(String)
    section_c = Column(String, nullable=False)
    d_c = Column(Numeric(8, 4))
    t_cf = Column(Numeric(20, 10))
    t_dp = Column(Numeric(6, 3), nullable=False)
    n_dp = Column(SmallInteger, nullable=False)
    lat = Column(Numeric(8, 6))
    lon = Column(Numeric(8, 6))
    t_dp_tot = column_property(t_dp * n_dp)


class ConnectionGlobal(Base):
    """
    Global
    """
    __tablename__ = 'connection_global'

    connection_id = Column(String,
                           ForeignKey('connection.id'),
                           primary_key=True,
                           index=True)
    id = Column(BigInteger, primary_key=True, autoincrement=True)

    story_drift_angle = Column(Numeric(20, 10), nullable=False)
    actuator_force = Column(Numeric(20, 10), nullable=False)


class ConnectionPanelZone(Base):
    """
    Panel Zone
    """
    __tablename__ = 'connection_panel_zone'

    connection_id = Column(String,
                           ForeignKey('connection.id'),
                           primary_key=True,
                           index=True)
    id = Column(BigInteger, primary_key=True, autoincrement=True)

    shear_distortion = Column(Numeric(20, 10), nullable=False)
    shear_force = Column(Numeric(20, 10), nullable=False)
