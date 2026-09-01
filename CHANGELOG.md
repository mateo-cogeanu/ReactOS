# Changelog

This changelog documents the experimental AMD64/UEFI/AHCI/WoW64/icon work in
this fork. It does not replace the complete upstream ReactOS Git history. All
timestamps below are Git author timestamps in Europe/Prague local time
(`UTC+02:00` during CEST and `UTC+01:00` during CET), unless a test event is
explicitly described instead.

For exact attribution and the full upstream history, use `git log`, consult
[`CREDITS`](CREDITS), and visit the
[official ReactOS repository](https://github.com/reactos/reactos).

## Unreleased — UEFI Setup framebuffer console

- 2026-09-01, after 17:25 CEST — Diagnosed corrupted UEFI text Setup output.
  `blue.sys` writes 80×50 character/attribute cells to legacy VGA memory at
  physical address `0xB8000`, while pure UEFI retains a 640×480×32 GOP linear
  framebuffer at `0x80000000`. This mismatch explains the colored top scanline,
  clipped text, and white rectangles.
- A framebuffer-backed `blue.sys` implementation was started locally, but it
  remains uncommitted and unvalidated. It is intentionally excluded from the
  completed feature list and from the documentation commit.

## 2026-09-01 — Integrated AMD64 + WoW64 build

### Integration and build-system fixes

- **16:51:19** — `69041a9f3` — Merged current ReactOS master into Marcin
  Jabłoński's WoW64 synchronization branch. Conflict resolution retained both
  current upstream changes and the experimental compatibility layer.
- **16:51:58** — `2e5c54a5e` — Added integrated SysWOW64 building on Unix-like
  hosts. The AMD64 build can orchestrate the subordinate i386 payload build.
- **16:52:25** — `f2ccaf06f` — Preserved full-width symbol pointers in DBGHELP
  when the host compiler itself runs on ARM64.
- **16:53:17** — `811b3363e` — Retained explicit client IDs required by WoW64
  TEB layouts.
- **17:03:28** — `a3e16952c` — Synchronized GDI thunk argument types in
  `wow64win`.
- **17:04:07** — `90b5ca441` — Made native pointer conversion helpers type-safe.
- **17:04:33** — `ba71a713f` — Corrected CSR captured-string pointer conversion.
- **17:05:31** — `e05323e13` — Synchronized object and USER thunk types.
- **17:06:28** — `fc8936519` — Enabled the integrated WoW64 payload by default
  for AMD64 and serialized CAB generation after the i386 payload, fixing a
  Ninja packaging race.
- **17:11:37** — `9d3492b42` — Fixed misleading indentation in the NETCFGX
  parameter parser exposed by the stricter integrated build.
- **17:12:50** — `791dcf91e` — Preserved native AppBar handle width in SHELL32.
- **17:13:56** — `1ec530456` — Widened native addresses through pointer-sized
  integers in WoW64 conversion paths.
- **17:14:45** — `40f5e97ed` — Converted the shared USER32 menu bitmap through
  the WoW64 pointer helper.
- **17:15:46** — `5f49deba2` — Kept kernel-debugging and boot-video DLLs native
  only instead of incorrectly duplicating them into SysWOW64.

### Build result

- **17:17 CEST** — Completed the full integrated AMD64 build and subordinate
  i386 SysWOW64 build. Produced a 1.0 GiB boot ISO.
- Output name:
  `reactos-amd64-uefi-ahci-wow64-modern-icons-2026-09-01.iso`
- SHA-256:
  `345bd42088e78a83e430a02995aca6387256f34fa96ee91062abca36cc758e8e`
- Confirmed native PE32+ AMD64 binaries: `ntoskrnl.exe`, native `ntdll.dll`,
  `wow64.dll`, and `wow64win.dll`.
- Confirmed PE32 i386 SysWOW64 binaries: `ntdll.dll`, `kernel32.dll`,
  `user32.dll`, `gdi32.dll`, and `cmd.exe`.
- Confirmed 720 i386 files assigned to SysWOW64 in the generated installation
  manifest.
- Confirmed AMD64 `uefildr.efi` and `EFI/BOOT/BOOTX64.EFI` in the EFI image.

### VM validation

- Booted under QEMU 11.0.3 using `q35`, TCG `x86_64`, UEFI pflash, an AHCI/SATA
  disk, and an AHCI/SATA CD-ROM.
- UEFI loaded FreeLoader from the SATA optical path and printed
  `UEFI EntryPoint: Starting freeldr from UEFI`.
- The AMD64 kernel booted, the SATA stack initialized, and the empty SATA test
  disk was detected.
- LiveCD reached Winlogon but terminated the critical process shortly after
  loading `kbdus.dll` (`KiRaiseException` returned `0xc000000d`).
- Repeated the same test with the previous non-WoW64 AMD64 modern-icon ISO; it
  failed at the same Winlogon point. This A/B result indicates that the observed
  LiveCD failure predates the integrated SysWOW64 payload.
- Setup boot confirmed source paths `\Device\CdRom0\amd64` and
  `\Device\CdRom0`.
- Unattended first-stage Setup detected the UEFI fixed disk, formatted its FAT32
  partition, copied the system, and installed
  `EFI\BOOT\BOOTX64.EFI` to the SATA disk.
- Full 32-bit application execution remains unverified because subsequent AMD64
  startup/registry issues prevent reaching a dependable installed desktop.

## 2026-08-31 to 2026-09-01 — Modern shell icons

- **2026-08-31 16:13:25 CEST** — `6ceab154d` — Added original modernized,
  high-visibility shell icons generated from geometric primitives. No Microsoft
  Windows icons were extracted or redistributed.
- **2026-09-01 11:49:09 CEST** — `8f22c381b` — Refined icon geometry and small
  sizes, and added a conservative PE resource-transplant tool for patching only
  selected icon groups in a disposable VM image.
- Generated ICO resources include 16, 24, 32, 48, and 64 pixel 32-bit RGBA
  representations for selected shell, Explorer, Command Prompt, and Applications
  Manager resources.

## 2026-08-31 — AMD64 UEFI installation and toolchain compatibility

- **10:55:40 CEST** — `dde1c9271` — Added AMD64 UEFI installation support,
  including copying the removable-media loader as `EFI/BOOT/BOOTX64.EFI` to the
  system partition and using the appropriate UEFI disk path.
- **10:55:56 CEST** — `94049773b` — Fixed AMD64 compilation with modern MinGW
  toolchains.

## 2026-08-26 — Modern firmware and SATA robustness

- **20:48:34 CEST** — `5efa7a746` — Improved AMD64 UEFI and PCIIDEX behavior
  for modern firmware and SATA controllers. Changes cover safer PCI discovery,
  storage-controller setup, and modern firmware assumptions.
- **20:49:20 CEST** — `f5e36477d` — Packed ACPI MCFG structures correctly on
  AMD64 so firmware PCI configuration data is interpreted with the expected
  layout.
- **20:49:55 CEST** — `24fabeb09` — Prevented UEFI FreeLoader from probing
  legacy PCI interrupt-routing memory that is not valid on pure UEFI systems.

## 2026-08-02 to 2026-08-05 — UEFI PCI enumeration foundation

These commits are authored by **Alex Mendoza** and retained with their original
authorship. They form the UEFI PCI discovery foundation used by this branch.

- **2026-08-02 20:01:43 CEST** — `186bfbdca` — Implemented PCI bus detection in
  UEFI FreeLoader.
- **2026-08-03 00:29:53 CEST** — `256199105` — Preferred ACPI MCFG for PCI bus
  count detection.
- **2026-08-03 01:07:09 CEST** — `ad2d683e8` — Follow-up build correction.
- **2026-08-03 13:07:01 CEST** — `c2f8a0b7b` — Moved common PCI helpers to
  `hwpci.c` for UEFI and i386 reuse.
- **2026-08-03 14:48:23 CEST** — `03bcf11ca` — Formatting/indentation cleanup.
- **2026-08-03 14:48:37 CEST** — `28b38a9b6` — Additional indentation cleanup.
- **2026-08-05 20:08:52 CEST** — `2ffd9fede` — Corrected `FIELD_OFFSET` use.
- **2026-08-05 20:10:56 CEST** — `e5fbd3c5f` — Tightened the FreeLoader loop
  bound.

## 2025-01-13 to 2026-08-19 — WoW64 foundation

This body of work is authored primarily by **Marcin Jabłoński** on the
experimental `wow64sync` line. This fork integrates and builds upon it; the
original commits and authorship are preserved in Git.

### 2025-01 to 2025-03 — Runtime bootstrap

- **2025-01-13 02:36:29 CET** — `d47fdc292` — Initial ReactOS WoW64 commit.
- January 19–22 — Ported Wine-backed system, registry, virtual-memory,
  synchronization, file, and syscall components.
- January 26–30 — Added mixed-width console structures, moved initialization
  into `wow64.dll`, and implemented WoW64 DLL loading from NTDLL.
- February 1–7 — Removed a hard-coded program entry point, corrected console
  allocation, split process/thread initialization, and invoked per-thread
  WoW64 loader initialization.
- **2025-03-06 16:22:42 CET** — `1bcc925c2` — Initial `wow64win` commit for
  thunking USER/GDI kernel calls.

### 2025-04 to 2025-08 — Syscalls, exceptions, I/O, GUI, and networking

- April 3–12 — Expanded Win32k/USER/GDI syscall wrappers, filesystem
  redirection, message handling, button rendering, and initial exception
  support for 32-bit programs.
- April 13–21 — Added asynchronous I/O support, kernel-managed PEB32/TEB32
  allocation, an i386 WoW64 build sub-architecture, APC handling, Task Manager
  improvements, `IoIs32bitProcess`, and `NtCreateProcess(Ex)` support.
- April 22–30 — Added message-call wrappers, build guards, security wrappers,
  clipboard support, system-information conversion fixes, and CSR cleanup.
- May 3 — Imported/adapted the Wine WoW64 specification and corrected temporary
  allocation behavior.
- July 17–August 4 — Added PEB32 version data, improved WndProc translation,
  I/O status handling, filesystem-redirection control, and initial WoW64
  networking through AFD/TCPIP.

### 2025-10 to 2026-03 — Process creation and application compatibility

- October–November 2025 — Adapted AFD select behavior and reworked entry-point
  translation.
- December 2025 — Implemented dynamic system-root resolution and entry-point
  fixups; improved 32/64-bit process creation, synchronization behavior,
  Firefox rendering paths, Task Manager, comboboxes, and security wrappers.
- January–March 2026 — Added further USER/GDI wrappers, corrected AFD select,
  enlarged codepage buffers, and added `NtQueryInformationThread` wrappers.

### 2026-07 to 2026-08 — Synchronization and integrated SysWOW64 preparation

- **2026-07-30 22:13:15 CEST** — `f25f09725` — Finished a major synchronization
  with then-current ReactOS master.
- August 8–13 — Added Windows and Unix-hosted subordinate i386 build support,
  SysWOW64 CD/CAB population, CMake exclusions for native-only components,
  `spec2def` WoW64 modes, shared thunk code, CSR wrappers, and MinGW fixes.
- August 13–14 — Corrected USER class handling, kernel-debugger prompts, and
  numerous CSR/console issues.
- August 19 — Corrected icon information, filesystem-redirection flag meaning,
  common-control WndProc returns, and applied a temporary Win32k IME heap fix.
- **2026-08-19 15:14:18 CEST** — `7b47770a1` — Last WoW64 synchronization
  commit before the current ReactOS master merge.

## Upstream ReactOS history

The upstream project predates and vastly exceeds the experimental work listed
above. This repository deliberately preserves that history rather than copying
thousands of upstream entries into this file. Use:

```sh
git log --date=iso --format=fuller
git shortlog -sne --all
```

The Git history currently contains at least 136 distinct author identity
records, in addition to organizations and third-party projects represented by
component-local notices. [`CREDITS`](CREDITS) is also retained unchanged.

## Status vocabulary

- **Built** means compilation and packaging completed without an error.
- **Inspected** means the resulting file type or ISO manifest was examined.
- **Booted** means execution reached the explicitly stated boot milestone.
- **Verified** is never intended to imply complete hardware compatibility.
- Anything described as **unverified**, **experimental**, or **in development**
  must not be represented as production-ready functionality.
