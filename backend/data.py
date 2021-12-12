"""
CLI for uploading csv to database
"""
import argparse
import csv
import os
from abc import ABC, abstractmethod
from decimal import Decimal
from enum import Enum
from typing import Any, Callable, List

from sqlalchemy import create_engine, delete
from sqlalchemy.orm import Session
from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import Boolean, Integer, Numeric

from resslab_tools.models.database import (Connection, ConnectionGlobal,
                                           ConnectionPanelZone)
from resslab_tools.services.database import Base, url

engine = create_engine(url, echo=False)
session = Session(engine)


class Type(Enum):
    CONNECTION = 'connection'
    CONNECTION_GLOBAL = 'connection-global'
    CONNECTION_PANEL_ZONE = 'connection-panel-zone'


class Uploader(ABC):
    """
    Abstract class for all uploaders
    """

    @abstractmethod
    def upload_one(self, file_path: str) -> None:
        """
        Upload one file
        """

    def upload_all(self, file_paths: List[str]) -> None:
        """
        Upload multiple files
        """
        for filename in file_paths:
            self.upload_one(filename)

    @staticmethod
    def get_abs_path(file_path: str) -> str:
        """
        Get absolute path
        """
        abs_path = os.path.abspath(file_path)
        print(f'uploading from {abs_path}')
        return abs_path


class TableUploader(Uploader):
    """
    Uploader from csv to table (csv header and table column name should match)
    """

    def __init__(self,
                 base_model: Base) -> None:
        self.base_model = base_model

    def upload_one(self, file_path: str) -> None:
        file_path = self.get_abs_path(file_path)
        with open(file_path, 'rt', encoding='utf-8') as file:
            reader = csv.reader(file, strict=True)
            header = next(reader)  # skip header
            for row in reader:
                data = {column.key: self.__get_value(column, header, row)
                        for column
                        in self.base_model.__table__.c}
                session.merge(self.base_model(**data))
        session.commit()

    @staticmethod
    def __get_value(column: Column, header: List[str], row: List[str]) -> Any:

        index = header.index(column.key)
        value = row[index]
        if isinstance(column.type, Integer):
            return int(value)
        if isinstance(column.type, Numeric):
            return Decimal(value)
        if isinstance(column.type, Boolean):
            return bool(value)
        return str(value)


class CsvFileUploader(Uploader):
    """
    Uploader from csv to table
    """

    def __init__(self,
                 get_delete: Callable[[str], delete],
                 get_instance: Callable[[str, int, List[str]], Any]) -> None:
        self.get_delete = get_delete
        self.get_instance = get_instance

    def upload_one(self, file_path: str) -> None:
        file_path = self.get_abs_path(file_path)
        filename = self.__get_filename(file_path)
        with open(file_path, 'rt', encoding='utf-8') as file:
            reader = csv.reader(file, strict=True)
            next(reader)  # skip header
            session.execute(
                self.get_delete(filename)
            )
            for index, value in enumerate(reader):
                session.add(self.get_instance(filename, index, value))
        session.commit()

    @staticmethod
    def __get_filename(file_path: str) -> str:
        basename = os.path.basename(file_path)
        return os.path.splitext(basename)[0]


def main():
    parser = argparse.ArgumentParser(
        description='Upload csv files to database')
    parser.add_argument('type', type=Type, choices=list(Type))
    parser.add_argument('filenames',
                        nargs='+',
                        help='data input file pattern')

    args = parser.parse_args()
    input_type: Type = args.type
    filenames: List[str] = args.filenames

    if input_type == Type.CONNECTION:
        uploader = TableUploader(
            Connection
        )
    elif input_type == Type.CONNECTION_GLOBAL:
        uploader = CsvFileUploader(
            lambda id: delete(ConnectionGlobal)
            .where(ConnectionGlobal.connection_id == id),
            lambda id, index, value: ConnectionGlobal(
                connection_id=id,
                id=index,
                story_drift_angle=value[0],
                actuator_force=value[1],
            ))
    elif input_type == Type.CONNECTION_PANEL_ZONE:
        uploader = CsvFileUploader(
            lambda id: delete(ConnectionPanelZone)
            .where(ConnectionPanelZone.connection_id == id),
            lambda id, index, value: ConnectionPanelZone(
                connection_id=id,
                id=index,
                shear_distortion=value[0],
                shear_force=value[1],
            ))
    else:
        raise NotImplementedError(f'unknown type {input_type}')

    uploader.upload_all(filenames)


if __name__ == '__main__':
    main()
