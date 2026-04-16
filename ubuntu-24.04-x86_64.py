from xinstaller.common import *
from xinstaller.recipes import *
from install_sv2v import install_sv2v
import argparse

def install(keep_logs: bool = False) -> None:
    prefix=shexpand("$HOME/.local/opt/hdlstuff")
    ctx = Context(prefix=prefix)

    install_sv2v(prefix)
    
    AptInstall(ctx, "utils", ["wget", "curl", "tar", "git", "parallel"])
    AptInstall(ctx, "cpp-stuff", ["g++", "gcc", "gdb", "ninja-build", "make"])
    AptInstall(ctx, "python3-stuff", ["python3", "python3-pip", "python3-venv", "python3-setuptools"])
    AptInstall(ctx, "gtkwave", ["gtkwave"])

    InstallSbtDebian(ctx)

    InstallCMake(ctx, "https://github.com/Kitware/CMake/releases/download/v4.0.2/cmake-4.0.2-linux-x86_64.sh")

    # add other boost dependencies
    InstallBoost(ctx, "https://github.com/boostorg/boost/releases/download/boost-1.87.0/boost-1.87.0-cmake.tar.gz")

    InstallFmt(ctx, "https://github.com/fmtlib/fmt/archive/refs/tags/11.1.4.tar.gz")

    InstallSystemC(ctx, "https://github.com/accellera-official/systemc/archive/refs/tags/3.0.1.tar.gz")

    AptInstall(ctx, "verilator-deps", [
        "git", "help2man", "perl", "python3", "make",
        "g++",  # Both compilers
        "libgz",  # Non-Ubuntu (ignore if gives error)
        "libfl2", "libfl-dev",  # Ubuntu only (ignore if gives error)
        "zlibc", "zlib1g", "zlib1g-dev",  # Ubuntu only (ignore if gives error)
        "ccache",  # If present at build, needed for run
        "mold",  # If present at build, needed for run
        "libgoogle-perftools-dev", "numactl",
        "perl-doc",
        "autoconf", "flex", "bison"
    ])
    InstallVerilator(ctx, "https://github.com/verilator/verilator/archive/refs/tags/v5.034.tar.gz")

    PythonCreateVenv(ctx)

    PythonPipInstallLocal(ctx, "hdlinfo_python", "repos/hdlinfo/python")
    PythonPipInstallLocal(ctx, "hdlscw_python", "repos/hdlscw/python")
    PythonPipInstallLocal(ctx, "hdlscw_python", "repos/hdlscw/python")
    PythonPipInstallLocal(ctx, "chext-test_python", "repos/chext-test/python")
    PythonPipInstallLocal(ctx, "sctlm_python", "repos/sctlm/python")

    PythonPipInstall(ctx, "plotting_stuff", ["numpy", "matplotlib"])

    CMakeLocal(ctx, "hdlscw_cpp", "repos/hdlscw/cpp", cmake_args=[
        "-DCMAKE_BUILD_TYPE=Release",
    ], cmake_install_mode="ABS_SYMLINK")

    CMakeLocal(ctx, "hdlstuff-hal", "repos/hdlstuff-hal", cmake_args=[
        "-DCMAKE_BUILD_TYPE=Release",
    ], cmake_install_mode="ABS_SYMLINK")

    CMakeLocal(ctx, "chext-test_cpp", "repos/chext-test/cpp", cmake_args=[
        "-DCMAKE_BUILD_TYPE=Release",
    ], cmake_install_mode="ABS_SYMLINK")

    CMakeLocal(ctx, "sctlm_cpp", "repos/sctlm/cpp", cmake_args=[
        "-DCMAKE_BUILD_TYPE=Release",
    ], cmake_install_mode="ABS_SYMLINK")

    SbtPublishLocal(ctx, "hdlinfo_scala", "repos/hdlinfo/scala")
    SbtPublishLocal(ctx, "chext_scala", "repos/chext")

    InstallFiles(ctx, "prefix/ubuntu", ["bin/activate-hdlstuff.sh"])

    ctx.run()
    ctx.log(f"Please activate the environment using: {ctx.prefix('bin/activate-hdlstuff.sh')}")
    # Only remove logs if keep_logs is False
    if not keep_logs:
        ctx.remove_logs()
    else:
        ctx.log("Note: Installation logs have been preserved.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="HDL Toolchain Installer")
    parser.add_argument(
        "--keep-logs", 
        action="store_true", 
        help="Do not delete the installation logs after completion (default: False)"
    )
    
    args = parser.parse_args()
    install(keep_logs=args.keep_logs)
