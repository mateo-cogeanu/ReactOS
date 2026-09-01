#!/usr/bin/env python3
"""Patch selected PE icon groups without replacing code or other resources.

The installed binary remains the base. Icon image and group payloads from a
newly built donor are appended in a new read-only data section, then only the
matching RT_ICON and RT_GROUP_ICON data entries in the installed resource tree
are redirected to those payloads. This is useful when the donor was built from
a source tree that is not ABI-compatible with an older installation.
"""

import argparse
import hashlib
from pathlib import Path
import struct

import pefile


RT_ICON = 3
RT_GROUP_ICON = 14
SECTION_CHARACTERISTICS = 0x40000040  # initialized data, readable
GROUP_HEADER = struct.Struct("<HHH")
GROUP_ENTRY = struct.Struct("<BBBBHHIH")


def align(value, alignment):
    return (value + alignment - 1) & ~(alignment - 1)


def numeric_id(entry):
    if entry.name is not None:
        return str(entry.name)
    return entry.id


def resource_map(pe):
    """Return {(type, name, language): IMAGE_RESOURCE_DATA_ENTRY}."""
    result = {}
    root = getattr(pe, "DIRECTORY_ENTRY_RESOURCE", None)
    if root is None:
        return result
    for type_entry in root.entries:
        if not hasattr(type_entry, "directory"):
            continue
        for name_entry in type_entry.directory.entries:
            if not hasattr(name_entry, "directory"):
                continue
            for lang_entry in name_entry.directory.entries:
                if not hasattr(lang_entry, "data"):
                    continue
                key = (
                    numeric_id(type_entry),
                    numeric_id(name_entry),
                    numeric_id(lang_entry),
                )
                result[key] = lang_entry.data.struct
    return result


def resource_bytes(pe, leaf):
    return pe.get_data(leaf.OffsetToData, leaf.Size)


def find_leaf(resources, resource_type, resource_id, language):
    exact = resources.get((resource_type, resource_id, language))
    if exact is not None:
        return exact
    matches = [
        leaf
        for (kind, name, _lang), leaf in resources.items()
        if kind == resource_type and name == resource_id
    ]
    if len(matches) != 1:
        raise ValueError(
            f"cannot uniquely resolve resource {resource_type}/{resource_id} "
            f"for language {language}"
        )
    return matches[0]


def parse_group(data):
    if len(data) < GROUP_HEADER.size:
        raise ValueError("truncated icon group")
    reserved, kind, count = GROUP_HEADER.unpack_from(data)
    if reserved != 0 or kind != 1:
        raise ValueError("resource is not an icon group")
    expected = GROUP_HEADER.size + count * GROUP_ENTRY.size
    if len(data) < expected:
        raise ValueError("truncated icon group entries")
    return [
        GROUP_ENTRY.unpack_from(data, GROUP_HEADER.size + index * GROUP_ENTRY.size)
        for index in range(count)
    ]


def dimension(value):
    return 256 if value == 0 else value


def choose_frame(target_entry, donor_entries):
    target_width = dimension(target_entry[0])
    target_height = dimension(target_entry[1])

    def score(entry):
        width = dimension(entry[0])
        height = dimension(entry[1])
        exact = width == target_width and height == target_height
        distance = abs(width - target_width) + abs(height - target_height)
        depth_penalty = -entry[5]
        return (not exact, distance, depth_penalty)

    return min(donor_entries, key=score)


def section_named(pe, name):
    wanted = name.encode("ascii")
    for section in pe.sections:
        if section.Name.rstrip(b"\0") == wanted:
            return section
    raise ValueError(f"PE file has no {name} section")


def imported_symbols(pe):
    result = []
    for descriptor in getattr(pe, "DIRECTORY_ENTRY_IMPORT", []):
        symbols = tuple(
            imported.name or f"#{imported.ordinal}".encode()
            for imported in descriptor.imports
        )
        result.append((descriptor.dll.lower(), symbols))
    return tuple(result)


def text_hash(pe):
    return hashlib.sha256(section_named(pe, ".text").get_data()).hexdigest()


def append_payload(payload, data):
    offset = align(len(payload), 4)
    payload.extend(b"\0" * (offset - len(payload)))
    payload.extend(data)
    return offset


