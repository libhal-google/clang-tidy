from conan import ConanFile
from conan.tools.files import get, copy, download
from conan.errors import ConanInvalidConfiguration
import os


required_conan_version = ">=2.0.6"


class ClangTidy(ConanFile):
    name = "clang-tidy"
    license = ("")
    url = "https://github.com/conan-io/conan-center-index"
    homepage = ""
    description = ("Conan installer for clang-tidy")
    topics = ()
    settings = "os", "arch", 'compiler', 'build_type'
    exports_sources = ""
    package_type = "application"
    short_paths = True

    @property
    def download_info(self):
        version = self.version
        conan_os = str(self._settings_build.os)
        arch = str(self._settings_build.arch)
        return self.conan_data.get("sources", {}).get(version, {}).get(conan_os, {}).get(arch)

    @property
    def license_url(self):
        pass

    @property
    def _settings_build(self):
        return getattr(self, "settings_build", self.settings)

    def package_id(self):
        del self.info.settings.compiler
        del self.info.settings.build_type

    def validate(self):
        supported_build_operating_systems = ["Linux", "Macos", "Windows"]
        if not self._settings_build.os in supported_build_operating_systems:
            raise ConanInvalidConfiguration(
                f"The build os '{self._settings_build.os}' is not supported. "
                "Pre-compiled binaries are only available for "
                f"{supported_build_operating_systems}."
            )

        supported_build_architectures = {
            "Linux": ["armv8", "x86_64"],
            "Macos": ["armv8", "x86_64"],
            "Windows": ["x86_64"],
        }

        if (
            not self._settings_build.arch
            in supported_build_architectures[str(self._settings_build.os)]
        ):
            build_os = str(self._settings_build.os)
            raise ConanInvalidConfiguration(
                f"The build architecture '{self._settings_build.arch}' "
                f"is not supported for {self._settings_build.os}. "
                "Pre-compiled binaries are only available for "
                f"{supported_build_architectures[build_os]}."
            )

    def source(self):
        pass

    def build(self):
        get(self,
            **self.conan_data["sources"][self.version][str(self._settings_build.os)][str(self._settings_build.arch)],
            destination=self.build_folder, strip_root=True)

    def package(self):
        destination = os.path.join(self.package_folder, "bin")

        copy(self, pattern="bin/*", src=self.build_folder,
             dst=destination, keep_path=True)

    def package_info(self):
        self.cpp_info.includedirs = []

        bin_folder = os.path.join(self.package_folder, "bin/bin")
        self.cpp_info.bindirs = [bin_folder]
        self.buildenv_info.append_path("PATH", bin_folder)
