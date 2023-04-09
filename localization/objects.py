from collections import namedtuple


ResourceFileRelation = namedtuple(
    "ResourceFileRelation", "resource_id filepath filename"
)

Resource = namedtuple(
    "Resource", "resource_id name slug"
)
