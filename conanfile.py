from conans import ConanFile, tools, CMake
import os
import shutil


class Live555Conan(ConanFile):
    name = "live555"
    package_revision = "-r3"
    upstream_version = "1.21.0"
    version = "{0}{1}".format(upstream_version, package_revision)
    generators = "cmake"
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False]}
    default_options = "shared=True"
    url = "https://git.ircad.fr/conan/conan-live555"
    license = "GNU LGPL"
    exports = [
        "patches/CMakeProjectWrapper.txt"
    ]
    description = "Multimedia streaming library, using open standard protocols (RTP/RTCP, RTSP, SIP)"
    source_subfolder = "source_subfolder"
    build_subfolder = "build_subfolder"

    def requirements(self):
        self.requires("common/1.0.1@sight/testing")

    def source(self):
        tools.get("https://github.com/MobotixAG/live666/archive/releases/{0}.tar.gz".format(self.upstream_version))
        os.rename("live666-releases-" + self.upstream_version, self.source_subfolder)

    def build(self):
        # Import common flags and defines
        import common

        shutil.move("patches/CMakeProjectWrapper.txt", "CMakeLists.txt")
        cmake = CMake(self)

        # Export common flags
        cmake.definitions["SIGHT_CMAKE_CXX_FLAGS"] = common.get_cxx_flags()
        cmake.definitions["SIGHT_CMAKE_CXX_FLAGS_RELEASE"] = common.get_cxx_flags_release()
        cmake.definitions["SIGHT_CMAKE_CXX_FLAGS_DEBUG"] = common.get_cxx_flags_debug()
        cmake.definitions["SIGHT_CMAKE_CXX_FLAGS_RELWITHDEBINFO"] = common.get_cxx_flags_relwithdebinfo()

        cmake.configure(build_folder=self.build_subfolder)
        if not tools.os_info.is_windows:
            cmake.definitions["CMAKE_POSITION_INDEPENDENT_CODE"] = "ON"
        cmake.build()
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
