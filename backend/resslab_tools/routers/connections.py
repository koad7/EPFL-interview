"""
Handle /connections requests
"""
import math
from decimal import Decimal
from distutils.util import strtobool
from typing import Any, List, Optional, Union

from fastapi import APIRouter, Depends, Path, Query, Request
from fastapi.responses import StreamingResponse
from fastapi_pagination import Page
from fastapi_pagination.ext.async_sqlalchemy import paginate
from resslab_tools.models.api import (ConnectionField, ConnectionModel,
                                      ConnectionNumberField, CountModel,
                                      DownloadModel, RangeModel)
from resslab_tools.models.database import (Connection, ConnectionGlobal,
                                           ConnectionPanelZone)
from resslab_tools.services.database import get_session
from resslab_tools.utils.fastapi import HttpHeader, MediaType, attachment
from sqlalchemy import and_, desc, func, or_, select, tuple_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.selectable import Select
from sqlalchemy.sql.sqltypes import Boolean, Integer, Numeric, String

router = APIRouter(
    prefix='/connections',
    tags=['connections'],
)


@router.get('', response_model=Page[ConnectionModel])
async def get_connections(
        session: AsyncSession = Depends(get_session),
        query: Optional[str] = Query(None),
        sort_by: List[str] = Query([]),
        sort_desc: List[bool] = Query([]),
):
    """
    Get paginated Connections
    """
    where_clauses: List[Any] = __get_where_clauses(query)
    order_clauses: List[Any] = [Connection.__dict__[key]
                                if not is_desc
                                else desc(Connection.__dict__[key])
                                for key, is_desc
                                in zip(sort_by, sort_desc)]
    return await paginate(
        session,
        select(Connection)
        .where(and_(*where_clauses))
        .order_by(*order_clauses)
    )


@router.get('/counts', response_model=List[CountModel])
async def get_counts(
    session: AsyncSession = Depends(get_session),
    fields: List[ConnectionField] = Query(...),
    query: Optional[str] = Query(None),
) -> List[CountModel]:
    """
    Get occurences count of field values
    """
    where_clauses: List[Any] = __get_where_clauses(query)
    columns = [Connection.__dict__[field.value] for field in fields]
    tuples = await session.execute(
        select([*columns, func.count()])
        .where(and_(*where_clauses))
        .group_by(func.grouping_sets(tuple_(*columns)))
    )
    return [
        CountModel(
            names=[
                __format_value(value)
                for value
                in list(tuple)[:-1]
            ],
            value=tuple[len(columns)])
        for tuple
        in tuples
    ]


@router.get('/range', response_model=RangeModel)
async def get_range(
    session: AsyncSession = Depends(get_session),
    field: ConnectionNumberField = Query(...),
) -> RangeModel:
    """
    Get range of field
    """
    column: Column[Union[Integer, Decimal]] = Connection.__dict__[field.value]
    tuples = await session.execute(
        select([func.min(column), func.max(column)])
    )
    row = next(tuples)
    return RangeModel(min=row[0], max=row[1])


@router.get('/{connection_id}/download', response_model=DownloadModel)
async def get_download(
    request: Request,
    connection_id: str = Path(...),
) -> DownloadModel:
    return DownloadModel(
        global_csv=request.url_for(
            "get_global_csv",
            connection_id=connection_id
        ),
        panel_zone_csv=request.url_for(
            "get_panel_zones_csv",
            connection_id=connection_id
        )
    )


@router.get('/{connection_id}/globals', response_model=List[List[Decimal]])
async def get_globals(
    session: AsyncSession = Depends(get_session),
    connection_id: str = Path(...),
    size: int = Query(1024, ge=0),
) -> List[List[Decimal]]:
    """
    Get global series from connection
    """
    return await __get_series(
        session,
        size,
        select([
            ConnectionGlobal.story_drift_angle,
            ConnectionGlobal.actuator_force,
        ])
        .where(ConnectionGlobal.connection_id == connection_id)
        .order_by(ConnectionGlobal.id),
        ConnectionGlobal.id
    )


@router.get('/{connection_id}/globals/csv',
            response_class=StreamingResponse)
async def get_global_csv(
    session: AsyncSession = Depends(get_session),
    connection_id: str = Path(...),
) -> StreamingResponse:
    """
    Get global csv from connection
    """
    filename = f'connection-global_{connection_id}.csv'
    return __get_csv_response(
        session,
        select([
            ConnectionGlobal.story_drift_angle,
            ConnectionGlobal.actuator_force,
        ])
        .where(ConnectionGlobal.connection_id == connection_id)
        .order_by(ConnectionGlobal.id),
        ['Total story drift angle (rad)', 'Force in the actuator (kN)'],
        filename,
    )


