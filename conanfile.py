from conans import ConanFile, tools, CMake
import os


class Live555Conan(ConanFile):
    name = "live555"
    package_revision = ""
    upstream_version = "2022.01.11"
    version = "{0}{1}".format(upstream_version, package_revision)
    generators = "cmake"
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False]}
    default_options = "shared=True"
    url = "https://github.com/TUM-CONAN/conan-live555"
    license = "GNU LGPL"
    exports = ["patches/*",]
    description = "Multimedia streaming library, using open standard protocols (RTP/RTCP, RTSP, SIP)"
    source_subfolder = "source_subfolder"
    build_subfolder = "build_subfolder"

    def requirements(self):
        self.requires("ircad_common/1.0.2@camposs/stable")

    def source(self):
        tools.get("https://github.com/TUM-CAMP-NARVIS/live666/archive/refs/tags/{}.zip".format(self.upstream_version))
        os.rename("live666-" + self.upstream_version, self.source_subfolder)

    def build(self):
        # Import common flags and defines
        import common
        tools.patch(base_path=self.source_subfolder, patch_file='patches/increase_bank_size.patch')

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
        self.cpp_info.includedirs = ['include', 'include/live555/UsageEnvironment', 'include/live555/BasicUsageEnvironment', 'include/live555/groupsock', 'include/live555/liveMedia']
