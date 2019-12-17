from conans import ConanFile, tools, CMake
import os


class Live555Conan(ConanFile):
    name = "live555"
    package_revision = ""
    upstream_version = "1.22.0"
    version = "{0}{1}".format(upstream_version, package_revision)
    generators = "cmake"
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False]}
    default_options = "shared=True"
    url = "https://git.ircad.fr/conan/conan-live555"
    license = "GNU LGPL"
    description = "Multimedia streaming library, using open standard protocols (RTP/RTCP, RTSP, SIP)"
    source_subfolder = "source_subfolder"
    build_subfolder = "build_subfolder"

    def requirements(self):
        self.requires("common/1.0.2@sight/stable")
        if not tools.os_info.is_linux:
            self.requires("openssl/1.1.1b-r3@sight/stable")

    def source(self):
        live666_hash = "ebb28604c30a68bac49c5643b962b72344ccd409"
        tools.get("https://github.com/greenjava/live666/archive/{}.tar.gz".format(live666_hash))
        os.rename("live666-" + live666_hash, self.source_subfolder)

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
        cmake.definitions["WITH_SSL"] = "ON"
        if not tools.os_info.is_windows:
            cmake.definitions["CMAKE_POSITION_INDEPENDENT_CODE"] = "ON"

        cmake.configure()
        cmake.build()
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