@router.get('/{connection_id}/panel-zones', response_model=List[List[Decimal]])
async def get_panel_zones(
    session: AsyncSession = Depends(get_session),
    connection_id: str = Path(...),
    size: int = Query(1024, ge=0),
) -> List[List[Decimal]]:
    """
    Get panel zone series from connection
    """
    return await __get_series(
        session,
        size,
        select([
            ConnectionPanelZone.shear_distortion,
            ConnectionPanelZone.shear_force,
        ])
        .where(ConnectionPanelZone.connection_id == connection_id)
        .order_by(ConnectionPanelZone.id),
        ConnectionPanelZone.id
    )


@router.get('/{connection_id}/panel-zones/csv',
            response_class=StreamingResponse)
async def get_panel_zones_csv(
    session: AsyncSession = Depends(get_session),
    connection_id: str = Path(...),
) -> StreamingResponse:
    """
    Get panel zone csv from connection
    """
    filename = f'connection-panel-zone_{connection_id}.csv'
    return __get_csv_response(
        session,
        select([
            ConnectionPanelZone.shear_distortion,
            ConnectionPanelZone.shear_force,
        ])
        .where(ConnectionPanelZone.connection_id == connection_id)
        .order_by(ConnectionPanelZone.id),
        ['Panel zone shear distortion (rad)', 'Panel zone shear force (kN)'],
        filename,
    )


async def __get_series(
        session: AsyncSession,
        size: int,
        statement: Select,
        id_column: Column[int]
) -> List[List[Decimal]]:
    if size > 0:
        count: int = await session.scalar(
            select(func.count()).select_from(statement)
        )
        if count == 0:
            return []
        if count > size:
            n = math.ceil(float(count) / float(size))
            statement = statement.where(func.mod(id_column, n) == 0)
    tuples = await session.execute(statement)
    return [[tuple[0], tuple[1]] for tuple in tuples]


def __get_where_clauses(query: Optional[str]) -> List[Any]:
    """
    Get where clauses
    """
    return [__get_where_clause(q)
            for q
            in query.split(';')
            ] if query else []


def __get_where_clause(query: str) -> Any:
    """
    Get where clause
    """
    if ':' not in query:
        return or_(*[column.cast(String).ilike(query)
                     for column
                     in Connection.__table__.columns])
    key, expression = query.split(':', 2)
    column: Column[Any] = Connection.__dict__[key]
    return __get_predicate(column, expression)


def __get_predicate(column: Column[Any], expression: str) -> Any:
    if '&' in expression:
        return and_(*[__get_predicate(column, e)
                      for e
                      in expression.split('&')])
    if ',' in expression:
        return column.in_(expression.split(','))
    if '<<' in expression:
        [min, max] = expression.split('<<', 2)
        return column.between(Decimal(min), Decimal(max))
    if expression.startswith('<'):
        return column < int(expression[1:])
    if expression.startswith('>'):
        return column > int(expression[1:])
    if isinstance(column.type, String):
        return column.ilike(expression)
    if isinstance(column.type, Integer):
        return column == int(expression)
    if isinstance(column.type, Numeric):
        return column == Decimal(expression)
    if isinstance(column.type, Boolean):
        return column == bool(strtobool(expression))
    return column == expression


def __format_value(value: Any):
    if isinstance(value, Decimal):
        return Decimal(f'{value.normalize():f}')
    return value


def __get_csv_response(
    session: AsyncSession,
    statement: Select,
    headers: List[str],
    filename: str,
) -> StreamingResponse:
    return StreamingResponse(
        __get_csv_stream(
            session,
            statement,
            headers,
        ),
        headers={
            HttpHeader.CONTENT_DISPOSITION.value: attachment(filename)
        },
        media_type=MediaType.CSV.value)


async def __get_csv_stream(
        session: AsyncSession,
        statement: Select,
        headers: List[str],
        partition_size=128,
        separator=','):
    yield separator.join(headers) + '\n'
    result = await session.stream(statement)
    async for partition in result.partitions(partition_size):
        for row in partition:
            yield separator.join(
                [str(__format_value(item))
                 for item
                 in row]
            ) + '\n'
