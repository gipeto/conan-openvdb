from conans import ConanFile, CMake, tools


class OpenVDBConan(ConanFile):
    name = "openvdb"
    version = "8.0.0"
    license = "https://github.com/AcademySoftwareFoundation/openvdb/blob/master/LICENSE"
    url = "https://github.com/AcademySoftwareFoundation/openvdb"
    description = "OpenVDB - Sparse volume data structure and tools"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}
    generators = ["cmake"]

    short_paths = True

    scm = {
        "type": "git",
        "url": url,
        "revision": 'v{}'.format(version),
        "subfolder": "src",
    }

    def source(self):
        tools.replace_in_file("src/CMakeLists.txt", "project(OpenVDB LANGUAGES CXX)", '''project(OpenVDB LANGUAGES CXX) 
        include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
        conan_basic_setup()''')

    def config_options(self):
        if self.settings.os == "Windows":
            self.options.remove("fPIC")

    def requirements(self):
        self.requires('tbb/[>=2018.0]')
        self.requires('boost/[>=1.66.0]')
        self.requires('openexr/[>=2.2.0]')
        self.requires('c-blosc/[>=1.5.0]')
        self.requires('ilmbase/[>=2.2.0]')

    def imports(self):
        self.copy("*.dll", dst="bin", src="bin")
        self.copy("*.dylib*", dst="lib", src="lib")
        self.copy('*.so*', dst='lib', src='lib')

    def _configure(self):
        cmake = CMake(self)
        if self.settings.os == 'Macos':
            cmake.definitions['CMAKE_MACOSX_RPATH'] = "TRUE"

        cmake.definitions['OPENVDB_CORE_SHARED'] = "ON" if self.options.shared else "OFF"
        cmake.definitions['OPENVDB_CORE_STATIC'] = "OFF" if self.options.shared else "ON"
        cmake.definitions['OPENVDB_BUILD_BINARIES'] = "OFF"

        cmake.configure(source_folder="src")
        return cmake

    def build(self):
        cmake = self._configure()
        cmake.build()

    def package(self):
        cmake = self._configure()
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
