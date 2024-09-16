"""The common errno and exceptions used in Region test."""
import enum


class ExceptionCode(enum.Enum):
  """The Rt's common exception code."""
  # common errno 10~999
  ERROR_PARTIAL = 9
  ERROR_INTERNAL = 10
  ERROR_INPUT = 11
  ERROR_ROUTE = 20
  ERROR_OPERATION = 30
  ERROR_PUSH = 40
  ERROR_DATALINK = 50
  ERROR_DATAMAP = 60
  ERROR_PERMISSION = 500


class RtException(Exception):
  """The Rt Exception is the base exception used in Rt, and we can not
  use it directly in our Rt code, please use sub-exception instead.
  """

  def __init__(self, code, msg, data=None):
    # type: (int, str, object) -> None
    Exception.__init__(self, msg)
    self._code = code
    self._msg = msg
    self._data = data

  @property
  def code(self):
    # type: () -> int
    """The code property of the exception."""
    return self._code

  def msg(self):
    # type: () -> str
    """The msg property of the exception."""
    return self._msg

  @property
  def data(self):
    # type: () -> object
    """The msg property of the exception."""
    return self._data

  def __str__(self):
    # type: () -> str
    return ("raise exception with code: %d and message: %s" % (self._code,
                                                               self._msg))


class InternalException(RtException):
  """Used when the internal error occurs."""

  def __init__(self, msg):
    RtException.__init__(self, code=ExceptionCode.ERROR_INTERNAL.value, msg=msg)


class InputException(RtException):
  """Used when the internal error occurs."""

  def __init__(self, msg):
    RtException.__init__(self, code=ExceptionCode.ERROR_INPUT.value, msg=msg)


class PermissionException(RtException):
  """Used when the internal error occurs."""

  def __init__(self, msg):
    RtException.__init__(
        self, code=ExceptionCode.ERROR_PERMISSION.value, msg=msg)


class RouteException(RtException):
  """Used when the route error occurs."""

  def __init__(self, msg):
    RtException.__init__(self, code=ExceptionCode.ERROR_ROUTE.value, msg=msg)


class OperationException(RtException):
  """Used when the operation error occurs."""

  def __init__(self, msg):
    RtException.__init__(
        self, code=ExceptionCode.ERROR_OPERATION.value, msg=msg)


class PushException(RtException):
  """Used when the operation error occurs."""

  def __init__(self, msg):
    RtException.__init__(self, code=ExceptionCode.ERROR_PUSH.value, msg=msg)


class DatalinkException(RtException):
  """Used when the operation error occurs."""

  def __init__(self, msg):
    RtException.__init__(self, code=ExceptionCode.ERROR_DATALINK.value, msg=msg)


class DatamapException(RtException):
  """Used when the operation error occurs."""

  def __init__(self, msg):
    RtException.__init__(self, code=ExceptionCode.ERROR_DATAMAP.value, msg=msg)


class PartialException(RtException):
  """部分异常, 仍然需要返回部分数据"""
  def __init__(self, msg, data):
    RtException.__init__(self, code=ExceptionCode.ERROR_PARTIAL.value, msg=msg, data=data)
