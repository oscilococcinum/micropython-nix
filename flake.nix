{
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-24.11";
  };

  outputs = { nixpkgs, ... }@inputs: {

    devShells = builtins.listToAttrs (map (system: {
        name = system;
        value = with import nixpkgs { inherit system; config.allowUnfree = true; }; rec {

          esp32-dev = pkgs.mkShell {
            packages = with pkgs; [
              micropython
              esptool
              adafruit-ampy
              picocom
            ] ++ (with python3Packages; [
              pip
              numpy
            ]) ++ [
              (writeShellScriptBin ''esp32-erase'' ''esptool.py --port /dev/ttyUSB0 erase_flash'')
              (writeShellScriptBin ''esp32-deploy-firmware'' ''esptool.py --port /dev/ttyUSB0 --baud 460800 write_flash 0x1000 ESP32_GENERIC-20241129-v1.24.1.bin'') 
              (writeShellScriptBin ''esp32-REPL'' ''picocom /dev/ttyUSB0 -b115200'')
              (writeShellScriptBin ''esp32-flash'' ''ampy --port /dev/ttyUSB0 put main.py'')
            ];
            shellHook = ''
              export PIP_PREFIX=$(pwd)/_pip_packages
              export PYTHONPATH="$PIP_PREFIX/${pkgs.python3.sitePackages}:$PYTHONPATH"
              export PATH="$PIP_PREFIX/bin:$PATH"
              unset SOURCE_DATE_EPOCH
              if [ ! -d "$PIP_PREFIX" ]; then
               pip install micropython-esp32-stubs
              fi
            '';
          };

          default = esp32-dev;
        };
    })[ "x86_64-linux" ]);
  };
}
