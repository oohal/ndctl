---
title: ndctl
layout: pmdk
---

NAME
====

ndctl-inject-error - inject media errors at a namespace offset

SYNOPSIS
========

>     ndctl inject-error <namespace> [<options>]

DESCRIPTION
===========

A REGION, after resolving DPA aliasing and LABEL specified boundaries, surfaces one or more "namespace" devices. The arrival of a "namespace" device currently triggers either the nd\_blk or nd\_pmem driver to load and register a disk/block device.

ndctl-inject-error can be used to ask the platform to simulate media errors in the NVDIMM address space to aid debugging and development of features related to error handling.

> **Warning**
>
> These commands are DANGEROUS and can cause data loss. They are only provided for testing and debugging purposes.

EXAMPLES
========

Inject errors in namespace0.0 at block 12 for 2 blocks (i.e. 12, 13)

>     ndctl inject-error --block=12 --count=2 namespace0.0

Check status of injected errors on namespace0.0

>     ndctl inject-error --status namespace0.0

Uninject errors at block 12 for 2 blocks on namespace0.0

>     ndctl inject-error --uninject --block=12 --count=2 namespace0.0

OPTIONS
=======

`-B; --block=`  
Namespace block offset in 512 byte sized blocks where the error is to be injected.

    NOTE: The offset is interpreted in different ways based on the "mode"
    of the namespace. For "raw" mode, the offset is the base namespace
    offset. For "memory" mode (i.e. a "pfn" namespace), the offset is
    relative to the user-visible part of the namespace, and the offset
    introduced by the kernel's metadata will be accounted for. For a
    "sector" mode namespace (i.e. a "BTT" namespace), the offset is
    relative to the base namespace, as the BTT translation details are
    internal to the kernel, and can't be accounted for while injecting
    errors.

`-n; --count=`  
Number of blocks to inject as errors. This is also in terms of fixed, 512 byte blocks.

`-d; --uninject`  
This option will ask the platform to remove any injected errors for the specified block offset, and count.

    WARNING: This will not clear the kernel's internal badblock tracking,
    those can only be cleared by doing a write to the affected locations.
    Hence use the --clear option only if you know exactly what you are
    doing. For normal usage, injected errors should only be cleared by
    doing writes. Do not expect have the original data intact after
    injecting an error, and clearing it using --clear - it will be lost,
    as the only "real" way to clear the error location is to write to it
    or zero it (truncate/hole-punch).

`-t; --status`  
This option will retrieve the status of injected errors. Note that this will not retrieve all known/latent errors (i.e. non injected ones), and is NOT equivalent to performing an Address Range Scrub.

`-N; --no-notify`  
This option is only valid when injecting errors. By default, the error inject command and will ask platform firmware to trigger a notification in the kernel, asking it to update its state of known errors. With this option, the error will still be injected, the kernel will not get a notification, and the error will appear as a latent media error when the location is accessed. If the platform firmware does not support this feature, this will have no effect.

`-v; --verbose`  
Emit debug messages for the error injection process

`-u; --human`  
Format numbers representing storage sizes, or offsets as human readable strings with units instead of the default machine-friendly raw-integer data. Convert other numeric fields into hexadecimal strings.

`-r; --region=`  
A *regionX* device name, or a region id number. The keyword *all* can be specified to carry out the operation on every region in the system, optionally filtered by bus id (see --bus= option).

`-b; --bus=`  
Enforce that the operation only be carried on devices that are attached to the given bus. Where *bus* can be a provider name or a bus id number.

COPYRIGHT
=========

Copyright (c) 2016 - 2017, Intel Corporation. License GPLv2: GNU GPL version 2 <http://gnu.org/licenses/gpl.html>. This is free software: you are free to change and redistribute it. There is NO WARRANTY, to the extent permitted by law.

SEE ALSO
========

[ndctl-list](ndctl-list.md),