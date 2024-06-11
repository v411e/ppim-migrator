with import <nixpkgs> {};
with pkgs.python3Packages;

buildPythonPackage rec {
  name = "ppim-migrator";
  format = "pyproject";
  pname = "ppim_migrator";
  version = "0.0.3";
  src = fetchPypi {
        inherit pname version;
        sha256 = "sha256-hNmNvA8C66BLgXue/VtvqJj8LBu+NPsaqRlAAHmyPMg=";
      };
  propagatedBuildInputs = [
    click
    requests
    pyyaml
  ];
}