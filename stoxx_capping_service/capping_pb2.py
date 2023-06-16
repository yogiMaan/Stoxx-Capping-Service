# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: capping.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\rcapping.proto\x12\x07\x63\x61pping\"(\n\x04Mcap\x12\x0c\n\x04mcap\x18\x01 \x01(\x01\x12\x12\n\ncomponents\x18\x02 \x03(\t\"@\n\tLimitInfo\x12\r\n\x05limit\x18\x01 \x01(\x01\x12\x16\n\tlimitName\x18\x02 \x01(\tH\x00\x88\x01\x01\x42\x0c\n\n_limitName\"\xd6\x01\n\x0fMethodologyData\x12&\n\nlimitInfos\x18\x01 \x03(\x0b\x32\x12.capping.LimitInfo\x12+\n\x1e\x61pplyLimitToNthLargestAndBelow\x18\x02 \x01(\x05H\x00\x88\x01\x01\x12K\n\x1cnotEnoughComponentsBehaviour\x18\x03 \x01(\x0e\x32%.capping.NotEnoughComponentsBehaviourB!\n\x1f_applyLimitToNthLargestAndBelow\"\xa6\x01\n\x08\x43\x61pInput\x12)\n\x0bmethodology\x18\x01 \x01(\x0e\x32\x14.capping.Methodology\x12\x32\n\x10methodologyDatas\x18\x02 \x03(\x0b\x32\x18.capping.MethodologyData\x12\x1c\n\x05mcaps\x18\x03 \x03(\x0b\x32\r.capping.Mcap\x12\x1d\n\x15mcapDecreasingFactors\x18\x04 \x01(\x08\"\"\n\tCapResult\x12\x15\n\rCappingFactor\x18\x01 \x03(\x01*\xa1\x01\n\x1cNotEnoughComponentsBehaviour\x12&\n\"NotEnoughComponentsBehaviour_Error\x10\x00\x12)\n%NotEnoughComponentsBehaviour_OneOverN\x10\x01\x12.\n*NotEnoughComponentsBehaviour_NotApplicable\x10\x02*\xa3\x01\n\x0bMethodology\x12\x15\n\x11Methodology_Fixed\x10\x00\x12\x15\n\x11Methodology_Multi\x10\x01\x12\x16\n\x12Methodology_Ladder\x10\x02\x12\x1a\n\x16Methodology_Regulatory\x10\x03\x12\x18\n\x14Methodology_Exposure\x10\x04\x12\x18\n\x14Methodology_CapFloor\x10\x05\x32\x39\n\x07\x43\x61pping\x12.\n\x03\x43\x61p\x12\x11.capping.CapInput\x1a\x12.capping.CapResult\"\x00\x42\x16\x42\x0c\x43\x61ppingProtoP\x01\xa2\x02\x03\x43\x41Pb\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'capping_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'B\014CappingProtoP\001\242\002\003CAP'
  _NOTENOUGHCOMPONENTSBEHAVIOUR._serialized_start=557
  _NOTENOUGHCOMPONENTSBEHAVIOUR._serialized_end=718
  _METHODOLOGY._serialized_start=721
  _METHODOLOGY._serialized_end=884
  _MCAP._serialized_start=26
  _MCAP._serialized_end=66
  _LIMITINFO._serialized_start=68
  _LIMITINFO._serialized_end=132
  _METHODOLOGYDATA._serialized_start=135
  _METHODOLOGYDATA._serialized_end=349
  _CAPINPUT._serialized_start=352
  _CAPINPUT._serialized_end=518
  _CAPRESULT._serialized_start=520
  _CAPRESULT._serialized_end=554
  _CAPPING._serialized_start=886
  _CAPPING._serialized_end=943
# @@protoc_insertion_point(module_scope)
