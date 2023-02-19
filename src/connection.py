"""
    This file will pertian to all thing connection related.
"""

# -- Imports
from enum import Enum



"""
    :name: ConnectionType
    :desc: An "enum" for the different connection types
    
    :play: A connection that is trying to ingest a stream
    :publish: A connection that is trying to publish a stream
"""
class ConnectionType(Enum):
    PLAY = 'play'
    PUBLISH = 'publish'

    def __str__(self) -> str:
        return self.name

    """
        :name: figure
        :desc: Figure out the ConnectionType from a string
               or from another ConnectionType instance
    """
    def figure(value):
        # -- If the value is already a ConnectionType, return it
        if isinstance(value, ConnectionType):
            return value

        # -- Loop through all the ConnectionTypes
        for connection_type in ConnectionType:
            if connection_type.name == value.upper():
                return connection_type

        # -- If theres no value, return the default
        return ConnectionType.PUBLISH


    
"""
    :name: Connection
    :desc: A class that represents a connection to the server
"""
class Connection:
    def __init__(
        self,
        connection_type: ConnectionType,
        client_id: str,
        address: str,
        app: str,
        secret: str
    ):
        self.connection_type = connection_type
        self.client_id = client_id
        self.address = address
        self.app = app
        self.secret = secret

    def __str__(self) -> str:
        return f'[{self.connection_type}] ID:{self.client_id} - {self.address} - {self.secret} - {self.app}'

    
    """
        :name: get_info
        :desc: Get the info for the connection from
               nginx-rtmp, eg bitrate, etc.
    """