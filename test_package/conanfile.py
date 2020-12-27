import os

from conans import ConanFile, CMake, tools


class OpenVDBTestConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake"

    def build(self):
        cmake = CMake(self)
        if self.settings.os == 'Macos':
            cmake.definitions['CMAKE_MACOSX_RPATH'] = "TRUE"
        
        cmake.configure()
        cmake.build()

    def imports(self):
        self.copy("*.dll", dst="bin", src="bin")
        self.copy("*.dylib*", dst="bin", src="lib")
        self.copy('*.so*', dst='bin', src='lib')

    def test(self):
        self.run("./bin/{}".format('openvdb_test.exe' if self.settings.os ==
                                   "Windows" else 'openvdb_test'))
