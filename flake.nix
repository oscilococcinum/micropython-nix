{
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-25.05";
  };

  outputs =
    { nixpkgs, ... }@inputs:
    let
      pkgs = import <nixpkgs> { };
    in
    let
      packageOverrides = pkgs.callPackage ./python-packages.nix { };
      python = pkgs.python3.override { inherit packageOverrides; };
      pythonWithPackages = python.withPackages (ps: [ ps.micropython-esp32-stubs ]);
    in
    {
      devShells = builtins.listToAttrs (
        map (system: {
          name = system;
          value =
            with import nixpkgs {
              inherit system;
              config.allowUnfree = true;
            }; rec {

              esp32-dev = pkgs.mkShell {
                nativeBuildInputs =
                  with pkgs;
                  [
                    micropython
                    esptool
                    adafruit-ampy
                    picocom
                  ]
                  ++ (with python3Packages; [
                    numpy
                  ])
                  ++ [
                    pythonWithPackages
                    (writeShellScriptBin "mp-erase" "esptool.py --port /dev/ttyUSB0 erase_flash")
                    (writeShellScriptBin "mp-deploy-firmware" "esptool.py --port /dev/ttyUSB0 --baud 460800 write_flash 0x1000 $1")
                    (writeShellScriptBin "mp-REPL" "picocom /dev/ttyUSB0 -b115200")
                    (writeShellScriptBin "mp-flash" "ampy --port /dev/ttyUSB0 put $1 $2")
                  ];
                shellHook = "echo '#INFO To exit picocom(REPL) - Ctrl-a -> Ctrl-x'";
              };

              default = esp32-dev;
            };
        }) [ "x86_64-linux" ]
      );
    };
}
