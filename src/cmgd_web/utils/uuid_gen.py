#!/usr/bin/env python3
import uuid
from typing import List

BASE_UUID=uuid.UUID('00000000000000000000000000000000')

def uuid_from_srrs(srrs: List[str]) -> uuid:
    """convert a list of SRR/ERR/DRR strings to UUID

    To generalize the ID used to represent a sample,
    we use the UUID. In the case of samples derived from
    NCBI SRA, we use a sorted list of SRRS, space-separated
    to generate a Version 5 UUID. The base UUID is simply
    the `0` UUID. In practice, this code makes a reproducible
    UUID given the SRR accessions in a sample.

    Parameters
    ----------
    srrs: a list of str
        A list of accessions (ERRXXXXX, SRRXXXXXX, DRRXXXXX)

    Returns
    -------
    The str representation of the generated UUID

    Examples
    --------
    >>> from cmgd_web.metadata_cli import uuid_from_srrs
    >>> srrs = ['SRR000123','SRR000234'] #silly example
    >>> uuid_from_srrs(srrs)
    '71c421b8-6762-59e2-9d8a-f1d3d5d9a300'
    """
    res = uuid_from_string(' '.join(sorted(srrs)))
    return str(res)


def uuid_from_ncbi_accessions(srrs: str) -> uuid.UUID:
    """Convert a semicolon-separated (unsorted) ncbi accession list to uuid

    Parameters
    ----------
    srrs: str
        A semicolon-separated list like "SRR1234;SRR4567;ERR8347"

    Returns
    -------
    A `uuid.UUID` object

    Examples
    --------
    >>> from cmgd_web.metadata_cli import uuid_from_ncbi_accessions
    >>> srrs =  "SRR1234;SRR4567;ERR8347"
    >>> uuid_from_ncbi_accessions(srrs)

    """
    res = uuid_from_string(sorted(srrs.split(';')))
    return res


def uuid_from_string(string: str) -> uuid:
    """Generate a uuid from a string

    Given a string, generate a Version 5 UUID from
    it.

    Parameters
    ----------
    string: str

    Returns
    -------
    A formal `uuid.UUID`

    Examples
    --------
    >>> from cmgd_web.utils.uuid_gen import uuid_from_string
    >>> string = 'this is a test'
    >>> uuid_from_string(string)
    UUID('d02800cf-ac56-5706-bd34-a7a767047731')
    """
    res = uuid.uuid5(BASE_UUID,string)
    return res
