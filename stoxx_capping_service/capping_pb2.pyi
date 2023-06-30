from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor
Methodology_CapFloor: Methodology
Methodology_Exposure: Methodology
Methodology_Fixed: Methodology
Methodology_Ladder: Methodology
Methodology_Multi: Methodology
Methodology_Regulatory: Methodology
NotEnoughComponentsBehaviour_Error: NotEnoughComponentsBehaviour
NotEnoughComponentsBehaviour_NotApplicable: NotEnoughComponentsBehaviour
NotEnoughComponentsBehaviour_OneOverN: NotEnoughComponentsBehaviour

class CapInput(_message.Message):
    __slots__ = ["mcapDecreasingFactors", "mcaps", "methodology", "methodologyDatas"]
    MCAPDECREASINGFACTORS_FIELD_NUMBER: _ClassVar[int]
    MCAPS_FIELD_NUMBER: _ClassVar[int]
    METHODOLOGYDATAS_FIELD_NUMBER: _ClassVar[int]
    METHODOLOGY_FIELD_NUMBER: _ClassVar[int]
    mcapDecreasingFactors: bool
    mcaps: _containers.RepeatedCompositeFieldContainer[Mcap]
    methodology: Methodology
    methodologyDatas: _containers.RepeatedCompositeFieldContainer[MethodologyData]
    def __init__(self, methodology: _Optional[_Union[Methodology, str]] = ..., methodologyDatas: _Optional[_Iterable[_Union[MethodologyData, _Mapping]]] = ..., mcaps: _Optional[_Iterable[_Union[Mcap, _Mapping]]] = ..., mcapDecreasingFactors: bool = ...) -> None: ...

class CapResult(_message.Message):
    __slots__ = ["capfactors"]
    class CapfactorsEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: float
        def __init__(self, key: _Optional[str] = ..., value: _Optional[float] = ...) -> None: ...
    CAPFACTORS_FIELD_NUMBER: _ClassVar[int]
    capfactors: _containers.ScalarMap[str, float]
    def __init__(self, capfactors: _Optional[_Mapping[str, float]] = ...) -> None: ...

class LimitInfo(_message.Message):
    __slots__ = ["limit", "limitName"]
    LIMITNAME_FIELD_NUMBER: _ClassVar[int]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    limit: float
    limitName: str
    def __init__(self, limit: _Optional[float] = ..., limitName: _Optional[str] = ...) -> None: ...

class Mcap(_message.Message):
    __slots__ = ["ConstituentId", "components", "mcap"]
    COMPONENTS_FIELD_NUMBER: _ClassVar[int]
    CONSTITUENTID_FIELD_NUMBER: _ClassVar[int]
    ConstituentId: str
    MCAP_FIELD_NUMBER: _ClassVar[int]
    components: _containers.RepeatedScalarFieldContainer[str]
    mcap: float
    def __init__(self, mcap: _Optional[float] = ..., components: _Optional[_Iterable[str]] = ..., ConstituentId: _Optional[str] = ...) -> None: ...

class MethodologyData(_message.Message):
    __slots__ = ["applyLimitToNthLargestAndBelow", "limitInfos", "notEnoughComponentsBehaviour"]
    APPLYLIMITTONTHLARGESTANDBELOW_FIELD_NUMBER: _ClassVar[int]
    LIMITINFOS_FIELD_NUMBER: _ClassVar[int]
    NOTENOUGHCOMPONENTSBEHAVIOUR_FIELD_NUMBER: _ClassVar[int]
    applyLimitToNthLargestAndBelow: int
    limitInfos: _containers.RepeatedCompositeFieldContainer[LimitInfo]
    notEnoughComponentsBehaviour: NotEnoughComponentsBehaviour
    def __init__(self, limitInfos: _Optional[_Iterable[_Union[LimitInfo, _Mapping]]] = ..., applyLimitToNthLargestAndBelow: _Optional[int] = ..., notEnoughComponentsBehaviour: _Optional[_Union[NotEnoughComponentsBehaviour, str]] = ...) -> None: ...

class NotEnoughComponentsBehaviour(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []

class Methodology(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
