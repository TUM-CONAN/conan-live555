from conan import ConanFile
from conan.tools.cmake import CMake, CMakeToolchain, cmake_layout, CMakeDeps
from conan.tools.scm import Git
from conan.tools.files import load, update_conandata, copy, replace_in_file, collect_libs, patch
import os


class Live555Conan(ConanFile):

    name = "live555"
    package_revision = ""
    upstream_version = "2022.01.11"
    version = "{0}{1}".format(upstream_version, package_revision)

    description = "Multimedia streaming library, using open standard protocols (RTP/RTCP, RTSP, SIP)"
    url = "https://github.com/TUM-CONAN/conan-live555"
    license = "GNU LGPL"

    settings = "os", "arch", "compiler", "build_type"
    options = {
        "shared": [True, False],
    }
    default_options = {
        "shared": True,
    }

    exports = ["patches/*",]

    def export(self):
        update_conandata(self, {"sources": {
            "commit": "{}".format(self.version),
            "url": "https://github.com/TUM-CAMP-NARVIS/live666.git"
        }})

    def source(self):
        git = Git(self)
        sources = self.conan_data["sources"]
        git.clone(url=sources["url"], target=self.source_folder)
        git.checkout(commit=sources["commit"])

        patch(self, base_path=self.source_folder,
              patch_file=os.path.join(self.recipe_folder, "patches", "increase_bank_size.patch"))

    def generate(self):
        tc = CMakeToolchain(self)

        def add_cmake_option(option, value):
            var_name = "{}".format(option).upper()
            value_str = "{}".format(value)
            var_value = "ON" if value_str == 'True' else "OFF" if value_str == 'False' else value_str
            tc.variables[var_name] = var_value

        for option, value in self.options.items():
            add_cmake_option(option, value)

        tc.cache_variables["CMAKE_POSITION_INDEPENDENT_CODE"] = "ON"

        tc.generate()

        deps = CMakeDeps(self)
        deps.generate()

    def layout(self):
        cmake_layout(self, src_folder="source_folder")

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        cmake = CMake(self)
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = collect_libs(self)
        self.cpp_info.includedirs = ['include',
                                     'include/live555/UsageEnvironment',
                                     'include/live555/BasicUsageEnvironment', 'include/live555/groupsock', 'include/live555/liveMedia']
