with import <nixpkgs> {};
let
  my-python-packages = python-packages: with python-packages; [
    pygame
    pip
    pillow
    pytest
    mock
  ];
  python-with-my-packages = python3.withPackages my-python-packages;
in
pkgs.stdenv.mkDerivation {
  name = "photobooth";
  buildInputs = [
    python-with-my-packages
  ];
}
