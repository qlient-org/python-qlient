"""This module contains the graphql constants."""
# Protocols
GRAPHQL_WS_PROTOCOL = "graphql-ws"
GRAPHQL_TRANSPORT_WS_PROTOCOL = "graphql-transport-ws"

# GQL Control Strings
CONNECTION_INIT = "connection_init"
CONNECTION_ACKNOWLEDGED = "connection_ack"
CONNECTION_ERROR = "connection_error"
CONNECTION_KEEP_ALIVE = "ka"
START = "start"
STOP = "stop"
CONNECTION_TERMINATE = "connection_terminate"
DATA = "data"
ERROR = "error"
COMPLETE = "complete"