def patch_icons(target_path, donor_path, output_path, group_ids):
    target = pefile.PE(str(target_path))
    donor = pefile.PE(str(donor_path))
    if target.FILE_HEADER.Machine != donor.FILE_HEADER.Machine:
        raise ValueError("target and donor machine architectures differ")

    target_resources = resource_map(target)
    donor_resources = resource_map(donor)
    output = bytearray(target_path.read_bytes())
    payload = bytearray()
    redirects = {}
    groups_patched = 0

    for group_id in group_ids:
        target_groups = [
            (key, leaf)
            for key, leaf in target_resources.items()
            if key[0] == RT_GROUP_ICON and key[1] == group_id
        ]
        donor_groups = [
            (key, leaf)
            for key, leaf in donor_resources.items()
            if key[0] == RT_GROUP_ICON and key[1] == group_id
        ]
        if not target_groups:
            raise ValueError(f"target has no icon group {group_id}")
        if not donor_groups:
            raise ValueError(f"donor has no icon group {group_id}")

        for target_key, target_group_leaf in target_groups:
            target_language = target_key[2]
            donor_key, donor_group_leaf = min(
                donor_groups, key=lambda item: item[0][2] != target_language
            )
            donor_language = donor_key[2]
            target_entries = parse_group(resource_bytes(target, target_group_leaf))
            donor_entries = parse_group(resource_bytes(donor, donor_group_leaf))
            new_group = bytearray(GROUP_HEADER.pack(0, 1, len(target_entries)))

            for target_entry in target_entries:
                donor_entry = choose_frame(target_entry, donor_entries)
                target_icon_id = target_entry[7]
                donor_icon_id = donor_entry[7]
                target_icon_leaf = find_leaf(
                    target_resources, RT_ICON, target_icon_id, target_language
                )
                donor_icon_leaf = find_leaf(
                    donor_resources, RT_ICON, donor_icon_id, donor_language
                )
                donor_icon = resource_bytes(donor, donor_icon_leaf)
                redirect_key = target_icon_leaf.get_file_offset()
                previous = redirects.get(redirect_key)
                if previous is not None and previous[1] != donor_icon:
                    raise ValueError(
                        f"icon {target_icon_id} is shared by groups with "
                        "different replacement frames"
                    )
                if previous is None:
                    redirects[redirect_key] = (append_payload(payload, donor_icon), donor_icon)

                new_group.extend(
                    GROUP_ENTRY.pack(
                        donor_entry[0],
                        donor_entry[1],
                        donor_entry[2],
                        donor_entry[3],
                        donor_entry[4],
                        donor_entry[5],
                        len(donor_icon),
                        target_icon_id,
                    )
                )

            group_data = bytes(new_group)
            redirects[target_group_leaf.get_file_offset()] = (
                append_payload(payload, group_data),
                group_data,
            )
            groups_patched += 1

    file_alignment = target.OPTIONAL_HEADER.FileAlignment
    section_alignment = target.OPTIONAL_HEADER.SectionAlignment
    highest_end = max(
        section.VirtualAddress + max(section.Misc_VirtualSize, section.SizeOfRawData)
        for section in target.sections
    )
    new_rva = align(highest_end, section_alignment)
    raw_offset = align(len(output), file_alignment)
    raw_size = align(len(payload), file_alignment)

    section_header_offset = (
        target.sections[-1].get_file_offset() + 40
    )
    first_raw_offset = min(
        section.PointerToRawData
        for section in target.sections
        if section.PointerToRawData
    )
    if section_header_offset + 40 > first_raw_offset:
        raise ValueError("PE headers have no room for another section")

    output.extend(b"\0" * (raw_offset - len(output)))
    output.extend(payload)
    output.extend(b"\0" * (raw_size - len(payload)))

    for data_entry_offset, (payload_offset, data) in redirects.items():
        struct.pack_into("<II", output, data_entry_offset, new_rva + payload_offset, len(data))

    section_header = struct.pack(
        "<8sIIIIIIHHI",
        b".rosico\0",
        len(payload),
        new_rva,
        raw_size,
        raw_offset,
        0,
        0,
        0,
        0,
        SECTION_CHARACTERISTICS,
    )
    output[section_header_offset : section_header_offset + 40] = section_header
    struct.pack_into(
        "<H",
        output,
        target.FILE_HEADER.get_field_absolute_offset("NumberOfSections"),
        target.FILE_HEADER.NumberOfSections + 1,
    )
    struct.pack_into(
        "<I",
        output,
        target.OPTIONAL_HEADER.get_field_absolute_offset("SizeOfImage"),
        align(new_rva + len(payload), section_alignment),
    )
    struct.pack_into(
        "<I",
        output,
        target.OPTIONAL_HEADER.get_field_absolute_offset("CheckSum"),
        0,
    )
    output_path.write_bytes(output)

    patched = pefile.PE(str(output_path))
    if imported_symbols(patched) != imported_symbols(target):
        raise ValueError("patched import table differs from target")
    if text_hash(patched) != text_hash(target):
        raise ValueError("patched code section differs from target")
    new_section = section_named(patched, ".rosico")
    for data_entry_offset in redirects:
        rva, size = struct.unpack_from("<II", output, data_entry_offset)
        if not (
            new_section.VirtualAddress
            <= rva
            < new_section.VirtualAddress + new_section.Misc_VirtualSize
        ):
            raise ValueError("resource redirect does not point into .rosico")
        if size == 0:
            raise ValueError("resource redirect has zero size")

    print(
        f"{output_path}: patched {groups_patched} icon groups and "
        f"{len(redirects) - groups_patched} icon images; preserved target imports and .text"
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("target", type=Path, help="installed ABI-compatible PE")
    parser.add_argument("donor", type=Path, help="newly built PE providing icons")
    parser.add_argument("output", type=Path, help="patched output PE")
    parser.add_argument(
        "--group-id",
        type=int,
        action="append",
        required=True,
        dest="group_ids",
        help="numeric RT_GROUP_ICON ID to replace; may be repeated",
    )
    args = parser.parse_args()
    patch_icons(args.target, args.donor, args.output, args.group_ids)


if __name__ == "__main__":
    main()
