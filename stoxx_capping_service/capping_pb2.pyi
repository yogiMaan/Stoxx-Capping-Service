from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor
Methodology_CapFloor: Methodology
Methodology_Exposure: Methodology
Methodology_FactorLimiter: Methodology
Methodology_Fixed: Methodology
Methodology_Ladder: Methodology
Methodology_Multi: Methodology
Methodology_Regulatory: Methodology
NotEnoughComponentsBehaviour_Error: NotEnoughComponentsBehaviour
NotEnoughComponentsBehaviour_NotApplicable: NotEnoughComponentsBehaviour
NotEnoughComponentsBehaviour_OneOverN: NotEnoughComponentsBehaviour

class CapInput(_message.Message):
    __slots__ = ["mcapDecreasingFactors", "mcaps", "methodologyDatas", "parent_mcaps"]
    MCAPDECREASINGFACTORS_FIELD_NUMBER: _ClassVar[int]
    MCAPS_FIELD_NUMBER: _ClassVar[int]
    METHODOLOGYDATAS_FIELD_NUMBER: _ClassVar[int]
    PARENT_MCAPS_FIELD_NUMBER: _ClassVar[int]
    mcapDecreasingFactors: bool
    mcaps: _containers.RepeatedCompositeFieldContainer[Mcap]
    methodologyDatas: _containers.RepeatedCompositeFieldContainer[MethodologyData]
    parent_mcaps: _containers.RepeatedCompositeFieldContainer[Mcap]
    def __init__(self, methodologyDatas: _Optional[_Iterable[_Union[MethodologyData, _Mapping]]] = ..., parent_mcaps: _Optional[_Iterable[_Union[Mcap, _Mapping]]] = ..., mcaps: _Optional[_Iterable[_Union[Mcap, _Mapping]]] = ..., mcapDecreasingFactors: bool = ...) -> None: ...

class CapResult(_message.Message):
    __slots__ = ["capfactors"]
    CAPFACTORS_FIELD_NUMBER: _ClassVar[int]
    capfactors: _containers.RepeatedCompositeFieldContainer[Capfactor]
    def __init__(self, capfactors: _Optional[_Iterable[_Union[Capfactor, _Mapping]]] = ...) -> None: ...

class Capfactor(_message.Message):
    __slots__ = ["ConstituentID", "factor"]
    CONSTITUENTID_FIELD_NUMBER: _ClassVar[int]
    ConstituentID: str
    FACTOR_FIELD_NUMBER: _ClassVar[int]
    factor: float
    def __init__(self, ConstituentID: _Optional[str] = ..., factor: _Optional[float] = ...) -> None: ...

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
    __slots__ = ["limitInfos", "methodology", "notEnoughComponentsBehaviour"]
    LIMITINFOS_FIELD_NUMBER: _ClassVar[int]
    METHODOLOGY_FIELD_NUMBER: _ClassVar[int]
    NOTENOUGHCOMPONENTSBEHAVIOUR_FIELD_NUMBER: _ClassVar[int]
    limitInfos: _containers.RepeatedCompositeFieldContainer[LimitInfo]
    methodology: Methodology
    notEnoughComponentsBehaviour: NotEnoughComponentsBehaviour
    def __init__(self, methodology: _Optional[_Union[Methodology, str]] = ..., limitInfos: _Optional[_Iterable[_Union[LimitInfo, _Mapping]]] = ..., notEnoughComponentsBehaviour: _Optional[_Union[NotEnoughComponentsBehaviour, str]] = ...) -> None: ...

class NotEnoughComponentsBehaviour(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []

class Methodology(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
