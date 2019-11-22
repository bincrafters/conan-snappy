from conans import ConanFile, CMake, tools
import os


class SnappyConan(ConanFile):
    name = "snappy"
    version = "1.1.7"
    description = "A fast compressor/decompressor"
    topics = ("conan", "snappy", "google", "compressor", "decompressor")
    url = "https://github.com/bincrafters/conan-snappy"
    homepage = "https://github.com/google/snappy"
    license = "BSD-3-Clause"
    exports = ["LICENSE.md"]
    exports_sources = ["CMakeLists.txt"]
    generators = "cmake"
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}
    _source_subfolder = "source_subfolder"
    _build_subfolder = "build_subfolder"


    def config_options(self):
        if self.settings.os == 'Windows':
            del self.options.fPIC

    def source(self):
        sha256="3dfa02e873ff51a11ee02b9ca391807f0c8ea0529a4924afa645fbf97163f9d4"
        tools.get("{0}/archive/{1}.tar.gz".format(self.homepage, self.version), sha256=sha256)
        extracted_dir = self.name + "-" + self.version
        os.rename(extracted_dir, self._source_subfolder)

    def _configure_cmake(self):
        cmake = CMake(self)
        cmake.definitions["SNAPPY_BUILD_TESTS"] = False
        cmake.configure(build_folder=self._build_subfolder)
        return cmake

    def build(self):
        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        self.copy(pattern="COPYING", dst="licenses", src=self._source_subfolder)
        cmake = self._configure_cmake()
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
