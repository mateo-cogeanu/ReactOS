# ReactOS AMD64 — UEFI, AHCI/SATA, WoW64, and modern shell icons

> [!IMPORTANT]
> This is an **experimental community development fork** of ReactOS. It is not
> an official ReactOS release, it is not supported by the ReactOS Project, and
> it is not ready for production use. Test it in a virtual machine or on a
> computer containing no valuable data.

This branch combines ongoing ReactOS AMD64 work with experimental UEFI boot,
modern AHCI/SATA compatibility work, an integrated i386 `SysWOW64` payload,
and original modernized shell icons. Its purpose is to make one reproducible
AMD64 research image for virtual-machine testing and eventual hardware testing.

Current development branch: `codex/amd64-wow64-sync`

## Attribution — please read this first

**ReactOS exists because of decades of work by the ReactOS Project and its
contributors. Nearly all of this repository is their work.** This fork is a
small experimental layer over that enormous upstream codebase; it must never
be represented as a new operating system written by this fork's maintainer or
by Codex.

Primary credit and upstream links:

- [The ReactOS Project](https://reactos.org/) and every past and present
  ReactOS contributor. The repository's preserved Git history is the most
  precise per-change attribution record.
- The historical names collected in [`CREDITS`](CREDITS), plus the many newer
  contributors visible in `git log` and the
  [ReactOS GitHub organization](https://github.com/reactos/reactos).
- [Marcin Jabłoński](https://github.com/TheNNX) for the experimental ReactOS
  WoW64 implementation and synchronization work that forms the foundation of
  the 32-on-64 compatibility layer in this branch.
- [Alex Mendoza](https://github.com/MuerteSeguraZ) for the UEFI FreeLoader PCI
  enumeration work incorporated into the modern firmware path.
- The [Wine Project](https://www.winehq.org/) and Wine contributors. ReactOS
  shares and adapts substantial user-mode compatibility code from Wine, and
  the experimental WoW64 work also ports/adapts Wine WoW64 components. Source
  headers and Git commits retain their applicable authorship and licenses.
- All upstream third-party projects whose code and data are distributed in
  ReactOS. Their copyright and license files remain beside the corresponding
  components throughout the tree.

The fork-specific integration commits are recorded in [`CHANGELOG.md`](CHANGELOG.md).
Copyright remains with the respective authors. No blanket claim of authorship
is made over upstream ReactOS, Wine, or third-party code.

## What this branch contains

- Native AMD64 ReactOS kernel and user-mode system.
- UEFI boot using an AMD64 `EFI/BOOT/BOOTX64.EFI` loader.
- UEFI installation support for copying the EFI loader to a FAT system
  partition.
- Improved FreeLoader PCI/ACPI enumeration and modern-firmware robustness.
- Improved PCI IDE/AHCI/SATA discovery and initialization for modern virtual
  and physical controllers.
- Experimental WoW64 runtime (`wow64.dll`, `wow64win.dll`, supporting NTDLL and
  kernel changes).
- An integrated i386 `SysWOW64` build generated together with the AMD64 image.
- Original, generated modern shell icons. These are inspired by contemporary
  interface design but are not extracted from Microsoft Windows.
- A resource-only VM patching utility for testing icon changes without
  replacing executable code.

## Current status

The combined build completes and produces a bootable ISO. The image has been
inspected to confirm this architecture split:

| Location/component | Architecture |
| --- | --- |
| `ntoskrnl.exe` | AMD64 / PE32+ |
| `System32/ntdll.dll` | AMD64 / PE32+ |
| `System32/wow64.dll` | AMD64 / PE32+ |
| `System32/wow64win.dll` | AMD64 / PE32+ |
| `SysWOW64/ntdll.dll` | i386 / PE32 |
| `SysWOW64/kernel32.dll` | i386 / PE32 |
| `SysWOW64/user32.dll` | i386 / PE32 |
| `SysWOW64/gdi32.dll` | i386 / PE32 |
| `SysWOW64/cmd.exe` | i386 / PE32 |
| `EFI/BOOT/BOOTX64.EFI` | AMD64 EFI application |

The inspected image contains 720 i386 payload entries assigned to SysWOW64.
UEFI boot and SATA CD/disk detection have been observed under QEMU `q35`.
First-stage Setup can format the SATA disk, copy the operating system, and
install `BOOTX64.EFI`.

### Known blockers

- Runtime execution of a 32-bit application through WoW64 is **not yet proven**.
- AMD64 LiveCD boot currently terminates Winlogon after loading `kbdus.dll`.
  An A/B test reproduced the same failure with the earlier non-WoW64 AMD64
  image, so it is not presently attributed to the SysWOW64 integration.
- Text-mode Setup's `blue.sys` still assumes legacy VGA text memory. Under
  pure UEFI/GOP this causes corrupted installer rendering. A framebuffer-backed
  console fix is in development but is deliberately not committed as complete.
- ReactOS AMD64, UEFI, AHCI and WoW64 support are all experimental. Hardware
  compatibility is neither complete nor guaranteed.

See [`CHANGELOG.md`](CHANGELOG.md) for the detailed timeline and test evidence.

## Building the experimental AMD64 image

Use an appropriate ReactOS Build Environment or a compatible cross-toolchain.
An out-of-tree build is strongly recommended.

```sh
mkdir reactos-build
cd reactos-build
../ReactOS/configure.sh -G Ninja -DARCH=amd64 -DCMAKE_BUILD_TYPE=Debug
ninja -j4 bootcd
```

On AMD64 this branch enables the integrated WoW64 payload. The native build
creates and consumes a subordinate i386 build for SysWOW64; do not separately
substitute an i386 boot image for the AMD64 output.

The bootable result is normally `bootcd.iso` in the build directory. Verify the
architectures of both `System32` and `SysWOW64` before distributing a result.

## Suggested VM configuration

- Architecture: emulated `x86_64`/AMD64, not ARM64 virtualization.
- Firmware: UEFI.
- Machine/chipset: QEMU `q35` or an equivalent modern PC model.
- Storage: SATA/AHCI disk and SATA/AHCI CD-ROM.
- Debugging: COM1 at 115200 baud when using a debug boot entry.
- Test disk: disposable and free of important data.

On Apple Silicon, UTM must use **Emulate** for this AMD64 guest. Native ARM64
virtualization cannot execute this x86-64 ReactOS image.

## Modern icon sources

The icon generator and its notes live in
[`media/graphics/modern_shell_icons`](media/graphics/modern_shell_icons/README.md).
The artwork is generated from geometric primitives and does not contain icons
extracted from Windows 10 or Windows 11.

## Licensing

ReactOS is primarily distributed under the GNU General Public License 2.0.
See [`COPYING`](COPYING), [`COPYING.LIB`](COPYING.LIB), [`COPYING3`](COPYING3),
[`COPYING3.LIB`](COPYING3.LIB), file headers, component-local license files,
and the preserved Git history. Some components use other compatible licenses;
their notices remain authoritative.

ReactOS is a registered trademark of the ReactOS Foundation. Microsoft and
Windows are trademarks of Microsoft Corporation. This fork is unaffiliated
with and not endorsed by Microsoft.

## Contributing and clean-room requirements

Follow [`CONTRIBUTING.md`](CONTRIBUTING.md) and the ReactOS clean-room rules.
Do not contribute code derived from leaked or proprietary Microsoft source.
When forwarding suitable fixes upstream, retain original authorship and explain
the test environment and experimental nature of the AMD64 path.

## Official ReactOS resources

- [Website](https://reactos.org/)
- [Official upstream source](https://github.com/reactos/reactos)
- [Build documentation](https://reactos.org/wiki/Building_ReactOS)
- [Wiki](https://reactos.org/wiki/)
- [Issue tracker](https://jira.reactos.org/)
- [Contributing](https://reactos.org/wiki/Commiting_Changes)
- [Donate to ReactOS](https://reactos.org/donate/)
