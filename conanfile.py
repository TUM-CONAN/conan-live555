from conans import ConanFile, tools, CMake
import os


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
        self.requires("common/1.0.1@sight/stable")

    def source(self):
        tools.get("https://github.com/MobotixAG/live666/archive/releases/{0}.tar.gz".format(self.upstream_version))
        os.rename("live666-releases-" + self.upstream_version, self.source_subfolder)

    def build(self):
        # Import common flags and defines
        import common

        # Generate Cmake wrapper
        common.generate_cmake_wrapper(
            cmakelists_path='CMakeLists.txt',
            source_subfolder=self.source_subfolder,
            build_type=self.settings.build_type
        )

        cmake = CMake(self)

        if not tools.os_info.is_windows:
            cmake.definitions["CMAKE_POSITION_INDEPENDENT_CODE"] = "ON"

        cmake.configure()
        cmake.build()
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
